"""
AR_AlignNodes

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Align Nodes
Version: 1.1.0
Description-US: Align selected nodes.

Written for Blackmagic Design Fusion Studio 19.0 build 59.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.2.0 (28.02.2025) - Added rotate buttons. Also added pivot point handling when activetool is selected.
1.1.0 (13.02.2025) - Added flip buttons.
1.0.1 (25.09.2024) - Modified code to follow more PEP 8 recommendations.
1.0.0 (02.09.2024) - Initial realease.
"""
# Libraries
import math


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()


# Functions     
def align_nodes(direction: str, gap: int) -> None:
    """Aligns selected nodes to the desired direction with a given gap.
    If an active tool is selected, it is used as the origin point for alignment.
    Otherwise, the outermost node in the specified direction is used as the pivot."""

    flow = comp.CurrentFrame.FlowView
    tools = comp.GetToolList(True).values()
    collected_nodes = []

    active_tool = comp.ActiveTool

    if active_tool:
        # Use active tool's position as the origin point.
        origin_x, origin_y = flow.GetPosTable(active_tool).values()
    else:
        # Determine the pivot point based on the direction.
        if direction == "Button_Right":
            # Select the node with the smallest x (leftmost).
            origin_x = min(flow.GetPosTable(tool)[1] for tool in tools)
            origin_y = [flow.GetPosTable(tool)[2] for tool in tools if flow.GetPosTable(tool)[1] == origin_x][0]
        elif direction == "Button_Left":
            # Select the node with the largest x (rightmost).
            origin_x = max(flow.GetPosTable(tool)[1] for tool in tools)
            origin_y = [flow.GetPosTable(tool)[2] for tool in tools if flow.GetPosTable(tool)[1] == origin_x][0]
        elif direction == "Button_Up":
            # Select the node with the largest y (topmost).
            origin_y = max(flow.GetPosTable(tool)[2] for tool in tools)
            origin_x = [flow.GetPosTable(tool)[1] for tool in tools if flow.GetPosTable(tool)[2] == origin_y][0]
        elif direction == "Button_Down":
            # Select the node with the smallest y (bottommost).
            origin_y = min(flow.GetPosTable(tool)[2] for tool in tools)
            origin_x = [flow.GetPosTable(tool)[1] for tool in tools if flow.GetPosTable(tool)[2] == origin_y][0]

    # Collect node positions.
    for tool in tools:
        x, y = flow.GetPosTable(tool).values()
        collected_nodes.append([tool, x, y])

    sortedByX = []
    sortedByY = []

    if direction == "Button_Right":
        sortedByX = sorted(collected_nodes, key=lambda x: x[1], reverse=False)
        val = origin_x
        for i, item in enumerate(sortedByX):
            x = val
            y = sortedByX[0][2]
            flow.SetPos(item[0], x, y)
            val = val + gap

    if direction == "Button_Left":
        sortedByX = sorted(collected_nodes, key=lambda x: x[1], reverse=True)
        val = origin_x
        for i, item in enumerate(sortedByX):
            x = val
            y = sortedByX[0][2]
            flow.SetPos(item[0], x, y)
            val = val - gap

    if direction == "Button_Up":
        sortedByY = sorted(collected_nodes, key=lambda x: x[2], reverse=True)
        val = origin_y
        for i, item in enumerate(sortedByY):
            x = sortedByY[0][1]
            y = val
            flow.SetPos(item[0], x, y)
            val = val - gap

    if direction == "Button_Down":
        sortedByY = sorted(collected_nodes, key=lambda x: x[2], reverse=False)
        val = origin_y
        for i, item in enumerate(sortedByY):
            x = sortedByY[0][1]
            y = val
            flow.SetPos(item[0], x, y)
            val = val + gap


def flip_nodes(direction: str) -> None:
    """Flips selected nodes. If an active tool is selected, it is used as the pivot point. 
    Otherwise, the average center of the selected nodes is used."""
    
    flow = comp.CurrentFrame.FlowView
    tools = comp.GetToolList(True).values()

    # Get active tool, if available.
    active_tool = comp.ActiveTool
    
    if active_tool:
        # Use active tool's position as pivot point.
        pivot_x, pivot_y = flow.GetPosTable(active_tool).values()
    else:
        # Calculate the average center of all selected nodes.
        min_x = min(flow.GetPosTable(tool)[1] for tool in tools)
        max_x = max(flow.GetPosTable(tool)[1] for tool in tools)
        pivot_x = (min_x + max_x) / 2

        min_y = min(flow.GetPosTable(tool)[2] for tool in tools)
        max_y = max(flow.GetPosTable(tool)[2] for tool in tools)
        pivot_y = (min_y + max_y) / 2
    
    # Flip all selected nodes around the pivot point.
    for tool in tools:
        pos = flow.GetPosTable(tool)
        if direction == "Button_Flip_H":
            # Flip horizontally using pivot_x.
            new_x = pivot_x - (pos[1] - pivot_x)
            flow.SetPos(tool, new_x, pos[2])

        elif direction == "Button_Flip_V":
            # Flip vertically using pivot_y.
            new_y = pivot_y - (pos[2] - pivot_y)
            flow.SetPos(tool, pos[1], new_y)


