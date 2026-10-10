# -- Imports --

# standard lib
import errno
import re
from os import rename
from pathlib import Path
from shutil import copytree, rmtree

# PyQGIS
from qgis.core import QgsApplication, QgsError, QgsUserProfileManager

# plugin
from profile_manager.profiles.utils import (
    get_profile_qgis_ini_path,
    qgis_profiles_path,
)


# validation rule from QGIS' QgsUserProfileSelectionDialog
VALID_PROJECT_NAME_REGEX = "[^/\\\\]+"


def create_profile(profile_name: str):
    """Creates new profile"""
    if not profile_name:
        raise ValueError("Empty profile name provided")
    if not re.match(VALID_PROJECT_NAME_REGEX, profile_name):
        raise ValueError("Invalid profile name")

    # Unfortunately QgsUserProfileManager.createUserProfile() does not notice if
    # the target directory already exists as of QGIS 3.40.3...
    # So we have our own check here:
    if Path(qgis_profiles_path() / profile_name).exists():
        raise ValueError("Target directory already exists")

    qgs_profile_manager = QgsUserProfileManager(str(qgis_profiles_path()))
    error: QgsError = qgs_profile_manager.createUserProfile(profile_name)
    if not error.isEmpty():
        raise Exception(
            f"QGIS could not create the new user profile: {error.summary()}"
        )

    # Right now there is only the profile directory and the qgis.db in its root.
    # We want to be able to write things to the profile's settings INI file so:
    ini_path = get_profile_qgis_ini_path(profile_name)
    ini_path.parent.mkdir(parents=True, exist_ok=True)
    ini_path.touch()


def remove_profile(profile_name: str):
    """Removes profile"""
    if not profile_name:
        raise ValueError("Empty profile name provided")
    if not re.match(VALID_PROJECT_NAME_REGEX, profile_name):
        raise ValueError("Invalid profile name")
    if profile_name == Path(QgsApplication.qgisSettingsDirPath()).name:
        raise ValueError("Cannot remove the profile that is currently active")

    profile_path = qgis_profiles_path() / profile_name
    try:
        rmtree(profile_path)
    except OSError as e:
        if e.errno == errno.EEXIST:
            raise ValueError("A profile with the same name already exists.")
        else:
            raise


def copy_profile(source_profile_name: str, target_profile_name: str):
    if not source_profile_name:
        raise ValueError("Empty source profile name provided")
    if not target_profile_name:
        raise ValueError("Empty target profile name provided")
    if not re.match(VALID_PROJECT_NAME_REGEX, source_profile_name):
        raise ValueError("Invalid source profile name")
    if not re.match(VALID_PROJECT_NAME_REGEX, target_profile_name):
        raise ValueError("Invalid target profile name")
    if source_profile_name == target_profile_name:
        raise ValueError("Cannot copy profile to itself")

    source_profile_path = qgis_profiles_path() / source_profile_name
    profile_path = qgis_profiles_path() / target_profile_name

    try:
        copytree(source_profile_path, profile_path)
    except OSError as e:
        if e.errno == errno.EEXIST:
            raise ValueError("A profile with the same name already exists.")
        else:
            raise


def rename_profile(old_profile_name: str, new_profile_name: str):
    """Renames profile to new name."""
    if not old_profile_name:
        raise ValueError("Empty old profile name provided")
    if not old_profile_name:
        raise ValueError("Empty new profile name provided")
    if old_profile_name == new_profile_name:
        raise ValueError("New name is identical to old name")
    if not re.match(VALID_PROJECT_NAME_REGEX, old_profile_name):
        raise ValueError("Invalid old profile name")
    if not re.match(VALID_PROJECT_NAME_REGEX, new_profile_name):
        raise ValueError("Invalid new profile name")
    if old_profile_name == Path(QgsApplication.qgisSettingsDirPath()).name:
        raise ValueError("Cannot rename the profile that is currently active")

    profile_before_change = qgis_profiles_path() / old_profile_name
    profile_after_change = qgis_profiles_path() / new_profile_name

    try:
        rename(profile_before_change, profile_after_change)
    except OSError as e:
        if e.errno == errno.ENOTEMPTY:
            raise ValueError("A profile with the same name already exists.")
        else:
            raise
