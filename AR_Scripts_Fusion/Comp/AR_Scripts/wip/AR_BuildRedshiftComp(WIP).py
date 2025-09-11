"""
AR_BuildRedshiftComp(WIP)

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Build Redshift Comp (WIP)
Version: 1.0.0
Description-US: Builds Redshift composition setup from given image sequence paths.

Written for Blackmagic Design Fusion Studio 19.0 build 59.
Python version 3 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Dependencies:
    - Cryptomatte (Fuse)
    - RS Camera Extractor (Fuse)

Changelog:
1.0.0 (02.09.2024) - Initial release.
"""
# Libraries
import os
import re

#import BlackmagicFusion as bmd


# Global variables
bmd = bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()

colors = {
    'Orange'   : {'R': 235.0/255.0, 'G': 110.0/255.0, 'B': 0.0/255.0},
    'Apricot'  : {'R': 255.0/255.0, 'G': 168.0/255.0, 'B': 51.0/255.0},
    'Yellow'   : {'R': 226.0/255.0, 'G': 169.0/255.0, 'B': 28.0/255.0},
    'Lime'     : {'R': 159.0/255.0, 'G': 198.0/255.0, 'B': 21.0/255.0},
    'Olive'    : {'R': 95.0/255.0,  'G': 153.0/255.0, 'B': 32.0/255.0},
    'Green'    : {'R': 64.0/255.0,  'G': 143.0/255.0, 'B': 101.0/255.0},
    'Teal'     : {'R': 0.0/255.0,   'G': 152.0/255.0, 'B': 153.0/255.0},
    'Navy'     : {'R': 21.0/255.0,  'G': 98.0/255.0,  'B': 132.0/255.0},
    'Blue'     : {'R': 121.0/255.0, 'G': 168.0/255.0, 'B': 208.0/255.0},
    'Purple'   : {'R': 153.0/255.0, 'G': 115.0/255.0, 'B': 160.0/255.0},
    'Violet'   : {'R': 149.0/255.0, 'G': 75.0/255.0,  'B': 205.0/255.0},
    'Pink'     : {'R': 233.0/255.0, 'G': 140.0/255.0, 'B': 181.0/255.0},
    'Tan'      : {'R': 185.0/255.0, 'G': 176.0/255.0, 'B': 151.0/255.0},
    'Beige'    : {'R': 198.0/255.0, 'G': 160.0/255.0, 'B': 119.0/255.0},
    'Brown'    : {'R': 153.0/255.0, 'G': 102.0/255.0, 'B': 0.0/255.0},
    'Chocolate': {'R': 140.0/255.0, 'G': 90.0/255.0,  'B': 63.0/255.0}
}

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


def get_frame_range(path):
    clean_path = re.sub(r'(.*?)(\d+)\.[a-zA-Z]+$', r'\1', path)
    file_name  = os.path.basename(clean_path)
    dir_path   = os.path.dirname(path)
    extension  = os.path.splitext(path)[1]

    found = False
    first_frame = 0
    last_frame  = 0

    file_name_pattern = rf"{re.escape(file_name)}\d+{re.escape(extension)}"
    digits_pattern = r'\d+(?!.*\d)'

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


def set_loader_global_in(loader, path):
    start_frame, end_frame = get_frame_range(path)
    length = end_frame - start_frame

    loader.SetInput("GlobalOut", end_frame)
    loader.SetInput("GlobalIn", start_frame)
    loader.SetInput("ClipTimeEnd", length)
    loader.SetInput("ClipTimeStart", 0)
    loader.SetInput("Holdlast_frame", 0)
    loader.SetInput("Holdfirst_frame", 0)
    
    return True


def create_aces_node(x, y):
    aces_transform = comp.AddTool("AcesTransform", x, y)
    aces_transform.SetAttrs({'AcesVersion' : 'ACES_VERSION_1_3_0'})
    aces_transform.SetAttrs({'InputTransform130' : 'IDT_ACESCG'})
    aces_transform.SetAttrs({'OutputTransform130' : 'ODT_SRGB'})

    return aces_transform


def create_sticky_note(name, comment, x, y):

    sticky_note = comp.AddTool("Note", x, y)
    sticky_note.SetAttrs({'TOOLS_Name': name})
    sticky_note.Comments[comp.CurrentTime] = comment

    return sticky_note


