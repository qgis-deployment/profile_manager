# standard
from configparser import NoSectionError, RawConfigParser
from datetime import datetime
from pathlib import Path
from shutil import copytree, rmtree

# PyQGIS
from qgis.core import Qgis

# plugin
from profile_manager.toolbelt import PlgLogger


# -- GLOBALS
logger = PlgLogger()

# Via QGIS/python/plugins/CMakeLists.txt
CORE_PLUGINS = [
    "db_manager",
    "GdalTools",  # not a plugin anymore since QGIS 3.0
    "grassprovider",  # plugin since 3.22
    "MetaSearch",
    "otbprovider",  # plugin since 3.22
    "processing",
    "sagaprovider",  # removed in 3.30
]


def collect_plugin_names(qgis_ini_file: Path) -> list[str]:
    # TODO use ini AND file system, ini might have empty leftovers...
    logger.log(
        log_level=Qgis.MessageLevel.Info,
        message=f"Collecting plugin names from  {qgis_ini_file}",
    )
    start_time = datetime.now()

    ini_parser = RawConfigParser()
    ini_parser.optionxform = str  # str = case-sensitive option names
    ini_parser.read(qgis_ini_file)

    try:
        plugins_in_profile = ini_parser.options("PythonPlugins")
    except NoSectionError:
        logger.log(
            log_level=Qgis.MessageLevel.Warning,
            message=f"No plugins found in {qgis_ini_file}!",
        )
        plugins_in_profile = []

    time_taken = datetime.now() - start_time
    logger.log(
        log_level=Qgis.MessageLevel.NoLevel,
        message=f"Collecting plugin names from {qgis_ini_file} took {time_taken.microseconds / 1000} ms",
    )

    return plugins_in_profile


def import_plugins(
    source_profile_path: Path,
    target_profile_path: Path,
    target_qgis_ini_file: Path,
    plugin_names: list[str],
):
    """Copies the specified plugins from source to target profile.

    Copies the files and sets the INI options accordingly.
    Imported plugins are always set to be active.

    Note: Plugin specific settings are not copied as we have no way of knowing where or how they are stored.

    Plugins are stored in python/plugins/
    Their active state is tracked in QGIS/QGIS3.ini's [PythonPlugins] section, e.g.:

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
        plugin_names: List of plugins (names according to QGIS3.ini) to import
    """
    logger.log(
        log_level=Qgis.MessageLevel.Info,
        message=f"Importing {len(plugin_names)} data sources to {target_profile_path}",
    )
    start_time = datetime.now()

    ini_parser = RawConfigParser()
    ini_parser.optionxform = str  # str = case-sensitive option names
    ini_parser.read(target_qgis_ini_file)

    if not ini_parser.has_section("PythonPlugins"):
        ini_parser["PythonPlugins"] = {}

    for plugin_name in plugin_names:
        ini_parser.set("PythonPlugins", plugin_name, "true")

        source_plugin_dir = source_profile_path / "python" / "plugins" / plugin_name
        target_plugins_dir = target_profile_path / "python" / "plugins"
        target_plugin_dir = target_plugins_dir / plugin_name

        if source_plugin_dir.exists():
            if not target_plugins_dir.exists():  # TODO necessary?
                target_plugins_dir.mkdir(parents=True, exist_ok=True)
            if not target_plugin_dir.is_dir():
                copytree(source_plugin_dir, target_plugin_dir)
        else:
            continue  # TODO error, dont skip silently!

    with open(target_qgis_ini_file, "w") as qgisconf:
        ini_parser.write(qgisconf, space_around_delimiters=False)

    time_taken = datetime.now() - start_time
    logger.log(
        log_level=Qgis.MessageLevel.NoLevel,
        message=f"Importing plugins to {target_profile_path} took {time_taken.microseconds / 1000} ms",
    )


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
        plugin_names: List of plugins (names according to QGIS3.ini) to remove
    """
    logger.log(
        log_level=Qgis.MessageLevel.Info,
        message=f"Removing {len(plugin_names)} data sources from {profile_path}",
    )
    start_time = datetime.now()

    ini_parser = RawConfigParser()
    ini_parser.optionxform = str  # str = case-sensitive option names
    ini_parser.read(qgis_ini_file)

    for plugin_name in plugin_names:
        if plugin_name in CORE_PLUGINS:
            continue
        # Remove plugin from active state list in PythonPlugins section
        if ini_parser.has_option("PythonPlugins", plugin_name):
            ini_parser.remove_option("PythonPlugins", plugin_name)

        # Remove plugin dir
        plugins_dir = profile_path / "python" / "plugins" / plugin_name
        rmtree(plugins_dir)

    with open(qgis_ini_file, "w") as qgisconf:
        ini_parser.write(qgisconf, space_around_delimiters=False)

    time_taken = datetime.now() - start_time
    logger.log(
        log_level=Qgis.MessageLevel.NoLevel,
        message=f"Removing plugins from {profile_path} took {time_taken.microseconds / 1000} ms",
    )
