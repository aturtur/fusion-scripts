"""
ar_RangeManager
Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Range Manager
Version: 1.5.1
Description-US: Set global and render range easily.

Written for Blackmagic Design Fusion Studio 19.0 build 59.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Default: Set render range.
Shift: Get render range.
Ctrl: Set Global range.
Ctrl+Shift: Get global range.

Changelog:
1.5.1 (09.01.2026)  - Fixed a bug with two last slots.
1.5.0 (21.11.2025)  - Added two more slots.
1.4.0 (03.06.2025)  - Removed Get buttons. Keymodiers will change set buttons' state.
1.3.0 (15.05.2025)  - GUI width reduced a bit.
                    - Expand the timeline if given range is shorter/longer than the current timeline.
1.2.2 (14.05.2025)  - Major bug fixes.
                    - If sticky note is created it's selected.
                    - Swapped global range and render range key modifiers.
1.2.1 (07.05.2025)  - Added hotkey Ctrl+Q to close the dialog.
1.2.0 (09.10.2024)  - Name changed from AR_SetRange to AR_RangeManager.
                    - Added load and save buttons. Stores data to sticky note!
                    - Removed method combobox and added buttons instead.
1.1.0 (21.04.2024)  - Added get buttons.
1.0.0 (25.03.2023)  - Initial release.
"""
# Libraries
...


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()

note_name = "RangeManager"
alphabets = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

ALT: str = "ALT"
CTRL: str = "CTRL"
SHIFT: str = "SHIFT"


# Functions
def set_range(start, end, method):
    """Sets timeline range with given values."""

    current_global_start = comp.GetAttrs("COMPN_GlobalStart")
    current_global_end = comp.GetAttrs("COMPN_GlobalEnd")

    if method == "render":
        # If global range is smaller than given render range -> extend time line.
        if start <= current_global_start:
            comp.SetAttrs({"COMPN_GlobalStart": start})
        if end >= current_global_end:
            comp.SetAttrs({"COMPN_GlobalEnd": end})

        # Set render range,
        comp.SetAttrs({"COMPN_RenderStart": start,
                       "COMPN_RenderEnd": end})
                
    elif method == "global":
        # Set global range,
        comp.SetAttrs({"COMPN_GlobalStart": start,
                       "COMPN_GlobalEnd": end})


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
    """Gets values from note."""

    def clear_values(itm) -> None:
        for alphabet in alphabets:
            itm['Comment'+alphabet].Text = ""
            itm['Start'+alphabet].Value = 0
            itm['End'+alphabet].Value = 0

    tool = comp.FindTool(note_name)

    if tool:
        content = tool.Comments[1]
        lines = content.split("\n")

        if content != "":
            for i, line in enumerate(lines):
                if line != "":
                    values = line.split(",")
                    comment = values[0]
                    start = values[1]
                    end = values[2]

                    itm['Comment'+alphabets[i]].Text = str(comment)
                    itm['Start'+alphabets[i]].Value = int(start)
                    itm['End'+alphabets[i]].Value = int(end)
        else:
            clear_values(itm)
    else:
        clear_values(itm)


def save_values(itm) -> None:
    """Writes to note."""

    content = [
        [f"{itm['CommentA'].Text},{itm['StartA'].Value},{itm['EndA'].Value}\n"],
        [f"{itm['CommentB'].Text},{itm['StartB'].Value},{itm['EndB'].Value}\n"],
        [f"{itm['CommentC'].Text},{itm['StartC'].Value},{itm['EndC'].Value}\n"],
        [f"{itm['CommentD'].Text},{itm['StartD'].Value},{itm['EndD'].Value}\n"],
        [f"{itm['CommentE'].Text},{itm['StartE'].Value},{itm['EndE'].Value}\n"],
        [f"{itm['CommentF'].Text},{itm['StartF'].Value},{itm['EndF'].Value}\n"],
        [f"{itm['CommentG'].Text},{itm['StartG'].Value},{itm['EndG'].Value}\n"],
        [f"{itm['CommentH'].Text},{itm['StartH'].Value},{itm['EndH'].Value}\n"],
        [f"{itm['CommentI'].Text},{itm['StartI'].Value},{itm['EndI'].Value}\n"],
        [f"{itm['CommentJ'].Text},{itm['StartJ'].Value},{itm['EndJ'].Value}\n"]
    ]

    comments = ''.join([item[0] for item in content])

    sticky_note = comp.FindTool(note_name)
    if not sticky_note:
        sticky_note = comp.AddTool("Note")
        
        flow = comp.CurrentFrame.FlowView
        flow.Select()
        flow.Select(sticky_note)

    sticky_note.SetAttrs({'TOOLS_Name': note_name})
    sticky_note.Comments[comp.CurrentTime] = comments


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


