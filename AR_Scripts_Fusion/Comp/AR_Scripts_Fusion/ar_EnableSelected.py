"""
ar_EnableSelected

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Enable Selected
Version: 1.0.0
Description-US: Enables selected tool(s) in the active composition.

Written for Blackmagic Design Fusion Studio 19.0 build 59.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.0.0 (27.01.2026) - Initial release.
"""
# Libraries
...


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()


# Functions
def enable_tool(tool) -> None:
    """Enables tool."""

    tool.SetAttrs({'TOOLB_PassThrough': False})


def main() -> None:
    """The main function."""

    comp.StartUndo("Enable selected")    
    tools = comp.GetToolList(True).values()

    for tool in tools:
        enable_tool(tool)
        
    comp.EndUndo(True)


if __name__ == "__main__":
    main()