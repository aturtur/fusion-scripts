"""
AR_CropToDoD

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Crop to DoD
Version: 1.1.0
Description-US: Crops to selected tools' DoD (Domain of Definition).

Written for Blackmagic Design Fusion Studio 19.1.3 build 5.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp
  
Changelog:
1.1.0 (30.03.2025) - Added support for multiple tools.
1.0.0 (25.02.2025) - Initial release.
"""
# Libraries
...


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()


# Functions
def crop_to_dod(tool) -> None:
    """Crops to selected tools' DoD (Domain of Definition)."""
    
    flow = comp.CurrentFrame.FlowView
    flow.Select()
    x, y = flow.GetPosTable(tool).values()
    crop_node = comp.AddTool("Crop", x+2, y)
    crop_node.SetAttrs({"TOOLS_Name": "CropToDoD"})
    crop_node.Input = tool.Output
    crop_node.AutoCrop = 1
    flow.Select(crop_node)

    #windowlist = comp.GetFrameList()
    #for window in windowlist.values():
        #window.ViewOn(crop_node, 1)


def main() -> None:
    """The main function."""

    comp.StartUndo("Crop To DoD")
    tools = comp.GetToolList(True).values()
    for tool in tools:
        crop_to_dod(tool)
    comp.EndUndo()

if __name__ == "__main__":
    main()