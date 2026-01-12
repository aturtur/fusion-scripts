"""
ar_SetRangeFromMetadata

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Set Range From Metadata
Version: 1.2.0
Description-US: Sets render range from selected tool's metadata.

Written for Blackmagic Design Fusion Studio 19.0 build 59.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.2.0 (19.09.2025) - Support for macros and group nodes, where Output port is sometimes named as MainOutput1 or Output1.
1.1.0 (16.09.2025) - Added SHIFT modifier to set also the global range.
1.0.2 (05.09.2025) - Tweaking.
1.0.1 (28.05.2025) - Small improvement.
1.0.0 (27.05.2025) - Initial realease.
"""
# Libraries
...


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()

try:
    key_modifiers = key_modifiers
except Exception:
    key_modifiers = None

ALT: str = "ALT"
CTRL: str = "CTRL"
SHIFT: str = "SHIFT"

start_keys = ["startframe",
              "start_frame",
              "firstframe",
              "first_frame",
              "cfx_startframe"]

end_keys = ["endframe",
            "end_frame",
            "lastframe",
            "last_frame",
            "cfx_endframe"]


# Functions
def set_range(start, end) -> None:
    """Sets the range."""

    if (start != None) and (end != None):

        current_start = float(comp.GetAttrs("COMPN_GlobalStart"))
        current_end = float(comp.GetAttrs("COMPN_GlobalEnd"))
        
        # If the current global start frame is bigger than the given start frame, move the global start.
        if current_start > start:
            comp.SetAttrs({"COMPN_GlobalStart":start})

        # If the current global end frame is smaller than the given end frame, move the global end.
        if current_end < end:
            comp.SetAttrs({"COMPN_GlobalEnd":end})

        # If SHIFT keyboard modifier pressed, set also the global range.
        if key_modifiers != None:
            if SHIFT in key_modifiers:
                comp.SetAttrs({"COMPN_GlobalStart":start})
                comp.SetAttrs({"COMPN_GlobalEnd":end})

        comp.SetAttrs({"COMPN_RenderStart":start,
                    "COMPN_RenderEnd":end})
    

def set_current_time(frame: int) -> None:
    """Sets composition's current time to given value."""

    comp.SetAttrs({"COMPN_CurrentTime": frame})


def get_range_from_metadata(tool) -> tuple[int, int]:
    metadata = comp.ActiveTool.GetOutputList()[1][comp.CurrentTime].Metadata

    start_frame = None
    end_frame = None

    for key, value in metadata.items():
        try:
            if key.lower() in start_keys:
                start_frame = value

            if key.lower() in end_keys:
                end_frame = value
        except:
            pass

    return start_frame, end_frame


def main() -> None:
    """The main function."""

    comp.StartUndo("Set Range From Metadata")

    tool = comp.ActiveTool

    try:
        start, end = get_range_from_metadata(tool)
        set_range(float(start), float(end))
        set_current_time(start)
    except Exception:
        print("Couldn't set the range.")

    comp.EndUndo(True)


if __name__ == "__main__":
    main()