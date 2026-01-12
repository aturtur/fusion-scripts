"""
ar_ReverseCrop

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Reverse Crop
Version: 1.0.0
Description-US: Puts the cropped image back in place.

Written for Blackmagic Design Fusion Studio 19.1.3 build 5.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp
  
Changelog:
1.0.0 (12.03.2025) - Initial release.
"""
# Libraries
...


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()


# Functions
def reverse_crop() -> None:
    """Puts the cropped image back in place."""

    tool = comp.ActiveTool()
    connected_node = tool.Input.GetConnectedOutput().GetTool()

    width = connected_node.GetAttrs("TOOLI_ImageWidth")
    height = connected_node.GetAttrs("TOOLI_ImageHeight")

    now = comp.CurrentTime

    x1 = tool.GetInput("XOffset", now)
    y1 = tool.GetInput("YOffset", now)
    crop_width = tool.GetInput("XSize", now)
    crop_height = tool.GetInput("YSize", now)

    x2 = x1 + crop_width
    y2 = y1 + crop_height

    center_x = (x1 + x2) / 2
    center_y = (y1 + y2) / 2

    remapped_center_x = (center_x - 0) / (width - 0)
    remapped_center_y = (center_y - 0) / (height - 0)

    transform_x = 0.5 + ((remapped_center_x - 0.5) * (width / (x2-x1)))
    transform_y = 0.5 + ((remapped_center_y - 0.5) * (height / (y2-y1)))

    flow = comp.CurrentFrame.FlowView
    x, y = flow.GetPosTable(tool).values()
    transform_node = comp.AddTool("Transform", x+2, y+1)
    transform_node.SetInput("Center", {1: transform_x, 2: transform_y, 3: 0.0})
    merge_node = comp.AddTool("Merge", x+2, y)

    transform_node.Input = tool.Output
    merge_node.Background = connected_node.Output
    merge_node.Foreground = transform_node.Output

    
def main() -> None:
    """The main function."""

    comp.StartUndo("Reverse Crop")    
    reverse_crop()
    comp.EndUndo()


if __name__ == "__main__":
    main()