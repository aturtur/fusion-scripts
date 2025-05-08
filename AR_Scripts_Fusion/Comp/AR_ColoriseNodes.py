"""
AR_ColoriseNodes

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Colorise Nodes
Version: 1.0.3
Description-US: Colorises selected nodes.

Written for Blackmagic Design Fusion Studio 19.0 build 59.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.0.3 (07.05.2025) - Added hotkey Ctrl+Q to close the dialog.
1.0.2 (20.09.2024) - Modified code to follow more PEP 8 recommendations.
                   - Gets now automatically correct icon file paths.
1.0.1 (08.11.2022) - Semantic versioning.
1.0.0 (26.04.2022) - Initial release.
"""
# Libraries
import inspect
from pathlib import Path


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()

# Icons folder path.
script_dir  = Path(inspect.getfile(lambda: None)).resolve().parent
icon_folder = script_dir / "Icons"

# Color icon paths.
orange_icon     = icon_folder / "color_orange.png"
apricot_icon    = icon_folder / "color_apricot.png"
yellow_icon     = icon_folder / "color_yellow.png"
lime_icon       = icon_folder / "color_lime.png"
olive_icon      = icon_folder / "color_olive.png"
green_icon      = icon_folder / "color_green.png"
teal_icon       = icon_folder / "color_teal.png"
navy_icon       = icon_folder / "color_navy.png"
blue_icon       = icon_folder / "color_blue.png"
purple_icon     = icon_folder / "color_purple.png"
violet_icon     = icon_folder / "color_violet.png"
pink_icon       = icon_folder / "color_pink.png"
tan_icon        = icon_folder / "color_tan.png"
beige_icon      = icon_folder / "color_beige.png"
brown_icon      = icon_folder / "color_brown.png"
chocolate_icon  = icon_folder / "color_chocolate.png"

# Color dictionary.
colors = {
    'Orange': {'R': 235.0/255.0, 'G': 110.0/255.0, 'B': 0.0/255.0},
    'Apricot': {'R': 255.0/255.0, 'G': 168.0/255.0, 'B': 51.0/255.0},
    'Yellow': {'R': 226.0/255.0, 'G': 169.0/255.0, 'B': 28.0/255.0},
    'Lime': {'R': 159.0/255.0, 'G': 198.0/255.0, 'B': 21.0/255.0},
    'Olive': {'R': 95.0/255.0, 'G': 153.0/255.0, 'B': 32.0/255.0},
    'Green': {'R': 64.0/255.0, 'G': 143.0/255.0, 'B': 101.0/255.0},
    'Teal': {'R': 0.0/255.0, 'G': 152.0/255.0, 'B': 153.0/255.0},
    'Navy': {'R': 21.0/255.0, 'G': 98.0/255.0, 'B': 132.0/255.0},
    'Blue': {'R': 121.0/255.0, 'G': 168.0/255.0, 'B': 208.0/255.0},
    'Purple': {'R': 153.0/255.0, 'G': 115.0/255.0, 'B': 160.0/255.0},
    'Violet': {'R': 149.0/255.0, 'G': 75.0/255.0, 'B': 205.0/255.0},
    'Pink': {'R': 233.0/255.0, 'G': 140.0/255.0, 'B': 181.0/255.0},
    'Tan': {'R': 185.0/255.0, 'G': 176.0/255.0, 'B': 151.0/255.0},
    'Beige': {'R': 198.0/255.0, 'G': 160.0/255.0, 'B': 119.0/255.0},
    'Brown': {'R': 153.0/255.0, 'G': 102.0/255.0, 'B': 0.0/255.0},
    'Chocolate': {'R': 140.0/255.0, 'G': 90.0/255.0, 'B': 63.0/255.0}
}

# Key modifiers.
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


def change_color(color) -> None:
    """Changes selected nodes with given color."""

    tools = comp.GetToolList(True).values()

    for tool in tools:
        if color == 'Clear':
            tool.TileColor = None
        else:
            tool.TileColor = colors[color]


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


gui_geo = gui_geometry(100, 500, 0.5, 0.5)


