# standard
from configparser import RawConfigParser
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from re import compile
from urllib.parse import unquote

# PyQGIS
from qgis.core import Qgis

# plugin
from profile_manager.toolbelt import PlgLogger


# -- GLOBALS
logger = PlgLogger()


@dataclass
class Rule:
    """Section and regex for find data source connections in a QGIS3.ini file."""

    section: str  # INI section in which to search for regex matches
    regex: str  # regex to search for in the keys of the section


DATA_SOURCE_SEARCH_RULES = {
    # Where to search for which provider's data sources in the QGIS3.ini.
    # A list of searching rules each; not just one rule, because QGIS changed between
    # versions AND stores stuff in various places anyways.
    # This is based on a config grown over years, currently in 3.38.
    # Each regex must include a group for getting the (encoded) *data source name*,
    # e.g. ([^=^\\]+) between delimiters:
    # - ^= to not get into the *value* part of the line into the group
    #   e.g. ows\items\WMS\connections\items\foo\http-header=@Variant(\0\0\0\b\0\0\0\0)
    # - ^\\ to not get issues in the group if an option includes more backslashes
    #   e.g. connections-vector-tile\foo%20bar\http-header\referer=baz
    "GeoPackage": [Rule("providers", r"^ogr\\GPKG\\connections\\([^=^\\]+)\\")],
    "SpatiaLite": [Rule("SpatiaLite", r"^connections\\([^=^\\]+)\\")],
    "PostgreSQL": [Rule("PostgreSQL", r"^connections\\([^=^\\]+)\\")],
    "MS SQL Server": [Rule("MSSQL", r"^connections\\([^=^\\]+)\\")],
    "Vector Tiles": [
        Rule("connections", r"^vector-tile\\items\\([^=^\\]+)\\"),
        Rule("qgis", r"^connections-vector-tile\\([^=^\\]+)\\"),
    ],
    "WMS/WMTS": [
        # only authcfg, password and username at "ows\items\WMS", the rest is at "ows\items\wms"
        Rule("connections", r"^ows\\items\\WMS\\connections\\items\\([^=^\\]+)\\"),
        Rule("connections", r"^ows\\items\\wms\\connections\\items\\([^=^\\]+)\\"),
        Rule("qgis", r"WMS\\([^=^\\]+)\\"),  # only authcfg, password and username
        # only authcfg, password and username at "connections\WMS", the rest is at "connections-wms"
        Rule("qgis", r"^connections\\WMS\\([^=^\\]+)\\"),
        Rule("qgis", r"^connections-wms\\([^=^\\]+)\\"),
    ],
    "WFS / OGC API - Features": [  # same as WMS
        # only authcfg, password and username at "ows\items\WFS", the rest is at "ows\items\wfs"
        Rule("connections", r"^ows\\items\\WFS\\connections\\items\\([^=^\\]+)\\"),
        Rule("connections", r"^ows\\items\\wfs\\connections\\items\\([^=^\\]+)\\"),
        Rule("qgis", r"WFS\\([^=^\\]+)\\"),  # only authcfg, password and username
        # only authcfg, password and username at "connections\WFS", the rest is at "connections-wfs"
        Rule("qgis", r"^connections\\WFS\\([^=^\\]+)\\"),
        Rule("qgis", r"^connections-wfs\\([^=^\\]+)\\"),
    ],
    "WCS": [  # same as WMS
        # only authcfg, password and username at "ows\items\WCS", the rest is at "ows\items\wcs"
        Rule("connections", r"^ows\\items\\WCS\\connections\\items\\([^=^\\]+)\\"),
        Rule("connections", r"^ows\\items\\wcs\\connections\\items\\([^=^\\]+)\\"),
        Rule("qgis", r"WCS\\([^=^\\]+)\\"),  # only authcfg, password and username
        # only authcfg, password and username at "connections\WCS", the rest is at "connections-wcs"
        Rule("qgis", r"^connections\\WCS\\([^=^\\]+)\\"),
        Rule("qgis", r"^connections-wcs\\([^=^\\]+)\\"),
    ],
    "XYZ Tiles": [
        Rule("connections", r"^xyz\\items\\([^=^\\]+)\\"),
        Rule("qgis", r"^connections-xyz\\([^=^\\]+)\\"),
    ],
    "ArcGIS-REST-Server": [
        # both feature and map servers as using "featureserver" as defined below...
        Rule("qgis", r"^ARCGISFEATURESERVER\\([^=^\\]+)\\"),
        Rule("qgis", r"^connections-arcgisfeatureserver\\([^=^\\]+)\\"),
        Rule("connections", r"^arcgisfeatureserver\\items\\([^=^\\]+)\\"),
    ],
    "Scenes": [
        Rule("connections", r"^tiled-scene\\items([^=^\\]+)\\"),
    ],
    "SensorThings": [
        Rule("connections", r"^sensorthings\\items([^=^\\]+)\\"),
    ],
}


