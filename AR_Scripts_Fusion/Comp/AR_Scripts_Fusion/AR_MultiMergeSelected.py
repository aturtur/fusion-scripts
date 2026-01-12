"""
ar_MultiMergeSelected

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Multi Merge Selected
Version: 1.0.1
Description-US: Merge selected tools using a multi merge tool.

Written for Blackmagic Design Fusion Studio 19.0.3 build 3.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.0.1 (11.14.2025) - Added support for different types of outputports (e.g. Mask).
1.0.0 (07.05.2025) - Initial realease.
"""
# Libraries
...
import pprint


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

    for i, tool in enumerate(tools):

        output_port = tool.GetOutputList()[1]
    
        if i == 0:
            pos_x, pos_y = flow.GetPosTable(tool).values()
            multimerge = comp.AddTool("MultiMerge", pos_x + 2, pos_y)
            multimerge.ConnectInput("Background", output_port)

        if i != 0:
            multimerge.ConnectInput(f"Layer{i}.Foreground", output_port)
            #multimerge.SetInput(f"Layer{i}.Gain", 0)  # Set Alpha Gain to Add.
            flow.Select(multimerge, True)
    

def main() -> None:
    """The main function."""

    comp.Lock()
    comp.StartUndo("Merge selected")

    merge_selected_tools()

    comp.EndUndo(True)
    comp.Unlock()


if __name__ == "__main__":
    main()