# Keyboard based cursor
A simple Python script which displays an overlay containing a grid of characters. When pressing a combination of characters the mouse will move to its location and perform a single click.

## Dependencies
To install dependencies, run:

```bash
pip install -r requirements.txt
```

## Usage
One way to toggle the script is by using AutoHotkey.

1. Install [AutoHotkey](https://www.autohotkey.com/).
2. Open the Run dialog (`Windows+R`) and type `shell:startup`.
3. Move [hotkey.ahk](hotkey.ahk) into the folder.

The overlay will now be displayed when the hotkey (`CTRL+ALT+O`) is detected.
