"""
AR_OpenScriptFolder

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Open Script Folder
Version: 1.0.0
Description-US: Opens the script folder in explorer.

Written for Blackmagic Design Fusion Studio 19.0.3 build 3.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.0.0 (02.11.2024) - Initial realease.
"""
# Libraries
import pathlib
import subprocess


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()

scripts = []


# Functions
def open_script_folder() -> None:
    """Opens the Script/Comp folder in the explorer."""

    script_dir = pathlib.Path.home() / "AppData" / "Roaming" / "Blackmagic Design" / "Fusion" / "Scripts" / "Comp"
    subprocess.Popen(["explorer", script_dir])


def main() -> None:
    """The main function."""

    open_script_folder()


if __name__ == "__main__":
    main()