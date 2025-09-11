"""
AR_VersionUp

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Version Up
Version: 1.4.0
Description-US: Easily change between different versions.

Written for Blackmagic Design Fusion Studio 19.0 build 59.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp
Uses v character paired with digits to point out the version number (e.g. v1, v01, v001)
File path syntax example: ../VERSIONS/ProjectName_v001/../../ProjectName_v001_0000.tif

Changelog:
1.4.0 (11.09.2025) - Added path mapping support (manual).
1.3.6 (25.05.2025) - Fixed length value.
1.3.5 (22.05.2025) - Tweaked how stuff is printed to the console.
1.3.4 (07.05.2025) - Added hotkey Ctrl+Q to close the dialog.
1.3.3 (11.04.2025) - Added error checking and tooltip.
1.3.2 (09.10.2024) - Added handling for hold frames.
1.3.1 (26.09.2024) - Fine tuning.
1.3.0 (24.09.2024) - Modified to code follow more PEP 8 recommendations.
                   - Removed keep settings checkbox, settings are always recovered.
                   - Removed print info checkbox, prints always info to console.
                   - Added checkbox to keep old start frame position.
                   - Bug fix to handle global in value.
1.2.0 (22.04.2024) - Added checkbox to keep loader's settings (trims and hold frames...).
                   - Added checkbox to print information to console.
1.1.0 (21.04.2024) - Rework, better algorithm.
1.0.2 (07.03.2024) - Cleaning etc.
1.0.1 (08.11.2022) - Semantic versioning.
1.0.0 (04.10.2021) - Initial release.
"""
# Libraries
import os
import re


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()

pattern = r'(?:[^a-zA-Z]|^)v\d{1,4}(?:[^a-zA-Z]|$)'  # Searches v1, v01, v001, v0001 types of versioning.
tries = 50  # Amount of tries for looking newer or older version number.
path_mappings = {"\\server": "\\\\server"}  # Custom path mappings.

ALT: str = "ALT"
CTRL: str = "CTRL"
SHIFT: str = "SHIFT"


# Functions
def get_key_modifiers(ev: dict) -> list:
    """Get keyboard modifiers."""

    key_modifiers = []
    if ev['modifiers']['AltModifier'] == True:
        key_modifiers.append(ALT)
    if ev['modifiers']['ControlModifier'] == True:
        key_modifiers.append(CTRL)
    if ev['modifiers']['ShiftModifier'] == True:
        key_modifiers.append(SHIFT)

    return key_modifiers


def check_path_compatibility(file_path: str) -> bool:
    """Check if the file path is compatible with VersionUp."""

    check = re.search(pattern, file_path) is not None
    if not check:
        print(f"Warning! File path is not compatible with VersionUp:\n\t{file_path}")
    return check


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
    print(reversed_path)
    tool.SetInput("Clip", reversed_path + "")

    return True
    

def check_file(file_path: str) -> bool:
    """Checks does the file exist."""

    if os.path.exists(file_path):
        return True
    else:
        return False
    

def check_hold_frame(tool) -> bool:
    """Checks if loader is hold frame."""

    settings = get_loader_settings(tool)
    duration = settings['TrimOut'] - settings['TrimIn']
    loop = settings['Loop']

    if (duration == 0) and (loop == True):
        return True
    else:
        return False
    

def get_current_version(file_path: str) -> int:
    """Get current version from the file path."""

    path = os.path.normpath(file_path)
    splitted_path = path.split(os.sep)

    for part in splitted_path:
        found = re.findall(pattern, part)

        if len(found) != 0:
            raw_version = found[0]
            version = re.findall(r"\d+", raw_version)[0]
            number = int(version)

            return number
        

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

    if os.path.exists(dir_path) and os.path.isdir(dir_path):
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


def replace_frame_number(file_path: str, frame_number: int) -> str:
    """Replaces file paths frame number with given one."""

    all_numbers = re.findall(r'\d+', file_path)
    
    if not all_numbers:
        return file_path
    
    last_number = all_numbers[-1]
    padded_new_number = str(frame_number).zfill(len(last_number))
    updated_file_path = re.sub(r'(\d+)(?=\D*$)', padded_new_number, file_path)

    return updated_file_path
                

