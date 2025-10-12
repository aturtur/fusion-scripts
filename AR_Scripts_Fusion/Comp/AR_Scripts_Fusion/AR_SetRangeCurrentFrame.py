"""
AR_SetRangeCurrentFrame

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Set Range Current Frame
Version: 1.1.0
Description-US: Sets render range to the current frame.

Written for Blackmagic Design Fusion Studio 19.0.3 build 3.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.1.0 (16.09.2025) - Added SHIFT modifier to set also the global range.
1.0.0 (02.11.2024) - Initial realease.
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


# Functions
def set_range(start, end) -> None:
    """Sets the range."""

    if (start != None) and (end != None):

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


def main() -> None:
    """The main function."""

    current_time = comp.CurrentTime
    set_range(current_time, current_time)
    set_current_time(current_time)
    

if __name__ == "__main__":
    main()