gui_geo = gui_geometry(500, 375, 0.5, 0.5)


# GUI
ui   = fusion.UIManager
disp = bmd.UIDispatcher(ui)
dlg  = disp.AddWindow({"WindowTitle": "Range Manager",
                       "ID": "MyWin",
                       "Events": {"Close": True,
                                  "KeyPress": True,
                                  "KeyRelease": True},
                       "Geometry": [gui_geo['x'], gui_geo['y'], gui_geo['width'], gui_geo['height']]
                       },
    [
        ui.VGroup({"Spacing": 5},
        [
            ui.HGroup([
                ui.LineEdit({"ID": "CommentA", "Text": "", "PlaceholderText": "Comment", "Weight": 0.6}),
                #ui.Button({"Text": "Get", "ID": "Button_Get_A", "Weight": 0.1, "ToolTip": "Get Range In/Out, Shift: Global Range"}),
                ui.SpinBox({"ID": "StartA", "Minimum": 0, "Maximum": 1000000, "Value": comp.GetAttrs("COMPN_GlobalStart"), "Weight": 0.1}),
                ui.SpinBox({"ID": "EndA", "Minimum": 0, "Maximum": 1000000, "Value": comp.GetAttrs("COMPN_GlobalEnd"), "Weight": 0.1}),
                ui.Button({"Text": "Set Render", "ID": "Button_Set_A", "Weight": 0.1, "ToolTip": "Set Range In/Out\nShift: Get Render Range\nCtrl: Set Global Range\nCtrl+Shift: Get Global Range"}),
            ]),
            ui.HGroup([
                ui.LineEdit({"ID": "CommentB", "Text": "", "PlaceholderText": "Comment", "Weight": 0.6}),
                ui.SpinBox({"ID": "StartB", "Minimum": 0, "Maximum": 1000000, "Value": comp.GetAttrs("COMPN_GlobalStart"), "Weight": 0.1}),
                ui.SpinBox({"ID": "EndB", "Minimum": 0, "Maximum": 1000000, "Value": comp.GetAttrs("COMPN_GlobalEnd"), "Weight": 0.1}),
                ui.Button({"Text": "Set Render", "ID": "Button_Set_B", "Weight": 0.1, "ToolTip": "Set Range In/Out\nShift: Get Render Range\nCtrl: Set Global Range\nCtrl+Shift: Get Global Range"}),
            ]),
            ui.HGroup([
                ui.LineEdit({"ID": "CommentC", "Text": "", "PlaceholderText": "Comment", "Weight": 0.6}),
                ui.SpinBox({"ID": "StartC", "Minimum": 0, "Maximum": 1000000, "Value": comp.GetAttrs("COMPN_GlobalStart"), "Weight": 0.1}),
                ui.SpinBox({"ID": "EndC", "Minimum": 0, "Maximum": 1000000, "Value": comp.GetAttrs("COMPN_GlobalEnd"), "Weight": 0.1}),
                ui.Button({"Text": "Set Render", "ID": "Button_Set_C", "Weight": 0.1, "ToolTip": "Set Range In/Out\nShift: Get Render Range\nCtrl: Set Global Range\nCtrl+Shift: Get Global Range"}),
            ]),
            ui.HGroup([
                ui.LineEdit({"ID": "CommentD", "Text": "", "PlaceholderText": "Comment", "Weight": 0.6}),
                ui.SpinBox({"ID": "StartD", "Minimum": 0, "Maximum": 1000000, "Value": comp.GetAttrs("COMPN_GlobalStart"), "Weight": 0.1}),
                ui.SpinBox({"ID": "EndD", "Minimum": 0, "Maximum": 1000000, "Value": comp.GetAttrs("COMPN_GlobalEnd"), "Weight": 0.1}),
                ui.Button({"Text": "Set Render", "ID": "Button_Set_D", "Weight": 0.1, "ToolTip": "Set Range In/Out\nShift: Get Render Range\nCtrl: Set Global Range\nCtrl+Shift: Get Global Range"}),
            ]),
            ui.HGroup([
                ui.LineEdit({"ID": "CommentE", "Text": "", "PlaceholderText": "Comment", "Weight": 0.6}),
                ui.SpinBox({"ID": "StartE", "Minimum": 0, "Maximum": 1000000, "Value": comp.GetAttrs("COMPN_GlobalStart"), "Weight": 0.1}),
                ui.SpinBox({"ID": "EndE", "Minimum": 0, "Maximum": 1000000, "Value": comp.GetAttrs("COMPN_GlobalEnd"), "Weight": 0.1}),
                ui.Button({"Text": "Set Render", "ID": "Button_Set_E", "Weight": 0.1, "ToolTip": "Set Range In/Out\nShift: Get Render Range\nCtrl: Set Global Range\nCtrl+Shift: Get Global Range"}),
            ]),
            ui.HGroup([
                ui.LineEdit({"ID": "CommentF", "Text": "", "PlaceholderText": "Comment", "Weight": 0.6}),
                ui.SpinBox({"ID": "StartF", "Minimum": 0, "Maximum": 1000000, "Value": comp.GetAttrs("COMPN_GlobalStart"), "Weight": 0.1}),
                ui.SpinBox({"ID": "EndF", "Minimum": 0, "Maximum": 1000000, "Value": comp.GetAttrs("COMPN_GlobalEnd"), "Weight": 0.1}),
                ui.Button({"Text": "Set Render", "ID": "Button_Set_F", "Weight": 0.1, "ToolTip": "Set Range In/Out\nShift: Get Render Range\nCtrl: Set Global Range\nCtrl+Shift: Get Global Range"}),
            ]),
            ui.HGroup([
                ui.LineEdit({"ID": "CommentG", "Text": "", "PlaceholderText": "Comment", "Weight": 0.6}),
                ui.SpinBox({"ID": "StartG", "Minimum": 0, "Maximum": 1000000, "Value": comp.GetAttrs("COMPN_GlobalStart"), "Weight": 0.1}),
                ui.SpinBox({"ID": "EndG", "Minimum": 0, "Maximum": 1000000, "Value": comp.GetAttrs("COMPN_GlobalEnd"), "Weight": 0.1}),
                ui.Button({"Text": "Set Render", "ID": "Button_Set_G", "Weight": 0.1, "ToolTip": "Set Range In/Out\nShift: Get Render Range\nCtrl: Set Global Range\nCtrl+Shift: Get Global Range"}),
            ]),
            ui.HGroup([
                ui.LineEdit({"ID": "CommentH", "Text": "", "PlaceholderText": "Comment", "Weight": 0.6}),
                ui.SpinBox({"ID": "StartH", "Minimum": 0, "Maximum": 1000000, "Value": comp.GetAttrs("COMPN_GlobalStart"), "Weight": 0.1}),
                ui.SpinBox({"ID": "EndH", "Minimum": 0, "Maximum": 1000000, "Value": comp.GetAttrs("COMPN_GlobalEnd"), "Weight": 0.1}),
                ui.Button({"Text": "Set Render", "ID": "Button_Set_H", "Weight": 0.1, "ToolTip": "Set Range In/Out\nShift: Get Render Range\nCtrl: Set Global Range\nCtrl+Shift: Get Global Range"}),
            ]),
            ui.HGroup([
                ui.LineEdit({"ID": "CommentI", "Text": "", "PlaceholderText": "Comment", "Weight": 0.6}),
                ui.SpinBox({"ID": "StartI", "Minimum": 0, "Maximum": 1000000, "Value": comp.GetAttrs("COMPN_GlobalStart"), "Weight": 0.1}),
                ui.SpinBox({"ID": "EndI", "Minimum": 0, "Maximum": 1000000, "Value": comp.GetAttrs("COMPN_GlobalEnd"), "Weight": 0.1}),
                ui.Button({"Text": "Set Render", "ID": "Button_Set_I", "Weight": 0.1, "ToolTip": "Set Range In/Out\nShift: Get Render Range\nCtrl: Set Global Range\nCtrl+Shift: Get Global Range"}),
            ]),
            ui.HGroup([
                ui.LineEdit({"ID": "CommentJ", "Text": "", "PlaceholderText": "Comment", "Weight": 0.6}),
                ui.SpinBox({"ID": "StartJ", "Minimum": 0, "Maximum": 1000000, "Value": comp.GetAttrs("COMPN_GlobalStart"), "Weight": 0.1}),
                ui.SpinBox({"ID": "EndJ", "Minimum": 0, "Maximum": 1000000, "Value": comp.GetAttrs("COMPN_GlobalEnd"), "Weight": 0.1}),
                ui.Button({"Text": "Set Render", "ID": "Button_Set_J", "Weight": 0.1, "ToolTip": "Set Range In/Out\nShift: Get Render Range\nCtrl: Set Global Range\nCtrl+Shift: Get Global Range"}),
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


# Keys are pressed.
def _func(ev):
    key_modifiers = get_key_modifiers(ev)
    if CTRL in key_modifiers and ev['Key'] == 81:  # Ctrl + Q.
        disp.ExitLoop()
        dlg.Hide()

    if SHIFT in key_modifiers:
        itm['Button_Set_A'].Text = "Get Render"
        itm['Button_Set_B'].Text = "Get Render"
        itm['Button_Set_C'].Text = "Get Render"
        itm['Button_Set_D'].Text = "Get Render"
        itm['Button_Set_E'].Text = "Get Render"
        itm['Button_Set_F'].Text = "Get Render"
        itm['Button_Set_G'].Text = "Get Render"
        itm['Button_Set_H'].Text = "Get Render"
        itm['Button_Set_I'].Text = "Get Render"
        itm['Button_Set_J'].Text = "Get Render"

    if CTRL in key_modifiers:
        itm['Button_Set_A'].Text = "Set Global"
        itm['Button_Set_B'].Text = "Set Global"
        itm['Button_Set_C'].Text = "Set Global"
        itm['Button_Set_D'].Text = "Set Global"
        itm['Button_Set_E'].Text = "Set Global"
        itm['Button_Set_F'].Text = "Set Global"
        itm['Button_Set_G'].Text = "Set Global"
        itm['Button_Set_H'].Text = "Set Global"
        itm['Button_Set_I'].Text = "Set Global"
        itm['Button_Set_J'].Text = "Set Global"

    required = {CTRL, SHIFT}
    if required.issubset(key_modifiers):
        itm['Button_Set_A'].Text = "Get Global"
        itm['Button_Set_B'].Text = "Get Global"
        itm['Button_Set_C'].Text = "Get Global"
        itm['Button_Set_D'].Text = "Get Global"
        itm['Button_Set_E'].Text = "Get Global"
        itm['Button_Set_F'].Text = "Get Global"
        itm['Button_Set_G'].Text = "Get Global"
        itm['Button_Set_H'].Text = "Get Global"
        itm['Button_Set_I'].Text = "Get Global"
        itm['Button_Set_J'].Text = "Get Global"
dlg.On.MyWin.KeyPress = _func

# Keys are released
def _func(ev):
    key_modifiers = get_key_modifiers(ev)
    if SHIFT in key_modifiers or CTRL in key_modifiers:
        itm['Button_Set_A'].Text = "Set Render"
        itm['Button_Set_B'].Text = "Set Render"
        itm['Button_Set_C'].Text = "Set Render"
        itm['Button_Set_D'].Text = "Set Render"
        itm['Button_Set_E'].Text = "Set Render"
        itm['Button_Set_F'].Text = "Set Render"
        itm['Button_Set_G'].Text = "Set Render"
        itm['Button_Set_H'].Text = "Set Render"
        itm['Button_Set_I'].Text = "Set Render"
        itm['Button_Set_J'].Text = "Set Render"
dlg.On.MyWin.KeyRelease = _func


# Buttons are pressed.
# Set Range.
def _func(ev):
    comp.StartUndo("Set Range")
    idx = ev['who'][11:]
    key_modifiers = get_key_modifiers(ev)
    if not key_modifiers:
        set_range(itm['Start'+idx].Value, itm['End'+idx].Value, "render")
    if [SHIFT] == key_modifiers:
        itm['Start'+idx].Value = comp.GetAttrs("COMPN_RenderStart")
        itm['End'+idx].Value = comp.GetAttrs("COMPN_RenderEnd")
    if [CTRL] == key_modifiers:
        set_range(itm['Start'+idx].Value, itm['End'+idx].Value, "global")
    required = {CTRL, SHIFT}
    if required.issubset(key_modifiers):
        itm['Start'+idx].Value = comp.GetAttrs("COMPN_GlobalStart")
        itm['End'+idx].Value = comp.GetAttrs("COMPN_GlobalEnd")
    comp.EndUndo(True)
dlg.On.Button_Set_A.Clicked = _func
dlg.On.Button_Set_B.Clicked = _func
dlg.On.Button_Set_C.Clicked = _func
dlg.On.Button_Set_D.Clicked = _func
dlg.On.Button_Set_E.Clicked = _func
dlg.On.Button_Set_F.Clicked = _func
dlg.On.Button_Set_G.Clicked = _func
dlg.On.Button_Set_H.Clicked = _func
dlg.On.Button_Set_I.Clicked = _func
dlg.On.Button_Set_J.Clicked = _func


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