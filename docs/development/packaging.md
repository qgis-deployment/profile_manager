# Packaging and deployment

## Packaging

This plugin is using the [qgis-plugin-ci](https://github.com/opengisch/qgis-plugin-ci/) tool to perform packaging operations.  
The package command is performing a `git archive` run based on changelog.

Install additional dependencies:

```sh
python -m pip install -U -r requirements/packaging.txt
```

```sh
# package a specific version
qgis-plugin-ci package 1.3.1
# package latest version
qgis-plugin-ci package latest
```

## Release a version

Everything is done through the continuous deployment:

1. Add the new version to the `CHANGELOG.md`. You can write it manually or use the auto-generated release notes by Github:
    1. Go to [project's releases](https://github.com/qgis-deployment/profile_manager/releases) and click on `Draft a new release`
    1. In `Choose a tag`, enter the new tag
    1. Click on `Generate release notes`
    1. Copy/paste the generated text from `## What's changed` until the line before `**Full changelog**:...` in the CHANGELOG.md replacing `What's changed` with the tag and the publication date
1. Change the version number in `metadata.txt`
1. Apply a git tag with the relevant version: `git tag -a 0.3.0 {git commit hash} -m "This version rocks!"`
1. Push tag to main branch: `git push origin 0.3.0`

The release job publishes to <https://plugins.qgis.org> with a plugin upload token stored in the `QGIS_PLUGIN_TOKEN` repository secret, not with a personal OSGeo account. To create or rotate it, generate a new token at <https://plugins.qgis.org/plugins/profile_manager/tokens/create/> (plugin maintainers only) and update the secret.
