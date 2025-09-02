"""
AR_SwtichFromSelected

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Switch From Selected
Version: 1.0.0
Description-US: Creates a switch tool from selected tools.

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
def swtich_from_selected() -> None:
    """Creates a switch tool from selected tools."""

    flow = comp.CurrentFrame.FlowView
    tools = comp.GetToolList(True).values()
    flow.Select()

    for i, tool in enumerate(tools):
    
        if i == 0:
            pos_x, pos_y = flow.GetPosTable(tool).values()
            switch = comp.AddTool("Switch", pos_x + 2, pos_y)
            switch.NumberOfInputs = len(tools)
            switch.ConnectInput("Input0", tool.Output)

        if i != 0:
            switch.ConnectInput(f"Input{i}", tool.Output)
            flow.Select(switch, True)
    

def main() -> None:
    """The main function."""

    comp.Lock()
    comp.StartUndo("Switch selected")

    swtich_from_selected()

    comp.EndUndo(True)
    comp.Unlock()


if __name__ == "__main__":
    main()