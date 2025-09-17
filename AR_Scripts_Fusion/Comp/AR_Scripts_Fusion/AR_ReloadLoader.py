"""
AR_ReloadLoader

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Reload Loader
Version: 1.3.0
Description-US: Reloads selected loaders and extends ranges if needed.

Note:   - The script resets trim values!
        - Old length value has hold frame values included and new length value doesn't!

Written for Blackmagic Design Fusion Studio 19.0 build 59.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.3.0 (17.09.2025) - Added support for path mapping (manual).
1.2.0 (24.05.2025) - Prints useful data to the console.
                   - Hold frame handling.
                   - Fixed length value.
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
    """Restores path mapping from given tool"""

    reversed_path = reverse_path_mapping(str(tool.GetInput("Clip")))
    tool.SetInput("Clip", reversed_path + "")

    return True


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


def check_hold_frame(tool) -> bool:
    """Checks if loader is hold frame."""

    duration = tool.ClipTimeEnd[1] - tool.ClipTimeStart[1]
    loop = tool.Loop[1]

    if (duration == 0) and (loop == True):
        return True
    else:
        return False


def print_data(pd) -> None:
    """Prints data to the console about changed values."""

    old_in = int(pd['old_global_in'])
    old_out = int(pd['old_global_out'])
    old_len = int(pd['old_length'])
    new_in = int(pd['new_global_in'])
    new_out = int(pd['new_global_out'])
    new_len = int(pd['new_length'])

    in_change = new_in - old_in
    out_change = new_out - old_out
    len_change = new_len - old_len

    print(f"\tGlobal In:\t\t{(old_in):<5} → {(new_in):<5} ({in_change} F)")
    print(f"\tGlobal Out:\t\t{(old_out):<5} → {(new_out):<5} ({out_change} F)")
    print(f"\tLength:\t\t\t{(old_len):<5} → {(new_len):<5} ({len_change} F)")


def refresh_tool(tool) -> None:
    """Refresh tool by toggling pass through parameter on and off."""

    current = tool.GetAttrs()['TOOLB_PassThrough']
    tool.SetAttrs({'TOOLB_PassThrough': True})
    tool.SetAttrs({'TOOLB_PassThrough': False})
    tool.SetAttrs({'TOOLB_PassThrough': current})


def reload_loader(loader) -> bool:
    """Reloads loader and updates the frame range if it has changed."""

    # Get current clip's attributes.
    loader_name         = loader.Name
    clip_file_path      = loader.GetInput("Clip")
    clip_global_in      = loader.GlobalIn[1]
    clip_global_out     = loader.GlobalOut[1]
    clip_trim_start     = loader.ClipTimeStart[1]
    clip_trim_end       = loader.ClipTimeEnd[1]
    clip_hold_first     = loader.HoldFirstFrame[1]
    clip_hold_last      = loader.HoldLastFrame[1]
    clip_reverse        = loader.Reverse[1]
    clip_loop           = loader.Loop[1]
    clip_missing_frames = loader.MissingFrames[1]

    old_length = clip_global_out - clip_global_in + 1

    # Apply path mapping.
    clip_file_path = apply_path_mapping(clip_file_path)

    # Get possibly changed start and end frames from file.
    file_start_frame, file_end_frame = get_frame_range(clip_file_path)
    file_length = file_end_frame - file_start_frame + 1

    # Check if holdrame
    hold_frame = check_hold_frame(loader)

    if hold_frame:
        print("")
        print(f"{loader_name} - Hold frame found, this loader is ignored!")
        print("")        
        return False

    # Check if length has changed.
    if old_length != file_length:

        # Calculate offset and new start and and frames.
        offset = clip_global_in - loader.GetAttrs()['TOOLIT_Clip_StartFrame'][1]
        start_frame = file_start_frame + offset
        end_frame = file_end_frame + offset + clip_hold_first + clip_hold_last

        # Update loader's attributes.
        loader.Clip[1] = clip_file_path+""  # Update file path.
        loader.SetAttrs({'TOOLIT_Clip_StartFrame': file_start_frame})
        loader.SetInput("StartFrame", file_start_frame)
        loader.SetInput("GlobalOut", end_frame)
        loader.SetInput("GlobalIn", start_frame)
        loader.SetInput("ClipTimeEnd", file_length-1)  # Trim out.
        loader.SetInput("ClipTimeStart", 0)  # Trim in.
        loader.SetInput("HoldFirstFrame", clip_hold_first)
        loader.SetInput("HoldLastFrame", clip_hold_last)
        loader.SetInput("Loop", clip_loop)
        loader.SetInput("Reverse", clip_reverse)
        loader.SetInput("MissingFrames", clip_missing_frames)

        # Collect some data for printing.
        pd = {}
        pd['old_global_in'] = clip_global_in
        pd['new_global_in'] = start_frame
        pd['old_global_out'] = clip_global_out
        pd['new_global_out'] = end_frame
        pd['old_length'] = old_length
        pd['new_length'] = file_length #+ clip_hold_first + clip_hold_last

        print("")
        print(f"{loader_name} - Updated!")
        print_data(pd)
        print("")

    else:
        print("")
        print(f"{loader_name} - No new frames found!")
        print("")

    refresh_tool(loader)
    restore_path_mapping(loader)

    return True

        
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