"""
AR_MoveNodes

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Move Nodes
Version: 1.0.0
Description-US: Moves selected node(s).

Written for Blackmagic Design Fusion Studio 19.0 build 59.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.0.0 (05.02.2025) - Initial realease.
"""
# Libraries
import os


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()


# Functions     
def move_nodes(direction, amount) -> None:
    """Moves selected nodes to wanted direction with given amount."""

    flow = comp.CurrentFrame.FlowView
    tools = comp.GetToolList(True).values()

    for tool in tools:
        x, y = flow.GetPosTable(tool).values() # Get node's position

        if direction == "RIGHT":
            flow.SetPos(tool, x+amount, y)

        if direction == "LEFT":
            flow.SetPos(tool, x-amount, y)

        if direction == "UP":
            flow.SetPos(tool, x, y-amount)

        if direction == "DOWN":
            flow.SetPos(tool, x, y+amount)


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


gui_geo = gui_geometry(100, 125, 0.5, 0.5)


# GUI 
ui   = fusion.UIManager
disp = bmd.UIDispatcher(ui)
dlg  = disp.AddWindow({"WindowTitle": "Move Nodes",
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
                ui.Button({"Text": "^", "ID": "BTN_UP"}),
            ]),
            ui.HGroup([
                ui.Button({"Text": "<", "ID": "BTN_LEFT"}),
                ui.Button({"Text": ">", "ID": "BTN_RIGHT"}),
            ]),
            ui.HGroup([
                ui.Button({"Text": "v", "ID": "BTN_DOWN"}),
            ]),
            ui.HGroup([
                ui.Label({"ID": "Label", "Text": "Amount:"}),
                ui.SpinBox({"ID": "Amount", "Minimum": 1.0, "Maximum": 1000000.0, "Value": 1.0}),
            ]),
        ]),
    ])


# Collect ui items.
itm = dlg.GetItems()


# The window was closed.
def _func(ev):
    disp.ExitLoop()
dlg.On.MyWin.Close = _func


# GUI element based event functions.
def _func(ev):
    comp.StartUndo("Align nodes")
    move_nodes("LEFT", itm['Amount'].Value)
    comp.EndUndo(True)
dlg.On.BTN_LEFT.Clicked = _func


def _func(ev):
    comp.StartUndo("Align nodes")
    move_nodes("RIGHT", itm['Amount'].Value)
    comp.EndUndo(True)
dlg.On.BTN_RIGHT.Clicked = _func


def _func(ev):
    comp.StartUndo("Align nodes")
    move_nodes("UP", itm['Amount'].Value)
    comp.EndUndo(True)
dlg.On.BTN_UP.Clicked = _func


def _func(ev):
    comp.StartUndo("Align nodes")
    move_nodes("DOWN", itm['Amount'].Value)
    comp.EndUndo(True)
dlg.On.BTN_DOWN.Clicked = _func


# Open the dialog.
dlg.Show()
disp.RunLoop()
dlg.Hide()