"""
AR_SelectAllThisType

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Select All This Type
Version: 1.0.1
Description-US: Selects all tools that are same type as the currently active tool.

Written for Blackmagic Design Fusion Studio 19.0 build 59.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.0.1 (25.09.2024) - Modified code to follow more PEP 8 recommendations.
1.0.0 (08.11.2022) - Initial release.
"""
# Libraries
...


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()


# Functions
def select_all_this_type() -> None:
    """Selects all tools that are same type as the currently active tool."""

    active_tool_type = comp.ActiveTool().ID 
    tools = comp.GetToolList(False, active_tool_type).values()
    flow = comp.CurrentFrame.FlowView # Get flow view
    flow.Select() # Deselect all, if old selections

    for tool in tools:
        flow.Select(tool, True)


def main() -> None:
    """The main function."""

    select_all_this_type()


if __name__ == "__main__":
    main()