"""
AR_ReverseStabilizationSetup

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_ReverseStabilizationSetup
Version: 1.0.1
Description-US: Creates reverse stabilization setup for clean up painting from Tracker Node created by Mocha "Stabilized Tracking Data"

Written for Blackmagic Design Fusion Studio 18.0.4 build 5
Python version 3 (64-bit)

1. Track in Mocha Pro
2. Go to Stabilize tab
3. Stabilize motions what needed (X Translation, Y Translation, Rotation, Zoom, Shears, Perspective)
4. Check "Maximum smoothing"
5. Click "Export Stabilized Tracking Data..."
6. Paste Tracker Node, connect correct input
7. Select Tracker Node and run this script

Change log:
1.0.1 (08.11.2022) - Semantic versioning
1.0.0 (26.04.2021) - Initial release
"""

# Installation path: %appdata%\Roaming\Blackmagic Design\Fusion\Scripts\Tool

# Functions
def ReverseStabilizationSetup():
    node = comp.ActiveTool() # Get active tool
    
    flow = comp.CurrentFrame.FlowView # Get flow view
    x, y = flow.GetPosTable(node).values() # Get node's position

    comp.SetActiveTool(node) # Set active tool
    comp.Copy() # Copy active tool
    paint = comp.AddTool("Paint", x+2, y) # Add paint
    paint.ConnectInput("Input", node)
    comp.SetActiveTool(paint) # Set active tool
    comp.Paste() # Paste active tool

    node.Operation = 2 # Set operation to "Corner Positioning"
    clone = comp.ActiveTool()
    clone.Operation = 3 # Set operation to "Perspective Positioning"

    inputNode = node.Input.GetConnectedOutput().GetTool()

    node.Foreground = inputNode.Output
    clone.Input = inputNode.Output
    clone.Foreground = paint.Output

# Run the script
ReverseStabilizationSetup() # Run the function