def search_passes(itm):
    folder_path = itm['FolderPath'].Text

    search_dict = {'Beauty'        : {'name' : 'Beauty',           'check' : False },
                   'Diffuse'       : {'name' : 'DiffuseLighting',  'check' : False },
                   'Reflections'   : {'name' : 'Reflections',      'check' : False },
                   'Refractions'   : {'name' : 'Refractions',      'check' : False },
                   'Specular'      : {'name' : 'SpecularLighting', 'check' : False },
                   'GI'            : {'name' : 'GI',               'check' : False },
                   'SSS'           : {'name' : 'SSS',              'check' : False },
                   'Emission'      : {'name' : 'Emission',         'check' : False },
                   'Volume'        : {'name' : 'VolumeLighting',   'check' : False },
                   'Caustics'      : {'name' : 'Caustics',         'check' : False },
                   'Cryptomatte'   : {'name' : 'Cryptomatte',      'check' : False },
                   'PuzzleMatte'   : {'name' : 'PuzzleMatte',      'check' : False },
                   'MotionVectors' : {'name' : 'MotionVectors',    'check' : False },
                   'Depth'         : {'name' : 'Z',                'check' : False },
                   'Normals'       : {'name' : 'N',                'check' : False },
                   'Position'      : {'name' : 'P',                'check' : False }
                   }

    preview_check = False
    for file in sorted(os.listdir(folder_path)):

        # Preview
        file_name, file_extension = os.path.splitext(file)
        if (file_extension == ".jpg") and (preview_check == False):
            itm['CHK_Preview'].Checked = True
            itm['EDT_Preview'].Text = os.path.join(folder_path, file)
            preview_check = True

        for key, value in search_dict.items():
            pass_name = value['name']
            pattern = rf".*{re.escape(pass_name)}\d+.*"
            if (re.match(pattern, file)) and (value['check'] == False):
                itm['CHK_'+key].Checked = True
                itm['EDT_'+key].Text = os.path.join(folder_path, file)
                value['check'] = True

    pass


