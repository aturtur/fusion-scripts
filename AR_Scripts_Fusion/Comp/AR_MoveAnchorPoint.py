"""
AR_MoveAnchorPoint

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Move Anchor Point
Version: 1.0.0
Description-US: Moves the anchor point (pivot) using the DoD values.

Written for Blackmagic Design Fusion Studio 19.1.3 build 5
Python version 3.10.8 (64-bit)

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

To do:
- Support for elements that are outside the canvas?
  
Changelog:
1.0.0 (05.03.2025) - Initial release.
"""
# Libraries
...
import time


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()


# Functions
def interpolate(value: float, x1: float, x2: float, y1: float, y2: float) -> float:
    """Perform linear interpolation for value between (x1,y1) and (x2,y2) """

    return ((y2 - y1) * value + x2 * y1 - x1 * y2) / (x2 - x1)


def auto_crop(tool) -> tuple:
    """Does the auto crop and returns the values."""

    flow = comp.CurrentFrame.FlowView
    x, y = flow.GetPosTable(tool).values()
    crop_node = comp.AddTool("Crop", x+1, y)
    crop_node.SetAttrs({"TOOLS_Name": "AutoCrop"})
    crop_node.Input = tool.Output
    crop_node.AutoCrop = 1
    
    comp.Lock()
    comp.Unlock()
    time.sleep(0.5)

    x_offset = crop_node.GetInput("XOffset", comp.CurrentTime)
    y_offset = crop_node.GetInput("YOffset", comp.CurrentTime)
    x_size = crop_node.GetInput("XSize", comp.CurrentTime)
    y_size = crop_node.GetInput("YSize", comp.CurrentTime)
    
    x1 = x_offset
    y1 = y_offset
    x2 = (x_offset + x_size)
    y2 = (y_offset + y_size)

    crop_node.Delete()

    return (x1, y1), (x2, y2)


def move_anchor_point(method: str) -> None:
    """Clears preview windows, also both A and B buffers."""

    active_tool = comp.ActiveTool()

    width = active_tool.GetAttrs("TOOLI_ImageWidth")
    height = active_tool.GetAttrs("TOOLI_ImageHeight")

    crop_data = auto_crop(active_tool)
    dod_x1 = crop_data[0][0]
    dod_y1 = crop_data[0][1]
    dod_x2 = crop_data[1][0]
    dod_y2 = crop_data[1][1]

    if method == "BTN_BOT_LEFT":
        pos_x = interpolate(dod_x1, 0, width, 0, 1)
        pos_y = interpolate(dod_y1, 0, height, 0, 1)
    elif method == "BTN_BOT_CENTER":
        pos_x = interpolate((dod_x1+dod_x2)/2, 0, width, 0, 1)
        pos_y = interpolate(dod_y1, 0, height, 0, 1)
    elif method == "BTN_BOT_RIGHT":
        pos_x = interpolate(dod_x2, 0, width, 0, 1)
        pos_y = interpolate(dod_y1, 0, height, 0, 1)
    elif method == "BTN_MID_LEFT":
        pos_x = interpolate(dod_x1, 0, width, 0, 1)
        pos_y = interpolate((dod_y1+dod_y2)/2, 0, height, 0, 1)
    elif method == "BTN_MID_CENTER":
        pos_x = interpolate((dod_x1+dod_x2)/2, 0, width, 0, 1)
        pos_y = interpolate((dod_y1+dod_y2)/2, 0, height, 0, 1)
    elif method == "BTN_MID_RIGHT":
        pos_x = interpolate(dod_x2, 0, width, 0, 1)
        pos_y = interpolate((dod_y1+dod_y2)/2, 0, height, 0, 1)
    elif method == "BTN_TOP_LEFT":
        pos_x = interpolate(dod_x1, 0, width, 0, 1)
        pos_y = interpolate(dod_y2, 0, height, 0, 1)
    elif method == "BTN_TOP_CENTER":
        pos_x = interpolate((dod_x1+dod_x2)/2, 0, width, 0, 1)
        pos_y = interpolate(dod_y2, 0, height, 0, 1)
    elif method == "BTN_TOP_RIGHT":
        pos_x = interpolate(dod_x2, 0, width, 0, 1)
        pos_y = interpolate(dod_y2, 0, height, 0, 1)

    flow = comp.CurrentFrame.FlowView
    x, y = flow.GetPosTable(active_tool).values()
    transform_node = comp.AddTool("Transform", x+1, y)
    transform_node.SetAttrs({"TOOLS_Name": "MoveAnchorPoint"})
    transform_node.Input = active_tool.Output
    transform_node.SetInput("Pivot", {1: pos_x, 2: pos_y, 3: 0.0})


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
dlg  = disp.AddWindow({"WindowTitle": "Move Anchor Point",
                       "ID": "MyWin",
                       "WindowFlags": {
                          "Window": True,
                          "CustomizeWindowHint": True,
                          "WindowMinimizeButtonHint": False,
                          "WindowMaximizeButtonHint": False,
                          "WindowCloseButtonHint": True,
                        },
                       "Geometry": [gui_geo['x'], gui_geo['y'], gui_geo['width'], gui_geo['height']], },
    [
        ui.VGroup({ "Spacing": 5, },
        [
            ui.HGroup([
                ui.Button({"Text": "┌", "ID": "BTN_TOP_LEFT"}),
                ui.Button({"Text": "┬", "ID": "BTN_TOP_CENTER"}),
                ui.Button({"Text": "┐", "ID": "BTN_TOP_RIGHT"}),
            ]),
            ui.HGroup([
                ui.Button({"Text": "├", "ID": "BTN_MID_LEFT"}),
                ui.Button({"Text": "┼", "ID": "BTN_MID_CENTER"}),
                ui.Button({"Text": "┤", "ID": "BTN_MID_RIGHT"}),
            ]),
            ui.HGroup([
                ui.Button({"Text": "└", "ID": "BTN_BOT_LEFT"}),
                ui.Button({"Text": "┴", "ID": "BTN_BOT_CENTER"}),
                ui.Button({"Text": "┘", "ID": "BTN_BOT_RIGHT"}),
            ]),
        ]),
    ])

#

# Collect ui items.
itm = dlg.GetItems()


# The window was closed.
def _func(ev):
    disp.ExitLoop()
dlg.On.MyWin.Close = _func


# GUI element based event functions.
def _func(ev):
    comp.StartUndo("Move Anchor Point")
    
    move_anchor_point(ev['who'])
    comp.EndUndo(True)
dlg.On.BTN_TOP_LEFT.Clicked = _func
dlg.On.BTN_TOP_CENTER.Clicked = _func
dlg.On.BTN_TOP_RIGHT.Clicked = _func
dlg.On.BTN_MID_LEFT.Clicked = _func
dlg.On.BTN_MID_CENTER.Clicked = _func
dlg.On.BTN_MID_RIGHT.Clicked = _func
dlg.On.BTN_BOT_LEFT.Clicked = _func
dlg.On.BTN_BOT_CENTER.Clicked = _func
dlg.On.BTN_BOT_RIGHT.Clicked = _func


# Open the dialog.
dlg.Show()
disp.RunLoop()
dlg.Hide()