from os import listdir
from pathlib import Path
from shutil import copy2


def import_models(source_profile_path: Path, target_profile_path: Path):
    """Imports Processing models from source to target profile.

    Note: Existing models with identical filenames will be overwritten!

    Models are stored in the processing/models/ subdirectory of a profile, e.g.:

    .. code-block::

       ...
       processing/models/my_model.model3
       processing/models/das.model3
       ...

    Args:
        source_profile_path: Path of profile directory to import from
        target_profile_path: Path of profile directory to import to
    """
    source_models_dir = source_profile_path / "processing" / "models"
    target_models_dir = target_profile_path / "processing" / "models"

    if not source_models_dir.exists():
        return
    if not target_models_dir.exists():
        target_models_dir.mkdir(parents=True, exist_ok=True)
    for item in listdir(source_models_dir):
        source = source_models_dir / item
        dest = target_models_dir / item
        if source.is_dir():
            continue
        else:
            copy2(source, dest)
