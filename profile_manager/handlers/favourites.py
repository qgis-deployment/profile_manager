from pathlib import Path

from qgis.PyQt.QtCore import QSettings

from profile_manager.toolbelt.log_handler import PlgLogger


logger = PlgLogger()


def import_favourites(source_qgis_ini_file: Path, target_qgis_ini_file: Path):
    """Imports browser favourites from source to target profile.

    Note: Existing favourites are removed and overwritten.

    Favourites are stored in QGIS/QGIS3.ini's [browser] section, e.g.:

    .. code-block:: ini

       ...
       [browser]
       favourites=/path/to|||My favourite folder!, /tmp/test|||title, ...
       ...

    Args:
        source_qgis_ini_file: Path of source QGIS3.ini file
        target_qgis_ini_file: Path of target QGIS3.ini file
    """
    source_settings = QSettings(str(source_qgis_ini_file), QSettings.Format.IniFormat)
    target_settings = QSettings(str(target_qgis_ini_file), QSettings.Format.IniFormat)
    favourites = source_settings.value("browser/favourites")  # None if not exist
    if favourites is None:
        logger.log("No favourites found in source profile")
        return
    else:
        target_settings.setValue("browser/favourites", favourites)
        logger.log("Copying favourites to target profile")

    # writing the target file is handled by QSettings’s destructor