def build_redshift_comp(itm):

    """ Beauty = (Diffuse Lighting + Global Illumination + SpecularLighting + Reflections + Refractions + Subsurface Scattering +
                 Emission + Background + Caustics) x Volume Tint + Volume Emission + Volume Lighting
    """

    # Node position stuff.
    x   = 0
    y   = 0
    gap = 1

    # Options.
    global_in_from_file = itm['CHK_GlobalInFromFile'].Checked
    extract_rs_camera  = itm['CHK_ExtractRSCamera'].Checked

    #start_frame = itm['NUM_start_frame'].Value

    # Preview.
    if itm['CHK_Preview'].Checked == True:
        path = itm['EDT_Preview'].Text
        loader = comp.AddTool("Loader", x, y)
        loader.SetInput("Clip", path)
        loader.TileColor = colors['Teal']

        if global_in_from_file:
            set_loader_global_in(loader, path)

        y = y + gap
    
    # Beauty.
    if itm['CHK_Beauty'].Checked == True:
        path = itm['EDT_Beauty'].Text
        loader = comp.AddTool("Loader", x, y)
        loader.SetInput("Clip", path)
        loader.TileColor = colors['Teal']
        
        if global_in_from_file:
            set_loader_global_in(loader, path)

        # Create sticky note.
        note_name    = "Note"
        start, end   = get_frame_range(path)
        note_comment = "%s - %s" % (str(start), str(end))
        
        create_sticky_note(note_name, note_comment, x - 1, y)

        # Extract Redshift Camera.
        if extract_rs_camera:
            try:
                rs_camera_extractor = comp.AddTool("Fuse.RSCameraExtractor", x + gap, y)

                camera_3d = comp.AddTool("Camera3D", x + gap + 1, y)
                camera_3d.AovType = 1
                camera_3d.AoV.SetExpression("self.ImageInput.Metadata.RSCameraFOV or self.ImageInput.Metadata['rs/camera/fov']")
                camera_3d.PlaneOfFocus.SetExpression("self.ImageInput.Metadata.RSCameraDOFFocusDistance or self.ImageInput.Metadata['rs/camera/DOFFocusDistance']")
                camera_3d.FilmGate = "HD"
                camera_3d.ApertureW = 1.6
                camera_3d.ApertureH = 0.9
                camera_3d.ImagePlaneEnabled = 0
                camera_3d.Transform3DOp.Translate.X.SetExpression("self.ImageInput.Metadata.Translate.X")
                camera_3d.Transform3DOp.Translate.Y.SetExpression("self.ImageInput.Metadata.Translate.Y")
                camera_3d.Transform3DOp.Translate.Z.SetExpression("self.ImageInput.Metadata.Translate.Z")
                camera_3d.Transform3DOp.Rotate.RotOrder = "ZXY"
                camera_3d.Transform3DOp.Rotate.X.SetExpression("self.ImageInput.Metadata.Rotate.X")
                camera_3d.Transform3DOp.Rotate.Y.SetExpression("self.ImageInput.Metadata.Rotate.Y")
                camera_3d.Transform3DOp.Rotate.Z.SetExpression("self.ImageInput.Metadata.Rotate.Z")

                merge3D = comp.AddTool("Merge3D", x + gap + 2, y)

                rs_camera_extractor.Input = loader.Output
                camera_3d.ImageInput = rs_camera_extractor.Output
                merge3D.SceneInput1 = camera_3d.Output

            except:
                print("Couldn't create extract RS Camera setup... Maybe missing RS Camera Extractor Fuse?")

        y = y + gap

    # ---
    y = y + gap
    # ---

    # Multi Passes.
    multi_passes = []

    if itm['CHK_Diffuse'].Checked == True:
        multi_passes.append([itm['EDT_Diffuse'].Text, "Diffuse"])

    if itm['CHK_Reflections'].Checked == True:
        multi_passes.append([itm['EDT_Reflections'].Text, "Reflections"])

    if itm['CHK_Refractions'].Checked == True:
        multi_passes.append([itm['EDT_Refractions'].Text, "Refractions"])

    if itm['CHK_Specular'].Checked == True:
        multi_passes.append([itm['EDT_Specular'].Text, "Specular"])

    if itm['CHK_GI'].Checked == True:
        multi_passes.append([itm['EDT_GI'].Text, "GI"])

    if itm['CHK_SSS'].Checked == True:
        multi_passes.append([itm['EDT_SSS'].Text, "SSS"])

    if itm['CHK_Emission'].Checked == True:
        multi_passes.append([itm['EDT_Emission'].Text, "Emission"])

    if itm['CHK_Volume'].Checked == True:
        multi_passes.append([itm['EDT_Volume'].Text, "Volume"])

    if itm['CHK_Caustics'].Checked == True:
        multi_passes.append([itm['EDT_Caustics'].Text, "Caustics"])

    # Create Multi Pass Loaders.
    multi_pass_loaders = []
    merge_nodes = []
    for i, thePass in enumerate(multi_passes):
        path = thePass[0]
        loader = comp.AddTool("Loader", x, y)
        loader.SetInput("Clip", path)
        loader.SetAttrs({'TOOLS_Name' : ''+str(thePass[1])+''})
        loader.TileColor = colors['Navy']

        if global_in_from_file:
            set_loader_global_in(loader, path)

        y = y + gap
        multi_pass_loaders.append(loader)

    # Create merge nodes and connect nodes.
    if len(multi_pass_loaders) > 1:
        for i, the_loader in enumerate(multi_pass_loaders):

            if i != 0:
                flow = comp.CurrentFrame.FlowView  # Get flow view.
                loader_x, loader_y = flow.GetPosTable(the_loader).values()  # Get node's position.
                merge = comp.AddTool("Merge", loader_x + gap, loader_y)
                merge.SetInput("Gain", 0)  # Set Alpha Gain to Add.
                merge_nodes.append(merge)

        for i, the_merge in enumerate(merge_nodes):
            if i == 0:  # First run.
                the_merge.Background = multi_pass_loaders[0].Output
                the_merge.Foreground = multi_pass_loaders[1].Output
            else:  # Not first run.
                the_merge.Background = merge_nodes[i-1].Output
                the_merge.Foreground = multi_pass_loaders[i+1].Output
    # ---
    y = y + gap
    # ---

    # Matte passes.

    # Cryptomatte.
    if itm['CHK_Cryptomatte'].Checked == True:
        path = itm['EDT_Cryptomatte'].Text
        loader = comp.AddTool("Loader", x, y)
        loader.SetInput("Clip", path)
        loader.SetAttrs({'TOOLS_Name' : 'Cryptomatte'})
        loader.TileColor = colors['Orange']

        if global_in_from_file:
            set_loader_global_in(loader, path)

        try:
            cryptomatte = comp.AddTool("Fuse.Cryptomatte", x + gap, y)
            cryptomatte.Input = loader.Output
        except:
            print("Couldn't create Cryptomatte node... Maybe missing Cryptomatte Fuse?")

        y = y + gap
        pass

    # Puzzle Matte.
    if itm['CHK_PuzzleMatte'].Checked == True:
        path = itm['EDT_PuzzleMatte'].Text
        loader = comp.AddTool("Loader", x, y)
        loader.SetInput("Clip", itm['EDT_PuzzleMatte'].Text)
        loader.SetAttrs({'TOOLS_Name' : 'PuzzleMatte'})
        loader.TileColor = colors['Orange']

        if global_in_from_file:
            set_loader_global_in(loader, path)

        red_channel = comp.AddTool("ChannelBoolean", x + (gap * 2), y)
        red_channel.SetAttrs({'TOOLS_Name' : 'RedChannel'})
        red_channel.SetInput("Operation", 0)   # Copy.
        red_channel.SetInput("ToRed",     5)   # Red BG.
        red_channel.SetInput("ToGreen",   5)   # Red BG.
        red_channel.SetInput("ToBlue",    5)   # Red BG.
        red_channel.SetInput("ToAlpha",   8)   # Alpha BG.

        green_channel = comp.AddTool("ChannelBoolean", x + (gap * 2), y + 1)
        green_channel.SetAttrs({'TOOLS_Name' : 'GreenChannel'})
        green_channel.SetInput("Operation", 0) # Copy.
        green_channel.SetInput("ToRed",     6) # Green BG.
        green_channel.SetInput("ToGreen",   6) # Green BG.
        green_channel.SetInput("ToBlue",    6) # Green BG.
        green_channel.SetInput("ToAlpha",   8) # Alpha BG.

        blue_channel = comp.AddTool("ChannelBoolean", x + (gap * 2), y + 2)
        blue_channel.SetAttrs({'TOOLS_Name' : 'BlueChannel'})
        blue_channel.SetInput("Operation", 0)  # Copy.
        blue_channel.SetInput("ToRed",     7)  # Blue BG.
        blue_channel.SetInput("ToGreen",   7)  # Blue BG.
        blue_channel.SetInput("ToBlue",    7)  # Blue BG.
        blue_channel.SetInput("ToAlpha",   8)  # Alpha BG.

        red_channel.Background = loader.Output
        green_channel.Background = loader.Output
        blue_channel.Background = loader.Output

        y = y + gap + 2
        pass

    # ---
    y = y + gap
    # ---

    # Info passes.

    # Motion Vectors.
    if itm['CHK_MotionVectors'].Checked == True:
        loader = comp.AddTool("Loader", x, y)
        loader.SetInput("Clip", itm['EDT_MotionVectors'].Text)
        loader.SetAttrs({'TOOLS_Name' : 'MotionVectors'})
        loader.TileColor = colors['Teal']

        if global_in_from_file:
            set_loader_global_in(loader, path)

        channel_booleans = comp.AddTool("ChannelBoolean", x + (gap * 2), y)
        channel_booleans.SetInput("Operation", 0)           # Copy.
        channel_booleans.SetInput("ToRed", 4)               # Do Nothing.
        channel_booleans.SetInput("ToGreen", 4)             # Do Nothing.
        channel_booleans.SetInput("ToBlue", 4)              # Do Nothing.
        channel_booleans.SetInput("ToAlpha", 4)             # Do Nothing.

        channel_booleans.SetInput("EnableExtraChannels", 1) # Enable Extra channels.
        channel_booleans.SetInput("ToXVector", 0)           # Red FG.
        channel_booleans.SetInput("ToYVector", 1)           # Green FG.
        channel_booleans.SetAttrs({'TOOLS_Name' : 'AddMotionVectors'})

        vector_motion_blur = comp.AddTool("VectorMotionBlur", x + (gap * 3), y)

        channel_booleans.Foreground = loader.Output
        vector_motion_blur.Input = channel_booleans.Output

        if len(merge_nodes) > 0:
            channel_booleans.Background = merge_nodes[-1].Output

        y = y + gap

        pass

    # Depth.
    if itm['CHK_Depth'].Checked == True:
        loader = comp.AddTool("Loader", x, y)
        loader.SetInput("Clip", itm['EDT_Depth'].Text)
        loader.SetAttrs({'TOOLS_Name' : 'Depth'})
        loader.TileColor = colors['Teal']

        if global_in_from_file:
            set_loader_global_in(loader, path)

        channel_booleans = comp.AddTool("ChannelBoolean", x + (gap * 2), y)
        channel_booleans.SetInput("Operation", 0)           # Copy.
        channel_booleans.SetInput("ToRed", 4)               # Do Nothing.
        channel_booleans.SetInput("ToGreen", 4)             # Do Nothing.
        channel_booleans.SetInput("ToBlue", 4)              # Do Nothing.
        channel_booleans.SetInput("ToAlpha", 4)             # Do Nothing.

        channel_booleans.SetInput("EnableExtraChannels", 1) # Enable Extra channels.
        channel_booleans.SetInput("ToZBuffer", 18)          # Z Buffer FG.
        channel_booleans.SetAttrs({'TOOLS_Name' : 'AddDepth'})

        channel_booleans.Foreground = loader.Output

        if len(merge_nodes) > 0:
            channel_booleans.Background = merge_nodes[-1].Output

        y = y + gap
        pass

    # Normals.
    if itm['CHK_Normals'].Checked == True:
        loader = comp.AddTool("Loader", x, y)
        loader.SetInput("Clip", itm['EDT_Normals'].Text)
        loader.SetAttrs({'TOOLS_Name' : 'Normals'})
        loader.TileColor = colors['Teal']

        if global_in_from_file:
            set_loader_global_in(loader, path)

        channel_booleans = comp.AddTool("ChannelBoolean", x + (gap * 2), y)
        channel_booleans.SetInput("Operation", 0)           # Copy.
        channel_booleans.SetInput("ToRed", 4)               # Do Nothing.
        channel_booleans.SetInput("ToGreen", 4)             # Do Nothing.
        channel_booleans.SetInput("ToBlue", 4)              # Do Nothing.
        channel_booleans.SetInput("ToAlpha", 4)             # Do Nothing.

        channel_booleans.SetInput("EnableExtraChannels", 1) # Enable Extra channels.
        channel_booleans.SetInput("ToXNormal", )            # Red FG.
        channel_booleans.SetInput("ToYNormal", )            # Green FG.
        channel_booleans.SetInput("ToZNormal", )            # Blue FG.
        channel_booleans.SetAttrs({'TOOLS_Name' : 'AddNormals'})

        channel_booleans.ForeGround = loader.Output

        y = y + gap
        pass

    # Position.
    if itm['CHK_Position'].Checked == True:
        loader = comp.AddTool("Loader", x, y)
        loader.SetInput("Clip", itm['EDT_Position'].Text)
        loader.SetAttrs({'TOOLS_Name' : 'Position'})
        loader.TileColor = colors['Teal']

        if global_in_from_file:
            set_loader_global_in(loader, path)

        y = y + gap
        pass

    pass


