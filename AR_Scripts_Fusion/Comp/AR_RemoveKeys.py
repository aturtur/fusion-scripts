"""
AR_RemoveKeys

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Remove Keys
Version: 1.0.0
Description-US: Removes all keyframes from selected tools.

Written for Blackmagic Design Fusion Studio 19.0.3 build 3.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.0.0 (12.03.2025) - Initial realease.
"""
# Libraries
...


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()


# Functions
def remove_keyframes(tool) -> None:
    """Removes all keyframes from selected nodes."""

    for inp in tool.GetInputList().values():
        if inp.GetConnectedOutput():
            if inp.GetAttrs()["INPS_DataType"]:
                inp.ConnectTo(None)
    

def main() -> None:
    """The main function."""

    comp.Lock()
    comp.StartUndo("Remove keyframes")

    tools = comp.GetToolList(True).values()
    for tool in tools:
        remove_keyframes(tool)

    comp.EndUndo(True)
    comp.Unlock()


if __name__ == "__main__":
    main()