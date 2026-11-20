# standard
import json
from pathlib import Path
from shutil import copytree, rmtree
from typing import Any, Dict, Optional

# PyQGIS
import pyplugin_installer

# plugin
from profile_manager.constants import (
    QDT_EXPORT_EXCLUDED_DIRS,
    QDT_PROFILE_FILENAME,
    QDT_PROFILE_IMAGES_DIR,
    QDT_PROFILE_SCHEMA_URL,
)
from profile_manager.profiles.utils import (
    get_profile_plugin_list_information,
    qgis_profiles_path,
)
from profile_manager.qdt_export.models import QDTProfileInfos


def get_qdt_profile_infos_from_file(profile_file: Path) -> QDTProfileInfos:
    """Get QDT Profile informations from a profile.json file
    File must exists

    Args:
        profile_file (Path): profile.json path

    Returns:
        QDTProfileInfos: QDT Profile informations
    """
    with profile_file.open(encoding="UTF-8") as f:
        qdt_profile_data = json.load(f)

    # icon path is relative to the profile.json folder: resolve it to a local file
    icon_path = ""
    if icon := qdt_profile_data.get("icon"):
        icon_file = profile_file.parent / icon
        if icon_file.is_file():
            icon_path = str(icon_file.resolve())

    return QDTProfileInfos(
        icon=icon_path,
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
    icon_relative_path: Optional[str] = None,
) -> Dict[str, Any]:
    """Create QDT profile dict from QGIS profile

    Get informations from installed plugin and QDT profile informations

    Args:
        profile_name (str): profile name
        qdt_profile_infos (QDTProfileInfos): information for QDT profile creation
        export_inactive_plugin (bool, optional): True for inactive profile plugin
            export. Defaults to False.
        icon_relative_path (Optional[str], optional): icon path relative to the exported
            profile folder. Defaults to None (no icon).

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

    profile_dict = {
        "$schema": QDT_PROFILE_SCHEMA_URL,
        "name": profile_name,
        "folder_name": profile_name,  # TODO check for profile with space
        "description": qdt_profile_infos.description,
        "author": qdt_profile_infos.author,
        "email": qdt_profile_infos.email,
        "qgisMinimumVersion": qdt_profile_infos.qgis_min_version,
        "qgisMaximumVersion": qdt_profile_infos.qgis_max_version,
        "version": qdt_profile_infos.version,
        "plugins": [plugin.as_dict() for plugin in profile_plugin_list],
    }
    if icon_relative_path:
        profile_dict["icon"] = icon_relative_path
    return profile_dict


def _export_icon(
    icon_path: Path, icon_content: bytes, profile_path: Path, export_path: Path
) -> str:
    """Write the icon into the export folder and return its relative path.

    The icon keeps its relative location when it comes fomr the source profile or in
    the export folder. Otherwise it is copied into the images subfolder, following
    the QDT profile convention.

    Args:
        icon_path (Path): local icon path
        icon_content (bytes): icon content, read before the export folder clearing
        profile_path (Path): source QGIS profile folder
        export_path (Path): export folder

    Returns:
        str: icon path relative to the export folder, in POSIX form
    """
    icon_path = icon_path.resolve()
    for base_folder in (profile_path.resolve(), export_path.resolve()):
        if icon_path.is_relative_to(base_folder):
            icon_relative_path = icon_path.relative_to(base_folder)
            break
    else:
        icon_relative_path = QDT_PROFILE_IMAGES_DIR / icon_path.name

    target_icon_path = export_path / icon_relative_path
    target_icon_path.parent.mkdir(parents=True, exist_ok=True)
    target_icon_path.write_bytes(icon_content)
    return icon_relative_path.as_posix()


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

    profile_path = Path(qgis_profiles_path()) / profile_name

    # read icon before any deletion: it may lie in the export folder
    icon_path = Path(qdt_profile_infos.icon) if qdt_profile_infos.icon else None
    icon_content = icon_path.read_bytes() if icon_path and icon_path.is_file() else None

    if clear_export_path:
        # Delete current export content
        rmtree(export_path, ignore_errors=True)

    # Copy profile content to export path
    copytree(
        src=profile_path,
        dst=export_path,
        dirs_exist_ok=True,
    )

    # Delete caches and installed plugins (QDT installs them from profile.json)
    for excluded_dir in QDT_EXPORT_EXCLUDED_DIRS:
        rmtree(export_path / excluded_dir, ignore_errors=True)

    icon_relative_path = (
        _export_icon(icon_path, icon_content, profile_path, export_path)
        if icon_content is not None
        else None
    )

    profile_dict = qdt_profile_dict(
        profile_name=profile_name,
        qdt_profile_infos=qdt_profile_infos,
        export_inactive_plugin=export_inactive_plugin,
        icon_relative_path=icon_relative_path,
    )

    with export_path.joinpath(QDT_PROFILE_FILENAME).open("w", encoding="UTF-8") as f:
        json.dump(profile_dict, f, indent=4)
