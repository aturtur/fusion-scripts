"""
AR_ScriptLauncher

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Script Launcher
Version: 1.2.0
Description-US: Search and run sripts easily.

Written for Blackmagic Design Fusion Studio 19.0 build 59.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Pyautogui module is recommended but not required.

Highly recommended to add this script to hotkey:
    View -> Customize Hotkeys...
        Views -> New...
            <Enter Key Sequence> E.g. Shift+Tab
            Scripts -> AR_ScriptLauncher

Changelog:
1.2.0 (xx.04.2025) - Added support for icons.
1.1.1 (01.04.2025) - Error check for parsing data.
1.1.0 (24.03.2025) - Parses info from the script file and uses that to populate the treeview.
1.0.4 (27.02.2025) - Added Ctrl+Q hotkey to close the dialog.
1.0.3 (05.02.2025) - Update, sending more important variables.
1.0.2 (06.11.2024) - Small tweaks.
1.0.1 (10.10.2024) - Small QOL improvement.
1.0.0 (26.09.2024) - Initial realease.
"""
# Libraries
import re
import sys
import inspect
from pathlib import Path
import importlib.util
from collections import Counter

try:
    from pyautogui import press
except:
    pass


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
app = app
fu = fu
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()

script_dir  = Path(inspect.getfile(lambda: None)).resolve().parent
icon_folder = script_dir / "Icons"

use_icons = True

ALT: str = "ALT"
CTRL: str = "CTRL"
SHIFT: str = "SHIFT"

scripts = {}


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


def get_script_info(script) -> tuple[str, str]:
    """Parses script info from the script file."""

    label = script.name
    description = ""

    with open(script.resolve(), "r", encoding="utf-8") as file:
        for line in file:
            try:
                if line.startswith("Name-US: "):
                    label = line.split("Name-US: ", 1)[1].strip()
            except:
                pass
            try:
                if line.startswith("Description-US:"):
                    description = line.split("Description-US: ", 1)[1].strip()
            except:
                pass
            
        return label, description
                
    return label, description


def get_scripts() -> None:
    """Scans the folder and adds found scripts to the scripts list."""

    # Custom script directory path.
    #script_dir = pathlib.Path.home() / "AppData" / "Roaming" / "Blackmagic Design" / "Fusion" / "Scripts" / "Comp"

    # Folder where this script is located.
    script_dir = Path(inspect.getfile(lambda: None)).resolve().parent

    # Scan python scripts.
    found_scripts = [file for file in script_dir.rglob('*.py')]
    for script in found_scripts:
        
        script_label, script_description = get_script_info(script)

        scripts[script_label] = {
            "FileName": Path(script).stem,
            "Extension": Path(script).suffix,
            "Description": script_description,
            "Path": script.resolve()
        }


def populate_tree(tree, scripts: dict) -> None:
    """Populates ui.Tree with script names."""

    for script_name, details in scripts.items():
        itRow = tree.NewItem()
        itRow.Text[0] = "  " + script_name
        #itRow.Font[0] = ui.Font({ 'PointSize': 12})
        itRow.ToolTip[0] = details['Description']
        if use_icons:
            icon_path = icon_folder / f"{details['FileName']}.png"
            if icon_path.exists():
                itRow.Icon[0] = ui.Icon({"ID": "Orange", "File": str(icon_path)})
        tree.AddTopLevelItem(itRow)


def clear_tree(tree) -> None:
    """Clears all items from the ui.Tree."""

    tree.Clear()
            

def select_first_item(tree)-> None:
    """Select first item of the ui.Tree."""

    count = tree.TopLevelItemCount()
    if count > 0:
        item = tree.ItemAt(0)
        item.Selected = True


def search(string: str, keyword: str) -> None:
    """Checks if the given keywords can be found in the string."""

    keywords = keyword.split()
    keyword_counts = Counter(keywords)
    return all(len(re.findall(re.escape(k), string, re.IGNORECASE)) >= count
            for k, count in keyword_counts.items())


