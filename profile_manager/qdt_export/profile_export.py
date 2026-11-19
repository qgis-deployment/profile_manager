import json
from pathlib import Path
from shutil import copytree, rmtree
from typing import Any, Dict

import pyplugin_installer

from profile_manager.profiles.utils import (
    get_profile_plugin_list_information,
    qgis_profiles_path,
)
from profile_manager.qdt_export.models import QDTProfileInfos


QDT_PROFILE_SCHEMA = "https://raw.githubusercontent.com/qgis-deployment/qgis-deployment-toolbelt-cli/main/docs/schemas/profile/qgis_profile.json"


def get_qdt_profile_infos_from_file(profile_file: Path) -> QDTProfileInfos:
    """Get QDT Profile informations from a profile.json file
    File must exists

    Args:
        profile_file (Path): profile.json path

    Returns:
        QDTProfileInfos: QDT Profile informations
    """
    with open(profile_file, "r") as f:
        qdt_profile_data = json.load(f)
        return QDTProfileInfos(
            name=qdt_profile_data.get("name", ""),
            folder_name=qdt_profile_data.get("folder_name", ""),
            description=qdt_profile_data.get("description", ""),
            author=qdt_profile_data.get("author", ""),
            email=qdt_profile_data.get("email", ""),
            version=qdt_profile_data.get("version", ""),
            qgis_min_version=qdt_profile_data.get("qgisMinimumVersion", ""),
            qgis_max_version=qdt_profile_data.get("qgisMaximumVersion", ""),
        )


def qdt_profile_dict(
    profile_name: str,
    qdt_profile_infos: QDTProfileInfos,
    export_inactive_plugin: bool = False,
) -> Dict[str, Any]:
    """Create QDT profile dict from QGIS profile

    Get informations from installed plugin and QDT profile informations

    Args:
        profile_name (str): profile name
        qdt_profile_infos (QDTProfileInfos): information for QDT profile creation
        export_inactive_plugin (bool, optional): True for inactive profile plugin export. Defaults to False.

    Returns:
        Dict[str, Any]: QDT profile dict
    """
    # Get profile installed plugin
    only_activated = not export_inactive_plugin
    profile_plugin_list = sorted(
        get_profile_plugin_list_information(
            profile_name=profile_name, only_activated=only_activated
        ),
        key=lambda x: x.name.lower(),
    )

    return {
        "$schema": QDT_PROFILE_SCHEMA,
        "name": profile_name,
        "folder_name": profile_name,  # TODO check for profile with space
        "description": qdt_profile_infos.description,
        "author": qdt_profile_infos.author,
        "email": qdt_profile_infos.email,
        "icon": "TDB",  # TODO add icon
        "qgisMinimumVersion": qdt_profile_infos.qgis_min_version,
        "qgisMaximumVersion": qdt_profile_infos.qgis_max_version,
        "version": qdt_profile_infos.version,
        "plugins": [plugin.as_dict() for plugin in profile_plugin_list],
    }


def export_profile_for_qdt(
    profile_name: str,
    export_path: Path,
    qdt_profile_infos: QDTProfileInfos,
    clear_export_path: bool = False,
    export_inactive_plugin: bool = False,
) -> None:
    """Export QGIS profile for QDT

    Args:
        profile_name (str): name of profile to export
        export_path (Path): export path for QDT profile
        qdt_profile_infos (QDTProfileInfos): information for QDT profile creation
        clear_export_path (bool, optional): True for export path clear before export. Defaults to False.
        export_inactive_plugin (bool, optional): True for inactive profile plugin export. Defaults to False.
    """
    pyplugin_installer.instance().reloadAndExportData()

    if clear_export_path:
        # Delete current export content
        rmtree(export_path, ignore_errors=True)

    # Copy profile content to export path
    copytree(
        src=Path(qgis_profiles_path()) / profile_name,
        dst=export_path,
        dirs_exist_ok=True,
    )

    # Delete cache content
    rmtree(export_path / "cache", ignore_errors=True)
    rmtree(export_path / "oauth2-cache", ignore_errors=True)

    # Delete python/plugins content
    rmtree(export_path / "python" / "plugins", ignore_errors=True)

    profile_dict = qdt_profile_dict(
        profile_name=profile_name,
        qdt_profile_infos=qdt_profile_infos,
        export_inactive_plugin=export_inactive_plugin,
    )

    with open(export_path / "profile.json", "w", encoding="UTF-8") as f:
        json.dump(profile_dict, f, indent=4)