def update_file_path(file_path: str, position: int) -> str:
    """Updates the file path with given version (position)."""

    path = os.path.normpath(file_path)
    splitted_path = path.split(os.sep)
    updated_path = []

    for part in splitted_path:
        found = re.findall(pattern, part)

        if len(found) != 0:
            raw_version = found[0]
            version = re.findall(r"\d+", raw_version)[0]
            zpad = len(version)
            updated_version = str(position).zfill(zpad)
            updated_raw_version = re.sub(r"\d+", updated_version, raw_version)
            part = part.replace(raw_version, updated_raw_version)

        updated_path.append(part)

    result_path = os.path.sep.join(updated_path)
    
    return result_path


def get_loader_settings(tool) -> dict:
    """Gets loader's settings."""

    settings = {}  # Initialize a dictionary for storing settings.

    settings['GlobalIn']      = tool.GlobalIn[1]
    settings['GlobalOut']     = tool.GlobalOut[1]
    settings['TrimIn']        = tool.ClipTimeStart[1]
    settings['TrimOut']       = tool.ClipTimeEnd[1]
    settings['HoldFirst']     = tool.HoldFirstFrame[1]
    settings['HoldLast']      = tool.HoldLastFrame[1]
    settings['Reverse']       = tool.Reverse[1]
    settings['Loop']          = tool.Loop[1]
    settings['MissingFrames'] = tool.MissingFrames[1]
    settings['StartFrame']    = tool.GetAttrs()['TOOLIT_Clip_StartFrame'][1]

    return settings


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


def update_loader_settings(tool, settings: dict, path: str, lock_global_in: bool) -> dict:
    """Updates loader settings by checking if image sequence length has changed."""

    # Get possibly changed start and end frames from file (extended or reduced).
    file_start_frame, file_end_frame = get_frame_range(path)
    file_length = file_end_frame - file_start_frame + 1

    # Collect variables.
    old_global_in = settings['GlobalIn']
    old_global_out = settings['GlobalOut']
    clip_hold_last = settings['HoldLast']
    clip_hold_first = settings['HoldFirst']
    old_start_frame = tool.GetAttrs()['TOOLIT_Clip_StartFrame'][1]
    old_length = old_global_out - old_global_in
    new_start_frame = file_start_frame

    # Calculate frame positions.
    if not lock_global_in:
        offset = old_global_in - old_start_frame
    else:
        offset = old_global_in - new_start_frame
    
    new_global_in = new_start_frame + offset
    new_global_out = file_end_frame + offset + clip_hold_first + clip_hold_last

    # Update settings.
    tool.SetInput("Clip", path + "")
    settings['StartFrame'] = file_start_frame
    settings['GlobalOut'] = new_global_out
    settings['GlobalIn'] = new_global_in
    settings['TrimOut'] = file_length-1

    # Collect some data for printing.
    pd = {}
    pd['old_global_in'] = old_global_in
    pd['new_global_in'] = new_global_in
    pd['old_global_out'] = old_global_out
    pd['new_global_out'] = new_global_out
    pd['old_length'] = old_length
    pd['new_length'] = file_length

    return settings, pd


def set_loader_settings(tool, settings: dict) -> bool:
    """Sets loader's settings."""

    tool.GlobalOut[1]      = settings['GlobalOut']
    tool.GlobalIn[1]       = settings['GlobalIn']
    tool.ClipTimeEnd[1]    = settings['TrimOut']
    tool.ClipTimeStart[1]  = settings['TrimIn']
    tool.HoldLastFrame[1]  = settings['HoldLast']
    tool.HoldFirstFrame[1] = settings['HoldFirst']
    tool.Reverse[1]        = settings['Reverse']
    tool.Loop[1]           = settings['Loop']
    tool.MissingFrames[1]  = settings['MissingFrames']
    tool.SetAttrs({'TOOLIT_Clip_StartFrame': settings['StartFrame']})

    return True


def refresh_tool(tool) -> None:
    """Refresh tool by toggling pass through parameter on and off."""

    current = tool.GetAttrs()['TOOLB_PassThrough']
    tool.SetAttrs({'TOOLB_PassThrough': True})
    tool.SetAttrs({'TOOLB_PassThrough': False})
    tool.SetAttrs({'TOOLB_PassThrough': current})


