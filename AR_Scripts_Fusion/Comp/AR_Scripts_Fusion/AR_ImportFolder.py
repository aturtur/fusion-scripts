"""
AR_ImportFolder(WIP)

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Import Folder
Version: 1.4.0
Description-US: Import all image sequences from selected folder.

Written for Blackmagic Design Fusion Studio 19.1.3 build 5.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

To do:
- Detect and handle also still/single images and video files.

Changelog:
1.4.0 (31.05.2025) - Added support to import single images.
                   - Bug fix in image formats list.
1.3.1 (07.05.2025) - Added hotkey Ctrl+Q to close the dialog.
1.3.0 (14.02.2025) - Added option to set custom starting frame number and option so set starting frame from image sequence's first frame number.
1.2.0 (06.11.2024) - Added option to merge imported loaders.
1.1.0 (05.11.2024) - Added option to scan also subfolders.
1.0.0 (21.10.2024) - Initial release.
"""
# Libraries
import os
import re
from pathlib import Path


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()

ALT: str = "ALT"
CTRL: str = "CTRL"
SHIFT: str = "SHIFT"

image_formats = [".jpg", ".jpeg", ".png", ".tif", ".tiff", ".exr", ".dpx", ".bpm", ".tga", ".psd"]


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


def range_map(value: float, in_min: float, in_max: float, out_min: float, out_max: float) -> float:
    """Remaps values."""

    if in_max - in_min == 0:
        raise ValueError("input range cannot be zero")
    
    return (value - in_min) / (in_max - in_min) * (out_max - out_min) + out_min


def collect_images(dir_path: str, subfolders: bool) -> list[str]:
    """Collect images from given folder path."""

    collected_images = []
    path = Path(dir_path)

    print("OK1")

    if path.exists() and path.is_dir():

        print("OK2")

        if subfolders:
            for file_path in sorted(path.rglob("*")):
                if file_path.is_file():
                    if file_path.suffix.lower() in image_formats:

                        digits_pattern = r'\d+(?!.*\d)'
                        frame_number = int(re.search(digits_pattern, str(file_path)).group())
                        first_frame, last_frame = get_frame_range(file_path.as_posix())                        
                        length = last_frame-first_frame
                        trim_position = 0
                        if length != 0:
                            trim_position = range_map(frame_number, first_frame, last_frame, 0, length)

                        collected_images.append([file_path, trim_position])
        
        else:
            for file_path in sorted(path.iterdir()):
                if file_path.is_file():
                    if file_path.suffix.lower() in image_formats:

                        digits_pattern = r'\d+(?!.*\d)'
                        frame_number = int(re.search(digits_pattern, str(file_path)).group())
                        first_frame, last_frame = get_frame_range(file_path.as_posix())                        
                        length = last_frame-first_frame
                        trim_position = 0
                        if length != 0:
                            trim_position = range_map(frame_number, first_frame, last_frame, 0, length)

                        collected_images.append([file_path, trim_position])
    
    return collected_images


def collect_image_sequences(dir_path: str, subfolders: bool) -> list[str]:
    """Collect image sequences from given folder path."""

    collected_sequences = []
    path = Path(dir_path)

    if path.exists() and path.is_dir():

        if subfolders:
            for file_path in sorted(path.rglob("*")):
                if file_path.is_file():
                    if file_path.suffix.lower() in image_formats:
                        # Get file name without frame number.
                        file_wo_fn = re.sub(r'(\d+)(\.\w+)$', r'\2', file_path.name)
                        
                        # Create full path for the file without frame number.
                        full_path = file_path.with_name(file_wo_fn).as_posix()
                        if all(sublist[0] != full_path for sublist in collected_sequences):
                            first_frame, last_frame = get_frame_range(file_path.as_posix())
                            collected_sequences.append([full_path, first_frame, last_frame, file_path])
        
        else:
            for file_path in sorted(path.iterdir()):
                if file_path.is_file():
                    if file_path.suffix.lower() in image_formats:
                        # Get file name without frame number.
                        file_wo_fn = re.sub(r'(\d+)(\.\w+)$', r'\2', file_path.name)
                        
                        # Create full path for the file without frame number.
                        full_path = file_path.with_name(file_wo_fn).as_posix()
                       
                        if all(sublist[0] != full_path for sublist in collected_sequences):
                            first_frame, last_frame = get_frame_range(file_path.as_posix())
                            collected_sequences.append([full_path, first_frame, last_frame, file_path])
    
    return collected_sequences


