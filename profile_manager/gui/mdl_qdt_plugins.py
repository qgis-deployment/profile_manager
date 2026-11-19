from typing import Iterable, List, Optional

from qgis.PyQt.QtCore import QModelIndex, QObject, Qt
from qgis.PyQt.QtGui import QStandardItem, QStandardItemModel

from profile_manager.qdt_export.models import QdtPluginInformation


class QdtPluginListModel(QStandardItemModel):
    """QStandardItemModel to display plugins of a QDT profile"""

    NAME_COL = 0
    VERSION_COL = 1
    FOLDER_NAME_COL = 2
    PLUGIN_ID_COL = 3
    REPOSITORY_COL = 4

    # role storing the QdtPluginInformation on the name item of each row
    PLUGIN_ROLE = Qt.ItemDataRole.UserRole + 1

    def __init__(self, parent: QObject = None):
        """
        QStandardItemModel for QDT plugin list display

        Args:
            parent: QObject parent
        """
        super().__init__(parent)
        self.setHorizontalHeaderLabels(
            [
                self.tr("Name"),
                self.tr("Version"),
                self.tr("Folder name"),
                self.tr("ID"),
                self.tr("Repository"),
            ]
        )

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        """Define flags for an index.
        Used to disable edition.

        Args:
            index (QModelIndex): data index

        Returns:
            Qt.ItemFlags: flags
        """
        default_flags = super().flags(index)
        return default_flags & ~Qt.ItemFlag.ItemIsEditable  # Disable editing

    def set_plugins(self, plugins: Iterable[QdtPluginInformation]) -> None:
        """Replace model content with the given plugins

        Args:
            plugins (Iterable[QdtPluginInformation]): plugins to display
        """
        self.removeRows(0, self.rowCount())
        for plugin in plugins:
            self.insert_plugin(plugin)

    def insert_plugin(self, plugin: QdtPluginInformation) -> None:
        """Insert plugin in model

        Args:
            plugin (QdtPluginInformation): plugin to insert
        """
        if plugin.official_repository:
            repository = self.tr("Official (plugins.qgis.org)")
        else:
            repository = plugin.repository_url or ""

        name_item = QStandardItem(plugin.name)
        name_item.setData(plugin, self.PLUGIN_ROLE)
        id_item = QStandardItem()
        if plugin.plugin_id is not None:
            # numeric data so that sorting by ID is numeric
            id_item.setData(plugin.plugin_id, Qt.ItemDataRole.DisplayRole)

        row = [
            name_item,
            QStandardItem(plugin.version),
            QStandardItem(plugin.folder_name),
            id_item,
            QStandardItem(repository),
        ]

        tooltip = self._plugin_tooltip(plugin)
        for item in row:
            item.setToolTip(tooltip)

        self.appendRow(row)

    def plugins(self) -> List[QdtPluginInformation]:
        """Get plugins stored in model, in row order

        Returns:
            List[QdtPluginInformation]: plugins
        """
        return [self.plugin(row) for row in range(self.rowCount())]

    def plugin(self, row: int) -> Optional[QdtPluginInformation]:
        """Get plugin stored at a given row

        Args:
            row (int): model row

        Returns:
            Optional[QdtPluginInformation]: plugin, None if row is invalid
        """
        return self.data(self.index(row, self.NAME_COL), self.PLUGIN_ROLE)

    def _plugin_tooltip(self, plugin: QdtPluginInformation) -> str:
        """Build tooltip summarizing all plugin attributes

        Args:
            plugin (QdtPluginInformation): plugin

        Returns:
            str: tooltip text
        """
        lines = [
            f"{self.tr('Name')}: {plugin.name}",
            f"{self.tr('Version')}: {plugin.version}",
            f"{self.tr('Folder name')}: {plugin.folder_name}",
        ]
        if plugin.plugin_id is not None:
            lines.append(f"{self.tr('ID')}: {plugin.plugin_id}")
        if plugin.repository_url:
            lines.append(f"{self.tr('Repository')}: {plugin.repository_url}")
        if plugin.download_url:
            lines.append(f"{self.tr('Download URL')}: {plugin.download_url}")
        return "\n".join(lines)
