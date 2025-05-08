"""
AR_JumpToFrame

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Jump To Frame
Version: 1.3.1
Description-US: Jumps to given frame in the timeline.

Tip: Use Ctrl + 1-8 to jump to the frame.

Written for Blackmagic Design Fusion Studio 19.0 build 59.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.3.1 (07.05.2025) - Added hotkey Ctrl+Q to close the dialog.
1.3.0 (06.04.2025) - Added hotkeys to jump to frame (Ctrl + 1-8).
1.2.0 (29.09.2024) - Added load and save buttons. Stores data to sticky note!
1.1.1 (25.09.2024) - Changed code to follow more PEP 8 recommendations.
1.1.0 (21.04.2024) - Added get buttons.
1.0.0 (25.03.2023) - Initial release.
"""
# Libraries
...


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()

note_name = "JumpToFrame"
alphabets = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

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


def load_values(itm) -> None:
    """Gets values from note"""

    def clear_values(itm) -> None:
        for alphabet in alphabets:
            itm['COM_'+alphabet].Text = ""
            itm['FRM_'+alphabet].Value = 0

    tool = comp.FindTool(note_name)

    if tool:
        content = tool.Comments[1]
        lines = content.split("\n")

        if content != "":
            for i, line in enumerate(lines):
                if line != "":
                    values = line.split(",")
                    comment = values[0]
                    value = values[1]

                    itm['COM_'+alphabets[i]].Text = str(comment)
                    itm['FRM_'+alphabets[i]].Value = int(value)
        else:
            clear_values(itm)
    else:
        clear_values(itm)


def save_values(itm) -> None:
    """Writes to note."""

    content = [
        [f"{itm['COM_A'].Text},{itm['FRM_A'].Value}\n"],
        [f"{itm['COM_B'].Text},{itm['FRM_B'].Value}\n"],
        [f"{itm['COM_C'].Text},{itm['FRM_C'].Value}\n"],
        [f"{itm['COM_D'].Text},{itm['FRM_D'].Value}\n"],
        [f"{itm['COM_E'].Text},{itm['FRM_E'].Value}\n"],
        [f"{itm['COM_F'].Text},{itm['FRM_F'].Value}\n"],
        [f"{itm['COM_G'].Text},{itm['FRM_G'].Value}\n"],
        [f"{itm['COM_H'].Text},{itm['FRM_H'].Value}\n"]
    ]

    comments = ''.join([item[0] for item in content])

    sticky_note = comp.FindTool(note_name)
    if not sticky_note:
        sticky_note = comp.AddTool("Note")
    sticky_note.SetAttrs({'TOOLS_Name': note_name})
    sticky_note.Comments[comp.CurrentTime] = comments


def jump_to_frame(frame) -> None:
    """Sets compositions current time."""

    comp.CurrentTime = float(frame)


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


gui_geo = gui_geometry(400, 300, 0.5, 0.5)

# GUI
ui   = fusion.UIManager
disp = bmd.UIDispatcher(ui)

dlg  = disp.AddWindow({"WindowTitle": "Jump To Frame",
                       "ID": "MyWin",
                       "Events": {"Close": True,
                                  "KeyPress": True,
                                  "KeyRelease": True},
                       "Geometry": [gui_geo['x'], gui_geo['y'], gui_geo['width'], gui_geo['height']],
                       "Events": {"Close": True,
                                  "KeyPress": True,
                                  "KeyRelease": True},
                       },
    [
        ui.VGroup({"Spacing": 5},
        [
            ui.HGroup([
                ui.LineEdit({"ID": "COM_A", "Text": "", "PlaceholderText": "Comment", "Weight": 0.6}),
                ui.Button({"Text": "Go", "ID": "SET_A", "Weight": 0.1}),
                ui.Button({"Text": "Get", "ID": "GET_A", "Weight": 0.1}),
                ui.SpinBox({"ID": "FRM_A", "Minimum": 0, "Maximum": 1000000, "Weight": 0.2}),
            ]),

            ui.HGroup([
                ui.LineEdit({"ID": "COM_B", "Text": "", "PlaceholderText": "Comment", "Weight": 0.6}),
                ui.Button({"Text": "Go", "ID": "SET_B", "Weight": 0.1}),
                ui.Button({"Text": "Get", "ID": "GET_B", "Weight": 0.1}),
                ui.SpinBox({"ID": "FRM_B", "Minimum": 0, "Maximum": 1000000, "Weight": 0.2}),
            ]),

            ui.HGroup([
                ui.LineEdit({"ID": "COM_C", "Text": "", "PlaceholderText": "Comment", "Weight": 0.6}),
                ui.Button({"Text": "Go", "ID": "SET_C", "Weight": 0.1}),
                ui.Button({"Text": "Get", "ID": "GET_C", "Weight": 0.1}),
                ui.SpinBox({"ID": "FRM_C", "Minimum": 0, "Maximum": 1000000, "Weight": 0.2}),
            ]),

            ui.HGroup([
                ui.LineEdit({"ID": "COM_D", "Text": "", "PlaceholderText": "Comment", "Weight": 0.6}),
                ui.Button({"Text": "Go", "ID": "SET_D", "Weight": 0.1}),
                ui.Button({"Text": "Get", "ID": "GET_D", "Weight": 0.1}),
                ui.SpinBox({"ID": "FRM_D", "Minimum": 0, "Maximum": 1000000, "Weight": 0.2}),
            ]),

            ui.HGroup([
                ui.LineEdit({"ID": "COM_E", "Text": "", "PlaceholderText": "Comment", "Weight": 0.6}),
                ui.Button({"Text": "Go", "ID": "SET_E", "Weight": 0.1}),
                ui.Button({"Text": "Get", "ID": "GET_E", "Weight": 0.1}),
                ui.SpinBox({"ID": "FRM_E", "Minimum": 0, "Maximum": 1000000, "Weight": 0.2}),
            ]),

            ui.HGroup([
                ui.LineEdit({"ID": "COM_F", "Text": "", "PlaceholderText": "Comment", "Weight": 0.6}),
                ui.Button({"Text": "Go", "ID": "SET_F", "Weight": 0.1}),
                ui.Button({"Text": "Get", "ID": "GET_F", "Weight": 0.1}),
                ui.SpinBox({"ID": "FRM_F", "Minimum": 0, "Maximum": 1000000, "Weight": 0.2}),
            ]),

            ui.HGroup([
                ui.LineEdit({"ID": "COM_G", "Text": "", "PlaceholderText": "Comment", "Weight": 0.6}),
                ui.Button({"Text": "Go", "ID": "SET_G", "Weight": 0.1}),
                ui.Button({"Text": "Get", "ID": "GET_G", "Weight": 0.1}),
                ui.SpinBox({"ID": "FRM_G", "Minimum": 0, "Maximum": 1000000, "Weight": 0.2}),
            ]),

            ui.HGroup([
                ui.LineEdit({"ID": "COM_H", "Text": "", "PlaceholderText": "Comment", "Weight": 0.6}),
                ui.Button({"Text": "Go", "ID": "SET_H", "Weight": 0.1}),
                ui.Button({"Text": "Get", "ID": "GET_H", "Weight": 0.1}),
                ui.SpinBox({"ID": "FRM_H", "Minimum": 0, "Maximum": 1000000, "Weight": 0.2}),
            ]),

            ui.HGroup([
                ui.Button({"Text": "Load Data", "ID": "Button_Load_Data", "Weight": 0.5}),
                ui.Button({"Text": "Store Data", "ID": "Button_Save_Data", "Weight": 0.5}),
            ]),
        ]),
    ])


