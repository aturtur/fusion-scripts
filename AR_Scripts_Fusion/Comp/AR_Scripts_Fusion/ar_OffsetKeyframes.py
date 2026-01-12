"""
ar_OffsetKeyframes

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Offset Keyframes
Version: 1.0.2
Description-US: Offsets all keyframes of selected tool(s) by given value.\nSupports only BezierPaths!
Note: Does not support all kind of keyframes (e.g. Tracker).

Written for Blackmagic Design Fusion Studio 19.0.3 build 3.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.0.2 (25.09.2025) - Tweaking.
1.0.1 (07.05.2025) - Added hotkey Ctrl+Q to close the dialog.
1.0.0 (28.11.2024) - Initial release.
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


def offset_keyframes(tool, offset) -> None:
    """Offsets all keyframes of the tool by given value."""

    for inp in tool.GetInputList().values():
        if inp.GetConnectedOutput():
            data_type = inp.GetAttrs()["INPS_DataType"]
            if data_type:
                if data_type != "Image": 
                    splineout = inp.GetConnectedOutput()
                    spline = splineout.GetTool()
                    splinedata = spline.GetKeyFrames()

                    if spline.ID == "BezierSpline":
                        numeric_keys = [k for k in splinedata.keys() if isinstance(k, (int, float))]
                        first_key = min(numeric_keys)
                        last_key = max(numeric_keys)

                    elif spline.ID == "PolyPath":
                        print("PolyPath found. This script works only with BezierSplines!")
                        return False
    
                    spline.AdjustKeyFrames(first_key, last_key, offset, 0, "offset")


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


gui_geo = gui_geometry(100, 75, 0.5, 0.5)


# GUI
ui   = fusion.UIManager
disp = bmd.UIDispatcher(ui)
dlg  = disp.AddWindow({"WindowTitle": "Offset Keyframes",
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
            ui.HGroup([
                ui.Button({"Text": "<", "ID": "Button_Left"}),
                ui.Button({"Text": ">", "ID": "Button_Right"}),
            ]),
            ui.HGroup([
                ui.Label({"ID": "Label_Value", "Text": "Value:"}),
                ui.SpinBox({"ID": "Spinbox_Gap", "Minimum": 1, "Maximum": 1000000, "Value": 1}),
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
    comp.StartUndo("Offset keyframes")
    tools = comp.GetToolList(True).values()
    value = itm['Spinbox_Gap'].Value

    for tool in tools:
        offset_keyframes(tool, -value)
        
    comp.EndUndo(True)
dlg.On.Button_Left.Clicked = _func


def _func(ev):
    comp.StartUndo("Offset keyframes")
    tools = comp.GetToolList(True).values()
    value = itm['Spinbox_Gap'].Value

    for tool in tools:
        offset_keyframes(tool, value)
        
    comp.EndUndo(True)
dlg.On.Button_Right.Clicked = _func


# Open the dialog.
dlg.Show()
disp.RunLoop()
dlg.Hide()