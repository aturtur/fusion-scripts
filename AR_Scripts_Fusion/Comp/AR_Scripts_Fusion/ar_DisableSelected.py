"""
ar_DisableSelected

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Disable Selected
Version: 1.0.0
Description-US: Disables selected tool(s) in the active composition.

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
def disable_tool(tool) -> None:
    """Disables tool."""

    tool.SetAttrs({'TOOLB_PassThrough': True})


def main() -> None:
    """The main function."""

    comp.StartUndo("Disable selected")    
    tools = comp.GetToolList(True).values()

    for tool in tools:
        disable_tool(tool)
        
    comp.EndUndo(True)


if __name__ == "__main__":
    main()