def collect_data_sources_of_provider(
    ini_path: Path, provider: str
) -> dict[str, dict[str, dict[str, str]]]:
    """Returns all data source connections of the specified provider in the INI file.

    Pseudo example:

    .. code-block:: python

       {
           "data_source_name1": {
               "section1": {
                   "option1": "value1",
                   "option2": "value2",
                   ...
               },
               "section2": {
                   ...
               },
           },
           "data_source_name2": {
               ...
           },
           ...
       }

    Args:
        ini_path (str): Path of the INI file to read
        provider (str): Name of the provider to gather connections of

    Returns:
        Discovered data source connections with their sections, options and values

    Raises:
        NotImplementedError: If the provider name is not (yet) known here
    """
    search_rules = DATA_SOURCE_SEARCH_RULES.get(provider)
    if not search_rules:
        raise NotImplementedError(f"Unknown provider: {provider}")

    ini_parser = RawConfigParser()
    ini_parser.optionxform = str  # str = case-sensitive option names
    ini_parser.read(ini_path)

    data_sources = {}
    for rule in search_rules:
        # multiple rules might reference the same section, but different entries in it
        section = rule.section
        if not ini_parser.has_section(section):
            continue

        regex = compile(rule.regex)

        for option in ini_parser.options(section):
            match = regex.search(option)
            if match:
                # data source name = matching the () group in the regexs
                # unquoting is needed for e.g. %20 or umlauts, latin-1 is the correct encoding
                # TODO Emoji, e.g. "💩" are not rendered well, also fail to import to other profile...
                data_source_name = unquote(match.group(1), "latin-1")

                value = ini_parser.get(section, option)

                # TODO lol clean this up? :) Some modern, typed data structure would be nice.
                if not data_sources.get(data_source_name):
                    data_sources[data_source_name] = {}
                if not data_sources[data_source_name].get(section):
                    data_sources[data_source_name][section] = {}
                data_sources[data_source_name][section][option] = value

    logger.log(
        log_level=Qgis.MessageLevel.Info,
        message=f"Found {len(data_sources)} {provider!r} data sources",
    )
    return data_sources


def collect_data_sources(
    ini_path: Path,
) -> dict[str, dict[str, dict[str, dict[str, str]]]]:
    """Collect all data sources and their ini entries (=options and values inside sections)"""
    logger.log(
        log_level=Qgis.MessageLevel.Info,
        message=f"Collecting data sources from  {ini_path}",
    )
    start_time = datetime.now()

    all_data_sources = {}
    for provider in DATA_SOURCE_SEARCH_RULES.keys():
        data_source_connections = collect_data_sources_of_provider(ini_path, provider)
        all_data_sources[provider] = data_source_connections
        # -> provider -> data source -> section -> option -> value

    time_taken = datetime.now() - start_time
    logger.log(
        log_level=Qgis.MessageLevel.NoLevel,
        message=f"Collecting data sources from {ini_path} took {time_taken.microseconds / 1000} ms",
    )

    return all_data_sources


