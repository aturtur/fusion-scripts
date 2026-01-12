"""
ar_SampleImage

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Sample Image
Version: 1.0.2
Description-US: Creates a sample image setup for the selected tool(s).

Written for Blackmagic Design Fusion Studio 19.1 build 34.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.0.2 (18.04.2025) - Added support for different types of outputports.
1.0.1 (13.08.2025) - Bug fix - probe is now connected also to red channel.
                   - Previously red channel was clamped to 1.0 value.
1.0.0 (17.11.2024) - Initial release.
"""
# Libraries
...


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()


# Functions
def create_sample_image_node(tool) -> None:
    """Creates a custom tool node with a probe modifier that uses given tool as a input."""

    flow = comp.CurrentFrame.FlowView
    x, y = flow.GetPosTable(tool).values()

    custom_tool = comp.AddTool("Custom", x + 1, y)
    custom_tool.AddModifier("NumberIn1", "Probe")
    custom_tool.SetAttrs({'TOOLS_Name' : 'SampleImage1'})
    
    probe_modifier = custom_tool.NumberIn1.GetConnectedOutput().GetTool()
    #probe_modifier_info = fusion.GetRegAttrs(probe_modifier.ID)
    probe_modifier.ImageToProbe = tool

    custom_tool.NumberIn1.ConnectTo(probe_modifier.Red)
    custom_tool.NumberIn2.ConnectTo(probe_modifier.Green)
    custom_tool.NumberIn3.ConnectTo(probe_modifier.Blue)
    custom_tool.NumberIn4.ConnectTo(probe_modifier.Alpha)

    custom_tool.NameforNumber1 = "Red"
    custom_tool.NameforNumber2 = "Green"
    custom_tool.NameforNumber3 = "Blue"
    custom_tool.NameforNumber4 = "Alpha"

    custom_tool.RedExpression = "n1"
    custom_tool.GreenExpression = "n2"
    custom_tool.BlueExpression = "n3"
    custom_tool.AlphaExpression = "n4"

    custom_tool.ShowNumber5 = False
    custom_tool.ShowNumber6 = False
    custom_tool.ShowNumber7 = False
    custom_tool.ShowNumber8 = False

    custom_tool.ShowPoint1 = False
    custom_tool.ShowPoint2 = False
    custom_tool.ShowPoint3 = False
    custom_tool.ShowPoint4 = False

    custom_tool.ShowLUT1 = False
    custom_tool.ShowLUT2 = False
    custom_tool.ShowLUT3 = False
    custom_tool.ShowLUT4 = False

    output_port = tool.GetOutputList()[1]
    custom_tool.Image1 = output_port


def main() -> None:
    """The main function."""

    comp.StartUndo("Sample image")
    tools = comp.GetToolList(True).values()
    for tool in tools:
        create_sample_image_node(tool)        
    comp.EndUndo(True)


if __name__ == "__main__":
    main()