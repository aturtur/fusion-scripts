"""
AR_SetRangeFromMetadata

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Set Range From Metadata
Version: 1.0.1
Description-US: Sets global and render range from selected tool's metadata.

Written for Blackmagic Design Fusion Studio 19.0 build 59.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.0.1 (28.05.2025) - Small improvement.
1.0.0 (27.05.2025) - Initial realease.
"""
# Libraries
...


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()

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
    """Sets global and render range."""

    if (start != None) and (end != None):
        comp.SetAttrs({"COMPN_GlobalStart":start,
                    "COMPN_GlobalEnd":end})
        
        comp.SetAttrs({"COMPN_RenderStart":start,
                    "COMPN_RenderEnd":end})
    

def set_current_time(frame: int) -> None:
    """Sets composition's current time to given value."""

    comp.SetAttrs({"COMPN_CurrentTime": frame})


def get_range_from_metadata(tool) -> tuple[int, int]:
    current_time = comp.CurrentTime
    metadata = tool.Output[current_time].Metadata

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

    tool = comp.ActiveTool()
    start, end = get_range_from_metadata(tool)
    print(start, end)
    set_range(float(start), float(end))
    set_current_time(start)

    comp.EndUndo(True)


if __name__ == "__main__":
    main()