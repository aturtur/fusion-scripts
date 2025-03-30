"""
AR_RevealInExplorer

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Reveal In Explorer
Version: 1.0.1
Description-US: Opens saver's or loader's media input in the explorer.

Written for Blackmagic Design Fusion Studio 19.0 build 59.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp
                   Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Tool

Changelog:
1.1.0 (25.09.2024) - Modified code to follow more PEP 8 recommendations.
                   - Rewritten reaveal_in_explorer function with better logic.
1.0.1 (08.11.2022) - Semantic versioning.
1.0.0 (04.10.2021) - Initial release.
"""
# Libraries
import os
import subprocess


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()


# Functions
def reveal_in_explorer() -> None:
    """Opens selected loaders' or savers' in the explorer.
    If the file does not exist (not rendered savers), opens folder.
    """

    tools = comp.GetToolList(True).values()
    for tool in tools:
        try:
            file_path = tool.GetInput("Clip")
        except:
            file_path = None
        
        if file_path is not None:
            if os.path.exists(file_path):
                subprocess.Popen(["explorer", "/select,", file_path])
            else:
                folder_path = os.path.dirname(file_path)
                os.startfile(folder_path)


def main() -> None:
    """The main function."""

    reveal_in_explorer()


if __name__ == "__main__":
    main()