def version_up_run(lock_global_in: bool) -> bool:
    """Tries to get one newer version."""

    tools = comp.GetToolList(True, "Loader").values()
    for tool in tools:
        loader_name = tool.Name
        file_path = tool.GetInput("Clip")

        if not check_path_compatibility(file_path):
            break

        file_path = apply_path_mapping(file_path)
        current_version = get_current_version(file_path)

        for i in range(1, tries + 1):
            version_up = current_version + i
            updated_path_version = update_file_path(file_path, version_up)
            file_first_frame, _ = get_frame_range(updated_path_version)
            updated_path_full = replace_frame_number(updated_path_version, file_first_frame)
            hold_frame = check_hold_frame(tool)

            if hold_frame:
                if check_file(updated_path_version) == True:
                    settings = get_loader_settings(tool)
                    tool.SetInput("Clip", updated_path_version + "")
                    set_loader_settings(tool, settings)
                    refresh_tool(tool)
                    restore_path_mapping(tool)

                    # Print data to console.
                    print("")
                    print(f"{loader_name} - Updated!")
                    print(f"\tVersion change:\tv{current_version} → v{version_up}")
                    print(f"\tOld path:\t\t{file_path}")
                    print(f"\tUpdated path:\t{updated_path_version}")
                    print("\tHold frame")
                    print("")
                    break

            else:
                if check_file(updated_path_full) == True:
                    settings = get_loader_settings(tool)
                    settings, pd = update_loader_settings(tool, settings, updated_path_full, lock_global_in)
                    set_loader_settings(tool, settings)
                    refresh_tool(tool)                    
                    restore_path_mapping(tool)

                    # Print data to console.
                    print("")
                    print(f"{loader_name} - Updated!")
                    print(f"\tVersion change:\tv{current_version} → v{version_up}")
                    print(f"\tOld path:\t\t{file_path}")
                    print(f"\tUpdated path:\t{updated_path_full}")
                    print_data(pd)
                    print("")
                    break

        else:
            # Print errors to console.
            print("")
            print(f"{loader_name} - Newer version not found!")
            print("")
            return False
        
        return True
        

def version_down_run(lock_global_in: bool) -> bool:
    """Tries to get one older version."""

    tools = comp.GetToolList(True, "Loader").values()
    for tool in tools:
        loader_name = tool.Name
        file_path = tool.GetInput("Clip")

        if not check_path_compatibility(file_path):
            break

        file_path = apply_path_mapping(file_path)
        current_version = get_current_version(file_path)

        for i in range(1, tries + 1):
            version_down = current_version - i
            updated_path_version = update_file_path(file_path, version_down)
            file_first_frame, _ = get_frame_range(updated_path_version)
            updated_path_full = replace_frame_number(updated_path_version, file_first_frame)
            hold_frame = check_hold_frame(tool)

            if hold_frame:
                if check_file(updated_path_version) == True:
                    settings = get_loader_settings(tool)
                    tool.SetInput("Clip", updated_path_version + "")
                    set_loader_settings(tool, settings)
                    refresh_tool(tool)
                    restore_path_mapping(tool)

                    # Print data to console.
                    print("")
                    print(f"{loader_name} - Updated!")
                    print(f"\tVersion change:\tv{current_version} → v{version_down}")
                    print(f"\tOld path:\t\t{file_path}")
                    print(f"\tUpdated path:\t{updated_path_version}")
                    print("\tHold frame")
                    print("")
                    break

            else:
                if check_file(updated_path_full) == True:
                    settings = get_loader_settings(tool)
                    settings, pd = update_loader_settings(tool, settings, updated_path_full, lock_global_in)
                    set_loader_settings(tool, settings)
                    refresh_tool(tool)
                    restore_path_mapping(tool)

                    # Print data to console.
                    print("")
                    print(f"{loader_name} - Updated!")
                    print(f"\tVersion change:\tv{current_version} → v{version_down}")
                    print(f"\tOld path:\t\t{file_path}")
                    print(f"\tUpdated path:\t{updated_path_full}")
                    print_data(pd)
                    print("")
                    break

        else:
            # Print errors to console.
            print("")
            print(f"{loader_name} - Older version not found!")
            print("")
            return False
        
        return True
        

