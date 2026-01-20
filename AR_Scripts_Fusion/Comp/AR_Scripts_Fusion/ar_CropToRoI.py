"""
ar_CropToRoI

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Crop to RoI
Version: 1.1.0
Description-US: Crops the canvas based on the RoI (region of interest).

Written for Blackmagic Design Fusion Studio 19.0.3 build 3.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.1.0 (29.08.2025) - Added GUI to select which view to crop, instead of using active viewport.
1.0.0 (12.03.2025) - Initial realease.
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


def interpolate(value: float, x1: float, x2: float, y1: float, y2: float):
    """Perform linear interpolation for value between (x1,y1) and (x2,y2)."""

    return ((y2 - y1) * value + x2 * y1 - x1 * y2) / (x2 - x1)


def crop_to(tool, values) -> any:
    """Creates a crop node and crops with given values."""
    
    x1 = values['left']
    x2 = values['right']
    y1 = values['bot']
    y2 = values['top']

    flow = comp.CurrentFrame.FlowView
    x, y = flow.GetPosTable(tool).values()
    crop_node = comp.AddTool("Crop", x+1, y+1)
    crop_node.SetAttrs({'TOOLS_Name': "CropToRoI"})

    crop_node.SetInput("XOffset", x1)
    crop_node.SetInput("YOffset", y1)

    new_width = x2-x1
    new_height = y2-y1

    crop_node.SetInput("XSize", new_width)
    crop_node.SetInput("YSize", new_height)

    crop_node.SetInput("KeepAspect", 0)
    crop_node.SetInput("KeepCentered", 0)
    crop_node.SetInput("ChangePixelAspect", 0)
    crop_node.SetInput("ClippingMode", "Frame")

    return crop_node


def get_region_data(view, tool) -> dict:
    """Gets region data of the currently active window.
    Returns region points in pixels (based on the given tool's image dimensions).
    """

    width = tool.GetAttrs("TOOLI_ImageWidth")
    height = tool.GetAttrs("TOOLI_ImageHeight")

    try:
        if view == "Left A":
            region = comp.GetPrefs()['Comp']['Views']['LeftView']['Viewer']['Region']
        elif view == "Left B":
            region = comp.GetPrefs()['Comp']['Views']['LeftView']['SideB']['Viewer']['Region']
        elif view == "Right A":
            region = comp.GetPrefs()['Comp']['Views']['RightView']['Viewer']['Region']
        elif view == "Right B":
            region = comp.GetPrefs()['Comp']['Views']['RightView']['SideB']['Viewer']['Region']

        roi_left = region['Left']
        roi_bot = region['Bottom']
        roi_right = region['Right']
        roi_top = region['Top']

        region_values = {
            'left': int(interpolate(roi_left, 0, 1, 0, width)),
            'top': int(interpolate(roi_top, 0, 1, 0, height)),
            'right': int(interpolate(roi_right, 0, 1, 0, width)),
            'bot': int(interpolate(roi_bot, 0, 1, 0, height))
        }

        return region_values

    except Exception:
        print("No region found.")
        return None
    

def keep_in_place(tool, region_values) -> any:
    """Creates a transform node that keeps source in place with given values."""

    x1 = region_values['left']
    x2 = region_values['right']
    y1 = region_values['bot']
    y2 = region_values['top']

    width = tool.GetAttrs("TOOLI_ImageWidth")
    height = tool.GetAttrs("TOOLI_ImageHeight")

    center_x = (x1 + x2) / 2
    center_y = (y1 + y2) / 2

    remapped_center_x = (center_x - 0) / (width - 0)
    remapped_center_y = (center_y - 0) / (height - 0)

    transform_x = 0.5 + ((remapped_center_x - 0.5) * (width / (x2-x1)))
    transform_y = 0.5 + ((remapped_center_y - 0.5) * (height / (y2-y1)))

    flow = comp.CurrentFrame.FlowView
    x, y = flow.GetPosTable(tool).values()
    transform_node = comp.AddTool("Transform", x+2, y+1)
    transform_node.SetInput("Center", {1: transform_x, 2: transform_y, 3: 0.0})

    return transform_node


def crop_to_roi(view) -> None:
    """Crops the canvas to the region of interest.
    Creates also transform node that keeps cropped area in place.
    """

    try:
        tool = comp.ActiveTool()
    
    except Exception:
        print("No active node found!")
        return None
    
    region_values = get_region_data(view, tool)
    
    if region_values == None:
        return None

    crop_node = crop_to(tool, region_values)
    transform_node = keep_in_place(tool, region_values)

    flow = comp.CurrentFrame.FlowView
    x, y = flow.GetPosTable(tool).values()
    merge_node = comp.AddTool("Merge", x+2, y)

    output_port = tool.GetOutputList()[1]
    crop_node.Input = output_port
    transform_node.Input = crop_node.Output
    crop_node.Input = output_port
    merge_node.Background = output_port
    merge_node.Foreground = transform_node.Output


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
dlg  = disp.AddWindow({"WindowTitle": "Crop to RoI",
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
                ui.Label({"Text": "Viewport", "ID": "Label_Viewport", "Weight": 0.1}),
                ui.ComboBox(
                    {
                        "ID": "ComboBox_View",
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

combo_view = itm['ComboBox_View']
combo_view.AddItem("Left A")
combo_view.AddItem("Left B")
combo_view.AddItem("Right A")
combo_view.AddItem("Right B")

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
    selected_view = combo_view.CurrentText
    comp.Lock()
    comp.StartUndo("Crop to RoI")
    crop_to_roi(selected_view)
    comp.EndUndo(True)
    comp.Unlock()
    disp.ExitLoop()
dlg.On.Button_Ok.Clicked = _func

# Open the dialog.
dlg.Show()
disp.RunLoop()
dlg.Hide()