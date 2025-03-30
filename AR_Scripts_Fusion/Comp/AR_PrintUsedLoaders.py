"""
AR_PrintUsedLoaders

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Print Used Loaders
Version: 1.1.1
Description-US: Prints file paths that loaders of the current composition uses.

Written for Blackmagic Design Fusion Studio 19.0 build 59.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.1.1 (25.09.2024) - Modified code to follow more PEP 8 recommendations.
1.1.0 (20.10.2021) - Alphabetically sorted.
1.0.0 (19.10.2021) - Initial release.
"""
# Libraries
import os


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()


# Functions
def check_status(tool) -> str:
    """Checks status of the tool."""

    # Get output connections of the tool
    x = tool.Output.GetConnectedInputs().values()
    
    # If there's no any connections
    if len(x) == 0:
        return "[NOT USED]"
    
    # If tool is disabled
    if (tool.GetAttrs()["TOOLB_PassThrough"] == True):
        return "[DISABLED]"
    else:
        return "[ IN USE ]"
    
    
def sort_list(subList) -> list:
    """Sorts list alphabetically."""

    return(sorted(subList, key=lambda x: x[1]))


def print_used_loaders() -> None:
    """Prints used loaders."""

    loaders = comp.GetToolList(False, "Loader").values()
    loaders_list = []

    for loader in loaders:
        status = check_status(loader)    
        loader_clip = loader.GetInput("Clip")
        loaders_list.append([status, loader_clip, loader.Name])

    loaders_list = sort_list(loaders_list)

    for loader in loaders_list:
        print(loader)


def main() -> None:
    """The main function."""

    print_used_loaders()


if __name__ == "__main__":
    main()