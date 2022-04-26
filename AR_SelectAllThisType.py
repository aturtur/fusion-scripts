"""
AR_SelectAllThisType

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_SelectAllThisType
Description-US: Selects all tools that are same type as the current active tool.
E.g. tool has to be active not just selected!
Written for Fusion 16.2 build 22
Note: You need Python 2 (64-bit) installed to run this script (https://www.python.org/downloads/release/python-2717/)
"""
#Installation path: %appdata%\Roaming\Blackmagic Design\Fusion\Scripts\Comp
def SelectAllThisType():
    tool = comp.ActiveTool().ID # Get active tool's ID
    tools = comp.GetToolList(False, tool) # Get all of the tools with same ID
    flow = comp.CurrentFrame.FlowView # Get flow view
    flow.Select() # Deselect all
    for t in tools: # For each found tool
        flow.Select(tools[t], True) # Select the loader
SelectAllThisType() # Run the function