"""
AR_LoadersFromSavers

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Loaders From Savers
Version: 1.0.2
Description-US: Creates loaders from selected savers.

Written for Blackmagic Design Fusion Studio 19.0 build 59.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp
                   Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Tool
                   
Changelog:
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

video_files = [".mov", ".mp4"]


# Functions
def find(file_name, folder_path) -> str:
    """Tries to find the file in given folder path"""

    print(file_name)

    pattern = '^'+file_name+'\d'  # Accept digits after the file name.
    for file in listdir(folder_path):
        search = re.match(pattern, file)
        if search:
            return os.path.join(folder_path, file)
        
def loader_from_saver(saver) -> any:
    """Creates loader from saver."""

    flow = comp.CurrentFrame.FlowView
    x, y = flow.GetPosTable(saver).values()
    loader = comp.AddTool("Loader", x+1, y)
    file_path = saver.GetInput("Clip")
    folder = os.path.dirname(file_path)
    file = ntpath.basename(file_path)
    extension = os.path.splitext(file_path)[1]
    region_start = saver.GetAttrs()['TOOLNT_Region_Start'][1]

    # Check if video file.
    if extension in video_files:
        loader.SetInput("Clip", file_path)

    # Otherwise image sequence.
    else:
        name = file.replace(extension, "")
        loader.SetInput("Clip", find(name, folder))

    # Set loader's "global in" to match saver's "region start".
    clip_length = loader.GetInput("ClipTimeEnd")
    loader.SetInput("GlobalOut", region_start + clip_length)
    loader.SetInput("GlobalIn", region_start)
    loader.SetInput("ClipTimeStart", 0)
    loader.SetInput("ClipTimeEnd", clip_length)
    loader.SetInput("HoldFirstFrame", 0)
    loader.SetInput("HoldLastFrame", 0)

    return loader


def main() -> None:
    """The main function."""

    comp.Lock()
    comp.StartUndo("Loaders from savers")

    savers = comp.GetToolList(True, "Saver").values()
    for saver in savers:
        loader_from_saver(saver)

    comp.EndUndo(True)
    comp.Unlock()


if __name__ == "__main__":
    main()