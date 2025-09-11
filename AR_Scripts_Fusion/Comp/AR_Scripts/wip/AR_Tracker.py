"""
AR_ConnectTrackerToGridWarp

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Connect Tracker to GridWarp
Version: 1.0.0
Description-US: Connects the tracker point to the published grid warp points.

Written for Blackmagic Design Fusion Studio 19.1.4 build 6.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.0.0 (01.04.2025) - Initial realease.
"""
# Libraries
import re


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()


# Functions
def get_gridwarp_points(gridwarp) -> list:
    """Returns published grid warp points as a list."""

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


def get_tracker_points(tracker) -> list:
    """Returns a list of tracker points."""

    # Tracker points.
    tracker_points_list = []
    tracker_points_set = set()

    def add_tracker_point(item):
        if item not in tracker_points_set:
            tracker_points_list.append(item)
            tracker_points_set.add(item)

    tracker_outputs = tracker.GetOutputList().values()
    for output in tracker_outputs:

        if output.Name == "Unsteady Position":
            print(tracker.GetInput("Unsteady Position")[comp.CurrentTime])

        if output.Name.startswith("IntelliTrack ") or output.Name.startswith("Point "):
            tracker_point_name = output.Name.split(":")[0]
            add_tracker_point(tracker_point_name)

    # Tracaker data.
    # Tracker[i]TrackerCenter[j].X
    # Tracker[i]TrackerCenter[j].Y
    # Tracker[i]XOffset[j]
    # Tracker[i]YOffset[j]

    return tracker_points_list


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
                ui.Button({"Text": "Connect", "ID": "BTN_Connect", "Weight": 0.5}),
                ui.Button({"Text": "Cancel", "ID": "BTN_Cancel", "Weight": 0.5}),
            ]),
        ]),
    ])


# Collect ui items.
itm = dlg.GetItems()

# Get tools.
tools = comp.GetToolList(True).values()

tracker = None
gridwarp = None

for tool in tools:
    if tool.ID == "Tracker":
        tracker = tool
    if tool.ID == "GridWarp":
        gridwarp = tool

if tracker is None:
    print("Tracker not found.")
if gridwarp is None:
    print("GridWarp not found.")

# Populate combobox with tracker points.

if tracker is not None and gridwarp is not None:
    tracker_points = get_tracker_points(tracker)
    combo = itm['ComboBox_Options']
    for tracker_point in tracker_points:
        combo.AddItem(tracker_point)


    # The window was closed.
    def _func(ev):
        disp.ExitLoop()
    dlg.On.MyWin.Close = _func
    dlg.On.BTN_Cancel.Clicked = _func


    # Connect.
    def _func(ev):

        gridwarp_points = get_gridwarp_points(gridwarp)

        selected_tracker = combo.CurrentText
        selected_tracker_number = "".join(re.findall(r"\d+", selected_tracker))
 
        tracker_pos = tracker.TrackedCenter1[comp.CurrentTime]

        tracker_x = tracker_pos[1]
        tracker_y = tracker_pos[2]

        #gridwarp.Point0.SetExpression("0")
        
        for gridwarp_point in gridwarp_points:
            point_num = int(gridwarp_point.replace("Point ", ""))

            #grid_x = gridwarp.Point
            #grid_y = gridwarp

            #gridwarp.Point[point_num].SetExpression(f"Point({current_grid_x} -{tracker_x}+{tracker.Name}{selected_tracker_number}.Center.X,\
            #                                        {current_grid_y}-{tracker_y}+{tracker.Name}{selected_tracker_number}.Center.Y)")

    dlg.On.BTN_Connect.Clicked = _func


    # Open the dialog.
    dlg.Show()
    disp.RunLoop()
    dlg.Hide()

else:
    pass