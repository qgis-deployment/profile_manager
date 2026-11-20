#! python3  # noqa: E265

"""Static values shared across the plugin."""

# standard
import re
from pathlib import Path
from typing import Tuple


# -- QGIS profile layout (relative to a profile folder) --
PROFILE_BOOKMARKS_FILENAME: str = "bookmarks.xml"
PROFILE_MODELS_DIR: Path = Path("processing", "models")
PROFILE_MODELS_GLOB: str = "*.model3"
PROFILE_PLUGINS_DIR: Path = Path("python", "plugins")
PROFILE_PYTHON_EXPRESSIONS_DIR: Path = Path("python", "expressions")
PROFILE_SCRIPTS_DIR: Path = Path("processing", "scripts")
PROFILE_STYLE_DB_FILENAME: str = "symbology-style.db"
PYTHON_FILES_GLOB: str = "*.py"

# validation rule from QgsUserProfileSelectionDialog
PROFILE_NAME_RE: re.Pattern = re.compile(r"[^/\\]+")

# -- QGIS UI customization file, stored next to the settings INI file --
QGIS3_CUSTOMIZATION_FILENAME: str = "QGISCUSTOMIZATION3.ini"
QGIS4_CUSTOMIZATION_FILENAME: str = "QGISCUSTOMIZATION.xml"

# -- QGIS settings (QGIS3/4.ini...) sections and keys --
QGIS_SETTINGS_CUSTOMIZATION_ENABLED_KEY: str = "UI/Customization/enabled"
QGIS_SETTINGS_EXPRESSIONS_GROUP: str = "expressions/user"
QGIS_SETTINGS_EXPRESSION_KEY: str = "expression"
QGIS_SETTINGS_EXPRESSION_HELP_TEXT_KEY: str = "helpText"
QGIS_SETTINGS_FAVOURITES_KEY: str = "browser/favourites"
QGIS_SETTINGS_LOCALE_KEY: str = "locale/userLocale"
QGIS_SETTINGS_PLUGINS_SECTION: str = "PythonPlugins"

# -- QGIS plugins --
OFFICIAL_REPOSITORY_URL: str = "https://plugins.qgis.org/plugins/plugins.xml"
PLUGIN_METADATA_FILENAME: str = "metadata.txt"
PLUGIN_METADATA_SECTION: str = "general"

# -- Profile Manager --
BACKUP_DIR_NAME: str = "QGIS Profile Manager Backup"

# -- QDT --
QDT_EXPORT_EXCLUDED_DIRS: Tuple[Path, ...] = (
    Path("cache"),
    Path("oauth2-cache"),
    PROFILE_PLUGINS_DIR,
)
QDT_PROFILE_FILENAME: str = "profile.json"
QDT_PROFILE_REQUIRED_FIELDS: Tuple[str, ...] = ("author", "email", "version")
QDT_PROFILE_SCHEMA_URL: str = (
    "https://raw.githubusercontent.com/qgis-deployment/"
    "qgis-deployment-toolbelt-cli/main/docs/schemas/profile/qgis_profile.json"
)
# regex SemVer for different versions fields
QDT_VERSION_PATTERN: str = r"^(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)(?:\.(?:0|[1-9]\d*))?$"
QDT_VERSION_MAX_LENGTH: int = 14
