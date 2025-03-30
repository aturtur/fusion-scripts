"""
AR_OpenProjectFolder

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Open Project Folder
Version: 1.0.1
Description-US: Opens the folder where the project file is located.

Written for Blackmagic Design Fusion Studio 19.0 build 59.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.0.2 (25.09.2024) - Modified code to follow more PEP 8 recommendations.
1.0.1 (08.11.2022) - Semantic versioning.
1.0.0 (26.04.2022) - Initial release.
"""
# Libraries
import subprocess


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()


# Functions
def open_project_folder() -> None:
    """Opens the project folder in explorer, where the composition file is located."""

    path = comp.GetAttrs()['COMPS_FileName']  # Get composition's file path.
    subprocess.Popen(["explorer", "/select,", path])  # Open the folder and select the file.


def main() -> None:
    """The main function."""

    open_project_folder()


if __name__ == "__main__":
    main()