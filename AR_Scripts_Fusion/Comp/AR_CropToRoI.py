"""
AR_CropToRoI

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Crop To RoI
Version: 1.0.0
Description-US: Crops the canvas to the active viewport's region of interest.

Written for Blackmagic Design Fusion Studio 19.0.3 build 3.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.0.0 (12.03.2025) - Initial realease.
"""
# Libraries
...


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()


# Functions
def interpolate(value: float, x1: float, x2: float, y1: float, y2: float):
    """Perform linear interpolation for value between (x1,y1) and (x2,y2)."""

    return ((y2 - y1) * value + x2 * y1 - x1 * y2) / (x2 - x1)


def crop_to(tool, values) -> any:
    """Creates a crop node and crops with given values."""
    
    x1 = values['left']
    x2 = values['right']
    y1 = values['bot']
    y2 = values['top']

    flow = comp.CurrentFrame.FlowView
    x, y = flow.GetPosTable(tool).values()
    crop_node = comp.AddTool("Crop", x+1, y+1)
    crop_node.SetAttrs({'TOOLS_Name': "CropToRoI"})

    crop_node.SetInput("XOffset", x1)
    crop_node.SetInput("YOffset", y1)

    new_width = x2-x1
    new_height = y2-y1

    crop_node.SetInput("XSize", new_width)
    crop_node.SetInput("YSize", new_height)

    crop_node.SetInput("KeepAspect", 0)
    crop_node.SetInput("KeepCentered", 0)
    crop_node.SetInput("ChangePixelAspect", 0)
    crop_node.SetInput("ClippingMode", "Frame")

    return crop_node


def get_region_data(view, tool) -> dict:
    """Gets region data of the currently active window.
    Returns region points in pixels (based on the given tool's image dimensions).
    """

    #print(view)
    #previews = comp.CurrentFrame.GetPreviewList()
    #left_a_view = previews['LeftView'].View
    #left_b_view = previews['LeftView.B'].View
    #right_a_view = previews['RightView'].View
    #right_b_view = previews['RightView.B'].View

    width = tool.GetAttrs("TOOLI_ImageWidth")
    height = tool.GetAttrs("TOOLI_ImageHeight")

    view_prefs = view.GetPrefs()
    try:
        region = view_prefs['Viewer']['Region']
        roi_enabled = region['Enable']

        if roi_enabled == False:
            print("RoI not enabled.")
            return None
        else:
            roi_left = region['Left']
            roi_bot = region['Bottom']
            roi_right = region['Right']
            roi_top = region['Top']

            region_values = {
                'left': int(interpolate(roi_left, 0, 1, 0, width)),
                'top': int(interpolate(roi_top, 0, 1, 0, height)),
                'right': int(interpolate(roi_right, 0, 1, 0, width)),
                'bot': int(interpolate(roi_bot, 0, 1, 0, height))
            }

            #view.EnableRoI(False)  # Disable region of interest.
            return region_values

    except:
        print("No region found.")
        return None
    

def keep_in_place(tool, region_values) -> any:
    """Creates a transform node that keeps source in place with given values."""

    x1 = region_values['left']
    x2 = region_values['right']
    y1 = region_values['bot']
    y2 = region_values['top']

    width = tool.GetAttrs("TOOLI_ImageWidth")
    height = tool.GetAttrs("TOOLI_ImageHeight")

    center_x = (x1 + x2) / 2
    center_y = (y1 + y2) / 2

    remapped_center_x = (center_x - 0) / (width - 0)
    remapped_center_y = (center_y - 0) / (height - 0)

    transform_x = 0.5 + ((remapped_center_x - 0.5) * (width / (x2-x1)))
    transform_y = 0.5 + ((remapped_center_y - 0.5) * (height / (y2-y1)))

    flow = comp.CurrentFrame.FlowView
    x, y = flow.GetPosTable(tool).values()
    transform_node = comp.AddTool("Transform", x+2, y+1)
    transform_node.SetInput("Center", {1: transform_x, 2: transform_y, 3: 0.0})

    return transform_node


def crop_to_roi() -> None:
    """Crops the canvas to the region of interest.
    Creates also transform node that keeps cropped area in place.
    """

    try:
        tool = comp.ActiveTool()
    
    except:
        print("No active node found!")
        return None
        
    active_view = comp.CurrentFrame.CurrentView
    region_values = get_region_data(active_view, tool)
    crop_node = crop_to(tool, region_values)
    transform_node = keep_in_place(tool, region_values)

    flow = comp.CurrentFrame.FlowView
    x, y = flow.GetPosTable(tool).values()
    merge_node = comp.AddTool("Merge", x+2, y)

    crop_node.Input = tool.Output
    transform_node.Input = crop_node.Output
    crop_node.Input = tool.Output
    merge_node.Background = tool.Output
    merge_node.Foreground = transform_node.Output
    

def main() -> None:
    """The main function."""

    comp.Lock()
    comp.StartUndo("Crop to RoI")

    crop_to_roi()

    comp.EndUndo(True)
    comp.Unlock()


if __name__ == "__main__":
    main()