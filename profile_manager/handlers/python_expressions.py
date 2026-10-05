from pathlib import Path
from shutil import copy2

from profile_manager.toolbelt.log_handler import PlgLogger


logger = PlgLogger()


def import_python_expressions(source_profile_path: Path, target_profile_path: Path):
    """Imports Python expressions from source to target profile.

    Note: Existing modules with identical filenames will be overwritten!

    Expressions are stored in modules (.py files) python/expressions/ subdirectory
    of a profile, e.g.:

    .. code-block::

       ...
       python/expressions/__init__.py
       python/expressions/default.py
       python/expressions/foo.py
       ...

    Args:
        source_profile_path: Path of profile directory to import from
        target_profile_path: Path of profile directory to import to
    """
    source_expressions_dir = source_profile_path / "python" / "expressions"
    target_expressions_dir = target_profile_path / "python" / "expressions"

    if not source_expressions_dir.exists():
        logger.log("No Python expressions found in source profile")
        return

    if not target_expressions_dir.exists():
        target_expressions_dir.mkdir(parents=True, exist_ok=True)
        (target_expressions_dir / "__init__.py").touch()

    for python_file in Path(source_expressions_dir).glob("*.py"):
        filename = python_file.name
        logger.log(f"Copying Python expressions file: {filename}")
        dest = target_expressions_dir / filename
        copy2(python_file, dest)
