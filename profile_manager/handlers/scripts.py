from pathlib import Path
from shutil import copy2

from profile_manager.toolbelt.log_handler import PlgLogger


logger = PlgLogger()


def import_scripts(source_profile_path: Path, target_profile_path: Path):
    """Imports Processing scripts from source to target profile.

    Note: Existing scripts with identical filenames will be overwritten!

    Scripts are stored in the processing/scripts/ subdirectory of a profile, e.g.:

    .. code-block::

      ...
      processing/scripts/my_great_processing_script.py
      processing/scripts/snakes.py
      ...

    Args:
        source_profile_path: Path of profile directory to import from
        target_profile_path: Path of profile directory to import to
    """
    source_scripts_dir = source_profile_path / "processing" / "scripts"
    target_scripts_dir = target_profile_path / "processing" / "scripts"

    if not source_scripts_dir.exists():
        logger.log("No Processing python scripts found in source profile")
        return

    if not target_scripts_dir.exists():
        target_scripts_dir.mkdir(parents=True, exist_ok=True)

    for python_file in Path(source_scripts_dir).glob("*.py"):
        filename = python_file.name
        logger.log(f"Copying Processing python script: {filename}")
        dest = target_scripts_dir / filename
        copy2(python_file, dest)
