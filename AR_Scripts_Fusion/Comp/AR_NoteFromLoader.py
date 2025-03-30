"""
AR_NoteFromLoader

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Creates a sticky note filled with info from the selected loader(s).
Version: 1.0.0
Description-US: Creates sticky note filled with data from loader.

Written for Blackmagic Design Fusion Studio 19.0 build 59.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.0.0 (25.09.2024) - Initial release.
"""
# Libraries
import os
import re
from pathlib import Path


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()


# Functions
def get_frame_range(file_path: str) -> tuple[int, int]:
    """Returns first and last frame numbers from given image sequence path."""

    clean_path = re.sub(r'(.*?)(\d+)\.[a-zA-Z]+$', r'\1', file_path)
    file_name = os.path.basename(clean_path)
    dir_path = os.path.dirname(file_path)
    extension = os.path.splitext(file_path)[1]

    found = False
    first_frame = 0
    last_frame = 0

    file_name_pattern = rf"{re.escape(file_name)}\d+{re.escape(extension)}"
    digits_pattern = r'\d+(?!.*\d)'

    for file in sorted(os.listdir(dir_path)):
        match = re.search(file_name_pattern, file)

        if match:
            frame_number = int(re.search(digits_pattern, file).group())
            if found == False:
                first_frame = frame_number
                found = True
            else:
                last_frame = frame_number

    return first_frame, last_frame


def note_from_loader(loader) -> None:
    """Creates sticky note filled with data from loader."""

    flow = comp.CurrentFrame.FlowView
    x, y = flow.GetPosTable(loader).values()
    file_path = loader.GetInput("Clip")

    first_frame, last_frame = get_frame_range(file_path)
    file_name = re.sub(r'\d+$', '', Path(file_path).stem)

    global_in = int(loader.GetInput("GlobalIn"))
    global_out = int(loader.GetInput("GlobalOut"))
    
    note_name = "Note"
    note_content = f"{file_name}\n\nRange from file:\n{first_frame} - {last_frame}\n\nGlobal In/Out:\n{global_in} - {global_out}"
    
    note = comp.AddTool("Note", x-2, y)
    note.SetAttrs({'TOOLS_Name': note_name})
    note.Comments[comp.CurrentTime] = note_content


def main() -> None:
    """The main function."""

    comp.StartUndo("Note from loader")
    selected_loaders = comp.GetToolList(True, "Loader").values()
    for loader in selected_loaders:
        note_from_loader(loader)        
    comp.EndUndo(True)


if __name__ == "__main__":
    main()