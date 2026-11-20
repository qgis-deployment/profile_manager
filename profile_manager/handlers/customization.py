# standard
from pathlib import Path
from shutil import copy2

# PyQGIS
from qgis.PyQt.QtCore import QSettings

# plugin
from profile_manager.constants import QGIS_SETTINGS_CUSTOMIZATION_ENABLED_KEY
from profile_manager.profiles.utils import (
    get_qgis_customization_relative_path,
    get_qgis_ini_relative_path,
)
from profile_manager.toolbelt.log_handler import PlgLogger


logger = PlgLogger()


def import_customizations(source_profile_path: Path, target_profile_path: Path):
    r"""Imports UI customizations from source to target profile.

    Copies the whole customization file and enables customization in the settings
    INI file, as in the source profile.

    Note: Existing customization will be overwritten!

    Customizations are stored in QGIS/QGISCUSTOMIZATION3.ini (QGIS 3) or
    QGIS/QGISCUSTOMIZATION.xml (QGIS 4), and enabled in the settings INI file
    (QGIS3.ini, QGIS4.ini) under [UI]Customization\enabled=true

    Args:
        source_profile_path: Path of profile directory to import from
        target_profile_path: Path of profile directory to import to
    """
    # Copy (overwrite) the customization file if exist
    customization_relative_path = get_qgis_customization_relative_path()
    source_custom_path = source_profile_path / customization_relative_path
    target_custom_path = target_profile_path / customization_relative_path
    if source_custom_path.exists():
        logger.log(f"Copying {customization_relative_path.name} to target profile")
        target_custom_path.parent.mkdir(parents=True, exist_ok=True)
        copy2(source_custom_path, target_custom_path)
    else:
        logger.log(f"No {customization_relative_path.name} found in source profile")
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
    customization_setting = source_settings.value(
        QGIS_SETTINGS_CUSTOMIZATION_ENABLED_KEY, type=bool
    )
    if customization_setting is True:
        target_settings.setValue(QGIS_SETTINGS_CUSTOMIZATION_ENABLED_KEY, True)
        logger.log("Enabling UI customization in target profile")
    elif customization_setting is False:
        target_settings.setValue(QGIS_SETTINGS_CUSTOMIZATION_ENABLED_KEY, False)
        logger.log("Disabling UI customization in target profile")

    # writing the target file is handled by QSettings’s destructor
