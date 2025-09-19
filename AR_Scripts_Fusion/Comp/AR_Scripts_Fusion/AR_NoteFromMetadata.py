"""
AR_NoteFromMetadata

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Note From Metadata
Version: 1.1.0
Description-US: Creates a sticky note filled with metadata from selected tool(s).

Written for Blackmagic Design Fusion Studio 19.0.3 build 3.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.1.0 (19.09.2025) - Support for macros and group nodes, where Output port is sometimes named as MainOutput1 or Output1.
1.0.0 (09.11.2024) - Initial release.
"""
# Libraries
from pathlib import Path


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()


# Functions
def note_from_metadata(tool) -> None:
    """Creates sticky note filled with data from tool."""

    flow = comp.CurrentFrame.FlowView
    x, y = flow.GetPosTable(tool).values()

    note_name = "Metadata"
    note_content = ""

    metadata = comp.ActiveTool.GetOutputList()[1][comp.CurrentTime].Metadata
    
    for key, value in metadata.items():
        note_content += f"{key} = {value}\n"
    
    note = comp.AddTool("Note", x-2, y)
    note.SetAttrs({'TOOLS_Name': note_name})
    note.Comments[comp.CurrentTime] = note_content


def main() -> None:
    """The main function."""

    comp.StartUndo("Note from loader")
    selected_tools = comp.GetToolList(True).values()
    for tool in selected_tools:
        note_from_metadata(tool)        
    comp.EndUndo(True)


if __name__ == "__main__":
    main()