def ClearForms(itm):

    itm['CHK_Preview'].Checked = False
    itm['EDT_Preview'].Text = ""

    itm['CHK_Beauty'].Checked = False
    itm['EDT_Beauty'].Text = ""

    itm['CHK_Diffuse'].Checked = False
    itm['EDT_Diffuse'].Text = ""

    itm['CHK_Reflections'].Checked = False
    itm['EDT_Reflections'].Text = ""

    itm['CHK_Refractions'].Checked = False
    itm['EDT_Refractions'].Text = ""

    itm['CHK_Specular'].Checked = False
    itm['EDT_Specular'].Text = ""

    itm['CHK_GI'].Checked = False
    itm['EDT_GI'].Text = ""

    itm['CHK_SSS'].Checked = False
    itm['EDT_SSS'].Text = ""

    itm['CHK_Emission'].Checked = False
    itm['EDT_Emission'].Text = ""

    itm['CHK_Volume'].Checked = False
    itm['EDT_Volume'].Text = ""

    itm['CHK_Caustics'].Checked = False
    itm['EDT_Caustics'].Text = ""

    itm['CHK_Cryptomatte'].Checked = False
    itm['EDT_Cryptomatte'].Text = ""

    itm['CHK_PuzzleMatte'].Checked = False
    itm['EDT_PuzzleMatte'].Text = ""

    itm['CHK_MotionVectors'].Checked = False
    itm['EDT_MotionVectors'].Text = ""

    itm['CHK_Depth'].Checked = False
    itm['EDT_Depth'].Text = ""

    itm['CHK_Normals'].Checked = False
    itm['EDT_Normals'].Text = ""

    itm['CHK_Position'].Checked = False
    itm['EDT_Position'].Text = ""

    pass