# GUI
ui   = fusion.UIManager
disp = bmd.UIDispatcher(ui)
dlg  = disp.AddWindow({"WindowTitle": "Colorise Nodes",
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
            ui.Button({"Text": " Default", "ID": "Button_Clear", }),
            ui.Button({"Text": "     Orange", "ID": "Button_Orange", "Icon": ui.Icon({"ID": "Orange", "File": str(orange_icon)})}),
            ui.Button({"Text": "      Apricot", "ID": "Button_Apricot", "Icon": ui.Icon({"ID": "Apricot", "File": str(apricot_icon)})}),
            ui.Button({"Text": "       Yellow", "ID": "Button_Yellow", "Icon": ui.Icon({"ID": "Yellow", "File": str(yellow_icon)})}),
            ui.Button({"Text": "          Lime", "ID": "Button_Lime", "Icon": ui.Icon({"ID": "Lime", "File": str(lime_icon)})}),
            ui.Button({"Text": "          Olive", "ID": "Button_Olive", "Icon": ui.Icon({"ID": "Olive", "File": str(olive_icon)})}),
            ui.Button({"Text": "        Green", "ID": "Button_Green", "Icon": ui.Icon({"ID": "Green", "File": str(green_icon)})}),
            ui.Button({"Text": "            Teal", "ID": "Button_Teal", "Icon": ui.Icon({"ID": "Teal", "File": str(teal_icon)})}),
            ui.Button({"Text": "           Navy", "ID": "Button_Navy", "Icon": ui.Icon({"ID": "Navy", "File": str(navy_icon)})}),
            ui.Button({"Text": "           Blue", "ID": "Button_Blue", "Icon": ui.Icon({"ID": "Blue", "File": str(blue_icon)})}),
            ui.Button({"Text": "       Purple", "ID": "Button_Purple", "Icon": ui.Icon({"ID": "Purple", "File": str(purple_icon)})}),
            ui.Button({"Text": "         Violet", "ID": "Button_Violet", "Icon": ui.Icon({"ID": "Violet", "File": str(violet_icon)})}),
            ui.Button({"Text": "           Pink", "ID": "Button_Pink", "Icon": ui.Icon({"ID": "Pink", "File": str(pink_icon)})}),
            ui.Button({"Text": "            Tan", "ID": "Button_Tan", "Icon": ui.Icon({"ID": "Tan", "File": str(tan_icon)})}),
            ui.Button({"Text": "         Beige", "ID": "Button_Beige", "Icon": ui.Icon({"ID": "Beige", "File": str(beige_icon)})}),
            ui.Button({"Text": "        Brown", "ID": "Button_Brown", "Icon": ui.Icon({"ID": "Brown", "File": str(brown_icon)})}),
            ui.Button({"Text": "  Chocolate", "ID": "Button_Chocolate", "Icon": ui.Icon({"ID": "Chocolate", "File": str(chocolate_icon)})})
        ]),
    ])


# Collect ui items.
itm = dlg.GetItems()


# The window was closed.
def _func(ev):
    disp.ExitLoop()
dlg.On.MyWin.Close = _func


# Keys are pressed.
def _func(ev):
    key_modifiers = get_key_modifiers(ev)
    if CTRL in key_modifiers and ev['Key'] == 81:  # Ctrl + Q.
        disp.ExitLoop()
        dlg.Hide()
dlg.On.MyWin.KeyPress = _func


# Buttons are pressed.
def _func(ev):
    color = ev['who'].replace("Button_", "")
    change_color(color)
dlg.On.Button_Clear.Clicked = _func
dlg.On.Button_Orange.Clicked = _func
dlg.On.Button_Apricot.Clicked = _func
dlg.On.Button_Yellow.Clicked = _func
dlg.On.Button_Lime.Clicked = _func
dlg.On.Button_Olive.Clicked = _func
dlg.On.Button_Green.Clicked = _func
dlg.On.Button_Teal.Clicked = _func
dlg.On.Button_Navy.Clicked = _func
dlg.On.Button_Blue.Clicked = _func
dlg.On.Button_Purple.Clicked = _func
dlg.On.Button_Violet.Clicked = _func
dlg.On.Button_Pink.Clicked = _func
dlg.On.Button_Tan.Clicked = _func
dlg.On.Button_Beige.Clicked = _func
dlg.On.Button_Brown.Clicked = _func
dlg.On.Button_Chocolate.Clicked = _func


# Open the dialog.
dlg.Show()
disp.RunLoop()
dlg.Hide()