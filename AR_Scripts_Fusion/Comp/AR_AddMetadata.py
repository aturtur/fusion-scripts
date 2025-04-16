"""
AR_AddMetadata

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Add Metadata
Version: 1.2.0
Description-US: Adds metadata nodes to the composition.

Note: Grouping requires pyautogui module.

Written for Blackmagic Design Fusion Studio 19.0.3 build 3
Python version 3.10.8 (64-bit)

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.2.0 (14.04.2025) - Fixed bug if tool is not active.
                   - Group is now named.
                   - Added Fusion version preset.
1.1.0 (11.04.2025) - Added pyautogui grouping function.
1.0.0 (09.11.2024) - Initial release.
"""
# Libraries
import os

try:
    import pyautogui
except:
    pass



# Global variables
bmd = bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()

prefix = ""
suffix = ""

# Functions
def connect_metadata(metadata_nodes: list) -> None:
    """Connects given metadata nodes."""

    tool = None

    try:
        tool = comp.ActiveTool()
    except:
        pass
    
    flow = comp.CurrentFrame.FlowView

    pos_x = 0
    pos_y = 0
    
    if tool:
        pos_x, pos_y = flow.GetPosTable(tool).values()

    for i, metadata_node in enumerate(metadata_nodes):
        flow.SetPos(metadata_node, pos_x + 1 + i, pos_y)
        if i == 0:
            if tool != None:
                metadata_node.Input = tool.Output
                flow.Select()
        if i != 0:
            metadata_node.Input = metadata_nodes[i-1].Output
        flow.Select(metadata_node)
            

def add_metadata(itm: list) -> any:
    """Adds metadata nodes in the composition and returns them as a list."""

    metadata_nodes = []

    if itm['Checkbox_Custom1'].Checked:
        key = itm['Key1'].Text
        value = itm['Value1'].Text

        md_custom1 = comp.AddTool("Fuse.SetMetaData")
        md_custom1.SetInput("FieldName", key)
        md_custom1.SetInput("FieldValue", value)
        md_custom1.SetAttrs({'TOOLS_Name': 'Metadata_' + key})
        metadata_nodes.append(md_custom1)

    if itm['Checkbox_Custom2'].Checked:
        key = itm['Key2'].Text
        value = itm['Value2'].Text

        md_custom2 = comp.AddTool("Fuse.SetMetaData")
        md_custom2.SetInput("FieldName", key)
        md_custom2.SetInput("FieldValue", value)
        md_custom2.SetAttrs({'TOOLS_Name': 'Metadata_' + key})
        metadata_nodes.append(md_custom2)

    if itm['Checkbox_Custom3'].Checked:
        key = itm['Key3'].Text
        value = itm['Value3'].Text

        md_custom3 = comp.AddTool("Fuse.SetMetaData")
        md_custom3.SetInput("FieldName", key)
        md_custom3.SetInput("FieldValue", value)
        md_custom3.SetAttrs({'TOOLS_Name': 'Metadata_' + key})
        metadata_nodes.append(md_custom3)

    if itm['Checkbox_Custom4'].Checked:
        key = itm['Key4'].Text
        value = itm['Value4'].Text

        md_custom4 = comp.AddTool("Fuse.SetMetaData")
        md_custom4.SetInput("FieldName", key)
        md_custom4.SetInput("FieldValue", value)
        md_custom4.SetAttrs({'TOOLS_Name': 'Metadata_' + key})
        metadata_nodes.append(md_custom4)

    if itm['Checkbox_Compname'].Checked:
        key = "COMP_NAME"

        md_compname = comp.AddTool("Fuse.SetMetaData")
        md_compname.SetInput("FieldName", key)
        md_compname.FieldValue.SetExpression("Text(comp.Name)")
        md_compname.SetAttrs({'TOOLS_Name': 'Metadata_' + key})
        metadata_nodes.append(md_compname)

    if itm['Checkbox_Comppath'].Checked:
        key = "COMP_PATH"

        md_comppath = comp.AddTool("Fuse.SetMetaData")
        md_comppath.SetInput("FieldName", key)
        md_comppath.FieldValue.SetExpression("Text(comp.Filename)")
        md_comppath.SetAttrs({'TOOLS_Name': 'Metadata_' + key})
        metadata_nodes.append(md_comppath)

    if itm['Checkbox_Username'].Checked:
        key = "USER_NAME"

        md_username = comp.AddTool("Fuse.SetMetaData")
        md_username.SetInput("FieldName", key)
        md_username.FieldValue.SetExpression("Text(os.getenv('USERNAME'))")
        md_username.SetAttrs({'TOOLS_Name': 'Metadata_' + key})
        metadata_nodes.append(md_username)

    if itm['Checkbox_Computername'].Checked:
        key = "COMPUTER_NAME"

        md_computername = comp.AddTool("Fuse.SetMetaData")
        md_computername.SetInput("FieldName", key)
        md_computername.FieldValue.SetExpression("Text(os.getenv('COMPUTERNAME'))")
        md_computername.SetAttrs({'TOOLS_Name': 'Metadata_' + key})
        metadata_nodes.append(md_computername)

    if itm['Checkbox_Fusionversion'].Checked:
        key = "FUSION_VERSION"

        md_fusionversion = comp.AddTool("Fuse.SetMetaData")
        md_fusionversion.SetInput("FieldName", key)
        md_fusionversion.FieldValue.SetExpression("Text(bmd._VERSION)")
        md_fusionversion.SetAttrs({'TOOLS_Name': 'Metadata_' + key})
        metadata_nodes.append(md_fusionversion)

    return metadata_nodes


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


