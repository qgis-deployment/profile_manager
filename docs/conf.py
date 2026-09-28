#!python3

"""
Configuration for project documentation using Sphinx.
"""

# standard
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Union


# move into project package
sys.path.insert(0, f"{Path(__file__).parent.parent.resolve()}")

# 3rd party
import keepachangelog

# Package
from profile_manager import __about__


logger: logging.Logger = logging.getLogger(__name__)

# -- Project information -----------------------------------------------------
changes: dict[str, dict] = keepachangelog.to_dict("../CHANGELOG.md")
latest_version: str = [
    v for v in changes.keys() if v not in ("Unreleased", "version_tag")
][0]

author: str = __about__.__author__
copyright: str = __about__.__copyright__
description: str = __about__.__summary__
project: str = __about__.__title__
version = release = latest_version

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions: list[str] = [
    # Sphinx included
    "sphinx.ext.autodoc",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.extlinks",
    "sphinx.ext.githubpages",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    # 3rd party
    "myst_parser",
    "sphinx.ext.napoleon",  # google style docstrings
    "sphinx_copybutton",
]


# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
source_suffix = {".md": "markdown", ".rst": "restructuredtext"}
autosectionlabel_prefix_document = True
# The master toctree document.
master_doc = "index"


# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path .
exclude_patterns = [
    "_build",
    ".venv",
    "Thumbs.db",
    ".DS_Store",
    "_output",
    "ext_libs",
    "tests",
    "demo",
]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"


# -- Options for HTML output -------------------------------------------------

# -- Theme

html_favicon = str(__about__.__icon_path__)
html_logo = str(__about__.__icon_path__)
# uncomment next line if you store some statics which are not directly linked into the markdown/RST files
# html_static_path = ["static/include_additional"]
html_theme = "furo"

# -- EXTENSIONS --------------------------------------------------------

# Sphinx API doc
autodoc_mock_imports: list[str] = [
    "pyplugin_installer",
    "qgis.core",
    "qgis.gui",
    "qgis.PyQt",
    "qgis.PyQt.QtCore",
    "qgis.PyQt.QtGui",
    "qgis.PyQt.QtNetwork",
    "qgis.PyQt.QtWidgets",
    "qgis.utils",
]

# Configuration for intersphinx (refer to others docs).
intersphinx_mapping = {
    "PyQt5": ("https://www.riverbankcomputing.com/static/Docs/PyQt5", None),
    "python": ("https://docs.python.org/3/", None),
    "qgis": ("https://qgis.org/pyqgis/master/", None),
}

# MyST Parser
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "dollarmath",
    "html_image",
    "linkify",
    "replacements",
    "smartquotes",
    "substitution",
]

myst_substitutions = {
    "author": author,
    "date_update": datetime.now().strftime("%d %B %Y"),
    "description": description,
    "qgis_version_max": __about__.__plugin_md__.get("general").get(
        "qgismaximumversion"
    ),
    "qgis_version_min": __about__.__plugin_md__.get("general").get(
        "qgisminimumversion"
    ),
    "repo_url": __about__.__uri__,
    "title": project,
    "version": version,
}

myst_url_schemes = ("http", "https", "mailto")


# -- Functions ------------------------------------------------------------------
def generate_qdt_snippet(_) -> None:
    """Generate QDT snippet for profiles.json files."""
    logger.warning("=== START GENERATING QDT SNIPPET ===")

    qdt_snippet: dict[str, Union[str, bool, int]] = {
        "name": "Profile Manager",
        "folder_name": "profile_manager",
        "official_repository": True,
        "plugin_id": 3547,
        "version": f"{latest_version}",
    }

    with Path("./docs/static/qdt_snippet.json").open("w", encoding="UTF8") as wf:
        wf.write(json.dumps(qdt_snippet, indent=4, sort_keys=True))


# -- API Doc --------------------------------------------------------
# run api doc
def run_apidoc(_):
    from sphinx.ext.apidoc import main

    logger.info("=== START SPHINX API AUTODOC ===")

    cur_dir = Path(__file__).parent.resolve()
    output_path = str(cur_dir.joinpath("_apidoc").resolve())
    modules = str(cur_dir.joinpath("../profile_manager/").resolve())
    exclusions = ["../.venv", "../tests"]
    main(["-e", "-f", "-M", "-o", output_path, modules] + exclusions)


# launch setup
def setup(app):
    app.connect("builder-inited", run_apidoc)
    app.connect("builder-inited", generate_qdt_snippet)
