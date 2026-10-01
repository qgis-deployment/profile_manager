from datetime import datetime
from pathlib import Path
from shutil import copytree, rmtree

from qgis.core import Qgis
from qgis.PyQt.QtCore import QSettings
from qgis.utils import findPlugins

from profile_manager.toolbelt import PlgLogger


logger = PlgLogger()


def collect_plugin_names(profile_path: Path) -> list[str]:
    """Returns the directory names of installed plugins in the profile directory."""
    logger.log(f"Collecting plugin names from  {profile_path}")
    plugins_directory = profile_path / "python" / "plugins"
    installed_plugins = [p for p, _ in findPlugins(str(plugins_directory))]
    return sorted(installed_plugins)


def import_plugins(
    source_profile_path: Path,
    target_profile_path: Path,
    target_qgis_ini_file: Path,
    plugin_names: list[str],
):
    """Copies the specified plugins from source to target profile.

    Copies the files and sets the INI options accordingly.
    Imported plugins are always set to be active.

    Note: If a target plugin directory exists, it will be deleted/overwritten.

    Note: Plugin specific settings are not copied as we have no way of knowing where or how they are stored.

    Plugins are stored in python/plugins/
    Their active state is tracked in QGIS/QGIS3.ini's [PythonPlugins] section with an
    entry using the same name as the plugin's directory, e.g.:

    .. code-block:: ini

       ...
       [PythonPlugins]
       ...
       fooPlugin=true
       PluggyBar=true
       BaZ=false
       ...

    Args:
        source_profile_path: Path of profile directory to import from
        target_profile_path: Path of profile directory to import to
        target_qgis_ini_file: Path of target QGIS3.ini file to import to
        plugin_names: List of plugins (=their directory names) to import
    """
    logger.log(f"Importing {len(plugin_names)} data sources to {target_profile_path}")
    start_time = datetime.now()

    target_settings = QSettings(str(target_qgis_ini_file), QSettings.Format.IniFormat)
    target_settings.beginGroup("PythonPlugins")

    for plugin_name in plugin_names:
        source_plugin_dir = source_profile_path / "python" / "plugins" / plugin_name
        target_plugin_dir = target_profile_path / "python" / "plugins" / plugin_name

        # Copy the plugin to the target profile
        # We don't want to mix the source plugin with anything in the target directory,
        # so we delete that if it exists.
        if target_plugin_dir.is_dir():
            target_plugin_dir.unlink()
        # We don't need to check of the target profile already has a plugins directory,
        # because copytree automatically creates missing parent directories if needed.
        copytree(source_plugin_dir, target_plugin_dir)

        # Set plugin active in the target profile's settings
        target_settings.setValue(plugin_name, True)

    time_taken = datetime.now() - start_time
    logger.log(
        log_level=Qgis.MessageLevel.NoLevel,
        message=f"Importing plugins to {target_profile_path} took {time_taken.microseconds / 1000} ms",
    )

    # writing the settings INI file is handled by QSettings’s destructor


def remove_plugins(
    profile_path: Path,
    qgis_ini_file: Path,
    plugin_names: list[str],
):
    """Removes the specified plugins from the profile.

    Removes both the files from python/plugins/ and the QGIS/QGIS3.ini [PythonPlugins] section entries.

    Note: Plugin-specific *settings* are not removed as we have no way of knowing where or how they are stored.

    Args:
        profile_path: Path of profile directory to remove from
        qgis_ini_file: Path of target QGIS3.ini file to remove from
        plugin_names: List of plugins (=their directory names) to remove
    """
    logger.log(f"Removing {len(plugin_names)} plugins from {profile_path}")
    start_time = datetime.now()

    settings = QSettings(str(qgis_ini_file), QSettings.Format.IniFormat)
    settings.beginGroup("PythonPlugins")  # will be created as needed

    for plugin_name in plugin_names:
        # Remove plugin directory
        plugin_dir = profile_path / "python" / "plugins" / plugin_name
        rmtree(plugin_dir)

        # Remove plugin from active state list in PythonPlugins section
        settings.remove(plugin_name)

    time_taken = datetime.now() - start_time
    logger.log(
        log_level=Qgis.MessageLevel.NoLevel,
        message=f"Removing plugins from {profile_path} took {time_taken.microseconds / 1000} ms",
    )

    # writing the settings INI file is handled by QSettings’s destructor
