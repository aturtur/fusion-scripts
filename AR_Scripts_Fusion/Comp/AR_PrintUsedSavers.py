"""
AR_PrintUsedSavers

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Print Used Savers
Version: 1.1.1
Description-US: Prints file paths that savers of the current composition uses.  

Written for Blackmagic Design Fusion Studio 19.0 build 59.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.1.1 (25.09.2024) - Modified code to follow more PEP 8 recommendations.
1.1.0 (20.10.2021) - Alphabetically sorted.
1.0.0 (19.10.2021) - Initial release.
"""
# Libraries
...


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()


# Functions
def check_status(tool) -> str:
    """Checks status of the tool."""

    # Get output connections of the tool.
    x = tool.Output.GetConnectedInputs().values()
    
    # If there's no any connections.
    if len(x) == 0:
        return "[NOT USED]"
    
    # If tool is disabled.
    if (tool.GetAttrs()["TOOLB_PassThrough"] == True):
        return "[DISABLED]"
    else:
        return "[ IN USE ]"
    
    
def sort_list(subList) -> list:
    """Sorts list alphabetically."""

    return(sorted(subList, key=lambda x: x[1]))


def print_used_savers() -> None:
    """Prints used savers."""

    savers = comp.GetToolList(False, "Saver").values()
    savers_list = []

    for saver in savers:
        status = check_status(saver)    
        saver_clip = saver.GetInput("Clip")
        savers_list.append([status, saver_clip, saver.Name])

    savers_list = sort_list(savers_list)

    for saver in savers_list:
        print(saver)


def main() -> None:
    """The main function."""

    print_used_savers()


if __name__ == "__main__":
    main()