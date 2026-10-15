#! python3  # noqa: E265

"""Custom exceptions."""


class ProfileManagerError(Exception):
    """Base class for expected, user-facing errors raised by the plugin."""


class StyleDatabaseError(ProfileManagerError, RuntimeError):
    """A style database (``symbology-style.db``) cannot be loaded."""


class StyleDatabaseNotFoundError(ProfileManagerError, FileNotFoundError):
    """A style database (``symbology-style.db``) does not exist."""


class ItemImportError(ProfileManagerError, RuntimeError):
    """An item (bookmark, style item...) cannot be written to the target profile."""

    def __init__(
        self,
        message: str,
        *,
        item_type: str | None = None,
        item_name: str | None = None,
    ) -> None:
        """Initialization method.

        :param message: error message
        :type message: str
        :param item_type: human-readable type of the item, e.g. ``"symbols"``.
            Defaults to None.
        :type item_type: str | None, optional
        :param item_name: name of the item. Defaults to None.
        :type item_name: str | None, optional
        """
        super().__init__(message)
        self.item_type: str | None = item_type
        self.item_name: str | None = item_name


class InvalidItemError(ItemImportError, ValueError):
    """An item read from the source profile is invalid (null or unnamed)."""
