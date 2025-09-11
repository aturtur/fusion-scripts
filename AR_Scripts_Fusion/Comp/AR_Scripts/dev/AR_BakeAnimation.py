"""
AR_BakeAnimation(WIP)

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Bake Animation (WIP)
Version: 1.0.0
Description-US: Bakes animation from selected tool.

Written for Blackmagic Design Fusion Studio 19.0.3 build 3.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.0.0 (07.09.2025) - Initial release.
"""
# Global variables
bmd = bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()


tool = comp.ActiveTool

if not tool:
    comp.AskUser("Tool Script Error", {
        "description": {
            "Name": "description",
            "Control": "Text",
            "Lines": 5,
            "Default": "This is a tool script, you must select a tool in the flow to run this script",
            "ReadOnly": True,
            "Wrap": True,
        }
    })
    exit()

# We can't bake DT_Image or DT_Mask (and possibly others...)
unbakeable = {"Image": True, "Mask": True, "Particles": True, "DataType3D": True}

# Generate a list of inputs that are animated
inputs = []
input_id = []
for inp in tool.GetInputList().values():
    if inp.GetConnectedOutput() or inp.GetExpression():
        if inp.GetAttrs()["INPS_DataType"] not in unbakeable:
            inputs.append(inp.Name)
            input_id.append(inp.ID)

if not inputs:
    comp.AskUser("Nothing to Bake", {
        "description": {
            "Name": "description",
            "Control": "Text",
            "Lines": 5,
            "Default": "This tool has no inputs which can be baked by this script.",
            "ReadOnly": True,
            "Wrap": True,
        }
    })
    exit()

# Ask the user which input, and how often to set keyframes
settings = comp.AskUser("Bake Animation", {
    "Input": {
        "Name": "Input",
        "Control": "Dropdown",
        "Options": inputs
    },
    "Step": {
        "Name": "Step",
        "Control": "Slider",
        "Integer": True,
        "Default": 1,
        "Min": 1,
        "Max": 10,
    }
})

if settings:
    comp.Lock()
    comp.StartUndo("Bake Animation")

    inpname = input_id[settings["Input"] + 1]
    inp = tool[inpname]
    inpattrs = inp.GetAttrs()

    # Get the range to process from render range
    compattrs = comp.GetAttrs()
    start_frame = compattrs["COMPN_RenderStart"]
    end_frame = compattrs["COMPN_RenderEnd"]
    step = settings["Step"]

    # Record keyframes into a table for later use
    keyframes = {}
    print(f"Recording {(end_frame - start_frame + 1) / step} keyframes from {inp.Name}...")
    for i in range(start_frame, end_frame + 1, step):
        keyframes[i] = inp[i]

    # Create an appropriate modifier.
    # We assume BezierSpline unless it's a DT_Point, then we use a Path
    if inpattrs["INPS_DataType"] == "Point":
        modifier = comp.Path({})
    else:
        modifier = comp.BezierSpline({})

    if tool[inpname].GetExpression():
        tool[inpname].SetExpression(None)

    # Now connect it up. This removes the old modifier
    tool[inpname] = modifier

    # Now set the keyframes back in
    print("Baking keyframes...")
    for i in range(start_frame, end_frame + 1, step):
        inp[i] = keyframes[i]
    print("Done.")

    comp.EndUndo(True)
    comp.Unlock()