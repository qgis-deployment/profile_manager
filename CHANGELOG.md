# CHANGELOG

The format is based on [Keep a Changelog](https://keepachangelog.com/), and this project adheres to [Semantic Versioning](https://semver.org/).

<!--

Unreleased

## version_tag - YYYY-DD-mm

### Added

### Changed

### Removed

-->

## 0.8.0 - 2026-10-05

> 🤝 First release under the new QGIS Deployment organization

* fix: Don't swallow error messages of main import function by @kannes in <https://github.com/qgis-deployment/profile_manager/pull/141>
* chore: bump min QGIS version to 3.40.4 and Python to 3.11 by @Guts in <https://github.com/qgis-deployment/profile_manager/pull/125>
* QDT export: support plugins from unofficial repository by @Guts in <https://github.com/qgis-deployment/profile_manager/pull/75>
* Improve handlers by @kannes in <https://github.com/qgis-deployment/profile_manager/pull/142>
* Update GitHub references to qgis_deployment organisation by @kannes in <https://github.com/qgis-deployment/profile_manager/pull/128>
* Improve Sphinx docs by @kannes in <https://github.com/qgis-deployment/profile_manager/pull/138>
* remove(packaging): supportsQt6 flag is not a supported flag anymore in metadata.txt by @Guts in <https://github.com/qgis-deployment/profile_manager/pull/111>
* improve(ci): use token instead of personal credentials to release by @Guts in <https://github.com/qgis-deployment/profile_manager/pull/147>
* improve(ci): set GH token permissions by @Guts in <https://github.com/qgis-deployment/profile_manager/pull/148>

## 0.7.4 - 2026-01-20

> ♥️ Funded by Oslandia

* Proposal for a new logo by @sylvainbeo in <https://github.com/WhereGroup/profile_manager/pull/98>
* update(docs): add user guides by @Guts in <https://github.com/WhereGroup/profile_manager/pull/99>
* improve(ui): use freshly created SVG icon instead of small png by @Guts in <https://github.com/WhereGroup/profile_manager/pull/100>
* add(docs): auto generate QDT snippet and use keepachangelog to retrieve latest published verison from CHANGELOG.md by @Guts in <https://github.com/WhereGroup/profile_manager/pull/94>

## 0.7.3 - 2026-01-20

> ♥️ Funded by Oslandia

* fix(qt6): replace deprecated `Qt.ItemFlag.ItemIsTristate` with maintained `Qt.ItemFlag.ItemIsAutoTristate` by @Guts in <https://github.com/WhereGroup/profile_manager/pull/93>

## 0.7.2 - 2025-11-18

> ♥️ Funded by Oslandia

* fix(compatibility): imbricated f-string are not available in Python < 3.12 by @Guts in <https://github.com/WhereGroup/profile_manager/pull/87>

## 0.7.1 - 2025-10-27

> ♥️ Funded by Oslandia

* update(ui): add more icons and remove fixed size by @Guts in <https://github.com/WhereGroup/profile_manager/pull/81>
* update(i18n): complete French translations by @Guts in <https://github.com/WhereGroup/profile_manager/pull/82>

## 0.7.0 - 2025-10-22

* update(qdt): use new JSON schema URL by @Guts in <https://github.com/WhereGroup/profile_manager/pull/64>
* improve(ui): add icons to tabs by @Guts in <https://github.com/WhereGroup/profile_manager/pull/72>
* QDT export: sort plugins list a-Z by @Guts in <https://github.com/WhereGroup/profile_manager/pull/74>
* add(feature): replace Python logger with a centralized and QGIS integrated one by @Guts in <https://github.com/WhereGroup/profile_manager/pull/78>
* Fix translations loader by @Guts in <https://github.com/WhereGroup/profile_manager/pull/79>
* Improve: use icon path from metadata by @Guts in <https://github.com/WhereGroup/profile_manager/pull/80>
* fix(metadata): Remove hardcoded changelog from metadata.txt by @kannes in <https://github.com/WhereGroup/profile_manager/pull/61>
* improve(chore): modularize QDT related model by @Guts in <https://github.com/WhereGroup/profile_manager/pull/73>
* Update maximum QGIS version in metadata for QGIS 4 by @kannes in <https://github.com/WhereGroup/profile_manager/pull/77>

## 0.6.0 - 2025-04-03

* fix(qdt profile): plugin_id should be an int by @jmkerloch in <https://github.com/WhereGroup/profile_manager/pull/49>
* fix(docstrings): escape chars in sample ini files to allow code introspection by @Guts in <https://github.com/WhereGroup/profile_manager/pull/51>
* Big refactoring number 2 by @kannes in <https://github.com/WhereGroup/profile_manager/pull/34>
* Fix wrong enum by @kannes in <https://github.com/WhereGroup/profile_manager/pull/41>
* UI improvements by @kannes in <https://github.com/WhereGroup/profile_manager/pull/45>
* Misc improvements by @kannes in <https://github.com/WhereGroup/profile_manager/pull/44>
* Documentation: complete contributing guide and publish to GitHub Pages using GitHub Actions by @Guts in <https://github.com/WhereGroup/profile_manager/pull/52>
* Tooling: add script to update translation by @Guts in <https://github.com/WhereGroup/profile_manager/pull/54>
* update(tooling): add a proposed VS Code configuration to match contributing guidelines by @Guts in <https://github.com/WhereGroup/profile_manager/pull/53>
* add(tooling): dependabot configuration to track on dependencies update by @Guts in <https://github.com/WhereGroup/profile_manager/pull/58>
* Check Qt6 support flag by @kannes in <https://github.com/WhereGroup/profile_manager/pull/57>
* Adjust URLs to new profile directory name by @kannes in <https://github.com/WhereGroup/profile_manager/pull/40>
* change(license): use GPLv2 instead of MIT to comply with upstream licenses (Qt/QGIS) by @Guts in <https://github.com/WhereGroup/profile_manager/pull/18>
* Drop experimental flag by @kannes in <https://github.com/WhereGroup/profile_manager/pull/55>

## 0.5.0-beta2 - 2024-11-05

* First version after plugin's folder renaming under the hood (`profile-manager` --> `profile_manager` to comply with Python guidelines)
* Fix parameter order (broken import/removal of data sources) by @kannes in <https://github.com/WhereGroup/profile_manager/pull/33>
* Switch dialog tabs to back sensible defaults by @kannes in <https://github.com/WhereGroup/profile_manager/pull/32>
* update(ci): rm deprecated `set-output` command by @Guts in <https://github.com/WhereGroup/profile_manager/pull/31>

## 0.5.0-beta1 - 2024-10-09

* add tab to export profile ready for [QGIS Deployment Toolbelt](https://github.com/Guts/qgis-deployment-cli/) - See related [issue](https://github.com/WhereGroup/profile_manager/issues/10)
* add modern plugin's packaging using [QGIS Plugin CI](https://github.com/opengisch/qgis-plugin-ci/)
* apply Python coding rules to whole codebase (PEP8)
* remove dead code and every Plugin builder related files
* add Git hooks (pre-commit) and quality tooling
* ships the big refactoring started in 2023

## 0.4 - 2023-06-29

* Fairly big refactoring and cleanup
* Better and more verbose error handling
* Improve performance
* Reduce backup size, change backup directory
* Improve dialogs and messages
* Add support for Vector Tiles connections
* Fix a crash (thanks Ivano Giuliano!)

## 0.31 - 2022-07-31

* Update metadata

## 0.3 - 2022-07-13

* Fix scanning for bookmarks, favourites, exp functions, styles

## 0.21 - 2022-01-18

* Add support for BSD and other Unixes (thanks Loïc Bartoletti!)
* Add Italy - German translation (thanks Salvatore Fiandaca!)

## 0.2 - 2022-01-12

* First public release
