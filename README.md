# gh-update
A Python script to automatically update a portable program from a GitHub release. Automatically finds and downloads a GitHub release asset, then unpacks it into a folder. Supports unpacking zip or tar.* archives. Optionally backs up the existing folder first.

## Writing config files
Before you can start using gh-update, you'll need to create a config file either manually or programmatically. I've included a sample script called `write_ruffle_config` that creates a gh-update config file for the [Ruffle Flash emulator](https://ruffle.rs/).

A gh-update config file consists of a *general* section and one or more *asset config* sections. The *general* section contains two items:
- **repo**: Specifies the GitHub repository to download releases from.
- **download_prerelease**: Determines whether prerelease assets such as nightly builds are downloaded.

An *asset config* section should have a memorable name based on the name of the release asset that it downloads. The section contains two required items:
- **regex**: Specifies a regular expression to match the release asset names against. This determines what release asset file is downloaded.
- **extract_path**: Specifies the folder path that the downloaded release asset will be unpacked into.

This section may also contain 4 optional items:
- **backup_path**: Specifies the folder path that previous program versions will be copied into. If none is specified, no backups will be performed.
- **delete_files**: Determines whether to delete files from previous program versions. The default is False, meaning files are not deleted.
- **installed_name**: Specifies the name of the currently installed release. This is managed by gh-update and normally does not need to be edited.
- **installed_date**: Specifies the date that the currently installed release was published. This is managed by gh-update and normally does not need to be edited.

## Running gh-update
Once you have created a suitable config file, simply run `python gh_update.py config.ini asset_name` to update your portable program!

For example, to update the Ruffle desktop app on a 64-bit Windows machine, you would run `python gh_update.py ruffle.ini win64`.
