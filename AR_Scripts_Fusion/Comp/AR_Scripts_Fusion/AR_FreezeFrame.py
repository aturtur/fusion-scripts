"""
ar_FreezeFrame

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Freeze Frame
Version: 1.0.2
Description-US: Creates a TimeSpeed node that freezes frame at current frame.

Written for Blackmagic Design Fusion Studio 19.0 build 59.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.0.2 (18.04.2025) - Added support for different types of outputports (e.g. Mask).
1.0.1 (20.09.2024) - Modified code to follow more PEP 8 recommendations.
1.0.0 (02.09.2024) - Initial realease.
"""
# Libraries
...


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()


# Functions
def freeze_frame(tool) -> any:
    """Creates a time speed node that freezes frame at current time."""

    # Calculate freeze frame.
    current_time = int(comp.CurrentTime)
    freeze_time = current_time - tool.GetAttrs("TOOLNT_Region_Start")[1]

    # Create time speed node and set values.
    flow = comp.CurrentFrame.FlowView
    x, y = flow.GetPosTable(tool).values()
    time_speed = comp.AddTool("TimeSpeed", x+2, y)
    time_speed.SetInput("Speed", 0)
    time_speed.SetInput("Delay", freeze_time)
    time_speed.SetInput("InterpolateBetweenFrames", 0)
    time_speed.SetAttrs({"TOOLS_Name": f"FreezeFrame_{str(current_time)}"})
    
    # Connect nodes.
    output_port = tool.GetOutputList()[1]
    time_speed.Input.ConnectTo(output_port)

    return time_speed


def main() -> None:
    """The main function."""

    comp.StartUndo("Freeze frames")
    tools = comp.GetToolList(True).values()

    for tool in tools:
        freeze_frame(tool)

    comp.EndUndo(True)


if __name__ == "__main__":
    main()