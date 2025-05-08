"""
AR_JoinTiles

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Join Tiles
Version: 1.0.0
Description-US: Merges selected tools into one big image, based on node positions in Flow.

Written for Blackmagic Design Fusion Studio 19.0.3 build 3.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.0.0 (25.03.2025) - Initial release.
"""
# Libraries
import math


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()


# Functions
def join_tiles() -> None:
    """"Merges selected node into one big image, based on node position."""

    tools = comp.GetToolList(True).values()
    flow = comp.CurrentFrame.FlowView
    
    positions = {}
    default_width = 1920
    default_height = 1080

    for tool in tools:
        tool_width = tool.GetAttrs("TOOLI_ImageWidth") or default_width
        tool_height = tool.GetAttrs("TOOLI_ImageHeight") or default_height
        x, y = flow.GetPosTable(tool).values()
        x, y = math.floor(x), math.floor(y)
        positions[(x, y)] = (tool, tool_width, tool_height)

    if not positions:
        print("No selected tools.")
        return

    min_x = min(x for x, y in positions)
    max_x = max(x for x, y in positions)
    min_y = min(y for x, y in positions)
    max_y = max(y for x, y in positions)

    grid_width = max_x - min_x + 1
    grid_height = max_y - min_y + 1

    first_tool = next(iter(positions.values()), (None, default_width, default_height))
    _, tool_width, tool_height = first_tool
    
    background_width = grid_width * tool_width
    background_height = grid_height * tool_height

    background_node = comp.AddTool("Background")
    background_node.Width = background_width
    background_node.Height = background_height

    multimerge_node = comp.AddTool("MultiMerge")
    multimerge_node.Background = background_node.Output

    grid = [[None for _ in range(grid_width)] for _ in range(grid_height)]

    for (x, y), (tool, tool_width, tool_height) in positions.items():
        grid_y = y - min_y
        grid_x = x - min_x
        grid[grid_y][grid_x] = tool

    layer_index = 1
    for grid_y in range(grid_height):
        for grid_x in range(grid_width):
            tool = grid[grid_y][grid_x]
            if tool:
                multimerge_node.ConnectInput(f"Layer{layer_index}.Foreground", tool.Output)
                transform_x = (grid_x + 0.5) / grid_width
                transform_y = (grid_height - grid_y - 0.5) / grid_height

                multimerge_node.SetInput(f"Layer{layer_index}.Center", {1: transform_x, 2: transform_y})

                layer_index += 1


def main() -> None:
    """The main function."""

    comp.StartUndo("Join tiles")
    join_tiles()
    comp.EndUndo(True)


if __name__ == "__main__":
    main()