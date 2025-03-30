"""
AR_SetRangeThisFrame

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Set Range This Frame
Version: 1.0.0
Description-US: Sets render range to the current frame.

Written for Blackmagic Design Fusion Studio 19.0.3 build 3.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.0.0 (02.11.2024) - Initial realease.
"""
# Libraries
import os


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()


# Functions
def set_render_range(start, end) -> None:
    """Sets render range."""
   
    comp.SetAttrs({"COMPN_RenderStart":start,
                   "COMPN_RenderEnd":end})


def set_current_time(frame: int) -> None:
    """Sets composition's current time to given value."""

    comp.SetAttrs({"COMPN_CurrentTime": frame})


def main() -> None:
    """The main function."""

    current_time = comp.CurrentTime
    set_render_range(current_time, current_time)
    set_current_time(current_time)
    

if __name__ == "__main__":
    main()

