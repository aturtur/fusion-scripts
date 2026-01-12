"""
ar_CleanNodeNames

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Clean Node Names
Version: 1.2.0
Description-US: Cleans node names (eg. ..._1_1_1_1_1).

Note: Might take a long time to process if you have a huge composition.

Written for Blackmagic Design Fusion Studio 19.0 build 59.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.2.0 (04.09.2025) - Added support for frame render scripts, start render scripts and end render scripts.
                   - Prints now the process in the console.
1.1.0 (28.02.2025) - Improved the cleaning algorithm. Added expression handling.
1.0.0 (25.09.2024) - Initial release.
"""
# Libraries
import re
from collections import defaultdict


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()


def clean_and_serialize_node_names() -> dict[str, str]:
    """Cleans and renames nodes in a unique serialized order.
    Returns a mapping of old names to new names.
    """

    tools = comp.GetToolList(False).values()
    pattern = re.compile(r"^(.*?)(?:_?\d+)+$")  # Handles suffixes with or without underscores.
    tool_groups = defaultdict(list)
    name_map = {}
    counter = 0

    print("Updating tool name(s)...")

    # Step 1: Group tools by cleaned base name.
    for tool in tools:
        old_name = tool.Name
        match = pattern.match(old_name)
        base_name = match.group(1) if match else old_name  # Use cleaned name if matched.
        tool_groups[base_name].append(tool)

    # Step 2: Sort and rename with sequential numbers.
    for base_name, tool_list in tool_groups.items():
        tool_list.sort(key=lambda t: t.Name)  # Keep consistent order.

        for i, tool in enumerate(tool_list, start=1):
            new_name = f"{base_name}{i}"
            old_name = tool.Name
            tool.SetAttrs({'TOOLS_Name': new_name})
            if new_name != old_name:
                counter = counter + 1
            name_map[old_name] = new_name

    print(f"Updated {counter} tool name(s)!")

    return name_map


def update_expressions(name_map: dict[str, str]) -> None:
    """Updates all tool input expressions and scripts to reflect renamed nodes."""

    tools = comp.GetToolList(False).values()
    counter = 0

    print("Updating expressions and scripts...")

    for tool in tools:
        inputs = tool.GetInputList()

        # Update expressions.
        for input_name, inp in inputs.items():
            expression = inp.GetExpression()
            if expression:
                updated_expression = expression
                for old_name, new_name in sorted(name_map.items(), key=lambda x: -len(x[0])):
                    updated_expression = updated_expression.replace(old_name + ".", new_name + ".")                
                if updated_expression != expression:
                    inp.SetExpression(updated_expression)
                    counter = counter + 1
                    #print(f"Updated expression for {tool.Name}.{input_name}: {updated_expression}")
                    
        # Update frame render script.
        frame_render_script = tool.GetInput("FrameRenderScript")
        updated_frame_render_script = frame_render_script
        if updated_frame_render_script != None:
            for old_name, new_name in sorted(name_map.items(), key=lambda x: -len(x[0])):
                updated_frame_render_script = updated_frame_render_script.replace(old_name + ".", new_name + ".")
            if updated_frame_render_script != frame_render_script:
                tool.SetInput("FrameRenderScript", updated_frame_render_script)
                counter = counter + 1

        # Update start render script.
        start_render_script = tool.GetInput("StartRenderScript")
        updated_start_render_script = start_render_script
        if start_render_script != None:
            for old_name, new_name in sorted(name_map.items(), key=lambda x: -len(x[0])):
                updated_start_render_script = updated_start_render_script.replace(old_name + ".", new_name + ".")
            if updated_start_render_script != start_render_script:
                tool.SetInput("StartRenderScript", updated_start_render_script)
                counter = counter + 1

        # Update end render script.
        end_render_script = tool.GetInput("EndRenderScript")
        updated_end_render_script = end_render_script
        if end_render_script != None:
            for old_name, new_name in sorted(name_map.items(), key=lambda x: -len(x[0])):
                end_render_script = end_render_script.replace(old_name + ".", new_name + ".")
            if updated_end_render_script != start_render_script:
                tool.SetInput("EndRenderScript", updated_end_render_script)
                counter = counter + 1

    print(f"Updated {counter} expression(s)/script(s)!")


def main() -> None:
    """The main function."""

    comp.Lock()
    comp.StartUndo("Clean names")

    name_map = clean_and_serialize_node_names()
    update_expressions(name_map)

    print("Ready!")

    comp.EndUndo(True)
    comp.Unlock()


if __name__ == "__main__":
    main()