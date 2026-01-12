"""
ar_RemoveKeyframesBeforeCurrentFrame

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Remove Keyframes Before Current Frame
Version: 1.0.0
Description-US: Removes all keyframes from selected tool(s) before the current frame.\nGlobal Start Time is the start frame!

Written for Blackmagic Design Fusion Studio 19.0.3 build 3.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.0.0 (24.09.2025) - Initial realease.
"""
# Libraries
import pprint


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()


# Functions
def remove_keyframes_before_this_frame(tool) -> None:
    """Removes all keyframes from selected tool(s) before the current frame."""

    current_frame = comp.CurrentTime
    for inp in tool.GetInputList().values():
        if inp.GetConnectedOutput():
            data_type = inp.GetAttrs()["INPS_DataType"]
            if data_type:
                if data_type != "Image":
                    start = int(comp.GetAttrs("COMPN_GlobalStart"))
                    end = int(current_frame)
                    for i in range(start, end):
                        inp[float(i)] = None  # Delete keyframe from current frame.
                    comp.SetAttrs({"COMPN_CurrentTime": current_frame})  # Restore current frame.


def main() -> None:
    """The main function."""

    comp.Lock()
    comp.StartUndo("Remove keyframes")

    tools = comp.GetToolList(True).values()
    for tool in tools:
        remove_keyframes_before_this_frame(tool)

    comp.EndUndo(True)
    comp.Unlock()


if __name__ == "__main__":
    main()