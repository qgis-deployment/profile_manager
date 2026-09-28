from os import listdir
from pathlib import Path
from shutil import copy2


def import_scripts(source_profile_path: Path, target_profile_path: Path):
    """Imports Processing scripts from source to target profile.

    Note: Existing scripts with identical filenames will be overwritten!

    Scripts are stored in the processing/scripts/ subdirectory of a profile, e.g.:

    .. code-block:: ini

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
        return
    if not target_scripts_dir.exists():
        target_scripts_dir.mkdir(parents=True, exist_ok=True)
    for item in listdir(source_scripts_dir):
        source = source_scripts_dir / item
        dest = target_scripts_dir / item
        if source.is_dir():
            continue
        else:
            copy2(source, dest)
