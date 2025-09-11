"""
AR_SplitToTiles

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Split To Tiles
Version: 1.1.0
Description-US: Splits the active tool in to tiles by given rows and clomuns.

Written for Blackmagic Design Fusion Studio 19.0.3 build 3
Python version 3.10.8 (64-bit)

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.1.0 (07.09.2025) - By default transforms are made in multimerge node, but you can also expose transforms.
1.0.0 (24.03.2025) - Initial release.
"""
# Libraries
import math


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()


# Functions
def split_to_tiles(tool, rows: int, columns: int, join: bool, expose: bool) -> None:
    """Splits the active tool in to tiles by given rows and clomuns."""

    width = tool.GetAttrs("TOOLI_ImageWidth")
    height = tool.GetAttrs("TOOLI_ImageHeight")

    crop_nodes = []
    transform_nodes = []
    transforms = []

    flow = comp.CurrentFrame.FlowView
    x, y = flow.GetPosTable(tool).values()

    tile_w = width / columns
    tile_h = height / rows

    for i in range(rows):
        for j in range(columns):
            # Crop-node
            crop_node = comp.AddTool("Crop",
                                     math.floor(x) + 1 + j,
                                     math.floor(y) - i)
            crop_node.SetAttrs({'TOOLS_Name': f"Tile_{i+1}x{j+1}"})
            crop_node.Input = tool.Output

            x_offset = j * tile_w
            y_offset = i * tile_h

            crop_node.SetInput("XOffset", x_offset)
            crop_node.SetInput("YOffset", y_offset)
            crop_node.SetInput("XSize", tile_w)
            crop_node.SetInput("YSize", tile_h)

            crop_nodes.append(crop_node)

            if join:
                # Center
                x_center = (x_offset + tile_w / 2) / width
                y_center = (y_offset + tile_h / 2) / height

                # Transforms
                transform_x = 0.5 + ((x_center - 0.5) * (width / tile_w))
                transform_y = 0.5 + ((y_center - 0.5) * (height / tile_h))

                # Merge transforms
                transform_merge_x = 0.5 + ((transform_x - 0.5) / (width / tile_w))
                transform_merge_y = 0.5 + ((transform_y - 0.5) / (height / tile_h))

                transforms.append([transform_merge_x, transform_merge_y])

                if expose:
                    transform_node = comp.AddTool("Transform",
                                                math.floor(x) + 2 + columns + j,
                                                math.floor(y) - i)
                    transform_node.SetAttrs({'TOOLS_Name': f"Transform_{i+1}x{j+1}"})
                    transform_node.SetInput("Input", crop_node)
                    transform_node.SetInput("Center", {1: transform_x, 2: transform_y})
                    transform_nodes.append(transform_node)
                    
    if join:
        multimerge_node = comp.AddTool("MultiMerge", math.floor(x)+4+columns-j, math.floor(y)+2-i)
        multimerge_node.Background = tool.Output

        if expose:
            for i, transform_node in enumerate(transform_nodes):
                multimerge_node.ConnectInput(f"Layer{i+1}.Foreground", transform_node.Output)
        else:
            for i, crop_node in enumerate(crop_nodes):
                multimerge_node.ConnectInput(f"Layer{i+1}.Foreground", crop_node.Output)

                transform_x = transforms[i][0]
                transform_y = transforms[i][1]

                multimerge_node.SetInput(f"Layer{i+1}.Center", {1: transform_x, 2: transform_y})


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
                       "Geometry": [gui_geo['x'], gui_geo['y'], gui_geo['width'], gui_geo['height']]
                       },
    [
        ui.VGroup({"Spacing": 5},
        [
            # GUI elements.
            ui.HGroup([
                ui.Label({"ID": "Label", "Text": "Rows:"}),
                ui.SpinBox({"ID": "Spinbox_Rows", "Minimum": 1, "Maximum": 1000000, "Value": 2, "Weight": 1.0}),
            ]),

            ui.HGroup([
                ui.Label({"ID": "Label", "Text": "Columns:"}),
                ui.SpinBox({"ID": "Spinbox_Columns", "Minimum": 1, "Maximum": 1000000, "Value": 2, "Weight": 1.0}),
            ]),

            ui.HGroup([
                ui.CheckBox({"Text": "Create Join Tiles Setup", "ID": "Checkbox_Join", "Weight": 1.0}),
                ui.CheckBox({"Text": "Expose Transforms", "ID": "Checkbox_Transforms", "Weight": 1.0}),
            ]),

            ui.VGap(10),
            
            # Add and Cancel buttons.
            ui.HGroup(
            [
                ui.Button({"Text": "Split", "ID": "Button_Split"}),
                ui.Button({"Text": "Cancel", "ID": "Button_Cancel"}),
            ]),

        ]),
    ])


# Collect ui items.
itm = dlg.GetItems()

# The window was closed.
def _func(ev):
    disp.ExitLoop()
dlg.On.MyWin.Close = _func
dlg.On.Button_Cancel.Clicked = _func


# Add metadata.
def _func(ev):
    comp.StartUndo("Split to tiles")

    tool = comp.ActiveTool()
    rows = itm['Spinbox_Rows'].Value
    columns = itm['Spinbox_Columns'].Value
    join = itm['Checkbox_Join'].Checked
    expose = itm['Checkbox_Transforms'].Checked
    split_to_tiles(tool, rows, columns, join, expose)

    comp.EndUndo(True)
    disp.ExitLoop()
dlg.On.Button_Split.Clicked = _func


# Open the dialog.
dlg.Show()
disp.RunLoop()
dlg.Hide()