#----------------------------------------------------------------------------------------------------------------
# Creating user interface.
#----------------------------------------------------------------------------------------------------------------
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


gui_geo = gui_geometry(600, 790, 0.5, 0.5)

ui   = fusion.UIManager
disp = bmd.UIDispatcher(ui)
dlg  = disp.AddWindow({"WindowTitle": "Build Redshift Comp",
                       "ID": "MyWin",
                       "Geometry": [gui_geo['x'], gui_geo['y'], gui_geo['width'], gui_geo['height']],
                       "Events": {"Close": True,
                                  "KeyPress": True,
                                  "KeyRelease": True},
                       },
    [
        ui.VGroup({"Spacing": 5},
        [
            # GUI elements
            #ui.VGap(),

            # Select folder path.
            ui.HGroup(
            [
                ui.Label({"Text": "Folder Path", "ID": "Label", "Weight": 0.1}),
                ui.LineEdit({"Text": "", "PlaceholderText": "Pleace Enter a Folder Path", "ID": "FolderPath", "Weight": 0.9}),
                ui.Button({"Text": "...", "ID": "BTN_Browse", "Weight": 0.1}),
            ]),

            ui.HGroup(
            [
                ui.Button({"Text": "Get Data", "ID": "BTN_Search", "Weight": 1}),
                ui.Button({"Text": "Clear Data", "ID": "BTN_Clear", "Weight": 1}),
            ]),

            # ---

            # Preview.
            ui.VGap(5),
            ui.Label({ "Text": "Main", "ID": "Label" }),

            # JPG Preview.
            ui.HGroup(
            [
                ui.CheckBox({"ID": "CHK_Preview", "Text": "Preview", "Weight": 0.1}),
                ui.LineEdit({"ID": "EDT_Preview",  "Text": "",       "Weight": 0.9, "PlaceholderText": "Preview",}),
                ui.Button({  "ID": "BTN_Preview", "Text": "...",     "Weight": 0.1}),
            ]),

            # Beauty.
            ui.HGroup(
            [
                ui.CheckBox({"ID": "CHK_Beauty", "Text": "Beauty", "Weight": 0.1 }),
                ui.LineEdit({"ID": "EDT_Beauty",  "Text": "",       "Weight": 0.9, "PlaceholderText": "Beauty",}),
                ui.Button({  "ID": "BTN_Beauty", "Text": "...",    "Weight": 0.1 }),
            ]),

            # ---

            # AOVs.
            ui.VGap(5),
            ui.Label({ "Text": "AOVs", "ID": "Label" }),

            # Diffuse Lighting.
            ui.HGroup(
            [
                ui.CheckBox({"ID": "CHK_Diffuse", "Text": "Diffuse", "Weight": 0.1}),
                ui.LineEdit({"ID": "EDT_Diffuse",  "Text": "",       "Weight": 0.9, "PlaceholderText": "Diffuse",}),
                ui.Button({  "ID": "BTN_Diffuse", "Text": "...",     "Weight": 0.1}),
            ]),

            # Reflections.
            ui.HGroup(
            [
                ui.CheckBox({"ID": "CHK_Reflections", "Text": "Reflections", "Weight": 0.1}),
                ui.LineEdit({"ID": "EDT_Reflections",  "Text": "",           "Weight": 0.9, "PlaceholderText": "Reflections",}),
                ui.Button({  "ID": "BTN_Reflections", "Text": "...",         "Weight": 0.1}),
            ]),

            # Refractions.
            ui.HGroup(
            [
                ui.CheckBox({"ID": "CHK_Refractions", "Text": "Refractions", "Weight": 0.1}),
                ui.LineEdit({"ID": "EDT_Refractions",  "Text": "",           "Weight": 0.9, "PlaceholderText": "Refractions",}),
                ui.Button({  "ID": "BTN_Refractions", "Text": "...",         "Weight": 0.1}),
            ]),

            # Specular Lighting.
            ui.HGroup(
            [
                ui.CheckBox({"ID": "CHK_Specular", "Text": "Specular", "Weight": 0.1}),
                ui.LineEdit({"ID": "EDT_Specular",  "Text": "",        "Weight": 0.9, "PlaceholderText": "Specular",}),
                ui.Button({  "ID": "BTN_Specular", "Text": "...",      "Weight": 0.1}),
            ]),

            # Global Illumination.
            ui.HGroup(
            [
                ui.CheckBox({"ID": "CHK_GI", "Text": "GI",  "Weight": 0.1}),
                ui.LineEdit({"ID": "EDT_GI",  "Text": "",   "Weight": 0.9, "PlaceholderText": "Global Illumination (GI)",}),
                ui.Button({  "ID": "BTN_GI", "Text": "...", "Weight": 0.1}),
            ]),

            # Subsurface Scattering.
            ui.HGroup(
            [
                ui.CheckBox({"ID": "CHK_SSS", "Text": "SSS", "Weight": 0.1 }),
                ui.LineEdit({"ID": "EDT_SSS",  "Text": "",   "Weight": 0.9, "PlaceholderText": "Subsurface Scattering (SSS)",}),
                ui.Button({  "ID": "BTN_SSS", "Text": "...", "Weight": 0.1 }),
            ]),

            # Emission.
            ui.HGroup(
            [
                ui.CheckBox({"ID": "CHK_Emission", "Text": "Emission", "Weight": 0.1 }),
                ui.LineEdit({"ID": "EDT_Emission",  "Text": "",        "Weight": 0.9, "PlaceholderText": "Emission",}),
                ui.Button({  "ID": "BTN_Emission", "Text": "...",      "Weight": 0.1 }),
            ]),

            # Volume Lighting.
            ui.HGroup(
            [
                ui.CheckBox({"ID": "CHK_Volume", "Text": "Volume", "Weight": 0.1}),
                ui.LineEdit({"ID": "EDT_Volume",  "Text": "",      "Weight": 0.9, "PlaceholderText": "Volume",}),
                ui.Button({  "ID": "BTN_Volume", "Text": "...",    "Weight": 0.1}),
            ]),

            # Caustics.
            ui.HGroup(
            [
                ui.CheckBox({"ID": "CHK_Caustics", "Text": "Caustics", "Weight": 0.1}),
                ui.LineEdit({"ID": "EDT_Caustics",  "Text": "",        "Weight": 0.9, "PlaceholderText": "Caustics",}),
                ui.Button({  "ID": "BTN_Caustics", "Text": "...",      "Weight": 0.1}),
            ]),

            # ---

            # Matte passes.
            ui.VGap(5),
            ui.Label({"Text": "Matte Passes", "ID": "Label"}),

            # Cryptomatte.
            ui.HGroup(
            [
                ui.CheckBox({"ID": "CHK_Cryptomatte", "Text": "Cryptomatte", "Weight": 0.1}),
                ui.LineEdit({"ID": "EDT_Cryptomatte",  "Text": "",           "Weight": 0.9, "PlaceholderText": "Cryptomatte",}),
                ui.Button({  "ID": "BTN_Cryptomatte", "Text": "...",         "Weight": 0.1}),
            ]),

            # Puzzle Matte.
            ui.HGroup(
            [
                ui.CheckBox({"ID": "CHK_PuzzleMatte", "Text": "Puzzle Matte", "Weight": 0.1}),
                ui.LineEdit({"ID": "EDT_PuzzleMatte",  "Text": "",            "Weight": 0.9, "PlaceholderText": "Puzzle Matte",}),
                ui.Button({  "ID": "BTN_PuzzleMatte", "Text": "...",          "Weight": 0.1}),
            ]),

            # ---

            # Info passes.
            ui.VGap(5),
            ui.Label({"Text": "Info Passes", "ID": "Label"}),

            # Motion Vectors.
            ui.HGroup(
            [
                ui.CheckBox({"ID": "CHK_MotionVectors", "Text": "Motion Vectors", "Weight": 0.1}),
                ui.LineEdit({"ID": "EDT_MotionVectors",  "Text": "",              "Weight": 0.9, "PlaceholderText": "Motion Vectors",}),
                ui.Button({  "ID": "BTN_MotionVectors", "Text": "...",            "Weight": 0.1}),
            ]),

            # Depth Pass (Z).
            ui.HGroup(
            [
                ui.CheckBox({"ID": "CHK_Depth", "Text": "Depth (Z)", "Weight": 0.1}),
                ui.LineEdit({"ID": "EDT_Depth",  "Text": "",         "Weight": 0.9, "PlaceholderText": "Depth (Z)",}),
                ui.Button({  "ID": "BTN_Depth", "Text": "...",       "Weight": 0.1}),
            ]),

            # Normals (N).
            ui.HGroup(
            [
                ui.CheckBox({"ID": "CHK_Normals", "Text": "Normals (N)", "Weight": 0.1}),
                ui.LineEdit({"ID": "EDT_Normals",  "Text": "",           "Weight": 0.9, "PlaceholderText": "Normals (N)",}),
                ui.Button({  "ID": "BTN_Normals", "Text": "...",         "Weight": 0.1}),
            ]),

            # Position (P).
            ui.HGroup(
            [
                ui.CheckBox({ "ID": "CHK_Position", "Text": "Position (P)", "Weight": 0.1}),
                ui.LineEdit({ "ID": "EDT_Position",  "Text": "",            "Weight": 0.9, "PlaceholderText": "Position (P)",}),
                ui.Button({   "ID": "BTN_Position", "Text": "...",          "Weight": 0.1}),
            ]),

            # ---

            # Options.
            ui.VGap(5),
            ui.Label({"Text": "Options", "ID": "Label"}),

            ui.HGroup(
            [
                ui.CheckBox({"ID": "CHK_StickyNote", "Text": "Create Sticky Note", "Weight": 0.1}),
                ui.CheckBox({"ID": "CHK_GlobalInFromFile", "Text": "Global In From File", "Weight": 0.1}),
                ui.CheckBox({"ID": "CHK_ExtractRSCamera", "Text": "Extract RS Camera", "Weight": 0.1}),
            ]),

            # ---

            # Build Redshift Composition.
            ui.VGap(15),
            ui.Button({"Text": "Build Comp", "ID": "BTN_Build", "Weight": 1}),

        ]),
    ])

