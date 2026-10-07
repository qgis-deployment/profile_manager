from pathlib import Path

from qgis.core import QgsBookmarkManager

from profile_manager.exceptions import ItemImportError
from profile_manager.toolbelt import PlgLogger


logger = PlgLogger()


def import_bookmarks(source_bookmark_file: Path, target_bookmark_file: Path) -> None:
    """Imports spatial bookmarks from source to target file.

    Existing bookmarks will be updated/overwritten when IDs match.

    Spatial bookmarks are stored in bookmarks.xml.

    Note: QGIS does only flush edits to the bookmarks file when closed, so any edits
          to bookmarks in the same session as a Profile Manager import will not be
          reflected in the target file.

    :param source_bookmark_file: path of bookmarks file to import from
    :type source_bookmark_file: Path
    :param target_bookmark_file: path of bookmarks file to import to
    :type target_bookmark_file: Path

    :raises ItemImportError: if a bookmark cannot be added to or updated in the
        target
    """
    # This function *could* use QgsApplication.bookmarkManager() as source but let's
    # keep it similar to the other functions and have similar source and target
    # parameters. The benefit would be that bookmark changes during the same QGIS
    # session as the Profile Manager import would be included.
    # TODO reconsider this ^

    # There is also a method QgsBookmarkManager.importFromFile() that might look
    # relevant but that's for bookmark *exports* which use a different XML format.

    source_bmm = QgsBookmarkManager()
    source_bmm.initialize(str(source_bookmark_file))

    target_bmm = QgsBookmarkManager()
    target_bmm.initialize(str(target_bookmark_file))

    source_bookmarks = source_bmm.bookmarks()
    if not source_bookmarks:
        logger.log("No bookmarks found in source profile")
        return

    logger.log(f"Importing {len(source_bookmarks)} bookmarks...")
    for bookmark in source_bookmarks:
        # addBookmark() fails if ID exists and updateBookmark() fails if it doesn't.
        # addBookmark() says it can also fail due to other reasons, so we cannot
        # simply try that first and do updateBookmark() on fail.
        # bookmarkById() returns an empty bookmark if not found, there is no
        # other way to find out if a bookmark already exists in the target.
        # An empty bookmark has no special marker but an empty string as ID.
        # So, this is why this is written as it is:
        target_bookmark = target_bmm.bookmarkById(bookmark.id())
        if target_bookmark.id() == "":
            # ID does not exist in target, we should copy the bookmark to it
            _, success = target_bmm.addBookmark(bookmark)
            if not success:
                raise ItemImportError(
                    f"Failed to add bookmark {bookmark.name()!r}",
                    item_type="bookmark",
                    item_name=bookmark.name(),
                )
        elif not target_bmm.updateBookmark(bookmark):
            # ID exists in target so updateBookmark() should be able to replace it
            raise ItemImportError(
                f"Failed to update bookmark {bookmark.name()!r}",
                item_type="bookmark",
                item_name=bookmark.name(),
            )

    del target_bmm  # flush the target file
