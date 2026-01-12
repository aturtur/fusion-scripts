"""
ar_RevealInExplorer

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Reveal In Explorer
Version: 1.2.0
Description-US: Opens saver's or loader's media input in the explorer.

Written for Blackmagic Design Fusion Studio 19.0 build 59.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp
                   Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Tool

Changelog:
1.2.0 (11.09.2025) - Added support for path mapping (manual).
1.1.0 (25.09.2024) - Modified code to follow more PEP 8 recommendations.
                   - Rewritten reaveal_in_explorer function with better logic.
1.0.1 (08.11.2022) - Semantic versioning.
1.0.0 (04.10.2021) - Initial release.
"""
# Libraries
import os
import subprocess
import re


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()

path_mappings = {"\\server": "\\\\server"}


# Functions
def apply_path_mapping(file_path: str) -> str:
    """Does the path mapping."""
    
    for search, replace in path_mappings.items():
        pattern = r"^" + re.escape(search)
        if re.match(pattern, file_path):
            return re.sub(pattern, lambda m: replace, file_path, count=1)
    return file_path


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

            file_path = apply_path_mapping(file_path)

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