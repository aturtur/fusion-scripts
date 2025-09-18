"""
AR_AlignImage

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Align Image
Version: 1.1.0
Description-US: Aligns merge node's foreground image according to the background image.

How to use: Select merge node that has foreground and background inputs connected,
then press the button where you want to align the foreground image.

Written for Blackmagic Design Fusion Studio 19.1.3 build 5.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp
  
Changelog:
1.1.0 (07.09.2025) - Added option to set strength.
1.0.2 (07.05.2025) - Added hotkey Ctrl+Q to close the dialog.
1.0.1 (25.02.2025) - Added support for Merge node's Size parameter.
1.0.0 (12.02.2025) - Initial release.
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


def interpolate(value: float, x1: float, x2: float, y1: float, y2: float) -> float:
    """Perform linear interpolation for value between (x1,y1) and (x2,y2)."""

    return ((y2 - y1) * value + x2 * y1 - x1 * y2) / (x2 - x1)


def get_merge_data() -> tuple | bool:
    """Gets all important data from the selected merge node."""

    merge_node = comp.ActiveTool()
    if merge_node.ID == "Merge":
        bg_node = merge_node.FindMainInput(1).GetConnectedOutput().GetTool()
        fg_node = merge_node.FindMainInput(2).GetConnectedOutput().GetTool()

        bg_width = bg_node.GetAttrs("TOOLI_ImageWidth")
        bg_height = bg_node.GetAttrs("TOOLI_ImageHeight")

        fg_width = fg_node.GetAttrs("TOOLI_ImageWidth")
        fg_height = fg_node.GetAttrs("TOOLI_ImageHeight")

        return merge_node, bg_node, bg_width, bg_height, fg_node, fg_width, fg_height
    else:
        print("Select Merge node first!")
        return False


def align_image(method: str, strength: float) -> None:
    """Clears preview windows, also both A and B buffers."""

    if get_merge_data() == False: return
    merge_node, _, bg_width, bg_height, _, fg_width, fg_height = get_merge_data()
    merge_scale = merge_node.GetInput("Size")
    merge_x = float(merge_node.GetInput("Center")[1])
    merge_y = float(merge_node.GetInput("Center")[2])

    step_x = interpolate(0.5, 0, bg_width, 0, fg_width)
    step_y = interpolate(0.5, 0, bg_height, 0, fg_height)

    if method == "Button_Bot_Left":
        pos_x = interpolate(strength, 0, 1, merge_x, step_x * merge_scale)
        pos_y = interpolate(strength, 0, 1, merge_y, step_y * merge_scale)
    elif method == "Button_Bot_Center":
        pos_x = interpolate(strength, 0, 1, merge_x, 0.5)
        pos_y = interpolate(strength, 0, 1, merge_y, step_y * merge_scale)
    elif method == "Button_Bot_Right":
        pos_x = interpolate(strength, 0, 1, merge_x, 1-step_x * merge_scale)
        pos_y = interpolate(strength, 0, 1, merge_y, step_y * merge_scale)
    elif method == "Button_Mid_Left":
        pos_x = interpolate(strength, 0, 1, merge_x, step_x * merge_scale)
        pos_y = interpolate(strength, 0, 1, merge_y, 0.5)
    elif method == "Button_Mid_Center":
        pos_x = interpolate(strength, 0, 1, merge_x, 0.5)
        pos_y = interpolate(strength, 0, 1, merge_y, 0.5)
    elif method == "Button_Mid_Right":
        pos_x = interpolate(strength, 0, 1, merge_x, 1-step_x * merge_scale)
        pos_y = interpolate(strength, 0, 1, merge_y, 0.5)
    elif method == "Button_Top_Left":
        pos_x = interpolate(strength, 0, 1, merge_x, step_x * merge_scale)
        pos_y = interpolate(strength, 0, 1, merge_y, 1-step_y * merge_scale)
    elif method == "Button_Top_Center":
        pos_x = interpolate(strength, 0, 1, merge_x, 0.5)
        pos_y = interpolate(strength, 0, 1, merge_y, 1-step_y * merge_scale)
    elif method == "Button_Top_Right":
        pos_x = interpolate(strength, 0, 1, merge_x, 1-step_x * merge_scale)
        pos_y = interpolate(strength, 0, 1, merge_y, 1-step_y * merge_scale)

    merge_node.SetInput("Center", {1: pos_x, 2: pos_y, 3: 0.0})


def convert_merge_to_transform() -> None:
    """Converts center x and y values to the transform node."""

    if get_merge_data() == False: return
    merge_node, _, bg_width, bg_height, fg_node, fg_width, fg_height = get_merge_data()
    merge_scale = merge_node.GetInput("Size")

    merge_x = merge_node.GetInput("Center")[1]
    merge_y = merge_node.GetInput("Center")[2]

    transform_x = 0.5 + ((merge_x - 0.5) * (bg_width / fg_width))
    transform_y = 0.5 + ((merge_y - 0.5) * (bg_height / fg_height))

    flow = comp.CurrentFrame.FlowView
    x, y = flow.GetPosTable(merge_node).values()
    transform_node = comp.AddTool("Transform", x, y-1)
    merge_node.Foreground = transform_node.Output
    transform_node.Input = fg_node.Output

    merge_node.SetInput("Center", {1: 0.5, 2: 0.5, 3: 0.0})
    merge_node.SetInput("Size", 1)
    transform_node.SetInput("Center", {1: transform_x, 2: transform_y, 3: 0.0})
    transform_node.SetInput("Size", merge_scale)


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


gui_geo = gui_geometry(100, 100, 0.5, 0.5)


# GUI 
ui   = fusion.UIManager
disp = bmd.UIDispatcher(ui)
dlg  = disp.AddWindow({"WindowTitle": "Align Image",
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
                ui.Button({"Text": "┌", "ID": "Button_Top_Left"}),
                ui.Button({"Text": "┬", "ID": "Button_Top_Center"}),
                ui.Button({"Text": "┐", "ID": "Button_Top_Right"}),
            ]),
            ui.HGroup([
                ui.Button({"Text": "├", "ID": "Button_Mid_Left"}),
                ui.Button({"Text": "┼", "ID": "Button_Mid_Center"}),
                ui.Button({"Text": "┤", "ID": "Button_Mid_Right"}),
            ]),
            ui.HGroup([
                ui.Button({"Text": "└", "ID": "Button_Bot_Left"}),
                ui.Button({"Text": "┴", "ID": "Button_Bot_Center"}),
                ui.Button({"Text": "┘", "ID": "Button_Bot_Right"}),
            ]),

            ui.HGroup([
                ui.Slider({
                    "ID": "StrengthSlider",
                    "Min": 0,
                    "Max": 100,
                    "Value": 100,
                    "NumSteps": 101,
                    "Weight": 0.8,
                    "Tracking": True
                }),
                ui.LineEdit({
                    "ID": "StrengthEdit",
                    "Text": "1.00",
                    "Alignment": {"AlignHCenter": True},
                    "Weight": 0.2,
                    "ToolTip": "Strength"
                }),
            ]),

            ui.HGroup([
                ui.Button({"Text": "Convert to Transform", "ID": "Button_Convert"}),
            ]),
        ]),
    ])

#

# Collect ui items.
itm = dlg.GetItems()


def OnSlider(ev):
    val = itm["StrengthSlider"].Value / 100.0
    itm["StrengthEdit"].Text = f"{val:.2f}"
dlg.On.StrengthSlider.ValueChanged = OnSlider


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

    if ev['Key'] in [16777220, 16777221]:  # Enter.
        if itm["StrengthEdit"].HasFocus():
            try:
                val = float(itm["StrengthEdit"].Text)
            except ValueError:
                return
            val = max(0.0, min(1.0, val))
            itm["StrengthSlider"].Value = int(val * 100)
dlg.On.MyWin.KeyPress = _func


# Buttons are pressed.
def _func(ev):
    comp.StartUndo("Align Image")
    tool = comp.ActiveTool()
    if tool.ID == "Merge":
        strength = float(itm["StrengthEdit"].Text)
        align_image(ev['who'], strength)
    else:
        print("This script only supports the merge tool!")
    comp.EndUndo(True)
dlg.On.Button_Top_Left.Clicked = _func
dlg.On.Button_Top_Center.Clicked = _func
dlg.On.Button_Top_Right.Clicked = _func
dlg.On.Button_Mid_Left.Clicked = _func
dlg.On.Button_Mid_Center.Clicked = _func
dlg.On.Button_Mid_Right.Clicked = _func
dlg.On.Button_Bot_Left.Clicked = _func
dlg.On.Button_Bot_Center.Clicked = _func
dlg.On.Button_Bot_Right.Clicked = _func

def _func(ev):
    comp.StartUndo("Convert")
    convert_merge_to_transform()
    comp.EndUndo(True)
dlg.On.Button_Convert.Clicked = _func


# Open the dialog.
dlg.Show()
disp.RunLoop()
dlg.Hide()