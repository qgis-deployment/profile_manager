from pathlib import Path
from shutil import copy2

from qgis.PyQt.QtCore import QSettings

from profile_manager.profiles.utils import get_qgis_ini_relative_path
from profile_manager.toolbelt.log_handler import PlgLogger


logger = PlgLogger()


def import_customizations(source_profile_path: Path, target_profile_path: Path):
    r"""Imports UI customizations from source to target profile.

    Copies the whole QGISCUSTOMIZATION3.ini file and enables customization in QGIS3.ini.

    Note: Existing customization will be overwritten!

    Customizations are stored in QGISCUSTOMIZATION3.ini and enabled in QGIS3.ini
    under [UI]Customization\enabled=true

    Args:
        source_profile_path: Path of profile directory to import from
        target_profile_path: Path of profile directory to import to
    """
    # Copy (overwrite) the QGISCUSTOMIZATION3.ini if exist
    source_customini_path = source_profile_path / "QGIS" / "QGISCUSTOMIZATION3.ini"
    target_customini_path = target_profile_path / "QGIS" / "QGISCUSTOMIZATION3.ini"
    if source_customini_path.exists():
        logger.log("Copying QGISCUSTOMIZATION3.ini to target profile")
        copy2(source_customini_path, target_customini_path)
    else:
        logger.log("No QGISCUSTOMIZATION3.ini found in source profile")
        return

    # Toggle UI customization depending on the setting in the source profile
    source_settings = QSettings(
        str(source_profile_path / get_qgis_ini_relative_path()),
        QSettings.Format.IniFormat,
    )
    target_settings = QSettings(
        str(target_profile_path / get_qgis_ini_relative_path()),
        QSettings.Format.IniFormat,
    )
    customization_setting = source_settings.value("UI/Customization/enabled", type=bool)
    if customization_setting is True:
        target_settings.setValue("UI/Customization/enabled", True)
        logger.log("Enabling UI customization in target profile")
    elif customization_setting is False:
        target_settings.setValue("UI/Customization/enabled", False)
        logger.log("Disabling UI customization in target profile")

    # writing the target file is handled by QSettings’s destructor
