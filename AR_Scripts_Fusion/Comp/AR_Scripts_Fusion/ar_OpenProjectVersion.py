"""
ar_OpenProjectVersion

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Open Project Version
Version: 1.0.1
Description-US: Lists all versions of the project. Uses '_v' delimiter.

Written for Blackmagic Design Fusion Studio 20.3.1 build 5.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.0.1 (30.01.2026) - Added error checking.
1.0.0 (28.01.2026) - Initial release.
"""
# Libraries
import re
from pathlib import Path


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()

ALT: str = "ALT"
CTRL: str = "CTRL"
SHIFT: str = "SHIFT"

projects = {}


# Functions
def refresh(dir_path: str) -> bool:
    """Refreshes the project dict and populates the comboboxes."""

    global projects

    projects = collect_projects(dir_path)
    first_project_name = next(iter(projects))

    itm = dlg.GetItems()
    itm["Combobox_Project"].Clear()  # Clear old items.
    itm["Combobox_Version"].Clear()  # Clear old items.
    for project_name in projects:
        itm['Combobox_Project'].AddItem(project_name)

    itm['Combobox_Project'].CurrentText = first_project_name

    versions = list(projects[first_project_name].keys())
    versions_sorted = sorted(versions, key=lambda v: int(v[1:]))
    for version in versions_sorted:
        itm['Combobox_Version'].AddItem(version)
    itm['Combobox_Version'].CurrentText = versions_sorted[-1]

    return True


def open_the_project(projects: dict, project_name: str, version: str) -> bool:
    """Opens the project."""

    project_path = projects[project_name][version]
    fusion.LoadComp(project_path)

    return True


def populate_combobox_project(projects: dict) -> bool:
    """Populates the project combobox."""

    itm = dlg.GetItems()
    itm["Combobox_Project"].Clear()  # Clear old items.

    for project_name in projects:
        itm['Combobox_Project'].AddItem(project_name)

    return True


def populate_combobox_version(projects: dict, project_name: str) -> bool:
    """Populates the version combobox."""

    itm = dlg.GetItems()
    itm["Combobox_Version"].Clear()  # Clear old items.

    try:
        versions = list(projects[project_name].keys())
        versions_sorted = sorted(versions, key=lambda v: int(v[1:]))
        for version in versions_sorted:
            itm['Combobox_Version'].AddItem(version)

        itm['Combobox_Version'].CurrentText = versions_sorted[-1]
    except:
        pass

    return True


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


def collect_projects(dir_path: str) -> list | bool:
    """Collects all projects from the given folder path."""

    project_dir = Path(dir_path)
    pattern = re.compile(r"(.+)_v(\d+)\.comp$", re.IGNORECASE)
    projects = {}

    if dir_path != "":

        for comp_file in project_dir.rglob("*.comp"):
            match = pattern.match(comp_file.name)
            if not match:
                continue

            project_name = match.group(1)
            version_number = match.group(2)

            version = f"v{version_number}"

            projects.setdefault(project_name, {})[version] = str(comp_file.resolve())


        projects_sorted = {
            project: dict(
                sorted(
                    versions.items(),
                    key=lambda item: int(item[0][1:])
                )
            )
            for project, versions in projects.items()
        }
        
        return projects

    else:
        return False


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


gui_geo = gui_geometry(600, 125, 0.5, 0.5)


# GUI
ui   = fusion.UIManager
disp = bmd.UIDispatcher(ui)
dlg  = disp.AddWindow({"WindowTitle": "Open Project Version",
                       "ID": "MyWin",
                       "Geometry": [gui_geo['x'], gui_geo['y'], gui_geo['width'], gui_geo['height']],
                       "Events": {"Close": True,
                                  "KeyPress": True,
                                  "KeyRelease": True}
                       },
    [
        ui.VGroup({"Spacing": 5},
        [
            # GUI elements.

            # Select the folder path.
            ui.HGroup(
            [
                ui.Label({"Text": "Folder Path", "ID": "Label_FolderPath", "Weight": 0.1}),
                ui.LineEdit({"Text": "", "PlaceholderText": "Please Enter the Folder Path...", "ID": "Lineedit_FolderPath", "Weight": 0.8}),
                ui.Button({"Text": "...", "ID": "Button_Browse", "Weight": 0.05, "ToolTip": "Browse"}),
                ui.Button({"Text": "↻", "ID": "Button_Refresh", "Weight": 0.05, "ToolTip": "Refresh"}),
            ]),

            # Project.
            ui.HGroup(
            [
                ui.Label({"Text": "Project:", "ID": "Label_Project", "Weight": 0.1}),
                ui.ComboBox({"ID": "Combobox_Project", "Weight": 0.6}),
                ui.ComboBox({"ID": "Combobox_Version", "Weight": 0.3}),

            ]),

            # Import and Cancel buttons.
            ui.HGroup(
            [
                ui.Button({"Text": "Open", "ID": "Button_Open", "Weight": 0.5}),
                ui.Button({"Text": "Cancel", "ID": "Button_Cancel", "Weight": 0.5}),
            ]),
        ]),
    ])


# Collect ui items.
itm = dlg.GetItems()

project_path = comp.GetAttrs()['COMPS_FileName']
if project_path != "":
    project_path = Path(project_path)
    project_folder = project_path.parent
    itm['Lineedit_FolderPath'].Text = str(project_folder)
    pattern = re.compile(r"(.+)_v(\d+)", re.IGNORECASE)
    match = pattern.match(project_path.stem)
    current_project_name = match.group(1)
    current_project_version = "v"+match.group(2)
    projects = collect_projects(project_folder)

if projects:
    # Add combobox items.
    populate_combobox_project(projects)
    itm['Combobox_Project'].CurrentText = current_project_name
    populate_combobox_version(projects, current_project_name)

# Comboboxes.
def combo_project_changed(ev):
    for project_name in projects:
        if itm['Combobox_Project'].CurrentText == project_name:
            populate_combobox_version(projects, itm['Combobox_Project'].CurrentText)
dlg.On.Combobox_Project.CurrentIndexChanged = combo_project_changed


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


# Browse the folder path.
def _func(ev):
    selectedFolderPath = fusion.RequestDir(itm['Lineedit_FolderPath'].Text)
    if selectedFolderPath:
        itm['Lineedit_FolderPath'].Text = str(selectedFolderPath)
dlg.On.Button_Browse.Clicked = _func


# Refresh.
def _func(ev):
    comp.Lock()
    refresh(itm['Lineedit_FolderPath'].Text)
    comp.Unlock()
dlg.On.Button_Refresh.Clicked = _func


# Open the project.
def _func(ev):
    comp.Lock()  # Put the composition to lock mode, so it won't open dialogs.

    project = itm['Combobox_Project'].CurrentText
    version = itm['Combobox_Version'].CurrentText

    open_the_project(projects, project, version)
    comp.Unlock()
    disp.ExitLoop()
dlg.On.Button_Open.Clicked = _func


# Open the dialog.

dlg.Show()
itm['Combobox_Version'].SetFocus()
disp.RunLoop()
dlg.Hide()