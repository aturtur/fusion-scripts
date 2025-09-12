"""
AR_TrimLoaderWithTimecode(SMPTE)

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Trim Loader With Timecode (SMPTE)
Version: 1.0.3
Description-US: Trims the loader with SMPTE timecode.

Written for Blackmagic Design Fusion Studio 19.0 build 59.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.0.3 (08.05.2025) - Added hotkey Ctrl+Q to close the dialog.
1.0.2 (06.11.2024) - Changed print to use f-string.
1.0.1 (25.09.2024) - Modified code to follow more PEP 8 recommendations.
1.0.0 (20.10.2023) - Initial release.
"""
# Libraries
...


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()

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


def check_metadata(tool) -> None:
    """Check if tool has timecode metadata."""

    metadata = None
    timecode = None

    try:
        timecode = tool.Output[tool.GetAttrs("TOOLNT_Region_Start")[1]].Metadata["TimeCode"]
    except:
        pass

    if timecode is not None:
        metadata = True
    
    return metadata


def trim_with_timecode(tool, start, end, fps, lock_global_in) -> None:
    """Trims loader with given timecode values."""

    start_time_code = tool.Output[tool.GetAttrs("TOOLNT_Region_Start")[1]].Metadata["TimeCode"]
    end_time_code = tool.Output[tool.GetAttrs("TOOLNT_Region_End")[1]].Metadata["TimeCode"]

    old_global_in = tool.GlobalIn[1]
    old_global_out = tool.GlobalOut[1]

    old_start_frames = timecode_to_frames(start_time_code, fps)
    old_end_frames = timecode_to_frames(end_time_code, fps)

    new_start_frames = timecode_to_frames(start, fps)
    new_end_frames = timecode_to_frames(end, fps)

    start_trim = new_start_frames - old_start_frames
    end_trim =  new_end_frames - old_end_frames

    if lock_global_in:
        tool.ClipTimeEnd[1] = tool.ClipTimeEnd[1] + end_trim
        tool.ClipTimeStart[1] = tool.ClipTimeStart[1] + start_trim

    else:
        tool.GlobalOut[1] = old_global_out + end_trim
        tool.GlobalIn[1] = old_global_in + start_trim


def get_frame_rate(tool) -> int:
    """Gets frame rate from tool's metadata."""

    frame_rate: int = 0
    search: list = ["framerate", "framespersecond", "fps", "frame_rate"]

    start_time = tool.GetAttrs("TOOLNT_Region_Start")[1]
    metadata = tool.Output[start_time].Metadata
    for key, value in metadata.items():
        if key.lower() in search:
            frame_rate = int(value)

    return frame_rate


def timecode_to_frames(timecode: str, frame_rate: int) -> int:
    """Converts timecode (SMPTE) to frames."""

    # Split timecode "hh:mm:ss:ff".
    hours, minutes, seconds, frames = map(int, timecode.split(":"))
    
    # Calculate total amount of frames.
    total_frames = (
        hours * 3600 * frame_rate +  # hours in seconds * frame rate.
        minutes * 60 * frame_rate +  # minutes in seconds * frame rate.
        seconds * frame_rate +       # seconds * frame rate.
        frames                       # frames.
    )
    
    return total_frames


def frames_to_timecode(frame_number: int, frame_rate: int) -> str:
    """Converts frames to timecode (SMPTE)."""

    # Calculate hours, minutes, seconds and frames.
    hours = frame_number // (3600 * frame_rate)
    frame_number %= 3600 * frame_rate
    
    minutes = frame_number // (60 * frame_rate)
    frame_number %= 60 * frame_rate
    
    seconds = frame_number // frame_rate
    frames = frame_number % frame_rate

    # Format output to SMPTE timecode.
    timecode = f"{hours:02}:{minutes:02}:{seconds:02}:{frames:02}"

    return timecode


def refill_fields(itm, tool) -> None:
    """Refills UI fields with given tool's data."""

    start_time = tool.GetAttrs("TOOLNT_Region_Start")[1]
    end_time = tool.GetAttrs("TOOLNT_Region_End")[1]

    start_time_code = tool.Output[start_time].Metadata["TimeCode"]
    end_time_code = tool.Output[end_time].Metadata["TimeCode"]

    itm["LE_Loader"].Text = tool.Name
    itm["LE_Start_TC"].Text = start_time_code
    itm["LE_End_TC"].Text = end_time_code
    itm["SB_FrameRate"].Value = get_frame_rate(tool)



def reload(itm) -> None:
    """Reloads data. If tool is selected use it, otherwise use loader input in the UI."""

    active_tool = None
    found_tool = None

    try:
        active_tool = comp.ActiveTool()
    except:
        pass

    try:
        found_tool = comp.FindTool(itm["LE_Loader"].Text)
    except:
        pass

    if active_tool:
        refill_fields(itm, active_tool)
    elif found_tool:
        refill_fields(itm, found_tool)
    else:
        return None


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