def rotate_nodes(angle: float) -> None:
    """Rotates selected nodes around the active tool's position by the given angle (in degrees).
       If no active tool is selected, uses the average center of all selected nodes."""
    
    flow = comp.CurrentFrame.FlowView
    tools = comp.GetToolList(True).values()
    
    # Get active tool, if available.
    active_tool = comp.ActiveTool
    
    if active_tool:
        # Use active tool's position as pivot point.
        pivot_x, pivot_y = flow.GetPosTable(active_tool).values()
    else:
        # Calculate the average center of all selected nodes.
        sum_x = 0
        sum_y = 0
        count = len(tools)
        
        for tool in tools:
            x, y = flow.GetPosTable(tool).values()
            sum_x += x
            sum_y += y
        
        pivot_x = sum_x / count
        pivot_y = sum_y / count
    
    # Rotate all selected nodes around the pivot point.
    for tool in tools:
        x, y = flow.GetPosTable(tool).values()
        
        # Calculate offset from pivot point.
        offset_x = x - pivot_x
        offset_y = y - pivot_y
        
        # Convert angle to radians.
        angle_rad = math.radians(angle)
        
        # Apply 90-degree rotation matrix (clockwise).
        new_x = pivot_x + (offset_x * math.cos(angle_rad) - offset_y * math.sin(angle_rad))
        new_y = pivot_y + (offset_x * math.sin(angle_rad) + offset_y * math.cos(angle_rad))
        
        # Set the new position for the node.
        flow.SetPos(tool, new_x, new_y)


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
dlg  = disp.AddWindow({"WindowTitle": "Align Nodes",
                       "ID": "MyWin",
                       "WindowFlags": {
                          "Window": True,
                          "CustomizeWindowHint": True,
                          "WindowMinimizeButtonHint": False,
                          "WindowMaximizeButtonHint": False,
                          "WindowCloseButtonHint": True,
                        },
                       "Geometry": [gui_geo['x'], gui_geo['y'], gui_geo['width'], gui_geo['height']]
                       },
    [
        ui.VGroup({"Spacing": 5},
        [
            ui.HGroup([
                ui.Button({"Text": "<", "ID": "Button_Left"}),
                ui.Button({"Text": ">", "ID": "Button_Right"}),
            ]),
            ui.HGroup([
                ui.Button({"Text": "^", "ID": "Button_Up"}),
                ui.Button({"Text": "v", "ID": "Button_Down"}),
            ]),
            ui.HGroup([
                ui.Label({"ID": "Label_Gap", "Text": "Gap:"}),
                ui.SpinBox({"ID": "Spinbox_Gap", "Minimum": 1, "Maximum": 1000000, "Value": 1}),
            ]),
            ui.HGroup([
                ui.Button({"Text": "Flip H", "ID": "Button_Flip_H"}),
                ui.Button({"Text": "Flip V", "ID": "Button_Flip_V"}),
            ]),
            ui.HGroup([
                ui.Button({"Text": "Rotate CCW", "ID": "Button_Rotate_CCW"}),
                ui.Button({"Text": "Rotate CW", "ID": "Button_Rotate_CW"}),
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
    align_nodes(ev['who'], itm['Spinbox_Gap'].Value)
    comp.EndUndo(True)
dlg.On.Button_Left.Clicked = _func
dlg.On.Button_Right.Clicked = _func
dlg.On.Button_Up.Clicked = _func
dlg.On.Button_Down.Clicked = _func


def _func(ev):
    comp.StartUndo("Flip nodes")
    flip_nodes(ev['who'])
    comp.EndUndo(True)
dlg.On.Button_Flip_H.Clicked = _func
dlg.On.Button_Flip_V.Clicked = _func


def _func(ev):
    comp.StartUndo("Rotate nodes")
    if ev['who'] == "Button_Rotate_CW":
        rotate_nodes(90)
    elif ev['who'] == "Button_Rotate_CCW":
        rotate_nodes(-90)
    comp.EndUndo(True)
dlg.On.Button_Rotate_CW.Clicked = _func
dlg.On.Button_Rotate_CCW.Clicked = _func


# Open the dialog.
dlg.Show()
disp.RunLoop()
dlg.Hide()