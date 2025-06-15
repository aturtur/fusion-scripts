"""
AR_PrintUsedSavers

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Print Used Savers
Version: 1.2.1
Description-US: Prints file paths that savers of the current composition uses.  

Written for Blackmagic Design Fusion Studio 19.0 build 59.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.2.1 (04.06.2025) - Small tweak.
1.2.0 (11.04.2025) - Added more stylized printing, added selection support and fixed a small bug.
1.1.1 (25.09.2024) - Modified code to follow more PEP 8 recommendations.
1.1.0 (20.10.2021) - Alphabetically sorted.
1.0.0 (19.10.2021) - Initial release.
"""
# Libraries
...

#def sort_list(subList) -> list:
    #"""Sorts list alphabetically."""

    #return(sorted(subList, key=lambda x: x[1]))

# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()


# Functions
def check_status(tool) -> str:
    """Checks status of the saver."""
    
    if tool.Input.GetConnectedOutput() == None:
        return "[ ]"  # Tool is not connected to anything.
    
    if (tool.GetAttrs()["TOOLB_PassThrough"] == True):
        return "[-]"  # Tool is connected but disabled.
    else:
        return "[x]"  # Tool is enabled and in use.
    
    
def sort_list(subList) -> list:
    """Sorts list alphabetically."""

    return(sorted(subList, key=lambda x: x[1]))


def print_used_savers(savers) -> None:
    """Prints used savers."""

    savers_data = {}

    for i, saver in enumerate(savers):
        savers_data[i] = {
            "Name": saver.Name,
            "Path": saver.GetInput("Clip"),
            "Status": check_status(saver)
        }

    max_name_length = max(len(item["Name"]) for item in savers_data.values())

    name   = "Saver Name:"
    status = "Mode:"
    path   = "Path:"

    print("")
    print("Used Savers:")
    print(f"{name:<{max_name_length+2}} {status:<8} {path}")

    for item in savers_data.values():
        print(f"{item['Name']:<{max_name_length+2}} {str(item['Status']):<8} {item['Path']}")

    print("")
    print("Mode: [x] in use \t [ ] not connected \t [-] connected but disabled.")
    print("")
    print("")


def main() -> None:
    """The main function."""

    selected_savers = comp.GetToolList(True, "Saver").values()
    if len(selected_savers) == 0:
        print_used_savers(comp.GetToolList(False, "Saver").values())
    else:
        print_used_savers(selected_savers)

if __name__ == "__main__":
    main()