itm = dlg.GetItems()  # Collect ui items.


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
# Browse folder path.
def _func(ev):
    selected_folder_path = fusion.RequestDir()
    if selected_folder_path:
        itm['FolderPath'].Text = str(selected_folder_path)
dlg.On.BTN_Browse.Clicked = _func


# Browse single pass.
def _func(ev):
    selected_file_path = fusion.RequestFile()
    if selected_file_path:
        single_passes = {
            'BTN_Preview' : 'EDT_Preview',
            'BTN_Beauty' : 'EDT_Beauty',
            'BTN_Diffuse' : 'EDT_Diffuse',
            'BTN_Reflection' : 'EDT_Reflection',
            'BTN_Refraction' : 'EDT_Refraction',
            'BTN_Specular' : 'EDT_Specular',
            'BTN_GI' : 'EDT_GI',
            'BTN_SSS' : 'EDT_SSS',
            'BTN_Emission' : 'EDT_Emission',
            'BTN_Volume' : 'EDT_Volume',
            'BTN_Caustics' : 'EDT_Caustics',
            'BTN_Cryptomatte' : 'EDT_Cryptomatte',
            'BTN_PuzzleMatte' : 'EDT_PuzzleMatte',
            'BTN_MotionVectors' : 'EDT_MotionVectors',
            'BTN_Depth' : 'EDT_Depth',
            'BTN_Normals' : 'EDT_Normals',
            'BTN_Position' : 'EDT_Position',
        }
        
        itm[single_passes[ev['who']]].Text = str(selected_file_path)