def import_data_sources(
    qgis_ini_file: Path,
    data_sources_to_be_imported: dict[str, list[str]],
    available_data_sources: dict[str, dict[str, dict[str, dict[str, str]]]],
):
    """Import data sources to a QGIS3.ini file.

    Args:
        qgis_ini_file: Path of the QGIS3.ini file to import data sources to
        data_sources_to_be_imported: Provider name -> List of data source names to import
        available_data_sources: Available data sources, will be used find which options and
            values have to be imported in which sections.
            Providers -> Data sources -> Sections -> Options -> Values
    """
    logger.log(
        log_level=Qgis.MessageLevel.Info,
        message=(
            f"Importing {sum([len(v) for v in data_sources_to_be_imported.values()])} "
            f"data sources to {qgis_ini_file}"
        ),
    )
    start_time = datetime.now()

    parser = RawConfigParser()
    parser.optionxform = str  # str = case-sensitive option names
    parser.read(qgis_ini_file)

    for provider, data_sources in data_sources_to_be_imported.items():
        for data_source in data_sources:
            logger.log(
                log_level=Qgis.MessageLevel.Info,
                message=f"Importing {provider!r}: {data_source!r}",
            )

            # fetch sections+options for import
            sections = available_data_sources[provider][data_source]

            for section, options in sections.items():
                logger.log(
                    log_level=Qgis.MessageLevel.NoLevel,
                    message=f"Importing {section=}, {options=}",
                )
                if not parser.has_section(section):
                    parser.add_section(section)
                for option, value in options.items():
                    parser.set(section, option, value)

    with open(qgis_ini_file, "w") as qgisconf:
        parser.write(qgisconf, space_around_delimiters=False)

    time_taken = datetime.now() - start_time
    logger.log(
        log_level=Qgis.MessageLevel.NoLevel,
        message=f"Importing data sources to {qgis_ini_file} took {time_taken.microseconds / 1000} ms",
    )


def remove_data_sources(
    qgis_ini_file: Path,
    data_sources_to_be_removed: dict[str, list[str]],
    available_data_sources: dict[str, dict[str, dict[str, dict[str, str]]]],
):
    """Handles data source removal from file

    Args:
        qgis_ini_file: Path of the QGIS3.ini file to remove data sources from
        data_sources_to_be_removed: Provider name -> List of data source names to remove
        available_data_sources: Available data sources, will be used find which options in
            which sections have to be removed.
            Providers -> Data sources -> Sections -> Options
    """
    logger.log(
        log_level=Qgis.MessageLevel.Info,
        message=(
            f"Removing {sum([len(v) for v in data_sources_to_be_removed.values()])} "
            f"data sources from {qgis_ini_file}"
        ),
    )
    start_time = datetime.now()

    parser = RawConfigParser()
    parser.optionxform = str  # str = case-sensitive option names
    parser.read(qgis_ini_file)

    for provider, data_sources in data_sources_to_be_removed.items():
        for data_source in data_sources:
            logger.log(
                log_level=Qgis.MessageLevel.Info,
                message=f"Removing {provider!r}: {data_source!r}",
            )

            # fetch sections+options for deletion
            sections = available_data_sources[provider][data_source]

            for section, options in sections.items():
                logger.log(
                    log_level=Qgis.MessageLevel.NoLevel,
                    message=f"Removing {section=}, {options=}",
                )
                for option in options.keys():
                    parser.remove_option(section, option)

    with open(qgis_ini_file, "w") as qgisconf:
        parser.write(qgisconf, space_around_delimiters=False)

    time_taken = datetime.now() - start_time
    logger.log(
        log_level=Qgis.MessageLevel.NoLevel,
        message=f"Removing data sources from {qgis_ini_file} took {time_taken.microseconds / 1000} ms",
    )