def latest_run(lock_global_in: bool) -> None:
    """Tries to get the newest version."""

    tools = comp.GetToolList(True, "Loader").values()
    for tool in tools:
        loader_name = tool.Name
        file_path = tool.GetInput("Clip")

        if not check_path_compatibility(file_path):
            break

        file_path = apply_path_mapping(file_path)
        current_version = get_current_version(file_path)

        found = False
        last_valid_path = ""
        last_valid_version = 0
        pd = {}

        old_settings = get_loader_settings(tool)

        for i in range(1, tries + 1):
            last_version = current_version + i
            updated_path_version = update_file_path(file_path, last_version)
            file_first_frame, _ = get_frame_range(updated_path_version)
            updated_path_full = replace_frame_number(updated_path_version, file_first_frame)
            hold_frame = check_hold_frame(tool)

            if hold_frame:
                if check_file(updated_path_version) == True:
                    last_valid_path = updated_path_version
                    last_valid_version = last_version

                    settings = get_loader_settings(tool)
                    tool.SetInput("Clip", updated_path_version + "")
                    set_loader_settings(tool, settings)
                    refresh_tool(tool)
                    restore_path_mapping(tool)

                    found = True

            else:
                if check_file(updated_path_full) == True:
                    last_valid_path = updated_path_full
                    last_valid_version = last_version

                    settings = get_loader_settings(tool)
                    settings, pd = update_loader_settings(tool, settings, last_valid_path, lock_global_in)
                    set_loader_settings(tool, settings)
                    refresh_tool(tool)
                    restore_path_mapping(tool)
                    
                    found = True
        
        if found:
            refresh_tool(tool)

            if hold_frame:
                    print("")
                    print(f"{loader_name} - Updated!")
                    print(f"\tVersion change:\tv{current_version} → v{last_valid_version}")
                    print(f"\tOld path:\t\t{file_path}")
                    print(f"\tUpdated path:\t{last_valid_path}")
                    print("\tHold frame")
                    print("")

            else:
                # Print data to console.
                pd['old_global_in'] = old_settings['GlobalIn']
                pd['old_global_out'] = old_settings['GlobalOut']
                pd['old_length'] = old_settings['GlobalOut'] - old_settings['GlobalIn']

                print("")
                print(f"{loader_name} - Updated!")
                print(f"\tVersion change:\tv{current_version} → v{last_valid_version}")
                print(f"\tOld path:\t\t{file_path}")
                print(f"\tUpdated path:\t{last_valid_path}")
                print_data(pd)
                print("")

        else:  # If newer version not found.
            # Print errors to console.
            print("")
            print(f"{loader_name} - Newer version not found!")
            print("")


def custom_run(custom_version: int, lock_global_in: bool) -> bool:
    """Tries to get specific version given by user."""

    tools = comp.GetToolList(True, "Loader").values()
    for tool in tools:
        pd = {}
        loader_name = tool.Name
        file_path = tool.GetInput("Clip")

        if not check_path_compatibility(file_path):
            break

        file_path = apply_path_mapping(file_path)
        current_version = get_current_version(file_path)

        updated_path_version = update_file_path(file_path, custom_version)
        file_first_frame, _ = get_frame_range(updated_path_version)
        updated_path_full = replace_frame_number(updated_path_version, file_first_frame)
        hold_frame = check_hold_frame(tool)

        if hold_frame:
            if check_file(updated_path_version) == True:
                settings = get_loader_settings(tool)
                tool.SetInput("Clip", updated_path_version + "")
                set_loader_settings(tool, settings)
                refresh_tool(tool)
                restore_path_mapping(tool)

                # Print data to console.
                print("")
                print(f"{loader_name} - Updated!")
                print(f"\tVersion change:\tv{current_version} → v{custom_version}")
                print(f"\tOld path:\t\t{file_path}")
                print(f"\tUpdated path:\t{updated_path_version}")
                print("\tHold frame")
                print("")
                return True

            else:
                # Print errors to console.
                print("")
                print(f"{loader_name} - Given version ({custom_version}) not found!")
                print("")
                return False

        else:
            if check_file(updated_path_full) == True:
                settings = get_loader_settings(tool)
                settings, pd = update_loader_settings(tool, settings, updated_path_full, lock_global_in)
                set_loader_settings(tool, settings)
                refresh_tool(tool)
                restore_path_mapping(tool)

                # Print data to console.
                print("")
                print(f"{loader_name} - Updated!")
                print(f"\tVersion change:\tv{current_version} → v{custom_version}")
                print(f"\tOld path:\t\t{file_path}")
                print(f"\tUpdated path:\t{updated_path_full}")
                print_data(pd)
                print("")
                return True

            else:
                # Print errors to console.
                print("")
                print(f"{loader_name} - Given version ({custom_version}) not found!")
                print("")
                return False


