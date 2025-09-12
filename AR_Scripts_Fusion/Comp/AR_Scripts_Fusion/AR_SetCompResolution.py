"""
AR_SetCompResolution

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Set Comp Resolution
Version: 1.0.1
Description-US: Sets composition's frame format resolution from the active tool.

Written for Blackmagic Design Fusion Studio 19.0 build 59.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.0.1 (25.09.2024) - Modified code to follow more PEP 8 recommendations.
1.0.0 (02.09.2024) - Initial realease.
"""
# Libraries
...


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()


# Functions
def set_comp_resolution() -> None:
    """Sets current composition resolution from active tool."""

    try:
        # Get resolution from active tool
        width = comp.ActiveTool.GetAttrs("TOOLI_ImageWidth")
        height = comp.ActiveTool.GetAttrs("TOOLI_ImageHeight")

        # Get composition preferences
        comp_preferences = comp.GetPrefs()

        # Change composition settings
        comp_preferences['Comp']['FrameFormat']['Width'] = width
        comp_preferences['Comp']['FrameFormat']['Height'] = height

        # Set new composition preferences
        comp.SetPrefs(comp_preferences)

        print("Comp resolution set to: " + str(width) + "x" + str(height))

    except:
        print("Couldn't set comp resolution")


def main() -> None:
    """The main function."""

    comp.StartUndo("Set comp resolution")
    set_comp_resolution()
    comp.EndUndo(True)


if __name__ == "__main__":
    main()