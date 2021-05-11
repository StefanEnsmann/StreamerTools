# Stream Avatars Editor
A batch editor for Stream Avatars written in Python.

Tested with Stream Avatars 7.108

## Features
- [x] List all installed avatars
- [x] Enable or disable installed avatars
- [x] Wipe data for custom spawned users named `spawned***`

## Usage
`python sa_editor.py [-h] [-s] [-l] [-w] [-ea] [-da] [-e AVATAR] [-d AVATAR] [-c COLUMNS] [-f PATH]`

Parameter             | Meaning
----------------------|----------
-h, --help            | Shows a help message
-s, --status          | Displays a count of all enabled and disabled avatars
-l, --list            | Displays a list of all avatars with their activation status
-w, --wipe-spawned    | Wipes all manually spawned test avatars from the database. Looking for 'spawned*'
-ea, --enable-all     | Enables all avatars, unless specified via --disable
-da, --disable-all    | Disables all avatars, unless specified via --enable
-e, --enable AVATAR   | Enables the given avatar, if it is present. Overrides --disable-all
-d, --disable AVATAR  | Disables the given avatar, if it is present. Overrides --enable-all
-c, --columns COLUMNS | Sets the amount of columns to use for list printing. Default: 10
-f, --file PATH       | Sets the path to streamavatars_json.txt

By default, this tool uses the file in this location:
`%APPDATA%/LocalLow/ClonzeWork/Streaming Avatars/data/streamavatars_json.txt`.

Mac users, please utilize `--file` for now.