def gui_geometry(width: int, height: int, x: float, y: float) -> dict:
    """Maps GUI position with 0-1 values.
    0.5 being in the center of the screen.
    Uses tkinter to get screen resolution."""

    import tkinter as tk

    def lerp(a: float, b: float, t: float) -> float:
        return a + t * (b - a)

    temp_win = tk.Tk()
    screen_width = temp_win.winfo_screenwidth()
    screen_height = temp_win.winfo_screenheight()
    temp_win.destroy()

    gui_width = width
    gui_height = height

    gui_x = lerp(0, screen_width, x) - (gui_width * 0.5)
    gui_y = lerp(0, screen_height, y) - (gui_height * 0.5)

    return {"width": gui_width, "height": gui_height, "x": gui_x, "y": gui_y}


gui_geo = gui_geometry(225, 140, 0.5, 0.5)


# GUI
ui   = fusion.UIManager
disp = bmd.UIDispatcher(ui)
dlg  = disp.AddWindow({"WindowTitle": "VersionUp",
                       "ID": "MyWin",
                       "WindowFlags": {
                          "Window": True,
                          "CustomizeWindowHint": True,
                          "WindowMinimizeButtonHint": False,
                          "WindowMaximizeButtonHint": False,
                          "WindowCloseButtonHint": True,
                        },
                       "Geometry": [gui_geo['x'], gui_geo['y'], gui_geo['width'], gui_geo['height']],
                       "Events": {"Close": True,
                                  "KeyPress": True,
                                  "KeyRelease": True},
                       },
    [
        ui.VGroup({"Spacing": 5},
        [
            # GUI elements
            ui.HGroup(
            [
                ui.Button({"Text": "^", "ID": "Button_Up"}),  # Button one version up.
                ui.Button({"Text": "v", "ID": "Button_Down"}),  # Button one version down.
            ]),
            #ui.VGap(),
            ui.Button({"Text": "Latest version", "ID": "Button_Latest"}),  # Button latest version.
            ui.HGroup(
            [
                ui.SpinBox({"ID": "Spinbox_VersionNumber", "Value":1, "Minimum":0, "Maximum":100000}),  # Input text field custom version.
                ui.Button({"Text": "Custom", "ID": "Button_Custom"}),  # Button apply custom version.
            ]),
            ui.HGroup([
                ui.CheckBox({"ID": "Checkbox_LockGlobalIn", "Text": "Lock Global In", "ToolTip": "Locks 'Global In' value in place."}),
            ]),
        ]),
    ])


# Collect ui items.
itm = dlg.GetItems()


# The window was closed.
def _func(ev):
    disp.ExitLoop()
dlg.On.MyWin.Close = _func


# Keys are pressed.
def _func(ev):
    key_modifiers = get_key_modifiers(ev)
    if CTRL in key_modifiers and ev['Key'] == 81:  # Ctrl + Q.
        disp.ExitLoop()
        dlg.Hide()
dlg.On.MyWin.KeyPress = _func


# Buttons are pressed.
def _func(ev):
    comp.Lock()
    comp.StartUndo("Custom version")
    lock_global_in = itm['Checkbox_LockGlobalIn'].Checked
    custom_version = itm['Spinbox_VersionNumber'].Value
    custom_run(custom_version, lock_global_in)
    comp.EndUndo(True)
    comp.Unlock()
dlg.On.Button_Custom.Clicked = _func


def _func(ev):
    comp.Lock()
    comp.StartUndo("Latest version")
    lock_global_in = itm['Checkbox_LockGlobalIn'].Checked
    latest_run(lock_global_in)
    comp.EndUndo(True)
    comp.Unlock()
dlg.On.Button_Latest.Clicked = _func


def _func(ev):
    comp.Lock()
    comp.StartUndo("Version up")
    lock_global_in = itm['Checkbox_LockGlobalIn'].Checked
    version_up_run(lock_global_in)
    comp.EndUndo(True)
    comp.Unlock()
dlg.On.Button_Up.Clicked = _func


def _func(ev):
    comp.Lock()
    comp.StartUndo("Version down")
    lock_global_in = itm['Checkbox_LockGlobalIn'].Checked
    version_down_run(lock_global_in)
    comp.EndUndo(True)
    comp.Unlock()
dlg.On.Button_Down.Clicked = _func


# Open the dialog.
dlg.Show()
disp.RunLoop()
dlg.Hide()