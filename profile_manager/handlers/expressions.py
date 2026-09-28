from configparser import RawConfigParser
from pathlib import Path


def import_expressions(source_qgis_ini_file: Path, target_qgis_ini_file: Path):
    r"""Imports custom expressions from source to target profile.

    Custom expressions are stored in QGIS/QGIS3.ini's [expressions] section, e.g.:

    .. code-block:: ini

       ...
       [expressions]
       ...
       user\test_expression\expression=1 + 1
       user\test_expression\helpText="..."
       ...

    Note: This does not handle Python expression functions yet. TODO

    Args:
        source_qgis_ini_file (str): Path of source QGIS3.ini file
        target_qgis_ini_file (str): Path of target QGIS3.ini file
    """
    source_ini_parser = RawConfigParser()
    source_ini_parser.optionxform = str  # str = case-sensitive option names
    source_ini_parser.read(source_qgis_ini_file)

    expressions = dict(source_ini_parser.items("expressions"))

    target_ini_parser = RawConfigParser()
    target_ini_parser.optionxform = str  # str = case-sensitive option names
    target_ini_parser.read(target_qgis_ini_file)

    if not target_ini_parser.has_section("expressions"):
        target_ini_parser["expressions"] = {}

    for entry in expressions:
        if "expression" in entry or "helpText" in entry:
            target_ini_parser.set("expressions", entry, expressions[entry])

    with open(target_qgis_ini_file, "w") as qgisconf:
        target_ini_parser.write(qgisconf, space_around_delimiters=False)
