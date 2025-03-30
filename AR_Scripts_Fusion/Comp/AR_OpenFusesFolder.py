"""
AR_OpenFuseFolder

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Open Fuse Folder
Version: 1.0.0
Description-US: Opens the folder where Fuses are located.

Written for Blackmagic Design Fusion Studio 19.0 build 59.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.0.0 (12.03.2025) - Initial release.
"""
# Libraries
import pathlib
import subprocess


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()


# Functions
def open_fuse_folder() -> None:
    """Opens the folder where Fuses are located."""

    script_dir = pathlib.Path.home() / "AppData" / "Roaming" / "Blackmagic Design" / "Fusion" / "Fuses"
    subprocess.Popen(["explorer", script_dir])


def main() -> None:
    """The main function."""

    open_fuse_folder()


if __name__ == "__main__":
    main()