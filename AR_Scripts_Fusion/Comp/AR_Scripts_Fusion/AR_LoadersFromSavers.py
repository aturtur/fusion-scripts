"""
AR_LoaderFromSaver

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Loader From Saver
Version: 1.2.0
Description-US: Creates loader(s) from selected saver(s).

Written for Blackmagic Design Fusion Studio 19.0 build 59.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp
                   Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Tool
                   
Changelog:
1.2.0 (11.10.2025) - Added support for path mapping (manual).
1.1.0 (05.04.2025) - Changed the way how the frame range is calculated.
1.0.2 (25.09.2024) - Modified code to follow more PEP 8 recommendations.
                   - Uses saver's region start attribute as loader's global in value.
1.0.1 (08.11.2022) - Semantic versioning.
1.0.0 (04.10.2021) - Initial release.
"""
# Libraries
import os
import re
import ntpath
from os import listdir


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()

path_mappings = {"\\server": "\\\\server"}


# Functions
def apply_path_mapping(file_path: str) -> str:
    """Does the path mapping."""
    
    for search, replace in path_mappings.items():
        pattern = r"^" + re.escape(search)
        if re.match(pattern, file_path):
            return re.sub(pattern, lambda m: replace, file_path, count=1)
    return file_path


def reverse_path_mapping(file_path: str) -> str:
    """Restores path mapped file_path to original."""

    for search, replace in path_mappings.items():
        pattern = r"^" + re.escape(replace)
        if re.match(pattern, file_path):
            return re.sub(pattern, lambda m: search, file_path, count=1)
    return file_path


def restore_path_mapping(tool) -> bool:
    """Restores path mapping from given tool."""

    reversed_path = reverse_path_mapping(str(tool.GetInput("Clip")))
    tool.SetInput("Clip", reversed_path + "")

    return True


def find(file_name: str, folder_path: str) -> str | None:
    """Tries to find the file from the given folder path"""

    pattern = r'^' + file_name + r'\d'  # Accept digits after the file name.
    for file in listdir(folder_path):
        search = re.match(pattern, file)
        if search:
            return os.path.join(folder_path, file)
        else:
            return None
        
def loader_from_saver(saver: any) -> any:
    """Creates a loader from the given saver."""

    flow = comp.CurrentFrame.FlowView
    x, y = flow.GetPosTable(saver).values()
    loader = comp.AddTool("Loader", x+1, y)
    file_path = saver.GetInput("Clip")
    file_path = apply_path_mapping(file_path)
    folder = os.path.dirname(file_path)
    file = ntpath.basename(file_path)
    extension = os.path.splitext(file_path)[1]
    region_start = saver.GetAttrs()['TOOLNT_Region_Start'][1]

    # Video file.
    if extension == ".mov":
        loader.SetInput("Clip", file_path)

        # Set loader's ranges to match saver's region data.
        clip_length = loader.GetInput("ClipTimeEnd")
        loader.SetInput("GlobalOut", region_start + clip_length)
        loader.SetInput("GlobalIn", region_start)
        loader.SetInput("ClipTimeStart", 0)
        loader.SetInput("ClipTimeEnd", clip_length)
        loader.SetInput("HoldFirstFrame", 0)
        loader.SetInput("HoldLastFrame", 0)

    # Image sequence.
    else:
        name = file.replace(extension, "")
        image_sequence_path = find(name, folder)
        loader.SetInput("Clip", image_sequence_path)
        file_start_frame, file_end_frame = get_frame_range(image_sequence_path)
        file_length = file_end_frame - file_start_frame

        # Set loader's ranges from found range data.
        clip_length = loader.GetInput("ClipTimeEnd")
        loader.SetInput("GlobalOut", file_start_frame + file_length)
        loader.SetInput("GlobalIn", file_start_frame)
        loader.SetInput("ClipTimeStart", 0)
        loader.SetInput("ClipTimeEnd", file_length)
        loader.SetInput("HoldFirstFrame", 0)
        loader.SetInput("HoldLastFrame", 0)

    restore_path_mapping(loader)
    return loader


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


def main() -> None:
    """The main function."""

    comp.Lock()
    comp.StartUndo("Loader from saver")

    savers = comp.GetToolList(True, "Saver").values()
    for saver in savers:
        loader_from_saver(saver)

    comp.EndUndo(True)
    comp.Unlock()


if __name__ == "__main__":
    main()