def create_loaders(method: int, items: list, merge: bool, select: bool, starting_frame_method: str, custom_frame: int) -> None:
    """Creates loaders."""
    
    flow = comp.CurrentFrame.FlowView
    loader_nodes = []
    merge_nodes = []
    x = 0
    y = 0

    # Loaders.
    if method == 0:  # Image sequences.
        for i, item in enumerate(items):
            loader = comp.AddTool("Loader", x, y)
            filename, extension = os.path.splitext(item[0])
            first_frame = item[1]
            last_frame = item[2]
            dir_path = os.path.dirname(item[0])
            file_path = os.path.join(dir_path, filename+str(first_frame)+extension)
            loader.SetInput("Clip", file_path)

            length = last_frame - first_frame

            if starting_frame_method == "Custom starting frame":
                loader.SetInput("GlobalOut", int(custom_frame+length))
                loader.SetInput("GlobalIn", int(custom_frame))

            elif starting_frame_method == "Starting frame from file":
                loader.SetInput("GlobalOut", int(last_frame))
                loader.SetInput("GlobalIn", int(first_frame))

            loader.SetInput("ClipTimeEnd", int(length))
            loader.SetInput("ClipTimeStart", 0)
            loader.SetInput("HoldLastFrame", 0)
            loader.SetInput("HoldFirstFrame", 0)

            if select:
                flow.Select(loader, True)

            if merge:
                loader_nodes.append(loader)

            y = y + 1

    else:  # Single images.
        for i, item in enumerate(items):
            loader = comp.AddTool("Loader", x, y)
            file_path = item[0]
            loader.SetInput("Clip", str(file_path))
            loader.SetInput("Loop", 1)

            loader.SetInput("ClipTimeStart", item[1])
            loader.SetInput("ClipTimeEnd", item[1])

            if select:
                flow.Select(loader, True)

            if merge:
                loader_nodes.append(loader)

            y = y + 1


    # Merges.
    if merge:
        for i, loader in enumerate(loader_nodes):

            if i != 0:
                flow = comp.CurrentFrame.FlowView
                pos_x, pos_y = flow.GetPosTable(loader).values()
                merge = comp.AddTool("Merge", pos_x + 1, pos_y)
                if select:
                    flow.Select(merge, True)
                merge_nodes.append(merge)

        for i, merge in enumerate(merge_nodes):
            if i == 0:
                merge.Background = loader_nodes[0].Output
                merge.Foreground = loader_nodes[1].Output
            else:
                merge.Background = merge_nodes[i-1].Output
                merge.Foreground = loader_nodes[i+1].Output


def replace_frame_number(file_path: str, frame_number: int) -> str:
    """Replaces file paths frame number with given one."""

    all_numbers = re.findall(r'\d+', file_path)
    
    if not all_numbers:
        return file_path
    
    last_number = all_numbers[-1]
    padded_new_number = str(frame_number).zfill(len(last_number))
    updated_file_path = re.sub(r'(\d+)(?=\D*$)', padded_new_number, file_path)

    return updated_file_path

            
def get_frame_range(file_path: str) -> tuple[int, int]:
    """Returns first and last frame numbers from given image sequence path."""

    clean_path = re.sub(r'(.*?)(\d+)\.[a-zA-Z]+$', r'\1', file_path)
    file_name = os.path.basename(clean_path)
    dir_path = os.path.dirname(file_path)
    extension = os.path.splitext(file_path)[1]

    found = False
    first_frame = 0
    last_frame = 0

    file_name_pattern = rf"{re.escape(file_name)}\d+{re.escape(extension)}"
    digits_pattern = r'\d+(?!.*\d)'

    if os.path.exists(dir_path) and os.path.isdir(dir_path):
        for file in sorted(os.listdir(dir_path)):
            match = re.search(file_name_pattern, file)

            if match:
                frame_number = int(re.search(digits_pattern, file).group())
                if found == False:
                    first_frame = frame_number
                    found = True
                else:
                    last_frame = frame_number

    return first_frame, last_frame


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


