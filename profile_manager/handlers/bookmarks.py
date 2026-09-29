from pathlib import Path

from lxml import etree as et


def import_bookmarks(source_bookmark_file: Path, target_bookmark_file: Path):
    """Imports spatial bookmarks from source to target file.

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

    TODO The deduplication seems garbage

    Args:
        source_bookmark_file: Path of bookmarks file to import from
        target_bookmark_file: Path of bookmarks file to import to
    """
    # get the element tree of the source file
    source_tree = et.parse(source_bookmark_file, et.XMLParser(remove_blank_text=True))

    # check if target file exists
    if not target_bookmark_file.is_file():
        with open(target_bookmark_file, "w") as new_file:
            new_file.write("<Bookmarks></Bookmarks>")

    # get the element tree of the target file
    # fill if empty
    target_tree = et.parse(target_bookmark_file, et.XMLParser(remove_blank_text=True))

    # find all bookmark elements
    source_root_tag = source_tree.findall("Bookmark")

    # get the root element "Bookmarks"  # TODO comment does not seem to fit the code?
    target_tree_root = target_tree.getroot()

    # Remove duplicate entries to prevent piling data
    target_tree_root = remove_duplicates(source_root_tag, target_tree, target_tree_root)

    # append the elements
    for element in source_root_tag:
        target_tree_root.append(element)

    # overwrite the xml file
    et.ElementTree(target_tree_root).write(
        target_bookmark_file,
        pretty_print=True,
        encoding="utf-8",
        xml_declaration=True,
    )


def remove_duplicates(
    source_root_tag: list[et.Element],
    target_tree: et.ElementTree,
    target_tree_root: et.Element,
):
    """Removes bookmarks from target that exist in the (to be imported) source too."""
    # TODO FIXME this only checks the name of the bookmarks which will lead to false positives
    #            it is ok and supported by QGIS to have the same name for multiple bookmarks
    #            TODO compare the complete content of the xml node!
    target_root_tag = target_tree.findall("Bookmark")
    for source_element in source_root_tag:
        for target_element in target_root_tag:
            if source_element.attrib["name"] == target_element.attrib["name"]:
                target_tree_root.remove(target_element)

    return target_tree_root
