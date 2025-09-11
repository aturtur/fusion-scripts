"""
AR_MergeSelected

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Merge Selected
Version: 1.0.0
Description-US: Merges selected tools.

Written for Blackmagic Design Fusion Studio 19.0.3 build 3.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.0.0 (07.05.2025) - Initial realease.
"""
# Libraries
...


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()


# Functions
def merge_selected_tools() -> None:
    """Merges all selected tools."""

    flow = comp.CurrentFrame.FlowView
    tools = comp.GetToolList(True).values()
    flow.Select()

    tool_positions = []
    merge_nodes = []

    for tool in tools:
        pos_x, pos_y = flow.GetPosTable(tool).values()
        tool_positions.append((pos_y, pos_x, tool))

    tool_positions.sort()

    for i, tool in enumerate(tool_positions):
        if i != 0:
            flow = comp.CurrentFrame.FlowView
            merge = comp.AddTool("Merge", tool[1] + 2, tool[0])
            #merge.SetInput("Gain", 0)  # Set Alpha Gain to Add.
            flow.Select(merge, True)
            merge_nodes.append(merge)

    sorted_tools = [tool for _, _, tool in tool_positions]

    for i, merge in enumerate(merge_nodes):
        if i == 0:
            merge.Background = sorted_tools[0].Output
            merge.Foreground = sorted_tools[1].Output
        else:
            merge.Background = merge_nodes[i-1].Output
            merge.Foreground = sorted_tools[i+1].Output
    

def main() -> None:
    """The main function."""

    comp.Lock()
    comp.StartUndo("Merge selected")

    merge_selected_tools()

    comp.EndUndo(True)
    comp.Unlock()


if __name__ == "__main__":
    main()