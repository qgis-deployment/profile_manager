# Profile Manager for QGIS

A QGIS plugin for managing your profiles and data source connections.

Published on the official QGIS plugins repository: <https://plugins.qgis.org/plugins/profile_manager/>.

<!-- markdownlint-disable MD033 -->
<a href="https://qgis-deployment.github.io/profile_manager/_images/profile_manager_ui_tab_manage-profiles.png"><img src="https://qgis-deployment.github.io/profile_manager/_images/profile_manager_ui_tab_manage-profiles.png" width="200" alt="Profile Manager for QGIS - Manage profiles" ></a>
<a href="https://qgis-deployment.github.io/profile_manager/_images/profile_manager_ui_tab_share_plugins.png"><img src="https://qgis-deployment.github.io/profile_manager/_images/profile_manager_ui_tab_share_plugins.png" width="200" alt="Profile Manager - Import plugins between profiles"></a>
<a href="https://qgis-deployment.github.io/profile_manager/_images/profile_manager_ui_tab_share_data-sources.png"><img src="https://qgis-deployment.github.io/profile_manager/_images/profile_manager_ui_tab_share_data-sources.png" width="200" alt="Profile Manager - Import data sources between profiles"></a>
<a href="https://qgis-deployment.github.io/profile_manager/_images/profile_manager_ui_tab_share_other.png"><img src="https://qgis-deployment.github.io/profile_manager/_images/profile_manager_ui_tab_share_other.png" width="200" alt="Profile Manager - Import other resources between profiles"></a>
<a href="https://qgis-deployment.github.io/profile_manager/_images/profile_manager_ui_tab_QDT-export.png"><img src="https://qgis-deployment.github.io/profile_manager/_images/profile_manager_ui_tab_QDT-export.png" width="200" alt="Profile Manager - Export for QDT"></a>
<!-- markdownlint-enable MD033 -->

📖 Check out the documentation: <https://qgis-deployment.github.io/profile_manager/>.

> [!IMPORTANT]
> Handle with care.  
> This plugin is still in an early stage. There is no thorough, automated testing yet.  
> Please consider everything potentially broken and make sure you thoroughly check the results of your actions. We welcome bug reports and ideas for improvement. Your collaboration in coding or documenting its features and limitations would be highly appreciated.

## Features

- Create a new profile
- Removing profiles
- Copying profiles
- Renaming profiles
- Importing data source connections from one profile to another
- Removing data source connections from a profile
- Importing (spatial) bookmarks
- Importing (data source) favourites
- Importing and removing plugins
- Importing expressions
- Importing Python expression functions
- Importing models
- Importing scripts
- Importing style items (color ramps, label settings, legend patch shapes, material settings (QGIS 4.2+), 3D symbols, symbols, text formats)
- Importing QGIS UI settings (e.g. hidden toolbar items)
- Exporting a profile in QGIS Deployment Toolkit (QDT) format

On all removal operations the user is being asked if they are certain that they want to delete given source/profile.
Additionally, before every import or deletion, a backup of the affected profile is created in the user's home directory.

## Known (current) limitations

- Not all data source connections might be recognized and imported/removed
- Not all data source connection types are supported
- Errors might not always be communicated clearly so please TEST your migrated configurations before discarding originals!
- Creating a new profile does not lead to the same result as creating a new profile in the QGIS GUI, e.g. the QGIS3.ini is not populated with defaults.

## Funding development

If you consider this plugin useful and would like to see it improved, e.g. with support for more profile settings, becoming more stable, being more thoroughly documented, leave the "experimental" plugin status or whatever you desire, you can fund development. Contact us at <info@wheregroup.com>.
