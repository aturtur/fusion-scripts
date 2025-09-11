"""
AR_PrintKeyPresses(DEV)

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Print Key Presses (DEV)
Version: 1.0.0
Description-US: Prints pressed keys to the console.

Written for Blackmagic Design Fusion Studio 19.1.3 build 5
Python version 3.10.8 (64-bit)

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp
  
Changelog:
1.0.0 (27.02.2025) - Initial release.
"""
# Libraries
...


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()


# Functions
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


gui_geo = gui_geometry(325, 200, 0.5, 0.5)


# GUI
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
                        "Geometry": [gui_geo['x'], gui_geo['y'], gui_geo['width'], gui_geo['height']], },
    [

        ui.VGroup({ "Spacing": 5, },
        [
            ui.Label({ "Text": "Press buttons", "ID": "StaticText" }),
        ]),
    ])


# Collect ui items
itm = dlg.GetItems()

# The window was closed
def _func(ev):
    disp.ExitLoop()
dlg.On.MyWin.Close = _func

# Keyboard events
def _func(ev):
    print(ev['Key'])
    print(ev['Modifiers'])

dlg.On.MyWin.KeyPress = _func

# Open the dialog
dlg.Show()
disp.RunLoop()
dlg.Hide()