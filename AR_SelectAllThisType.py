"""
AR_SelectAllThisType

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_SelectAllThisType
Version: 1.0.0
Description-US: Selects all tools that are same type as the current active tool

Written for Blackmagic Design Fusion Studio 18.0.4 build 5
Python version 3 (64-bit)

Change log:
1.0.0 (08.11.2022) - Initial release
"""

#Installation path: %appdata%\Roaming\Blackmagic Design\Fusion\Scripts\Comp

# Functions
def SelectAllThisType():
    tool = comp.ActiveTool().ID # Get active tool's ID
    tools = comp.GetToolList(False, tool) # Get all of the tools with same ID
    flow = comp.CurrentFrame.FlowView # Get flow view
    flow.Select() # Deselect all
    for t in tools: # For each found tool
        flow.Select(tools[t], True) # Select the loader

# Run the script
SelectAllThisType() # Run the function