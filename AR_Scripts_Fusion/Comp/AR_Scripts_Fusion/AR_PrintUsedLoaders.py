"""
AR_PrintUsedLoaders

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Print Used Loaders
Version: 1.3.0
Description-US: Prints file paths that loaders of the current composition uses.

Written for Blackmagic Design Fusion Studio 19.0 build 59.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.3.0 (16.09.2024) - Prints now using tabulate.
1.2.1 (04.06.2025) - Small tweak.
1.2.0 (11.04.2025) - Added more stylized printing and added selection support.
1.1.1 (25.09.2024) - Modified code to follow more PEP 8 recommendations.
1.1.0 (20.10.2021) - Alphabetically sorted.
1.0.0 (19.10.2021) - Initial release.
"""
# Libraries
from tabulate import tabulate


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()


# Functions
def check_status(tool) -> str:
    """Checks status of the loader."""

    if len(tool.Output.GetConnectedInputs().values()) == 0:
        return "[ ]"  # Tool is not connected to anything.
    
    if (tool.GetAttrs()["TOOLB_PassThrough"] == True):
        return "[-]"  # Tool is connected but disabled.
    else:
        return "[x]"  # Tool is enabled and in use.
    
    
def sort_list(subList) -> list:
    """Sorts list alphabetically."""

    return(sorted(subList, key=lambda x: x[1]))


def print_used_loaders(loaders) -> None:
    """Prints used loaders."""

    loaders_data = {}

    for i, loader in enumerate(loaders):
        loaders_data[i] = {
            "Name": loader.Name,
            "Path": loader.GetInput("Clip"),
            "Status": check_status(loader)
        }

    max_name_length = max(len(item["Name"]) for item in loaders_data.values())

    name   = "Loader Name:"
    status = "Mode:"
    path   = "Path:"


    print("")
    print("Used Loaders:")

    table = []
    for item in loaders_data.values():
        table.append([item['Name'], item['Status'], item['Path']])

    headers = ["Name", "Status", "Path"]

    print(tabulate(table, headers=headers, tablefmt="github"))

    print("")
    print("Mode: [x] in use \t [ ] not connected \t [-] connected but disabled.")
    print("")
    print("")


def main() -> None:
    """The main function."""

    selected_loaders = comp.GetToolList(True, "Loader").values()
    if len(selected_loaders) == 0:
        print_used_loaders(comp.GetToolList(False, "Loader").values())
    else:
        print_used_loaders(selected_loaders)

if __name__ == "__main__":
    main()