dlg.On.BTN_Preview.Clicked = _func
dlg.On.BTN_Beauty.Clicked = _func
dlg.On.BTN_Diffuse.Clicked = _func
dlg.On.BTN_Reflection.Clicked = _func
dlg.On.BTN_Refraction.Clicked = _func
dlg.On.BTN_Specular.Clicked = _func
dlg.On.BTN_GI.Clicked = _func
dlg.On.BTN_SSS.Clicked = _func
dlg.On.BTN_Emission.Clicked = _func
dlg.On.BTN_Volume.Clicked = _func
dlg.On.BTN_Caustics.Clicked = _func
dlg.On.BTN_Emission.Clicked = _func
dlg.On.BTN_Cryptomatte.Clicked = _func
dlg.On.BTN_PuzzleMatte.Clicked = _func
dlg.On.BTN_MotionVectors.Clicked = _func
dlg.On.BTN_Depth.Clicked = _func
dlg.On.BTN_Normals.Clicked = _func
dlg.On.BTN_Position.Clicked = _func


# Clear forms.
def _func(ev):
    ClearForms(itm)
dlg.On.BTN_Clear.Clicked = _func


# Search passes.
def _func(ev):
    search_passes(itm)
dlg.On.BTN_Search.Clicked = _func


# Build comp.
def _func(ev):
    comp.StartUndo("Build Redshift Comp")  # Start undo group.
    comp.Lock()  # Put composition to lock mode, so it won't open dialogs.
    build_redshift_comp(itm)
    comp.Unlock()  # Unlock composition.
    comp.EndUndo(True)  # End undo group.
dlg.On.BTN_Build.Clicked = _func


# Open the dialog.
dlg.Show()
disp.RunLoop()
dlg.Hide()