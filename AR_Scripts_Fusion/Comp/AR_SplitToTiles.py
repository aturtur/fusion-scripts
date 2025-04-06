"""
AR_SplitToTiles

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Split To Tiles
Version: 1.0.0
Description-US: Splits the active tool in to tiles by given rows and clomuns.

Written for Blackmagic Design Fusion Studio 19.0.3 build 3
Python version 3.10.8 (64-bit)

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.0.0 (24.03.2025) - Initial release.
"""
# Libraries
import math


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()


# Functions
def split_to_tiles(tool, rows: int, columns: int, join: bool) -> None:
    """Splits the active tool in to tiles by given rows and clomuns."""

    width = tool.GetAttrs("TOOLI_ImageWidth")
    height = tool.GetAttrs("TOOLI_ImageHeight")

    crop_nodes = []
    transform_nodes = []

    flow = comp.CurrentFrame.FlowView
    x, y = flow.GetPosTable(tool).values()

    for i, row in enumerate(range(rows)):
        for j, col in enumerate(range(columns)):
            crop_node = comp.AddTool("Crop", math.floor(x)+1+j, math.floor(y)-i)
            crop_node.SetAttrs({'TOOLS_Name': f"Tile_{i+1}x{j+1}"})
            crop_node.Input = tool.Output

            x_offset = (col * (width // columns))
            y_offset = (row * (height // rows))
            x_size = width // columns
            y_size = height // rows
            
            crop_node.SetInput("XOffset", x_offset)
            crop_node.SetInput("YOffset", y_offset)
            crop_node.SetInput("XSize", x_size)
            crop_node.SetInput("YSize", y_size)
            
            crop_nodes.append(crop_node)

            if join:
                x_size = width / columns
                y_size = height / rows
                x_offset = col * x_size
                y_offset = row * y_size
                x_center = (x_offset + x_size / 2) / width
                y_center = (y_offset + y_size / 2) / height

                transform_x = 0.5 + ((x_center - 0.5) * (width / x_size))
                transform_y = 0.5 + ((y_center - 0.5) * (height / y_size))
                transform_node = comp.AddTool("Transform", math.floor(x)+2+columns-j, math.floor(y)-i)
                transform_node.SetInput("Input", crop_node)
                transform_node.SetInput("Center", {1: transform_x,
                                                   2: transform_y})
                transform_nodes.append(transform_node)
    if join:
        multimerge_node = comp.AddTool("MultiMerge", math.floor(x)+4+columns-j, math.floor(y)+2-i)
        multimerge_node.Background = tool.Output
        for i, transform in enumerate(transform_nodes):
            multimerge_node.ConnectInput(f"Layer{i+1}.Foreground", transform.Output)


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


gui_geo = gui_geometry(250, 140, 0.5, 0.5)


# GUI
ui   = fusion.UIManager
disp = bmd.UIDispatcher(ui)
dlg  = disp.AddWindow({"WindowTitle": "Split To Tiles",
                       "ID": "MyWin",
                       "Geometry": [gui_geo['x'], gui_geo['y'], gui_geo['width'], gui_geo['height']],
                       },
    [
        ui.VGroup({"Spacing": 5},
        [
            # GUI elements.
            ui.HGroup([
                ui.Label({"ID": "Label", "Text": "Rows:"}),
                ui.SpinBox({"ID": "SPN_Rows", "Minimum": 1, "Maximum": 1000000, "Value": 2, "Weight": 1.0}),
            ]),

            ui.HGroup([
                ui.Label({"ID": "Label", "Text": "Columns:"}),
                ui.SpinBox({"ID": "SPN_Columns", "Minimum": 1, "Maximum": 1000000, "Value": 2, "Weight": 1.0}),
            ]),

            ui.HGroup([
                ui.CheckBox({"Text": "Create Join Tiles Setup", "ID": "CHK_Join", "Weight": 1.0}),
            ]),

            ui.VGap(10),
            
            # Add and Cancel buttons.
            ui.HGroup(
            [
                ui.Button({"Text": "Split", "ID": "BTN_Split"}),
                ui.Button({"Text": "Cancel", "ID": "BTN_Cancel"}),
            ]),

        ]),
    ])


# Collect ui items.
itm = dlg.GetItems()

# The window was closed.
def _func(ev):
    disp.ExitLoop()
dlg.On.MyWin.Close = _func
dlg.On.BTN_Cancel.Clicked = _func


# Add metadata.
def _func(ev):
    comp.StartUndo("Split to tiles")

    tool = comp.ActiveTool()
    rows = itm['SPN_Rows'].Value
    columns = itm['SPN_Columns'].Value
    join = itm['CHK_Join'].Checked
    split_to_tiles(tool, rows, columns, join)

    comp.EndUndo(True)
    disp.ExitLoop()
dlg.On.BTN_Split.Clicked = _func


# Open the dialog.
dlg.Show()
disp.RunLoop()
dlg.Hide()