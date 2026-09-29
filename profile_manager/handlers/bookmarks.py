from pathlib import Path

from lxml import etree as et

from profile_manager.toolbelt import PlgLogger


logger = PlgLogger()


def import_bookmarks(source_bookmark_file: Path, target_bookmark_file: Path):
    """Imports spatial bookmarks from source to target file.

    Skips bookmarks by id (uuid) that already exist in the target. QGIS allows

    Spatial bookmarks are stored in bookmarks.xml, e.g.:

    .. code-block:: xml

       <Bookmarks>
           <Bookmark id="..." group="" extent="POLYGON((...))" name="Test Bookmark">
               <spatialrefsys nativeFormat="Wkt">
               ...
               </spatialrefsys>
           </Bookmark>
           ...
       </Bookmarks>

    Args:
        source_bookmark_file: Path of bookmarks file to import from
        target_bookmark_file: Path of bookmarks file to import to
    """
    source_tree = et.parse(source_bookmark_file, et.XMLParser(remove_blank_text=True))

    if not target_bookmark_file.is_file():
        with open(target_bookmark_file, "w") as new_file:
            new_file.write("<Bookmarks></Bookmarks>")

    target_tree = et.parse(target_bookmark_file, et.XMLParser(remove_blank_text=True))

    source_bookmarks = source_tree.findall("Bookmark")
    target_tree_root = target_tree.getroot()  # The <Bookmarks> element
    target_bookmarks = target_tree.findall("Bookmark")

    target_bookmark_ids = [tb.attrib["id"] for tb in target_bookmarks]
    for source_bookmark in source_bookmarks:
        source_bookmark_id = source_bookmark.attrib["id"]
        if source_bookmark.attrib["id"] in target_bookmark_ids:
            logger.log(
                message=f"Skipping duplicate bookmark: {source_bookmark.attrib['name']} ({source_bookmark_id})"
            )
            continue
        else:
            logger.log(
                message=f"Writing bookmark: {source_bookmark.attrib['name']} ({source_bookmark_id})"
            )
            target_tree_root.append(source_bookmark)

    et.ElementTree(target_tree_root).write(
        target_bookmark_file,
        pretty_print=True,
        encoding="utf-8",
        xml_declaration=True,
    )