gui_geo = gui_geometry(400, 345, 0.5, 0.5)


# GUI
ui   = fusion.UIManager
disp = bmd.UIDispatcher(ui)
dlg  = disp.AddWindow({"WindowTitle": "Add Metadata",
                       "ID": "MyWin",
                       "Geometry": [gui_geo['x'], gui_geo['y'], gui_geo['width'], gui_geo['height']],
                       },
    [
        ui.VGroup({"Spacing": 5},
        [
            # GUI elements.
            ui.VGroup(
            [
                ui.Label({"Text": "Custom", "ID": "Label"}),
                ui.HGroup(
                [
                    ui.CheckBox({"Text": "Custom 1", "ID": "Checkbox_Custom1", "Weight": 0.1}),
                    ui.LineEdit({"Text": "", "PlaceholderText": "Key", "ID": "Key1"}),
                    ui.LineEdit({"Text": "", "PlaceholderText": "Value", "ID": "Value1"}),
                ]),
                ui.HGroup(
                [
                    ui.CheckBox({"Text": "Custom 2", "ID": "Checkbox_Custom2", "Weight": 0.1}),
                    ui.LineEdit({"Text": "", "PlaceholderText": "Key", "ID": "Key2"}),
                    ui.LineEdit({"Text": "", "PlaceholderText": "Value", "ID": "Value2"}),
                ]),
                ui.HGroup(
                [
                    ui.CheckBox({"Text": "Custom 3", "ID": "Checkbox_Custom3", "Weight": 0.1}),
                    ui.LineEdit({"Text": "", "PlaceholderText": "Key", "ID": "Key3"}),
                    ui.LineEdit({"Text": "", "PlaceholderText": "Value", "ID": "Value3"}),
                ]),
                ui.HGroup(
                [
                    ui.CheckBox({"Text": "Custom 4", "ID": "Checkbox_Custom4", "Weight": 0.1}),
                    ui.LineEdit({"Text": "", "PlaceholderText": "Key", "ID": "Key4"}),
                    ui.LineEdit({"Text": "", "PlaceholderText": "Value", "ID": "Value4"}),
                ]),
                
            ]),

            ui.VGroup(
            [
                ui.Label({"Text": "Presets", "ID": "Label"}),
                ui.HGroup(
                [
                    ui.CheckBox({"Text": "Composition Name", "ID": "Checkbox_Compname"}),
                    ui.CheckBox({"Text": "Computer User Name", "ID": "Checkbox_Username"}),
                ]),

                ui.HGroup(
                [
                    ui.CheckBox({"Text": "Composition File Path", "ID": "Checkbox_Comppath"}),
                    ui.CheckBox({"Text": "Computer Name", "ID": "Checkbox_Computername"}),
                ]),

                ui.HGroup(
                [
                    ui.CheckBox({"Text": "Fusion Version", "ID": "Checkbox_Fusionversion"}),
                    #ui.CheckBox({"Text": "Computer Name", "ID": "Checkbox_Computername"}),
                ]),

            ]),

            ui.VGap(10),

            ui.VGroup(
            [
                ui.Label({"Text": "Options", "ID": "Label"}),
                ui.CheckBox({"Text": "Group", "ID": "Checkbox_Group"}),
            ]),
            
            # Add and Cancel buttons.
            ui.HGroup(
            [
                ui.Button({"Text": "Add", "ID": "Button_Add"}),
                ui.Button({"Text": "Cancel", "ID": "Button_Cancel"}),
            ]),

        ]),
    ])


# Collect ui items.
itm = dlg.GetItems()
group = False


# Default values.
itm['Checkbox_Custom1'].Checked = True
itm['Key1'].Text = "Artist"
itm['Value1'].Text = os.getenv("USERNAME")


# The window was closed.
def _func(ev):
    disp.ExitLoop()
dlg.On.MyWin.Close = _func
dlg.On.Button_Cancel.Clicked = _func


# Add metadata.
def _func(ev):
    global group

    metadata_nodes = add_metadata(itm)
    group = itm['Checkbox_Group'].Checked
    connect_metadata(metadata_nodes)
    disp.ExitLoop()
dlg.On.Button_Add.Clicked = _func


# Open the dialog.
dlg.Show()
disp.RunLoop()
dlg.Hide()


# Grouping.
if group == True:
    try:
        pyautogui.hotkey('ctrl', 'g')
        group_node = comp.ActiveTool()
        group_node.SetAttrs({'TOOLS_Name': 'Metadata'})

        try:
            source_node = group_node.Input1.GetConnectedOutput().GetTool()
            flow = comp.CurrentFrame.FlowView
            pos_x, pos_y = flow.GetPosTable(source_node).values()
            flow.SetPos(group_node, pos_x + 2, pos_y)
        except:
            pass

    except:
        pass