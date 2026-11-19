from typing import Iterable

from qgis.PyQt.QtCore import QSortFilterProxyModel, Qt
from qgis.PyQt.QtWidgets import QAbstractItemView, QHeaderView, QTreeView, QWidget

from profile_manager.gui.mdl_qdt_plugins import QdtPluginListModel
from profile_manager.qdt_export.models import QdtPluginInformation


class QdtPluginListView(QTreeView):
    """Read-only, sortable, multi-column flat list of QDT profile plugins.

    A QTreeView without root decoration is used rather than a QListView, which
    can only display a single column.
    Owns its QdtPluginListModel; can be promoted from a QTreeView in Qt Designer.
    """

    def __init__(self, parent: QWidget | None = None):
        """
        Args:
            parent: QWidget parent
        """
        super().__init__(parent)
        self.plugin_model = QdtPluginListModel(self)

        # proxy for case-insensitive sorting by column
        self._proxy_model = QSortFilterProxyModel(self)
        self._proxy_model.setSourceModel(self.plugin_model)
        self._proxy_model.setSortCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.setModel(self._proxy_model)

        self.setRootIsDecorated(False)
        self.setItemsExpandable(False)
        self.setUniformRowHeights(True)
        self.setAlternatingRowColors(True)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSortingEnabled(True)
        self.sortByColumn(QdtPluginListModel.NAME_COL, Qt.SortOrder.AscendingOrder)

        header = self.header()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        header.setStretchLastSection(True)

    def set_plugins(self, plugins: Iterable[QdtPluginInformation]) -> None:
        """Display the given plugins

        Args:
            plugins (Iterable[QdtPluginInformation]): plugins to display
        """
        self.plugin_model.set_plugins(plugins)

    def clear(self) -> None:
        """Remove all displayed plugins"""
        self.plugin_model.set_plugins([])
