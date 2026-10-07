# -- Imports --

# standard lib
from configparser import NoSectionError, RawConfigParser
from pathlib import Path
from typing import Any, Dict, List, Optional

# PyQGIS
import pyplugin_installer
from pyplugin_installer.installer_data import repositories
from qgis.core import Qgis, QgsApplication, QgsSettings, QgsUserProfileManager
from qgis.PyQt.QtCore import QCoreApplication
from qgis.utils import iface

# plugin
from profile_manager.qdt_export.models import QdtPluginInformation
from profile_manager.toolbelt import PlgLogger


# -- Globals--
logger = PlgLogger()


# -- Functions --
def qgis_profiles_path() -> Path:
    """Get QGIS profiles paths from current QGIS application

    Returns:
        Path: QGIS profiles path
    """
    return Path(iface.userProfileManager().rootLocation())


def get_qgis_ini_relative_path() -> Path:
    """Get the settings INI file path relative to a profile folder.

    :return: relative path
    :rtype: Path
    """
    active_ini = Path(QgsSettings().fileName())
    try:
        return active_ini.relative_to(QgsApplication.qgisSettingsDirPath())
    except ValueError:
        logger.log(
            message=f"Settings file {active_ini} is not inside the active profile "
            f"folder {QgsApplication.qgisSettingsDirPath()}, falling back to default.",
            log_level=Qgis.MessageLevel.Warning,
        )
        return Path("QGIS") / f"{QCoreApplication.applicationName()}.ini"


def get_profile_qgis_ini_path(profile_name: str) -> Path:
    """Get the settings INI file path (QGIS3.ini, QGIS4.ini...) for a profile.

    :param profile_name: profile name
    :type profile_name: str

    :return: settings INI file path
    :rtype: Path
    """
    return qgis_profiles_path() / profile_name / get_qgis_ini_relative_path()


def get_profile_plugin_metadata_path(profile_name: str, plugin_slug_name: str) -> Path:
    """Get path to metadata.txt for a plugin inside a profile

    Args:
        profile_name (str): profile name
        plugin_slug_name (str): plugin slug name

    Returns:
        Path: metadata.txt path
    """
    return (
        qgis_profiles_path()
        / profile_name
        / "python"
        / "plugins"
        / plugin_slug_name
        / "metadata.txt"
    )


def get_installed_plugin_list(
    profile_name: str, only_activated: bool = True
) -> List[str]:
    """Get installed plugin for a profile

    Args:
        profile_name (str): profile name
        only_activated (bool, optional): True to get only activated plugin, False to get all installed plugins. Defaults to True.

    Returns:
        List[str]: plugin slug name list
    """
    ini_parser = RawConfigParser()
    ini_parser.optionxform = str  # str = case-sensitive option names
    ini_parser.read(get_profile_qgis_ini_path(profile_name))
    try:
        plugins_in_profile = dict(ini_parser.items("PythonPlugins"))
    except NoSectionError:
        plugins_in_profile = {}

    if only_activated:
        return [key for key, value in plugins_in_profile.items() if value == "true"]
    else:
        return plugins_in_profile.keys()


def get_installed_plugin_metadata(
    profile_name: str, plugin_slug_name: str
) -> Dict[str, Any]:
    """Get metadata information from metadata.txt file in profile installed plugin

    Args:
        profile_name (str): profile name
        plugin_slug_name (str): plugin slug name

    Returns:
        Dict[str, Any]: metadata as dict. Empty dict if metadata unavailable
    """
    ini_parser = RawConfigParser()
    ini_parser.optionxform = str  # str = case-sensitive option names
    plg_metadata_path = get_profile_plugin_metadata_path(profile_name, plugin_slug_name)
    ini_parser.read(plg_metadata_path)
    try:
        metadata = dict(ini_parser.items("general"))
        metadata["folder_name"] = plg_metadata_path.parent.name
    except NoSectionError:
        metadata = {}
    return metadata


def get_plugin_info_from_qgis_manager(
    plugin_slug_name: str, reload_manager: bool = False
) -> Optional[Dict[str, str]]:
    """Get plugin informations from QGIS plugin manager

    Args:
        plugin_slug_name (str): _description_
        reload_manager (bool, optional): reload manager for new plugins. Defaults to False.

    Returns:
        Optional[Dict[str, str]]: metadata from plugin manager, None if plugin not found
    """
    if reload_manager:
        pyplugin_installer.instance().reloadAndExportData()
    return iface.pluginManagerInterface().pluginMetadata(plugin_slug_name)