# Collect ui items.
itm = dlg.GetItems()


# The window was closed.
def _func(ev):
    disp.ExitLoop()
dlg.On.MyWin.Close = _func


# Keyboard events.
def _func(ev):
    key_modifiers = get_key_modifiers(ev)
    if CTRL in key_modifiers and ev['Key'] == 81:  # Ctrl + Q.
        disp.ExitLoop()
        dlg.Hide()

    if ev['Key'] == 49:  # Ctrl + 1 (!).
        jump_to_frame(itm['FRM_A'].Value)
    if ev['Key'] == 50:  # Ctrl + 2 (").
        jump_to_frame(itm['FRM_B'].Value)
    if ev['Key'] == 51:  # Ctrl + 3 (#).
        jump_to_frame(itm['FRM_C'].Value)
    if ev['Key'] == 52:  # Ctrl + 4 (¤).
        jump_to_frame(itm['FRM_D'].Value)
    if ev['Key'] == 53:  # Ctrl + 5 (%).
        jump_to_frame(itm['FRM_E'].Value)
    if ev['Key'] == 54:  # Ctrl + 6 (&).
        jump_to_frame(itm['FRM_F'].Value)
    if ev['Key'] == 55:  # Ctrl + 7 (/).
        jump_to_frame(itm['FRM_G'].Value)
    if ev['Key'] == 56:  # Ctrl + 8 (().
        jump_to_frame(itm['FRM_H'].Value)
dlg.On.MyWin.KeyPress = _func


# Set frame.
def _func(ev):
    comp.StartUndo("Jump to frame")
    idx = ev['who'][4:]
    jump_to_frame(itm['FRM_'+idx].Value)
    comp.EndUndo(True)
dlg.On.SET_A.Clicked = _func
dlg.On.SET_B.Clicked = _func
dlg.On.SET_C.Clicked = _func
dlg.On.SET_D.Clicked = _func
dlg.On.SET_E.Clicked = _func
dlg.On.SET_F.Clicked = _func
dlg.On.SET_G.Clicked = _func
dlg.On.SET_H.Clicked = _func


# Get frame.
def _func(ev):
    comp.StartUndo("Get frame")
    idx = ev['who'][4:]
    itm['FRM_'+idx].Value = comp.CurrentTime
    comp.EndUndo(True)
dlg.On.GET_A.Clicked = _func
dlg.On.GET_B.Clicked = _func
dlg.On.GET_C.Clicked = _func
dlg.On.GET_D.Clicked = _func
dlg.On.GET_E.Clicked = _func
dlg.On.GET_F.Clicked = _func
dlg.On.GET_G.Clicked = _func
dlg.On.GET_H.Clicked = _func


# Load data.
def _func(ev):
    comp.StartUndo("Load data")
    load_values(itm)
    comp.EndUndo(True)
dlg.On.Button_Load_Data.Clicked = _func


# Save data.
def _func(ev):
    comp.StartUndo("Save data")
    save_values(itm)
    comp.EndUndo(True)
dlg.On.Button_Save_Data.Clicked = _func


# Open the dialog.
dlg.Show()
disp.RunLoop()
dlg.Hide()