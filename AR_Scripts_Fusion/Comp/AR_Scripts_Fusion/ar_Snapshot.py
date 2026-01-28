"""
ar_Snapshot

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Snapshot
Version: 1.1.0
Description-US: Takes a snapshot from a given viewer.

Written for Blackmagic Design Fusion Studio 20.3.1 build 5.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

To do / ideas:
Method Combobox:
    Save only
    View on B Buffer
    View on other view
Presets Combobox:
    JPEG
    PNG
    TIFF
    EXR
Checkbox: Open snapshot folder

Changelog:
1.1.0 (21.01.2026) - Combobox is now populated based on views on use.
1.0.0 (20.01.2026) - Initial realease.
"""
# Libraries
from datetime import datetime
from pathlib import Path
import pprint


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()


# Functions
def disable_tools(tools: list) -> bool:
    """Disables given tools."""

    for tool in tools:
        tool.SetAttrs({'TOOLB_PassThrough':True})

    return True


def enable_tools(tools: list) -> bool:
    """Enables given tools."""

    for tool in tools:
        tool.SetAttrs({'TOOLB_PassThrough':False})

    return True


def collect_enabled_savers() -> list:
    """Collects and returns savers that are currently enabled."""

    enabled_savers = []
    savers = comp.GetToolList(False, "Saver").values()
    for saver in savers:
        if saver.GetAttrs("TOOLB_PassThrough"):
            enabled_savers.append(saver)

    return enabled_savers


def take_snapshot(view: str, import_snapshot: bool, bbuffer: bool) -> bool:
    """Takes a snaphot."""

    project_file_path = comp.GetAttrs()['COMPS_FileName']
    if project_file_path == "":
        print("Project has to be saved first!")
        return False

    windowlist = comp.GetFrameList()
    previews = comp.GetPreviewList()

    left_view = previews['LeftView'].GetConnectedOutput()
    right_view = previews['RightView'].GetConnectedOutput()
    
    if view == "Left":
        if left_view != None:
            left_view_tool_name = left_view.GetTool().Name
            left_view_tool = comp.FindTool(left_view_tool_name)
            tool_name = left_view_tool_name
            tool = left_view_tool
        else:
            print("Left view input not found!")
            return False
    
    elif view == "Right":
        if right_view != None:
            right_view_tool_name = right_view.GetTool().Name
            right_view_tool = comp.FindTool(right_view_tool_name)
            tool_name = right_view_tool_name
            tool = right_view_tool
        else:
            print("Right view input not found!")
            return False

    current_time = comp.CurrentTime
    current_global_start = comp.GetAttrs("COMPN_GlobalStart")
    current_global_end = comp.GetAttrs("COMPN_GlobalEnd")
    current_render_start = comp.GetAttrs("COMPN_RenderStart")
    current_render_end = comp.GetAttrs("COMPN_RenderEnd")

    comp.SetAttrs({"COMPN_GlobalStart":current_time,
                   "COMPN_GlobalEnd":current_time})    
    comp.SetAttrs({"COMPN_RenderStart":current_time,
                    "COMPN_RenderEnd":current_time})

    enabled_savers = collect_enabled_savers()
    disable_tools(enabled_savers)

    # Saver.
    file_path = comp.GetAttrs()['COMPS_FileName']
    now = datetime.now()
    timestamp = now.strftime("%y%m%d%H%M%S")
    file_name = "snapshot_" + tool_name + "_" + timestamp + "_.jpg"
    file_path = Path(file_path).parent / "snapshots" / file_name

    saver_node = comp.AddTool("Saver")
    output_port = tool
    saver_node.Input = output_port
    saver_node.TileColor = {'R': 233.0/255.0,  # Pink color.
                            'G': 140.0/255.0,
                            'B': 181.0/255.0}

    saver_node.SetInput("Clip", str(file_path))
    saver_node.SetInput("OutputFormat", "JpegFormat")

    comp.Render(True, current_time, current_time, 1)  # Take the snapshot (render the frame).
    saver_node.Delete()

    # Restore settings.
    comp.SetAttrs({"COMPN_GlobalStart":current_global_start,
                   "COMPN_GlobalEnd":current_global_end})    
    comp.SetAttrs({"COMPN_RenderStart":current_render_start,
                    "COMPN_RenderEnd":current_render_end})
    enable_tools(enabled_savers)

    # Loader.
    if import_snapshot:
        flow = comp.CurrentFrame.FlowView
        x, y = flow.GetPosTable(tool).values()
        loader_node = comp.AddTool("Loader", x, y+2)
        frame_numbers = str(int(current_time)).zfill(4)
        file_path = file_path.with_name(f"{file_path.stem}{frame_numbers}{file_path.suffix}")    
        loader_node.SetInput("Clip", str(file_path))

        if bbuffer:
            for window in windowlist.values():
                if view == "Left":
                    # Left preview window.
                    left = previews['LeftView'].View
                    left.SetBuffer(1)  # B Buffer.
                    window.ViewOn(loader_node, 2)
                    left.SetBuffer(2)  # Split Wipe Buffer.
                elif view == "Right":
                    # Right preview window.
                    right = previews['RightView'].View
                    right.SetBuffer(1)  # B Buffer.
                    window.ViewOn(loader_node, 2)
                    right.SetBuffer(2)  # Split Wipe Buffer.
    return True


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


gui_geo = gui_geometry(250, 100, 0.5, 0.5)


# GUI
ui   = fusion.UIManager
disp = bmd.UIDispatcher(ui)
dlg  = disp.AddWindow({"WindowTitle": "Snapshot",
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

            # Checkbox.
            ui.HGroup(
            [
                ui.CheckBox({"Text": "Import", "ID": "Checkbox_Import_Snapshot"}),
                ui.CheckBox({"Text": "View on B buffer", "ID": "Checkbox_BBuffer"}),
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

checkbox_import_snapshot = itm['Checkbox_Import_Snapshot']
checkbox_bbuffer = itm['Checkbox_BBuffer']


# Add combobox items.
combo_view = itm['ComboBox_View']

previews = comp.GetPreviewList()
left_a_view = previews['LeftView'].GetConnectedOutput()
#left_b_view = previews['LeftView.B'].GetConnectedOutput()
right_a_view = previews['RightView'].GetConnectedOutput()
#right_b_view = previews['RightView.B'].GetConnectedOutput()

if left_a_view:
    combo_view.AddItem("Left")
if right_a_view:
    combo_view.AddItem("Right")


def checkbox_import_snapshot_changed(ev):
    itm['Checkbox_BBuffer'].Enabled = (checkbox_import_snapshot.Checked == 1)
dlg.On.Checkbox_Import_Snapshot.Clicked = checkbox_import_snapshot_changed


# Default settings.
combo_view.CurrentText = "Left"
checkbox_import_snapshot.Checked = True
checkbox_bbuffer.Checked = True

checkbox_import_snapshot = itm['Checkbox_Import_Snapshot']
checkbox_bbuffer = itm['Checkbox_BBuffer']


# The window was closed.
def _func(ev):
    disp.ExitLoop()
dlg.On.MyWin.Close = _func
dlg.On.Button_Cancel.Clicked = _func


# GUI element based event functions.
def _func(ev):
    selected_view = combo_view.CurrentText
    import_snapshot = checkbox_import_snapshot.Checked
    bbuffer = checkbox_bbuffer.Checked
    comp.Lock()
    take_snapshot(selected_view, import_snapshot, bbuffer)
    comp.Unlock()
    disp.ExitLoop()
dlg.On.Button_Ok.Clicked = _func


# Open the dialog.
dlg.Show()
disp.RunLoop()
dlg.Hide()