gui_geo = gui_geometry(500, 180, 0.5, 0.5)


# GUI
ui   = fusion.UIManager
disp = bmd.UIDispatcher(ui)

dlg  = disp.AddWindow({"WindowTitle": "Trim loader with TimeCode (SMPTE)",
                       "ID": "MyWin",
                       "Geometry": [gui_geo['x'], gui_geo['y'], gui_geo['width'], gui_geo['height']],
                       "Events": {"Close": True,
                                  "KeyPress": True,
                                  "KeyRelease": True},
                      },
    [
        ui.VGroup({"Spacing": 5},
        [

            ui.HGroup([
                ui.Label({"Text": "Loader:", "ID": "L_Start_TC", "Weight": 0.1}),
                ui.LineEdit({"ID": "LE_Loader", "Text": "", "PlaceholderText": "Loader Name", "Weight": 0.6}),
                ui.Button({"Text": "Reload", "ID": "BTN_Reload", "Weight": 0.1}),
            ]),

            ui.VGap(10),

            ui.Label({"Text": "Timecode", "ID": "L_TimeCode", "Weight": 0.1}),
            ui.HGroup([
                ui.Label({"Text": "Start:", "ID": "L_Start_TC", "Weight": 0.1}),
                ui.LineEdit({"ID": "LE_Start_TC", "Text": "", "PlaceholderText": "TimeCode (00:00:00:00)", "Weight": 0.6}),
                ui.Label({"Text": "End:", "ID": "L_End_TC", "Weight": 0.1}),
                ui.LineEdit({"ID": "LE_End_TC", "Text": "", "PlaceholderText": "TimeCode (00:00:00:00)", "Weight": 0.6}),
                ui.Label({"Text": "FPS:", "ID": "L_FrameRate", "Weight": 0.1}),
                ui.SpinBox({"ID": "SB_FrameRate", "Minimum": 0, "Maximum": 1000000, "Value": 0, "Weight": 0.1}),
            ]),
            ui.HGroup([
                ui.CheckBox({"ID": "CB_LockGlobalIn", "Text": "Lock Global In"}),
            ]),

            ui.VGap(10),

            ui.HGroup([
                ui.Button({"Text": "Trim", "ID": "BTN_Trim", "Weight": 0.5}),
                ui.Button({"Text": "Cancel", "ID": "BTN_Cancel", "Weight": 0.5}),
            ]),
        ]),
    ])


# Collect ui items.
itm = dlg.GetItems()


# Default values.
tool = comp.ActiveTool
if tool:
    start_time = tool.GetAttrs("TOOLNT_Region_Start")[1]
    end_time = tool.GetAttrs("TOOLNT_Region_End")[1]

    start_time_code = tool.Output[start_time].Metadata["TimeCode"]
    end_time_code = tool.Output[end_time].Metadata["TimeCode"]

    itm["LE_Loader"].Text = tool.Name
    itm["LE_Start_TC"].Text = start_time_code
    itm["LE_End_TC"].Text = end_time_code
    itm["SB_FrameRate"].Value = get_frame_rate(tool)


# Keys are pressed.
def _func(ev):
    key_modifiers = get_key_modifiers(ev)
    if CTRL in key_modifiers and ev['Key'] == 81:  # Ctrl + Q.
        disp.ExitLoop()
        dlg.Hide()
dlg.On.MyWin.KeyPress = _func


# Trim.
def _func(ev):
    comp.StartUndo("Trim loader")
    
    tool = comp.FindTool(itm["LE_Loader"].Text)
    if tool:
        if tool.ID == "Loader":
            if check_metadata(tool):
                trim_with_timecode(tool,
                                itm["LE_Start_TC"].Text,
                                itm["LE_End_TC"].Text,
                                itm["SB_FrameRate"].Value,
                                itm["CB_LockGlobalIn"].Checked
                                )
            else:
                print("Required metadata not found!")
        else:
            print("Only loaders are supported!")
    else:
        print("No tool found!")

    comp.EndUndo(True)
dlg.On.BTN_Trim.Clicked = _func


# Reload.
def _func(ev):
    comp.StartUndo("Reload")
    reload(itm)
    comp.EndUndo(True)
dlg.On.BTN_Reload.Clicked = _func


# The window was closed.
def _func(ev):
    disp.ExitLoop()
dlg.On.MyWin.Close = _func
dlg.On.BTN_Cancel.Clicked = _func


# Open the dialog.
dlg.Show()
disp.RunLoop()
dlg.Hide()

