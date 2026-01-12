"""
ar_Stack

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Stack
Version: 1.1.0
Description-US: Stack selected tools.

Written for Blackmagic Design Fusion Studio 19.0.3 build 3.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.1.0 (18.09.2025) - Combined StackHorizontally and StackVertically scripts into this one script.
1.0.0 (17.09.2025) - Initial release.
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


def stack_horizontally(valign: str) -> None:
    """"Stack selected tools horizontally, based on node positions in Flow."""

    tools = comp.GetToolList(True).values()
    flow = comp.CurrentFrame.FlowView
    
    tool_data = []
    default_width = 1920
    default_height = 1080

    for tool in tools:
        tool_width = tool.GetAttrs("TOOLI_ImageWidth") or default_width
        tool_height = tool.GetAttrs("TOOLI_ImageHeight") or default_height
        x, y = flow.GetPosTable(tool).values()

        tool_data.append({
            "tool": tool,
            "x": x,
            "y": y,
            "tool_width": tool_width,
            "tool_height": tool_height
        })

    if not tool_data:
        print("No selected tools.")
        return
    
    tool_data.sort(key=lambda t: t["x"])
    total_width = sum(t["tool_width"] for t in tool_data)
    max_height = max(t["tool_height"] for t in tool_data)

    main_tool = tool_data[0]
    multimerge_node = comp.AddTool("MultiMerge", main_tool["x"]+4, main_tool["y"]+4)
    layer_index = 1
    prev_step = 0

    for i, item in enumerate(tool_data):
        tool = item["tool"]

        if i == 0:
            multimerge_node.Background = tool.Output
        else:
            step_x = interpolate(0.5, 0, main_tool["tool_width"], 0, item["tool_width"])
            step_y = interpolate(0.5, 0, main_tool["tool_height"], 0, item["tool_height"])
            
            pos_x = interpolate(1, 0, 1, 0.5, 1 + step_x + prev_step)

            if valign == "Top":
                pos_y = interpolate(1, 0, 1, 0.5, 1 - step_y)

            elif valign == "Middle":
                pos_y = interpolate(1, 0, 1, 0.5, 0.5)

            elif valign == "Bottom":
                pos_y = interpolate(1, 0, 1, 0.5, step_y)

            multimerge_node.ConnectInput(f"Layer{layer_index}.Foreground", tool.Output)
            multimerge_node.SetInput(f"Layer{layer_index}.Center", {1: pos_x, 2: pos_y})
            
            layer_index += 1

            prev_step += (step_x * 2)

    crop_node = comp.AddTool("Crop", main_tool["x"]+5, main_tool["y"]+4)
    crop_node.SetInput("XSize", total_width)
    crop_node.SetInput("YSize", max_height)
    
    if valign == "Top":
        crop_node.SetInput("YOffset", -(max_height - main_tool["tool_height"]))
    elif valign == "Middle":
        crop_node.SetInput("YOffset", -(max_height - main_tool["tool_height"]) / 2)
    elif valign == "Bottom":
        pass
    
    crop_node.SetInput("KeepAspect", 0)
    crop_node.SetInput("KeepCentered", 0)
    crop_node.SetInput("ChangePixelAspect", 0)
    crop_node.SetInput("ClippingMode", "Frame")

    crop_node.Input = multimerge_node.Output
    

