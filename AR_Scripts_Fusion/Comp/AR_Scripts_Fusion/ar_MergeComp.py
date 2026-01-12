"""
ar_MergeComp

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Merge Comp
Version: 1.0.1
Description-US: Merges the given composition with the active one.

Written for Blackmagic Design Fusion Studio 19.0 build 59.
Python version 3 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.0.1 (07.05.2025) - Added hotkey Ctrl+Q to close the dialog.
1.0.0 (28.02.2025) - Initial release.
"""
# Libraries
import pyperclip
from pathlib import Path


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


def merge_comp(comp_path: str) -> None:
    """Merges the given composition with the active one."""

    path = Path(comp_path)

    with open(path, "r", encoding="utf-8") as file:
        content = file.read()
    pyperclip.copy(content)
    comp.Paste()


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


gui_geo = gui_geometry(500, 80, 0.5, 0.5)


# GUI
ui   = fusion.UIManager
disp = bmd.UIDispatcher(ui)
dlg  = disp.AddWindow({"WindowTitle": "Merge Composition",
                       "ID": "MyWin",
                       "Geometry": [gui_geo['x'], gui_geo['y'], gui_geo['width'], gui_geo['height']],
                       "Events": {"Close": True,
                                  "KeyPress": True,
                                  "KeyRelease": True},
                       },
    [
        ui.VGroup({"Spacing": 5},
        [
            # GUI elements.

            # Select folder path.
            ui.HGroup(
            [
                ui.Label({"Text": "File Path", "ID": "Label_FolderPath", "Weight": 0.1}),
                ui.LineEdit({"Text": "", "PlaceholderText": "Please Enter the Composition File Path", "ID": "CompPath", "Weight": 0.9}),
                ui.Button({"Text": "...", "ID": "Button_Browse", "Weight": 0.1}),
            ]),

            # Import and Cancel buttons.
            ui.HGroup(
            [
                ui.Button({"Text": "Import", "ID": "Button_Merge", "Weight": 0.5}),
                ui.Button({"Text": "Cancel", "ID": "Button_Cancel", "Weight": 0.5}),
            ]),
        ]),
    ])


# Collect ui items.
itm = dlg.GetItems()


# The window was closed.
def _func(ev):
    disp.ExitLoop()
dlg.On.MyWin.Close = _func
dlg.On.Button_Cancel.Clicked = _func


# Keys are pressed.
def _func(ev):
    key_modifiers = get_key_modifiers(ev)
    if CTRL in key_modifiers and ev['Key'] == 81:  # Ctrl + Q.
        disp.ExitLoop()
        dlg.Hide()
dlg.On.MyWin.KeyPress = _func


# Browse the composition path.
def _func(ev):
    selectedCompPath = fusion.RequestFile(itm['CompPath'].Text)
    if selectedCompPath:
        itm['CompPath'].Text = str(selectedCompPath)
dlg.On.Button_Browse.Clicked = _func


# Merge comp.
def _func(ev):
    comp.Lock()
    comp.StartUndo("Merge Comp")

    merge_comp(itm['CompPath'].Text)

    comp.EndUndo(True)
    comp.Unlock()
dlg.On.Button_Merge.Clicked = _func


# Open the dialog.
dlg.Show()
disp.RunLoop()
dlg.Hide()