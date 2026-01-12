"""
ar_EnableAllSavers

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Enable All Savers
Version: 1.0.2
Description-US: Enables all savers in the active composition.

Written for Blackmagic Design Fusion Studio 19.0 build 59.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.0.2 (20.09.2024) - Modified code to follow more PEP 8 recommendations.
1.0.1 (08.11.2022) - Semantic versioning.
1.0.0 (26.04.2022) - Initial release.
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

    comp.StartUndo("Enable all savers")    
    savers = comp.GetToolList(False, "Saver").values()

    for saver in savers:
        enable_tool(saver)
        
    comp.EndUndo(True)


if __name__ == "__main__":
    main()