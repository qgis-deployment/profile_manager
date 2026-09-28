# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load ProfileManager class from file ProfileManager.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .profile_manager import ProfileManager

    return ProfileManager(iface)
