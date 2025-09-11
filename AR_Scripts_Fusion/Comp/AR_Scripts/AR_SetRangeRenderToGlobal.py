"""
AR_SetRangeRenderToGlobal

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Set Range Render To Global
Version: 1.0.0
Description-US: Sets render range to match global range.

Written for Blackmagic Design Fusion Studio 19.0 build 59.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.0.0 (27.02.2025) - Initial realease.
"""
# Libraries
...


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()


# Functions
def set_global_range(start, end) -> None:
    """Sets composition's global range."""

    comp.SetAttrs({"COMPN_GlobalStart":start,
                   "COMPN_GlobalEnd":end})
        

def set_render_range(start, end) -> None:
    """Sets composition's render range."""

    comp.SetAttrs({"COMPN_RenderStart":start,
                   "COMPN_RenderEnd":end})
    

def set_current_time(frame: int) -> None:
    """Sets composition's current time to given value."""

    comp.SetAttrs({"COMPN_CurrentTime": frame})


def main() -> None:
    """The main function."""

    start = comp.GetAttrs("COMPN_GlobalStart")
    end = comp.GetAttrs("COMPN_GlobalEnd")

    set_render_range(start, end)


if __name__ == "__main__":
    main()