"""
AR_2DTrackerTo3DSpace

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: 2D Tracker To 3D Space
Version: 1.1.0
Description-US: Creates a setup that converts active 2D tracker's point to 3D space.

Written for Blackmagic Design Fusion Studio 19.1.4 build 6.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.1.0 (04.04.2025) - Added GUI to select the tracker point.
1.0.0 (06.10.2024) - Initial realease.
"""
# Libraries
import re


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


def tracker_to_3d_space(tracker, tracker_id, aov_type) -> None:
    """Creates a setup that converts 2D tracker data to 3D space."""

    # Aov types.
    # 0 = Vertical (supported).
    # 1 = Horizontal (supported).
    # 2 = Diagonal.

    # Camera3D.
    camera3d = comp.AddTool("Camera3D")
    camera3d_name = camera3d.Name

    # Shape3D.
    shape3d = comp.AddTool("Shape3D")
    shape3d_name = shape3d.Name
    shape3d.SetInput("Shape", "SurfaceSphereInputs")

    if aov_type == "Vertical":
        camera3d.SetInput("AovType", 0.0)
        shape3d.Transform3DOp.Translate.X.SetExpression(f"({tracker.Name}.TrackedCenter{tracker_id}.X-0.5) * -(Transform3DOp.Translate.Z * (2 * math.tan({camera3d_name}.AoV * (math.pi / 180) * 0.5) * ({camera3d_name}.ApertureW / {camera3d_name}.ApertureH)))")
        shape3d.Transform3DOp.Translate.Y.SetExpression(f"({tracker.Name}.TrackedCenter{tracker_id}.Y-0.5) * -(Transform3DOp.Translate.Z * (math.tan({camera3d_name}.AoV * (math.pi / 180) * 0.5) * 2.0))")

    elif aov_type == "Horizontal":
        camera3d.SetInput("AovType", 1.0)
        shape3d.Transform3DOp.Translate.X.SetExpression(f"({tracker.Name}.TrackedCenter{tracker_id}.X-0.5) * -(Transform3DOp.Translate.Z * (math.tan({camera3d_name}.AoV * (math.pi / 180) * 0.5) * 2.0))")
        shape3d.Transform3DOp.Translate.Y.SetExpression(f"({tracker.Name}.TrackedCenter{tracker_id}.Y-0.5) * -(Transform3DOp.Translate.Z * (2 * math.atan(math.tan({camera3d_name}.AoV * (math.pi / 180) / 2) / ({camera3d_name}.ApertureW / {camera3d_name}.ApertureH))))")

    shape3d.SetInput("Transform3DOp.Translate.Z", -10)
    
    # Connect nodes.
    camera3d.SceneInput = shape3d.Output

    # Select nodes.
    flow = comp.CurrentFrame.FlowView
    flow.Select()
    flow.Select(shape3d, True)
    flow.Select(camera3d, True)

    return None


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

        if output.Name.startswith("IntelliTrack ") or output.Name.startswith("Point "):
            tracker_point_name = output.Name.split(":")[0]
            add_tracker_point(tracker_point_name)

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


gui_geo = gui_geometry(325, 100, 0.5, 0.5)


# GUI
ui   = fusion.UIManager
disp = bmd.UIDispatcher(ui)
dlg  = disp.AddWindow({"WindowTitle": "Tracker Thing",
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
            # GUI elements.

            # Select folder path.
            ui.HGroup(
            [
                ui.Label({"Text": "Tracker", "ID": "Label_Tracker", "Weight": 0.1}),
                ui.ComboBox(
                    {
                        "ID": "ComboBox_Tracker",
                        "Weight": 0.7,
                    }
                ),
            ]),

            ui.HGroup(
            [
                ui.Label({"Text": "Angle of View Type", "ID": "Label_AovType", "Weight": 0.1}),
                ui.ComboBox(
                    {
                        "ID": "ComboBox_AovType",
                        "Weight": 0.7,
                    }
                ),
            ]),

            # Import and Cancel buttons.
            ui.HGroup(
            [
                ui.Button({"Text": "Ok", "ID": "Button_Ok", "Weight": 0.5}),
                ui.Button({"Text": "Cancel", "ID": "Button_Cancel", "Weight": 0.5}),
            ]),
        ]),
    ])


# Collect ui items.
itm = dlg.GetItems()

# Get tools.
tools = comp.GetToolList(True).values()

tracker = None

try:
    tool = comp.ActiveTool()
    if tool.ID == "Tracker":
        tracker = tool
except:
    if tracker is None:
        print("Tracker not found.")
    else:
        print("Something went wrong.")

combo_aovtype = itm['ComboBox_AovType']
combo_aovtype.AddItem("Vertical")
combo_aovtype.AddItem("Horizontal")

# Populate combobox with tracker points.
if tracker is not None:
    tracker_points = get_tracker_points(tracker)
    combo_tracker = itm['ComboBox_Tracker']
    for tracker_point in tracker_points:
        combo_tracker.AddItem(tracker_point)

    # Keys are pressed.
    def _func(ev):
        key_modifiers = get_key_modifiers(ev)
        if CTRL in key_modifiers and ev['Key'] == 81:  # Ctrl + Q.
            disp.ExitLoop()
            dlg.Hide()
    dlg.On.MyWin.KeyPress = _func

    # The window was closed.
    def _func(ev):
        disp.ExitLoop()
    dlg.On.MyWin.Close = _func
    dlg.On.Button_Cancel.Clicked = _func

    # Ok.
    def _func(ev):
        selected_tracker = combo_tracker.CurrentText
        selected_tracker_number = "".join(re.findall(r"\d+", selected_tracker))
        aov_type = combo_aovtype.CurrentText
        comp.StartUndo("Tracker to 3D space")
        tracker_to_3d_space(tracker, selected_tracker_number, aov_type)
        comp.EndUndo(True)
        disp.ExitLoop()
    dlg.On.Button_Ok.Clicked = _func

    # Open the dialog.
    dlg.Show()
    disp.RunLoop()
    dlg.Hide()