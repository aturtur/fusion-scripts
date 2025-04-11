"""
AR_ReloadLoader

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Reload Loader
Version: 1.1.0
Description-US: Reloads selected loaders and extends ranges if needed.

Written for Blackmagic Design Fusion Studio 19.0 build 59.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.1.0 (11.04.2025) - Added support for selection.
1.0.0 (20.09.2024) - Initial release.
"""
# Libraries
import os
import re


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


def refresh_tool(tool) -> None:
    """Refresh tool by toggling pass through parameter on and off."""

    current = tool.GetAttrs()['TOOLB_PassThrough']
    tool.SetAttrs({'TOOLB_PassThrough': True})
    tool.SetAttrs({'TOOLB_PassThrough': False})
    tool.SetAttrs({'TOOLB_PassThrough': current})


def reload_loader(loader) -> None:
    """Reloads loader and updates the frame range if it has changed."""

    # Get current clip's attributes.
    clip_file_path      = loader.GetInput("Clip")
    clip_global_in      = loader.GlobalIn[1]
    clip_global_out     = loader.GlobalOut[1]
    clip_hold_first     = loader.HoldFirstFrame[1]
    clip_hold_last      = loader.HoldLastFrame[1]
    clip_reverse        = loader.Reverse[1]
    clip_loop           = loader.Loop[1]
    clip_missing_frames = loader.MissingFrames[1]

    # Get possibly changed start and end frames from file.
    file_start_frame, file_end_frame = get_frame_range(clip_file_path)
    file_length = file_end_frame - file_start_frame

    # Calculate offset and new start and and frames.
    offset = clip_global_in - loader.GetAttrs()['TOOLIT_Clip_StartFrame'][1]
    start_frame = file_start_frame + offset
    end_frame = file_end_frame + offset

    # Update loader's attributes.
    loader.Clip[1] = clip_file_path+""  # Update file path.
    loader.SetAttrs({'TOOLIT_Clip_StartFrame': file_start_frame})
    loader.SetInput("StartFrame", file_start_frame)
    loader.SetInput("GlobalOut", end_frame)
    loader.SetInput("GlobalIn", start_frame)
    loader.SetInput("ClipTimeEnd", file_length)  # Trim out.
    loader.SetInput("ClipTimeStart", 0)  # Trim in.
    loader.SetInput("HoldFirstFrame", clip_hold_last)
    loader.SetInput("HoldLastFrame", clip_hold_first)
    loader.SetInput("Loop", clip_loop)
    loader.SetInput("Reverse", clip_reverse)
    loader.SetInput("MissingFrames", clip_missing_frames)
    
    refresh_tool(loader)

        
def main() -> None:
    """The main function."""

    comp.Lock()
    comp.StartUndo("Reload loaders")

    selected_loaders = comp.GetToolList(True, "Loader").values()
    loaders = selected_loaders or comp.GetToolList(False, "Loader").values()

    for loader in loaders:
        reload_loader(loader)

    comp.EndUndo(True)
    comp.Unlock()


if __name__ == "__main__":
    main()