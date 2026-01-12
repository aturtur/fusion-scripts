"""
ar_ReverseStabilization

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Reverse Stabilization
Version: 1.0.2
Description-US: Creates reverse stabilization setup for clean up painting from a active Tracker Node.

Written for Blackmagic Design Fusion Studio 19.0 build 59.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp
                   Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Tool

Example:
1. Track in Mocha Pro.
2. Go to Stabilize tab.
3. Stabilize motions what needed (X Translation, Y Translation, Rotation, Zoom, Shears, Perspective).
4. Check "Maximum smoothing".
5. Click "Export Stabilized Tracking Data...".
6. Paste Tracker Node, connect correct input.
7. Select Tracker Node and run this script.

Changelog:
1.0.2 (27.09.2024) - Modified code to follow more PEP 8 recommendations.
1.0.1 (08.11.2022) - Semantic versioning.
1.0.0 (26.04.2021) - Initial release.
"""
# Libraries
...


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()


# Functions
def reverse_stabilization_mocha(tool) -> None:
    """Creates reverse stabilization setup for clean up painting from a active Tracker Node
    created by Mocha "Stabilized Tracking Data".
    """
    
    flow = comp.CurrentFrame.FlowView
    x, y = flow.GetPosTable(tool).values()

    comp.SetActiveTool(tool)
    comp.Copy()
    paint = comp.AddTool("Paint", x+2, y)
    paint.ConnectInput("Input", tool)
    comp.SetActiveTool(paint)
    comp.Paste()

    tool.Operation = 2  # "Corner Positioning".
    clone = comp.ActiveTool()
    clone.Operation = 3  # "Perspective Positioning".

    input_node = tool.Input.GetConnectedOutput().GetTool()

    tool.Foreground = input_node.Output
    clone.Input = input_node.Output
    clone.Foreground = paint.Output


def main() -> None:
    """The main function."""
    
    tool = comp.ActiveTool()
    reverse_stabilization_mocha(tool)


if __name__ == "__main__":
    main()