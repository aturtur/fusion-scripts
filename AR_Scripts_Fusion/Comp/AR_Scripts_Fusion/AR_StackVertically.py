"""
AR_StackVertically

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Stack Vertically
Version: 1.0.0
Description-US: Stack selected tools vertically, based on node positions in Flow.

Written for Blackmagic Design Fusion Studio 19.0.3 build 3.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.0.0 (17.09.2025) - Initial release.
"""
# Libraries
import math


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()


# Functions
def interpolate(value: float, x1: float, x2: float, y1: float, y2: float) -> float:
    """Perform linear interpolation for value between (x1,y1) and (x2,y2)."""

    return ((y2 - y1) * value + x2 * y1 - x1 * y2) / (x2 - x1)


def stack_vertically(align: str) -> None:
    """"Stack selected tools vertically, based on node positions in Flow."""

    tools = comp.GetToolList(True).values()
    flow = comp.CurrentFrame.FlowView
    
    tool_data = []
    default_width = 1920
    default_height = 1080

    for tool in tools:
        tool_width = tool.GetAttrs("TOOLI_ImageWidth") or default_width
        tool_height = tool.GetAttrs("TOOLI_ImageHeight") or default_height
        x, y = flow.GetPosTable(tool).values()

        tool_data.append({
            "tool": tool,
            "x": x,
            "y": y,
            "tool_width": tool_width,
            "tool_height": tool_height
        })

    if not tool_data:
        print("No selected tools.")
        return
    
    tool_data.sort(key=lambda t: t["y"], reverse=True)
    total_height = sum(t["tool_height"] for t in tool_data)
    max_width = max(t["tool_width"] for t in tool_data)

    main_tool = tool_data[0]
    multimerge_node = comp.AddTool("MultiMerge", main_tool["x"]+4, main_tool["y"]+4)
    layer_index = 1
    prev_step = 0

    for i, item in enumerate(tool_data):
        tool = item["tool"]

        if i == 0:
            multimerge_node.Background = tool.Output
        else:
            step_x = interpolate(0.5, 0, main_tool["tool_width"], 0, item["tool_width"])
            step_y = interpolate(0.5, 0, main_tool["tool_height"], 0, item["tool_height"])
            
            pos_y = interpolate(1, 0, 1, 0.5, 1 + step_y + prev_step)

            if align == "Right":
                pos_x = interpolate(1, 0, 1, 0.5, 1 - step_x)

            elif align == "Center":
                pos_x = interpolate(1, 0, 1, 0.5, 0.5)

            elif align == "Left":
                pos_x = interpolate(1, 0, 1, 0.5, step_x)

            multimerge_node.ConnectInput(f"Layer{layer_index}.Foreground", tool.Output)
            multimerge_node.SetInput(f"Layer{layer_index}.Center", {1: pos_x, 2: pos_y})
            
            layer_index += 1

            prev_step += (step_y * 2)


    crop_node = comp.AddTool("Crop", main_tool["x"]+5, main_tool["y"]+4)
    crop_node.SetInput("XSize", max_width)
    crop_node.SetInput("YSize", total_height)
    
    if align == "Right":
        crop_node.SetInput("XOffset", -(max_width - main_tool["tool_width"]))
    elif align == "Center":
        crop_node.SetInput("XOffset", -(max_width - main_tool["tool_width"]) / 2)
    elif align == "Left":
        pass
    
    crop_node.SetInput("KeepAspect", 0)
    crop_node.SetInput("KeepCentered", 0)
    crop_node.SetInput("ChangePixelAspect", 0)
    crop_node.SetInput("ClippingMode", "Frame")

    crop_node.Input = multimerge_node.Output
    

def main() -> None:
    """The main function."""

    comp.StartUndo("Stack Vertically")

    align = "Left"
    stack_vertically(align)
    comp.EndUndo(True)


if __name__ == "__main__":
    main()