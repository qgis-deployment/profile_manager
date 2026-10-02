from qgis.core import QgsSettings
from qgis.gui import QgsFileWidget, QgsOptionsPageWidget, QgsOptionsWidgetFactory
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QGridLayout, QGroupBox, QLabel, QVBoxLayout

from profile_manager.__about__ import __icon_path__


class ProfileManagerOptionsPage(QgsOptionsPageWidget):
    """Profile Manager options widget"""

    # inspired by SLYR <3

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("profileManagerOptions")

        groupbox = QGroupBox()
        groupbox.setTitle("Automatic Backups")
        backup_text = QLabel(
            "The Profile Manager can automatically store backups when a profile is manipulated."
        )
        backup_text.setStyleSheet("font-style: italic;")
        backup_directory_label = QLabel("Path to backup directory")
        self.backup_directory_widget = QgsFileWidget()

        backup_layout = QGridLayout()
        backup_layout.addWidget(backup_text, 0, 0, 1, 2)
        backup_layout.addWidget(backup_directory_label, 2, 0)
        backup_layout.addWidget(self.backup_directory_widget, 2, 1)
        groupbox.setLayout(backup_layout)

        layout = QVBoxLayout(self)
        layout.addWidget(groupbox)
        layout.addStretch()

        self.backup_directory_widget.setStorageMode(
            QgsFileWidget.StorageMode.GetDirectory
        )

        # set existing value from settings or use default
        self.backup_directory_widget.setFilePath(
            QgsSettings().value("/plugins/profile_manager/backup_directory", None)
        )

    def apply(self):
        """Applies the (new) settings"""
        QgsSettings().setValue(
            "/plugins/profile_manager/backup_directory",
            self.backup_directory_widget.filePath(),
        )


class ProfileManagerOptionsFactory(QgsOptionsWidgetFactory):
    """Factory class for Profile Manager options widget"""

    def __init__(self):
        super().__init__()

    def icon(self):
        return QIcon(str(__icon_path__))

    def createWidget(self, parent):
        return ProfileManagerOptionsPage(parent)
