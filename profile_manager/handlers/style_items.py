from pathlib import Path
from shutil import copy

from qgis.core import Qgis, QgsStyle

from profile_manager.toolbelt.log_handler import PlgLogger


logger = PlgLogger()

# relevant info and functions:
# - Human-readable name of the entity type (dammit SIP, why is this not easily available...) in plural
# - QgsStyle method name for getting the names of all existing entities of a specific type
# - QgsStyle method name for getting a specific entity by name
# - QgsStyle method name for adding an entity to the style
ENTITY_ACCESSORS = {
    QgsStyle.StyleEntity.ColorrampEntity: (
        "color ramps",
        "colorRampNames",
        "colorRamp",
        "addColorRamp",
    ),
    QgsStyle.StyleEntity.LabelSettingsEntity: (
        "label settings",
        "labelSettingsNames",
        "labelSettings",
        "addLabelSettings",
    ),
    QgsStyle.StyleEntity.LegendPatchShapeEntity: (
        "legend patch shapes",
        "legendPatchShapeNames",
        "legendPatchShape",
        "addLegendPatchShape",
    ),
    QgsStyle.StyleEntity.Symbol3DEntity: (
        "3D symbols",
        "symbol3DNames",
        "symbol3D",
        "addSymbol3D",
    ),
    QgsStyle.StyleEntity.SymbolEntity: (
        "symbols",
        "symbolNames",
        "symbol",
        "addSymbol",
    ),
    QgsStyle.StyleEntity.TextFormatEntity: (
        "text formats",
        "textFormatNames",
        "textFormat",
        "addTextFormat",
    ),
}  # as of QGIS 3.16

# QGIS 4.2 added Material Settings:
if Qgis.QGIS_VERSION_INT >= 40203:
    ENTITY_ACCESSORS[QgsStyle.StyleEntity.MaterialSettingsEntity] = (
        "material settings",
        "materialSettingsNames",
        "materialSettings",
        "addMaterialSettings",
    )


def _load_style_db(db_path: Path) -> QgsStyle:
    """Load a QGIS style database.

    :param db_path: path to the `symbology-style.db` file
    :type db_path: Path

    :raises RuntimeError: if the database cannot be loaded
    :return: loaded style database
    :rtype: QgsStyle
    """
    style_db = QgsStyle()
    if not style_db.load(str(db_path)):
        raise RuntimeError(
            f"Failed to load style database {db_path}: {style_db.errorString()}"
        )
    return style_db


def import_style_items(source_profile_path: Path, target_profile_path: Path) -> None:
    """Imports style items from source profile to target profile.

    Transfers color ramps, label settings, legend patch shapes, material
    settings (QGIS 4.2+), 3D symbols, symbols, text formats.
    Tags and the "favorite" mark of style items are also transferred.
    Note: Smart Groups are currently not transferred.

    Note: Existing style items with identical names will be overwritten!

    Style items are stored in symbology-style.db.

    :param source_profile_path: path of profile directory to import from
    :type source_profile_path: Path
    :param target_profile_path: path of profile directory to import to
    :type target_profile_path: Path

    :raises RuntimeError: if a database cannot be loaded or an item, its tags or
        its favorite mark cannot be written to the target
    """
    source_db_path = source_profile_path / "symbology-style.db"
    target_db_path = target_profile_path / "symbology-style.db"

    # try if we can straight up copy the file to the target profile
    if not target_db_path.is_file():
        logger.log("No existing style database in target, importing whole database.")
        copy(source_db_path, target_db_path)
        return

    source_style_db = _load_style_db(source_db_path)
    target_style_db = _load_style_db(target_db_path)

    for entity_type, (type_name, names_fn, get_fn, add_fn) in ENTITY_ACCESSORS.items():
        names = getattr(source_style_db, names_fn)()
        logger.log(f"Importing {len(names)} {type_name}")
        favorite_names = set(source_style_db.symbolsOfFavorite(entity_type))

        for name in names:
            # get from source, add to target
            entry = getattr(source_style_db, get_fn)(name)
            if not getattr(target_style_db, add_fn)(name, entry, update=True):
                raise RuntimeError(f"Failed to import {type_name}: {name!r}")

            # handle tags and favorite mark, if exist
            tags = source_style_db.tagsOfSymbol(entity_type, name)
            if tags and not target_style_db.tagSymbol(entity_type, name, tags):
                raise RuntimeError(f"Failed to tag {type_name}: {name!r}")
            if name in favorite_names and not target_style_db.addFavorite(
                entity_type, name
            ):
                raise RuntimeError(f"Failed to mark {type_name} as favorite: {name!r}")

    # we do not need to save the target file
