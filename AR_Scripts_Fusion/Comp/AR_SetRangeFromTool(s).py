"""
AR_SetRangeFromTool(s)

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Set Range From Tool(s)
Version: 1.0.0
Description-US: Sets global and render range from selected tool(s).

Written for Blackmagic Design Fusion Studio 19.0 build 59.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.0.0 (09.10.2024) - Initial realease.
"""
# Libraries
...


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()


# Functions
def set_range(start, end) -> None:
    """Sets global and render range."""

    comp.SetAttrs({"COMPN_GlobalStart":start,
                   "COMPN_GlobalEnd":end})
    
    comp.SetAttrs({"COMPN_RenderStart":start,
                   "COMPN_RenderEnd":end})
    

def set_current_time(frame: int) -> None:
    """Sets composition's current time to given value."""

    comp.SetAttrs({"COMPN_CurrentTime": frame})


def main() -> None:
    """The main function."""

    comp.StartUndo("Set Range")
    tools = comp.GetToolList(True).values()

    if tools:
        first_tool = next(iter(tools))
        start = first_tool.GetAttrs("TOOLNT_Region_Start")[1]
        end = first_tool.GetAttrs("TOOLNT_Region_End")[1]

        for tool in tools:
            current_start = tool.GetAttrs("TOOLNT_Region_Start")[1]
            current_end = tool.GetAttrs("TOOLNT_Region_End")[1]

            if start > current_start:
                start = current_start

            if end < current_end:
                end = current_end
        
        set_range(start, end)
        set_current_time(start)

    comp.EndUndo(True)


if __name__ == "__main__":
    main()

