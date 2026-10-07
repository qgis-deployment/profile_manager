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
        (
            "material settings",
            "materialSettingsNames",
            "materialSettings",
            "addMaterialSettings",
        ),
    )


def import_style_items(source_profile_path: Path, target_profile_path: Path):
    """Imports style items from source profile to target profile.

    Transfers color ramps, label settings, legend patch shapes, material
    settings (QGIS 4.2+), 3D symbols, symbols, text formats.
    Tags and the "favorite" mark of style items are also transferred.
    Note: Smart Groups are currently not transferred.

    Note: Existing style items with identical names will be overwritten!

    Style items are stored in symbology-style.db.

    Args:
        source_profile_path: Path of profile directory to import from
        target_profile_path: Path of profile directory to import to
    """
    # Simply using assertions to check return codes of QGIS functions here, because
    # this code should never run in environments where asserts are optimized away.

    source_db_path = source_profile_path / "symbology-style.db"
    target_db_path = target_profile_path / "symbology-style.db"

    # try if we can straight up copy the file to the target profile
    if not target_db_path.is_file():
        logger.log("No existing style database in target, importing whole database.")
        copy(source_db_path, target_db_path)
        return

    source_style_db = QgsStyle()
    assert source_style_db.load(str(source_db_path)), source_style_db.errorString()
    target_style_db = QgsStyle()
    assert target_style_db.load(str(target_db_path)), target_style_db.errorString()

    for entity_type, (type_name, names_fn, get_fn, add_fn) in ENTITY_ACCESSORS.items():
        names = getattr(source_style_db, names_fn)()
        logger.log(f"Importing {len(names)} {type_name}")
        favorite_names = set(source_style_db.symbolsOfFavorite(entity_type))

        for name in names:
            # get from source, add to target
            entry = getattr(source_style_db, get_fn)(name)
            assert getattr(target_style_db, add_fn)(name, entry, update=True)

            # handle tags and favorite mark, if exist
            tags = source_style_db.tagsOfSymbol(entity_type, name)
            if tags:
                assert target_style_db.tagSymbol(entity_type, name, tags)
            if name in favorite_names:
                assert target_style_db.addFavorite(entity_type, name)

    # we do not need to save the target file
