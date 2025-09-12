"""
AR_AutoBalanceFromSampleImage

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Auto White Balance From Sample Image
Version: 1.0.0
Description-US: Creates an auto white balance setup from selected sample image tool.\nCurrent frame is used as a reference frame.

Written for Blackmagic Design Fusion Studio 20.1 build 45.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Expressions snagged from:
    Stefan's Object Removal https://youtu.be/lhEgqLLXfKM?t=470

Changelog:
1.0.0 (13.08.2025) - Initial release.
"""
# Libraries
...


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()


# Functions
def create_auto_white_balance_from_sample_image_node(tool) -> None:
    """Creates an auto white balance setup from selected sample image tool."""

    flow = comp.CurrentFrame.FlowView
    x, y = flow.GetPosTable(tool).values()

    colorgain_tool = comp.AddTool("ColorGain", x + 1, y)
    colorgain_tool.SetAttrs({'TOOLS_Name' : 'AutoBalance1'})

    reference_frame = str(int(comp.CurrentTime))
    tool_name = tool.Name

    colorgain_tool.GainRed.SetExpression(f"{tool_name}:GetValue(\"NumberIn1\", time)/{tool_name}:GetValue(\"NumberIn1\", {reference_frame})")
    colorgain_tool.GainGreen.SetExpression(f"{tool_name}:GetValue(\"NumberIn2\", time)/{tool_name}:GetValue(\"NumberIn2\", {reference_frame})")
    colorgain_tool.GainBlue.SetExpression(f"{tool_name}:GetValue(\"NumberIn3\", time)/{tool_name}:GetValue(\"NumberIn3\", {reference_frame})")
    
    colorgain_tool.Input = tool.Output


def main() -> None:
    """The main function."""

    comp.StartUndo("Sample image")
    tools = comp.GetToolList(True).values()
    for tool in tools:
        create_auto_white_balance_from_sample_image_node(tool)        
    comp.EndUndo(True)


if __name__ == "__main__":
    main()