def stack_vertically(align: str) -> None:
    """"Stack selected tools vertically, based on node positions in Flow."""

    tools = comp.GetToolList(True).values()
    flow = comp.CurrentFrame.FlowView
    
    tool_data = []
    default_width = 1920
    default_height = 1080

    for tool in tools:
        tool_width = tool.GetAttrs("TOOLI_ImageWidth") or default_width
        tool_height = tool.GetAttrs("TOOLI_ImageHeight") or default_height
        x, y = flow.GetPosTable(tool).values()

        tool_data.append({
            "tool": tool,
            "x": x,
            "y": y,
            "tool_width": tool_width,
            "tool_height": tool_height
        })

    if not tool_data:
        print("No selected tools.")
        return
    
    tool_data.sort(key=lambda t: t["y"], reverse=True)
    total_height = sum(t["tool_height"] for t in tool_data)
    max_width = max(t["tool_width"] for t in tool_data)

    main_tool = tool_data[0]
    multimerge_node = comp.AddTool("MultiMerge", main_tool["x"]+4, main_tool["y"]+4)
    layer_index = 1
    prev_step = 0

    for i, item in enumerate(tool_data):
        tool = item["tool"]

        if i == 0:
            multimerge_node.Background = tool.Output
        else:
            step_x = interpolate(0.5, 0, main_tool["tool_width"], 0, item["tool_width"])
            step_y = interpolate(0.5, 0, main_tool["tool_height"], 0, item["tool_height"])
            
            pos_y = interpolate(1, 0, 1, 0.5, 1 + step_y + prev_step)

            if align == "Right":
                pos_x = interpolate(1, 0, 1, 0.5, 1 - step_x)

            elif align == "Center":
                pos_x = interpolate(1, 0, 1, 0.5, 0.5)

            elif align == "Left":
                pos_x = interpolate(1, 0, 1, 0.5, step_x)

            multimerge_node.ConnectInput(f"Layer{layer_index}.Foreground", tool.Output)
            multimerge_node.SetInput(f"Layer{layer_index}.Center", {1: pos_x, 2: pos_y})
            
            layer_index += 1

            prev_step += (step_y * 2)


    crop_node = comp.AddTool("Crop", main_tool["x"]+5, main_tool["y"]+4)
    crop_node.SetInput("XSize", max_width)
    crop_node.SetInput("YSize", total_height)
    
    if align == "Right":
        crop_node.SetInput("XOffset", -(max_width - main_tool["tool_width"]))
    elif align == "Center":
        crop_node.SetInput("XOffset", -(max_width - main_tool["tool_width"]) / 2)
    elif align == "Left":
        pass
    
    crop_node.SetInput("KeepAspect", 0)
    crop_node.SetInput("KeepCentered", 0)
    crop_node.SetInput("ChangePixelAspect", 0)
    crop_node.SetInput("ClippingMode", "Frame")

    crop_node.Input = multimerge_node.Output


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


gui_geo = gui_geometry(250, 150, 0.5, 0.5)


# GUI 
ui   = fusion.UIManager
disp = bmd.UIDispatcher(ui)
dlg  = disp.AddWindow({"WindowTitle": "Stack",
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
            ui.HGroup(
            [
                ui.Label({"Text": "Method:", "ID": "Label_Method", "Weight": 0.1}),
                ui.ComboBox({"ID": "Combobox_Method", "Weight": 0.9}),

            ]),

            ui.HGroup(
            [
                ui.Label({"Text": "Valign:", "ID": "Label_Valign", "Weight": 0.1}),
                ui.ComboBox({"ID": "Combobox_Valign", "Weight": 0.9}),

            ]),

            ui.HGroup(
            [
                ui.Label({"Text": "Align:", "ID": "Label_Align", "Weight": 0.1}),
                ui.ComboBox({"ID": "Combobox_Align", "Weight": 0.9}),

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

# Add combobox items.
itm['Combobox_Method'].AddItem("Horizontally")
itm['Combobox_Method'].AddItem("Vertically")

itm['Combobox_Align'].AddItem("Left")
itm['Combobox_Align'].AddItem("Center")
itm['Combobox_Align'].AddItem("Right")

itm['Combobox_Valign'].AddItem("Top")
itm['Combobox_Valign'].AddItem("Middle")
itm['Combobox_Valign'].AddItem("Bottom")

def combo_method_changed(ev):
    selected_index = itm['Combobox_Method'].CurrentIndex
    itm['Combobox_Align'].Enabled = (selected_index == 1)
    itm['Combobox_Valign'].Enabled = (selected_index == 0)
dlg.On.Combobox_Method.CurrentIndexChanged = combo_method_changed

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

# Stack.
def _func(ev):
    comp.StartUndo("Stack Horizontally")
    comp.Lock()  # Put the composition to lock mode, so it won't open dialogs.

    
    align = itm['Combobox_Align'].CurrentText
    valign = itm['Combobox_Valign'].CurrentText
    method = itm['Combobox_Method'].CurrentIndex
    if method == 0:
        stack_horizontally(valign)
    else:
        stack_vertically(align)

    comp.Unlock()
    comp.EndUndo(True)
dlg.On.Button_Ok.Clicked = _func


# Open the dialog.
dlg.Show()
disp.RunLoop()
dlg.Hide()