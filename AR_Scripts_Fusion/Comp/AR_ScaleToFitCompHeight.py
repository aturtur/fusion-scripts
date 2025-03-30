"""
AR_ScaleToFitCompHeight

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Scale To Fit Comp Height
Version: 1.0.0
Description-US: Scales proportionally foreground image to fit background image's height.

Written for Blackmagic Design Fusion Studio 19.1.3 build 5
Python version 3.10.8 (64-bit)

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp
  
Changelog:
1.0.0 (05.03.2025) - Initial release.
"""
# Libraries
...


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()


# Functions
def get_merge_data(merge_node) -> tuple | bool:
    """Gets all important data from the selected merge node."""

    if merge_node.ID == "Merge":
        bg_node = merge_node.FindMainInput(1).GetConnectedOutput().GetTool()
        fg_node = merge_node.FindMainInput(2).GetConnectedOutput().GetTool()

        bg_width = bg_node.GetAttrs("TOOLI_ImageWidth")
        bg_height = bg_node.GetAttrs("TOOLI_ImageHeight")

        fg_width = fg_node.GetAttrs("TOOLI_ImageWidth")
        fg_height = fg_node.GetAttrs("TOOLI_ImageHeight")

        return bg_node, bg_width, bg_height, fg_node, fg_width, fg_height
    else:
        print("Select Merge node first!")
        return False


def fit_comp_height(tool) -> None:
    """Scales proportionally foreground image to fit background image's height."""

    if get_merge_data(tool) == False: return None
    _, bg_width, bg_height, fg_node, fg_width, fg_height = get_merge_data(tool)

    size  = bg_height / fg_height

    flow = comp.CurrentFrame.FlowView
    flow.Select()
    x, y = flow.GetPosTable(tool).values()
    transform_node = comp.AddTool("Transform", x, y-1)
    transform_node.SetInput("Size", size)
    transform_node.SetAttrs({"TOOLS_Name": "FitToCompHeight"})
    tool.Foreground = transform_node.Output
    transform_node.Input = fg_node.Output
    flow.Select(transform_node)


def main() -> None:
    """The main function."""

    comp.StartUndo("Fit to comp")
    active_tool = comp.ActiveTool()
    fit_comp_height(active_tool)
    comp.EndUndo()

if __name__ == "__main__":
    main()