def get_plugin_repository_url(manager_metadata: Dict[str, Any]) -> Optional[str]:
    """Get plugins.xml URL of the repository a plugin was installed from.

    Only repositories known by the current QGIS session are available.

    Args:
        manager_metadata (Dict[str, Any]): metadata from QGIS plugin manager

    Returns:
        Optional[str]: repository URL, None for plugins not related to a repository
    """
    repo_name = manager_metadata.get("zip_repository")
    if not repo_name:
        return None
    return repositories.all().get(repo_name, {}).get("url") or None


def get_current_profile_name() -> str:
    """Get name of the profile used by the current QGIS session.

    Returns:
        str: current profile name
    """
    return iface.userProfileManager().userProfile().name()


def get_profile_name_list() -> List[str]:
    """Get profile name list from current installed QGIS

    Returns:
        List[str]: profile name list
    """
    return QgsUserProfileManager(qgis_profiles_path()).allProfiles()


def define_plugin_version_from_metadata(
    manager_metadata: Dict[str, Any], plugin_metadata: Dict[str, Any]
) -> str:
    """Define plugin version from available metadata

    Args:
        manager_metadata (Dict[str, Any]): QGIS plugin manager metadata
        plugin_metadata (Dict[str, Any]): installed plugin metadata

    Returns:
        str: plugin version
    """
    # Use version from plugin metadata
    if "version" in plugin_metadata:
        return plugin_metadata["version"]

    # Fallback to stable, experimental and available versions from plugin manager
    for key in (
        "version_available_stable",
        "version_available_experimental",
        "version_available",
    ):
        if version := manager_metadata.get(key):
            return version

    # No version defined
    return ""


def get_profile_plugin_information(
    profile_name: str, plugin_slug_name: str
) -> Optional[QdtPluginInformation]:
    """Get plugin information from profile, whatever the repository it was
    installed from (official, third-party or none).

    Args:
        profile_name (str): profile name
        plugin_slug_name (str):  plugin slug name

    Returns:
        Optional[QdtPluginInformation]: plugin information, None if the plugin is
            neither known by the QGIS plugin manager nor has readable metadata in
            the profile
    """
    manager_metadata = get_plugin_info_from_qgis_manager(
        plugin_slug_name=plugin_slug_name
    )

    plugin_metadata = get_installed_plugin_metadata(
        profile_name=profile_name, plugin_slug_name=plugin_slug_name
    )

    if not manager_metadata and not plugin_metadata:
        logger.log(
            message=f"Plugin {plugin_slug_name} not found in profile {profile_name}",
            log_level=Qgis.MessageLevel.Warning,
        )
        return None

    if manager_metadata is None:
        manager_metadata = {
            "name": plugin_metadata.get("name", plugin_slug_name),
            "download_url": None,
            "plugin_id": None,
        }

    return QdtPluginInformation(
        name=manager_metadata.get("name", plugin_slug_name),
        download_url=manager_metadata.get("download_url"),
        repository_url=get_plugin_repository_url(manager_metadata),
        folder_name=plugin_metadata.get("folder_name", plugin_slug_name),
        plugin_id=(
            int(manager_metadata["plugin_id"])
            if manager_metadata["plugin_id"]
            else None
        ),
        version=define_plugin_version_from_metadata(
            manager_metadata=manager_metadata,
            plugin_metadata=plugin_metadata,
        ),
    )


def get_profile_plugin_list_information(
    profile_name: str, only_activated: bool = True
) -> List[QdtPluginInformation]:
    """Get profile plugin information

    Args:
        profile_name (str): profile name
        only_activated (bool, optional): True to get only activated plugin, False to get all installed plugins. Defaults to True.

    Returns:
        List[QdtPluginInformation]: list of plugin information
    """
    plugin_list: List[str] = get_installed_plugin_list(
        profile_name=profile_name, only_activated=only_activated
    )

    # Get information about installed plugin
    profile_plugin_list: List[QdtPluginInformation] = []
    for plugin_name in plugin_list:
        plugin_info = get_profile_plugin_information(profile_name, plugin_name)
        if plugin_info:
            profile_plugin_list.append(plugin_info)

    return profile_plugin_list
