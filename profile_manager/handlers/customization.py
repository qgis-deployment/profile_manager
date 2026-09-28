from configparser import RawConfigParser
from pathlib import Path
from shutil import copy2


def import_customizations(source_profile_path: Path, target_profile_path: Path):
    r"""Imports UI customizations from source to target profile.

    Copies the whole QGISCUSTOMIZATION3.ini file and also transfers the [UI] section from QGIS3.ini if available

    TODO fix discrepancy between [UI] and [Customization]! Which one(s) exist and what do we want to transfer?

     :example:

      .. code-block:: ini
        [Customization]
        Browser=true
        Browser\AFS=false
        ...

    Args:
        source_profile_path: Path of profile directory to import from
        target_profile_path: Path of profile directory to import to
    """
    # Copy (overwrite) the QGISCUSTOMIZATION3.ini if exist
    source_customini_path = source_profile_path / "QGIS" / "QGISCUSTOMIZATION3.ini"
    target_customini_path = target_profile_path / "QGIS" / "QGISCUSTOMIZATION3.ini"
    if source_customini_path.exists():
        copy2(source_customini_path, target_customini_path)

    # Copy [UI] section from QGIS3.ini
    source_qgis3ini_path = source_profile_path / "QGIS" / "QGIS3.ini"
    target_qgis3ini_path = target_profile_path / "QGIS" / "QGIS3.ini"

    source_ini_parser = RawConfigParser()
    source_ini_parser.optionxform = str  # str = case-sensitive option names
    source_ini_parser.read(source_qgis3ini_path)

    # TODO this is broken, right? It looks for [UI] but even in QGIS 3.10 (didnt check older) the (single) section is named [Customization]
    if source_ini_parser.has_section("UI"):
        ui_data = dict(source_ini_parser.items("UI"))

        target_ini_parser = RawConfigParser()
        target_ini_parser.optionxform = str  # str = case-sensitive option names
        target_ini_parser.read(target_qgis3ini_path)

        for setting in ui_data:
            if not target_ini_parser.has_section("UI"):
                target_ini_parser["UI"] = {}

            target_ini_parser.set("UI", setting, ui_data[setting])

        with open(target_qgis3ini_path, "w") as qgisconf:
            target_ini_parser.write(qgisconf, space_around_delimiters=False)