gui_geo = gui_geometry(500, 150, 0.5, 0.5)


# GUI
ui   = fusion.UIManager
disp = bmd.UIDispatcher(ui)
dlg  = disp.AddWindow({"WindowTitle": "Import Folder",
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
                ui.LineEdit({"Text": "", "PlaceholderText": "Please Enter the Folder Path", "ID": "Lineedit_FolderPath", "Weight": 0.9}),
                ui.Button({"Text": "...", "ID": "Button_Browse", "Weight": 0.1}),
            ]),

            # Method
            ui.HGroup(
            [
                ui.Label({"Text": "Method:", "ID": "Label_Method", "Weight": 0.1}),
                ui.ComboBox({"ID": "Combobox_Method", "Weight": 0.9}),

            ]),

            # Combobox and custom frame input.
            ui.HGroup(
            [
                ui.ComboBox({"ID": "Combobox_Starting_Frame", "Weight": 0.6}),
                ui.Label({"Text": "Custom Start Frame:", "ID": "Label_CustomStartFrame", "Weight": 0.1}),
                ui.SpinBox({"ID": "Spinbox_CustomFrame", "Minimum": 0, "Maximum": 1000000, "Weight": 0.3}),
            ]),

            # Checkboxes.
            ui.HGroup(
            [
                ui.CheckBox({"Text": "Select tools", "ID": "Checkbox_Select"}),
                ui.CheckBox({"Text": "Merge imported", "ID": "Checkbox_Merge"}),
                ui.CheckBox({"Text": "Include subfolders", "ID": "Checkbox_Subfolders", "ToolTip": "Warning!\nScanning all subfolders might take a long time!"}),
            ]),


            # Import and Cancel buttons.
            ui.HGroup(
            [
                ui.Button({"Text": "Import", "ID": "Button_Import", "Weight": 0.5}),
                ui.Button({"Text": "Cancel", "ID": "Button_Cancel", "Weight": 0.5}),
            ]),
        ]),
    ])


# Collect ui items.
itm = dlg.GetItems()

# Add combobox items.
itm['Combobox_Method'].AddItem("Import Image Sequences")
itm['Combobox_Method'].AddItem("Import Single Images")

itm['Combobox_Starting_Frame'].AddItem("Custom starting frame")
itm['Combobox_Starting_Frame'].AddItem("Starting frame from file")

# Default settings.
itm['Checkbox_Select'].Checked = True


# Comboboxes.
def combo_method_changed(ev):
    selected_index = itm['Combobox_Method'].CurrentIndex
    itm['Spinbox_CustomFrame'].Enabled = (selected_index == 0)
    itm['Combobox_Starting_Frame'].Enabled = (selected_index == 0)
dlg.On.Combobox_Method.CurrentIndexChanged = combo_method_changed

def combo_starting_frame_changed(ev):
    selected_index = itm['Combobox_Starting_Frame'].CurrentIndex
    itm['Spinbox_CustomFrame'].Enabled = (selected_index == 0)
dlg.On.Combobox_Starting_Frame.CurrentIndexChanged = combo_starting_frame_changed


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


# Create loaders.
def _func(ev):
    comp.StartUndo("Create Loaders")
    comp.Lock()  # Put the composition to lock mode, so it won't open dialogs.

    method = itm['Combobox_Method'].CurrentIndex
    subfolders = itm['Checkbox_Subfolders'].Checked
    merge = itm['Checkbox_Merge'].Checked
    select = itm['Checkbox_Select'].Checked

    starting_frame_method = itm['Combobox_Starting_Frame'].CurrentText
    custom_frame = itm['Spinbox_CustomFrame'].Value

    flow = comp.CurrentFrame.FlowView
    if select:
        flow.Select()  # Deselect all tools.

    if method == 0:
        items = collect_image_sequences(itm['Lineedit_FolderPath'].Text, subfolders)
    else:
        items = collect_images(itm['Lineedit_FolderPath'].Text, subfolders)

    create_loaders(method, items, merge, select, starting_frame_method, custom_frame)

    comp.Unlock()
    comp.EndUndo(True)
dlg.On.Button_Import.Clicked = _func


# Open the dialog.
dlg.Show()
disp.RunLoop()
dlg.Hide()