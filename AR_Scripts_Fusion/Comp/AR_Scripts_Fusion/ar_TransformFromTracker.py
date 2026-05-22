"""
ar_TransformFromTracker

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Transform From Tracker
Version: 1.1.0
Description-US: Creates a Transform tool from selected Tracker.

Written for Blackmagic Design Fusion Studio 21.0 beta build 31.
Python version 3.13.7 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.1.0 (20.05.2026) - Added custom tool for control the strength.
1.0.0 (04.05.2026) - Initial realease.
"""
# Libraries
...


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()

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


def tracker_to_transform(tracker_tool) -> None:
    """Creates a Transform tool from selected Tracker."""

    if tracker_tool.ID != "Tracker":
        print("Please select only a tracker tool!")
        return False
    
    tracker_name = tracker_tool.Name
    flow = comp.CurrentFrame.FlowView
    x, y = flow.GetPosTable(tracker_tool).values()
    
    # Custom Tool.
    custom_tool = comp.AddTool("Custom", x+2, y)
    custom_tool.SetAttrs({'TOOLS_Name': f"{tracker_name}Strength"})
    custom_name = custom_tool.Name

    # Custom Tool name inputs.
    custom_tool.SetInput("NameforPoint1", "Position")
    custom_tool.SetInput("NameforPoint2", "Axis")
    custom_tool.SetInput("NameforNumber1", "Size")
    custom_tool.SetInput("NameforNumber2", "Angle")
    custom_tool.SetInput("NameforNumber3", "X Strength")
    custom_tool.SetInput("NameforNumber4", "Y Strength")
    custom_tool.SetInput("NameforNumber5", "Size Strength")
    custom_tool.SetInput("NameforNumber6", "Angle Strength")
    custom_tool.SetInput("NameforNumber7", "Global Strength")    

    # Custom Tool expressions.
    custom_tool.PointIn1.SetExpression(f"Point(({tracker_name}.SteadyPosition.X-0.5)*(NumberIn3*NumberIn7)+0.5,({tracker_name}.SteadyPosition.Y-0.5)*(NumberIn4*NumberIn7)+0.5)")
    custom_tool.PointIn2.SetExpression(f"Point(({tracker_name}.SteadyAxis.X-0.5)*(NumberIn3*NumberIn7)+0.5,({tracker_name}.SteadyAxis.Y-0.5)*(NumberIn4*NumberIn7)+0.5)")
    custom_tool.NumberIn1.SetExpression(f"({tracker_name}.SteadySize-1)*(NumberIn5*NumberIn7)+1")
    custom_tool.NumberIn2.SetExpression(f"{tracker_name}.SteadyAngle*(NumberIn6*NumberIn7)")

    # Custom Tool hide inputs.
    custom_tool.SetInput("ShowNumber8", 0)
    custom_tool.SetInput("ShowPoint3", 0)
    custom_tool.SetInput("ShowPoint4", 0)
    custom_tool.SetInput("ShowLUT1", 0)
    custom_tool.SetInput("ShowLUT2", 0)
    custom_tool.SetInput("ShowLUT3", 0)
    custom_tool.SetInput("ShowLUT4", 0)

    # Custom Tool default values.
    custom_tool.SetInput("NumberIn3", 1)
    custom_tool.SetInput("NumberIn4", 1)
    custom_tool.SetInput("NumberIn5", 1)
    custom_tool.SetInput("NumberIn6", 1)
    custom_tool.SetInput("NumberIn7", 1)

    # Transform.
    transform_tool = comp.AddTool("Transform", x+3, y)
    transform_tool.SetAttrs({'TOOLS_Name': f"{tracker_name}Transform"})

    # Transform expressions.   
    transform_tool.Center.SetExpression(f"Point({custom_name}.PointIn1.X, {custom_name}.PointIn1.Y)")
    transform_tool.Pivot.SetExpression(f"Point({custom_name}.PointIn2.X, {custom_name}.PointIn2.X)")
    transform_tool.Size.SetExpression(f"{custom_name}.NumberIn1")
    transform_tool.Angle.SetExpression(f"{custom_name}.NumberIn2")

    # Transform default values.
    transform_tool.SetInput("InvertTransform", 1)


def main() -> None:
    """The main function."""
    
    comp.Lock()
    comp.StartUndo("Transform from Tracker")

    tool = comp.ActiveTool()
    tracker_to_transform(tool)

    comp.EndUndo(True)
    comp.Unlock()


if __name__ == "__main__":
    main()