"""
AR_GetGridWarp

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: GetGridWarp
Version: 1.0.0
Description-US:

Written for Blackmagic Design Fusion Studio 19.1.4 build 6.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.0.0 (01.04.2025) - Initial realease.
"""
# Libraries
import os


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()


# Functions
def get_gridwarp_points(gridwarp) -> list:
    """."""

    # Tracker points.
    gridwarp_points_list = []

    gridwarp_inputs = gridwarp.GetInputList().values()
    for input in gridwarp_inputs:
        input_name = input.Name

        if input_name.startswith("Point "):
            gridwarp_points_list.append(input_name)

    # Published grid warp data.
    # GridWarp[i]Point[j].X
    # GridWarp[i]Point[j].Y

    return gridwarp_points_list


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
dlg  = disp.AddWindow({"WindowTitle": "Tracker Thing",
                       "ID": "MyWin",
                       "Geometry": [gui_geo['x'], gui_geo['y'], gui_geo['width'], gui_geo['height']],
                       },
    [
        ui.VGroup({"Spacing": 5,},
        [
            # GUI elements.

            # Select folder path.
            ui.HGroup(
            [
                ui.Label({"Text": "Tracker", "ID": "Label_Tracker", "Weight": 0.1}),
                ui.ComboBox(
                    {
                        "ID": "ComboBox_Options",
                        "Weight": 0.7,
                    }
                ),
            ]),

            # Import and Cancel buttons.
            ui.HGroup(
            [
                ui.Button({"Text": "Import", "ID": "BTN_Merge", "Weight": 0.5}),
                ui.Button({"Text": "Cancel", "ID": "BTN_Cancel", "Weight": 0.5}),
            ]),
        ]),
    ])

"""
# Collect ui items.
itm = dlg.GetItems()

# Populate combobox with tracker points.
active_tool = comp.ActiveTool()
if active_tool.ID == "Tracker":
    tracker_points = get_tracker_points(active_tool)

    combo = itm['ComboBox_Options']
    for tracker_point in tracker_points:
        combo.AddItem(tracker_point)
else:
    pass

# The window was closed.
def _func(ev):
    disp.ExitLoop()
dlg.On.MyWin.Close = _func
dlg.On.BTN_Cancel.Clicked = _func


# Open the dialog.
dlg.Show()
disp.RunLoop()
dlg.Hide()
"""
get_gridwarp_points(comp.ActiveTool())