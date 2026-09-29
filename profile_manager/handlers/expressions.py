from pathlib import Path

from qgis.PyQt.QtCore import QSettings

from profile_manager.toolbelt.log_handler import PlgLogger


logger = PlgLogger()


def import_expressions(source_qgis_ini_file: Path, target_qgis_ini_file: Path):
    r"""Imports custom expressions from source to target profile.

    Custom expressions are stored in QGIS/QGIS3.ini's [expressions] section, e.g.:

    .. code-block:: ini

       ...
       [expressions]
       ...
       user\test_expression\expression=1 + 1
       user\test_expression\helpText="..."
       ...

    Note: This does not handle Python expression functions.

    Args:
        source_qgis_ini_file: Path of source QGIS3.ini file
        target_qgis_ini_file: Path of target QGIS3.ini file
    """
    # Note: We are using QSettings because that will handle all the specialities
    #       of Qt's INI format for us. A standard INI parser (like configparser)
    #       would require extra work, e.g. for the child groups or percent encodings.
    source_settings = QSettings(str(source_qgis_ini_file), QSettings.Format.IniFormat)
    target_settings = QSettings(str(target_qgis_ini_file), QSettings.Format.IniFormat)

    # go into the "user" group of the "expressions" section
    source_settings.beginGroup("expressions/user")
    if not source_settings.childGroups():
        logger.log("No expressions found in source profile")
        return

    target_settings.beginGroup("expressions/user")  # will be created as needed

    # Expressions use two lines each, as child groups:
    # - expressions/user/FOO/expression
    # - expressions/user/FOO/helpText
    # - expressions/user/BAR/expression
    # - expressions/user/BAR/helpText
    # - expressions/user/BAZ/*
    # - expressions/user/OOF/*
    # = FOO, BAR, BAZ, OOF are child groups
    for source_expression_group in source_settings.childGroups():
        source_expression_name = source_expression_group
        logger.log(f"Copying expression: {source_expression_name}")

        source_settings.beginGroup(source_expression_name)
        source_expression_expression = source_settings.value("expression")
        source_expression_helptext = source_settings.value("helpText")
        source_settings.endGroup()

        target_settings.beginGroup(source_expression_name)
        target_settings.setValue("expression", source_expression_expression)
        target_settings.setValue("helpText", source_expression_helptext)
        target_settings.endGroup()

    # writing the target file is handled by QSettings’s destructor
