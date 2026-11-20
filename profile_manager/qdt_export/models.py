from dataclasses import dataclass
from typing import Any, Dict, Optional

from profile_manager.constants import OFFICIAL_REPOSITORY_URL


@dataclass
class QdtPluginInformation:
    """QGIS Plugin representation for QDT profile export."""

    name: str
    folder_name: str
    version: str
    download_url: Optional[str] = None
    plugin_id: Optional[int] = None
    repository_url: Optional[str] = None

    def as_dict(self) -> Dict[str, Any]:
        """Custom as_dict method to handle properties and specific vars.

        :return: plugin as dict, ready to be written into a QDT profile.json
        :rtype: Dict[str, Any]
        """
        out_dict = {
            "name": self.name,
            "folder_name": self.folder_name,
            "official_repository": self.official_repository,
            "plugin_id": self.plugin_id,
            "version": self.version,
        }
        if not self.official_repository:
            if self.repository_url:
                out_dict["repository_url_xml"] = self.repository_url
            # local plugins have a filesystem path as download URL: not exportable
            if self.download_url and self.download_url.startswith(
                ("http://", "https://")
            ):
                out_dict["url"] = self.download_url

        return out_dict

    @property
    def official_repository(self) -> bool:
        """Check if plugin is from official QGIS repository, based on the URL
        of the repository it was installed from.

        :return: True if plugin is from official QGIS repository.
        :rtype: bool
        """
        return self.repository_url == OFFICIAL_REPOSITORY_URL


@dataclass
class QDTProfileInfos:
    """Store informations for QDT profile creation"""

    author: str = ""
    description: str = ""
    email: str = ""
    folder_name: str = ""
    name: str = ""
    qgis_min_version: str = ""
    qgis_max_version: str = ""
    version: str = ""
