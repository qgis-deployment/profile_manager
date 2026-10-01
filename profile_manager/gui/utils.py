from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QListWidgetItem, QTreeWidgetItem


def data_sources_as_tree(
    provider: str, data_sources: dict, make_checkable: bool
) -> QTreeWidgetItem:
    """Returns a tree of checkable items for all specified data sources, the root item named by the provider.

    The tree contains a checkable item per data source found.

    Args:
        provider: Name of the provider to gather data sources for
        data_sources: TODO document structure
        make_checkable: Flag to indicate if items should be checkable

    Returns:
        QTreeWidgetItem: Tree widget item representing the data sources or None if none were found
    """

    tree_root_item = QTreeWidgetItem([provider])
    if make_checkable:
        tree_root_item.setFlags(
            tree_root_item.flags()
            | Qt.ItemFlag.ItemIsAutoTristate
            | Qt.ItemFlag.ItemIsUserCheckable
        )

    data_source_items = []
    for data_source in data_sources:
        data_source_item = QTreeWidgetItem([data_source])
        if make_checkable:
            data_source_item.setFlags(
                data_source_item.flags() | Qt.ItemFlag.ItemIsUserCheckable
            )
            data_source_item.setCheckState(0, Qt.CheckState.Unchecked)
        data_source_items.append(data_source_item)

    tree_root_item.addChildren(data_source_items)
    return tree_root_item


def plugins_as_items(plugins: list[str], make_checkable: bool) -> list[QListWidgetItem]:
    """Return the plugins as list of QListWidgetItem."""
    items = []
    for plugin_name in plugins:
        item = QListWidgetItem()

        if make_checkable:
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Unchecked)
        else:
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsSelectable)

        item.setText(plugin_name)

        items.append(item)

    return items