def get_script_path(name: str) -> str | None:
    """Gets script path by given script name."""

    return scripts.get(name.strip(), {}).get("Path")


def run_script(file_path: str) -> None:
    """Runs script file from given file path."""

    spec = importlib.util.spec_from_file_location(file_path.stem, file_path)
    module = importlib.util.module_from_spec(spec)
    
    # Set important variables.
    module.bmd = bmd
    module.app = app
    module.fusion = fusion
    module.fu = fu
    module.comp = comp
    
    sys.modules[file_path.stem] = module

    # Run the external python script.
    spec.loader.exec_module(module)
    if hasattr(module, 'main'):
        module.main()


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


gui_geo = gui_geometry(350, 400, 0.5, 0.5)


# GUI
ui   = fusion.UIManager
disp = bmd.UIDispatcher(ui)


dlg  = disp.AddWindow({"WindowTitle": "Script Launcher",
                      "ID": "MyWin",
                      "Geometry": [gui_geo['x'], gui_geo['y'], gui_geo['width'], gui_geo['height']],
                      "Spacing": 0,
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
                    }, [

                            ui.VGroup({"ID": "TreeView"}, [
                                ui.HGroup({"ID": "Group", "Weight": 0.075}, [
                                    ui.LineEdit({"ID": "Search",
                                                "Text": "",
                                                "PlaceholderText": "Search",
                                                }),
                                ]),

                            ui.Tree({
                            "ID": "Tree",
                            "HeaderHidden": True,
                            "Events": {
                                "CurrentItemChanged": True,
                                "ItemActivated": True,
                                "ItemClicked": True,
                                "ItemDoubleClicked": True,
                                },
                            "Weight": 0.925,
                            }),
                        ]),
                    ])


# Get UI items.
itm = dlg.GetItems()

# Scan and collect scipts.
get_scripts()

# Build the tree.
script_tree = itm['Tree']
header = script_tree.NewItem()
header.Text[0] = "Script"
script_tree.SetHeaderItem(header)
script_tree.ColumnCount = 1
script_tree.IconSize = [25, 25]
populate_tree(script_tree, scripts)
select_first_item(script_tree)

# Keyboard events.
def _func(ev):
    key_modifiers = get_key_modifiers(ev)
    if CTRL in key_modifiers and ev['Key'] == 81:  # Ctrl + Q.
        disp.ExitLoop()
        dlg.Hide()

    if itm['Search'].HasFocus():
        if ev['Key'] == 16777235: # Up.
            try:
                press('tab')
                press('up')
            except:
                pass
        if ev['Key'] == 16777237: # Down.
            try:
                press('tab')
                press('down')
            except:
                pass

    if ev['Key'] == 16777220: # Enter.
        current_item = script_tree.CurrentItem()
        count = script_tree.TopLevelItemCount()
        script_name = None

        if current_item is not None:
            script_name = current_item.Text[0]
        elif count > 0:
            script_name = script_tree.ItemAt(count).Text[0]

        disp.ExitLoop()
        dlg.Hide()

        if script_name:
            run_script(get_script_path(script_name))
dlg.On.MyWin.KeyPress = _func


# Tree item double clicked.
def _func(ev):
    disp.ExitLoop()
    dlg.Hide()
    run_script(get_script_path(str(ev['item'].Text[0])))
dlg.On.Tree.ItemDoubleClicked = _func


# LineEdit changed.
def _func(ev):
    if itm['Search'].Text == "":
        clear_tree(script_tree)
        populate_tree(script_tree, scripts)
    else:
        clear_tree(script_tree)
        filtered_scripts = {}
        keyword = itm['Search'].Text
        for script_name, script_data in scripts.items():
            if search(script_name, keyword):
                filtered_scripts[script_name] = script_data
        populate_tree(script_tree, filtered_scripts)
        select_first_item(script_tree)
dlg.On['Search'].TextChanged = _func


# The window was closed.
def _func(ev):
    disp.ExitLoop()
    dlg.Hide()
dlg.On.MyWin.Close = _func


# Open and run the dialog.
dlg.Show()
disp.RunLoop()
dlg.Hide()