"""
ar_ResizeCanvas

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Resize Canvas
Version: 1.0.1
Description-US: Resize canvas of the selected tool.

Written for Blackmagic Design Fusion Studio 19.1.3 build 5
Python version 3.10.8 (64-bit)

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp
  
Changelog:
1.0.1 (18.10.2025) - Added error checking.
1.0.0 (25.02.2025) - Initial release.
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

last_selection = None


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


def get_anchors() -> list:
    """Get anchors."""
    
    anchors = ["Button_Top_Left", "Button_Top_Center", "Button_Top_Right",
               "Button_Mid_Left", "Button_Mid_Center", "Button_Mid_Right",
               "Button_Bot_Left", "Button_Bot_Center", "Button_Bot_Right"]
    
    return anchors


def interpolate(value: float, x1: float, x2: float, y1: float, y2: float):
    """Perform linear interpolation for value between (x1,y1) and (x2,y2) """

    return ((y2 - y1) * value + x2 * y1 - x1 * y2) / (x2 - x1)


def get_tool_resolution(tool) -> tuple:
    """Gets the resolution of the given tool and returns it if possible."""

    width = tool.GetAttrs("TOOLI_ImageWidth")
    height = tool.GetAttrs("TOOLI_ImageHeight")

    if (width == None) or (height == None):
        print(f"Couldn't get the resolution data from tool: {tool.Name}")
        return False, False
    else:
        return width, height


def get_merge_data() -> tuple | bool:
    """Gets all important data from the selected merge node."""

    merge_node = comp.ActiveTool()

    if merge_node.ID == "Merge":
        bg_node = merge_node.FindMainInput(1).GetConnectedOutput().GetTool()
        fg_node = merge_node.FindMainInput(2).GetConnectedOutput().GetTool()

        bg_width, bg_height = get_tool_resolution(bg_node)
        if bg_width == None:
            return False

        fg_width, fg_height = get_tool_resolution(fg_node)
        if fg_width == None:
            return False

        return merge_node, bg_node, bg_width, bg_height, fg_node, fg_width, fg_height
    else:
        print("Select Merge node first!")
        return False


def resize_canvas(method: str, new_width: int, new_height: int) -> None:
    """Clears preview windows, also both A and B buffers."""
    
    active_tool = comp.ActiveTool()

    old_width, old_height = get_tool_resolution(active_tool)
    flow = comp.CurrentFrame.FlowView
    x, y = flow.GetPosTable(active_tool).values()
    crop_node = comp.AddTool("Crop", x+1, y)
    crop_node.SetAttrs({'TOOLS_Name': "ResizeCanvas"})
    crop_node.Input = active_tool.GetOutputList()[1]

    if method == "Button_Bot_Left":
        crop_node.SetInput("XOffset", 0)
        crop_node.SetInput("YOffset", 0)
    elif method == "Button_Bot_Center":
        crop_node.SetInput("XOffset", (old_width - new_width) / 2)
        crop_node.SetInput("YOffset", 0)
    elif method == "Button_Bot_Right":
        crop_node.SetInput("XOffset", (old_width - new_width))
        crop_node.SetInput("YOffset", 0)
    elif method == "Button_Mid_Left":
        crop_node.SetInput("XOffset", 0)
        crop_node.SetInput("YOffset", (old_height - new_height) / 2)
    elif method == "Button_Mid_Center":
        crop_node.SetInput("XOffset", (old_width - new_width) / 2)
        crop_node.SetInput("YOffset", (old_height - new_height) / 2)
    elif method == "Button_Mid_Right":
        crop_node.SetInput("XOffset", (old_width - new_width))
        crop_node.SetInput("YOffset", (old_height - new_height) / 2)
    elif method == "Button_Top_Left":
        crop_node.SetInput("XOffset", 0)
        crop_node.SetInput("YOffset", (old_height - new_height))
    elif method == "Button_Top_Center":
        crop_node.SetInput("XOffset", (old_width - new_width) / 2)
        crop_node.SetInput("YOffset", (old_height - new_height))
    elif method == "Button_Top_Right":
        crop_node.SetInput("XOffset", (old_width - new_width))
        crop_node.SetInput("YOffset", (old_height - new_height))

    crop_node.SetInput("XSize", new_width)
    crop_node.SetInput("YSize", new_height)

    crop_node.SetInput("KeepAspect", 0)
    crop_node.SetInput("KeepCentered", 0)
    crop_node.SetInput("ChangePixelAspect", 0)
    crop_node.SetInput("ClippingMode", "Frame")


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
    output_port = fg_node.GetOutputList()[1]
    transform_node.Input = output_port

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


gui_geo = gui_geometry(325, 230, 0.5, 0.5)


# GUI
try:
     width, height = get_tool_resolution(comp.ActiveTool())
except:
    comp_preferences = comp.GetPrefs()
    width = comp_preferences['Comp']['FrameFormat']['Width']
    height = comp_preferences['Comp']['FrameFormat']['Height']

ui   = fusion.UIManager
disp = bmd.UIDispatcher(ui)
dlg  = disp.AddWindow({"WindowTitle": "Resize Canvas",
                       "ID": "MyWin",
                       "WindowFlags": {
                          "Window": True,
                          "CustomizeWindowHint": True,
                          "WindowMinimizeButtonHint": False,
                          "WindowMaximizeButtonHint": False,
                          "WindowCloseButtonHint": True,
                        },
                        "Events": {"Close": True,
                                 "KeyPress": True,
                                 "KeyRelease": True},
                        "Geometry": [gui_geo['x'], gui_geo['y'], gui_geo['width'], gui_geo['height']]
                        },
    [

        ui.VGroup({"Spacing": 5},
        [
            ui.VGroup({"Spacing": 5},
            [
                ui.HGroup([
                    ui.Button({"Text": "┌", "ID": "Button_Top_Left", "Checkable": True}),
                    ui.Button({"Text": "┬", "ID": "Button_Top_Center", "Checkable": True}),
                    ui.Button({"Text": "┐", "ID": "Button_Top_Right", "Checkable": True}),
                ]),
                ui.HGroup([
                    ui.Button({"Text": "├", "ID": "Button_Mid_Left", "Checkable": True}),
                    ui.Button({"Text": "┼", "ID": "Button_Mid_Center", "Checkable": True}),
                    ui.Button({"Text": "┤", "ID": "Button_Mid_Right", "Checkable": True}),
                ]),
                ui.HGroup([
                    ui.Button({"Text": "└", "ID": "Button_Bot_Left", "Checkable": True}),
                    ui.Button({"Text": "┴", "ID": "Button_Bot_Center", "Checkable": True}),
                    ui.Button({"Text": "┘", "ID": "Button_Bot_Right", "Checkable": True}),
                ]),
            ]),
            ui.VGroup({"Spacing": 5},
            [
                ui.HGroup([
                    ui.Button({"Text": "Get Width", "ID": "Button_Get_Width", "Weight": 1}),
                    ui.Button({"Text": "Get Height", "ID": "Button_Get_Height", "Weight": 1}),
                ]),
                ui.HGroup([
                    ui.Label({"Text": "Width", "ID": "Label_Width", "Weight": 0.1}),
                    ui.LineEdit({"ID": "Lineedit_Width", "Text": str(width), "Weight": 1}),
                ]),
                ui.HGroup([
                    ui.Label({"Text": "Height", "ID": "Label_Height", "Weight": 0.1}),
                    ui.LineEdit({"ID": "Lineedit_Height", "Text": str(height), "Weight": 1}),
                ]),

                ui.HGroup([
                    ui.Button({"Text": "Resize", "ID": "Button_ResizeCanvas", "Weight": 1}),
                ]),
            ]),
        ]),
    ])


# Collect ui items
itm = dlg.GetItems()
itm["Button_Mid_Center"].Checked = True


# The window was closed
def _func(ev):
    disp.ExitLoop()
dlg.On.MyWin.Close = _func


# Keys are pressed.
def _func(ev):

    # Set step value.
    step = 1
    key_modifiers = get_key_modifiers(ev)
    if ALT in key_modifiers:
        step = 10
    if SHIFT in key_modifiers:
        step = 100

    if CTRL in key_modifiers and ev['Key'] == 81:  # Ctrl + Q.
        disp.ExitLoop()
        dlg.Hide()

    if ev['Key'] == 16777235:  # Up.
        
        if itm["Lineedit_Width"].HasFocus():
            itm["Lineedit_Width"].Text = str(int(float(itm["Lineedit_Width"].Text))+step)

        if itm["Lineedit_Height"].HasFocus():
            itm["Lineedit_Height"].Text = str(int(float(itm["Lineedit_Height"].Text))+step)

    if ev['Key'] == 16777237:  # Down.
        
        if itm["Lineedit_Width"].HasFocus():
            itm["Lineedit_Width"].Text = str(int(float(itm["Lineedit_Width"].Text))-step)

        if itm["Lineedit_Height"].HasFocus():
            itm["Lineedit_Height"].Text = str(int(float(itm["Lineedit_Height"].Text))-step)

    if ev['Key'] in [16777220, 16777221]:  # Enter.

        if itm["Lineedit_Width"].HasFocus():
            result = eval(itm["Lineedit_Width"].Text)
            itm["Lineedit_Width"].Text = str(result)

        if itm["Lineedit_Height"].HasFocus():
            result = eval(itm["Lineedit_Height"].Text)
            itm["Lineedit_Height"].Text = str(result)
dlg.On.MyWin.KeyPress = _func


# Buttons are pressed.
def _func(ev):
    all_anchors = get_anchors()
    anchors = get_anchors()
    anchors.remove(ev["who"])
    last_selection = ev["who"]
    for anchor in anchors:
        itm[anchor].Checked = False
    if all(not itm[anchor].Checked for anchor in all_anchors):
        itm[last_selection].Checked = True
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
    comp.StartUndo("Resize Canvas")
    anchors = get_anchors()
    for anchor in anchors:
        if itm[anchor].Checked == True:
            result_width = eval(itm["Lineedit_Width"].Text)
            itm["Lineedit_Width"].Text = str(result_width)
            result_height = eval(itm["Lineedit_Height"].Text)
            itm["Lineedit_Height"].Text = str(result_height)
            resize_canvas(itm[anchor].ID, int(result_width), int(result_height))
    comp.EndUndo(True)
dlg.On.Button_ResizeCanvas.Clicked = _func


def _func(ev):
    try:
        active_tool = comp.ActiveTool()
    except Exception:
        print("Select tool first!")
        return None
    width, _ = get_tool_resolution(active_tool)
    itm["Lineedit_Width"].Text = str(width)
dlg.On.Button_Get_Width.Clicked = _func


def _func(ev):
    try:
        active_tool = comp.ActiveTool()
    except Exception:
        print("Select tool first!")
        return None
    _, height = get_tool_resolution(active_tool)
    itm["Lineedit_Height"].Text = str(height)
dlg.On.Button_Get_Height.Clicked = _func


# Open the dialog.
dlg.Show()
disp.RunLoop()
dlg.Hide()