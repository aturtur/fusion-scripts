"""
AR_Trackers(Points)ToGridWarp

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Tracker's Points To GridWarp
Version: 1.0.0
Description-US: Connects Tracker's points to GridWarp's published points.

How to use: Select the Tracker and the GridWarp tools and run the script.
            Make sure the point count is same in Tracker and GridWarp (published points).
            Tracker point IDs starts from 1 and GridWarp point IDs starts from 0.

Note:       Use clean Tracker and clean GridWarp!
            Tracker point count and count of published GridWarp points must be the same!
            Order of the points must be the same!

Written for Blackmagic Design Fusion Studio 19.1.4 build 6.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.0.0 (02.04.2025) - Initial realease.
"""
# Libraries
...


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()


# Functions
def assign_tracker_to_gridwarp_points(gridwarp, tracker) -> list:
    """Assigns Tracker's points to GridWarp's published points using current time as a reference frame."""

    gridwarp_inputs = gridwarp.GetInputList().values()

    for inp in gridwarp_inputs:
        if inp.Name.startswith("Point "):
            point_num = int(inp.Name.replace("Point ", ""))
            #point_values = gridwarp.GetInput(inp.Name)
            #point_x = point_values[1]
            #point_y = point_values[2]
            inp.SetExpression(f"Point({tracker.Name}.TrackedCenter{point_num+1}.X+{tracker.Name}.XOffset{point_num+1}, {tracker.Name}.TrackedCenter{point_num+1}.Y+{tracker.Name}.YOffset{point_num+1})")


def main() -> None:
    """The main function."""
    
    comp.StartUndo("ConnectTrackerToGridWarp")

    tools = comp.GetToolList(False).values()

    tracker = None
    gridwarp = None

    for tool in tools:
        if tool.ID == "Tracker":
            tracker = tool
        if tool.ID == "GridWarp":
            gridwarp = tool

    if tracker is not None and gridwarp is not None:
        assign_tracker_to_gridwarp_points(gridwarp, tracker)

    comp.EndUndo(True)

if __name__ == "__main__":
    main()





# Point(Tracker2_1.TrackedCenter1.X+Tracker2_1.XOffset1, Tracker2_1.TrackedCenter1.Y+Tracker2_1.YOffset1)

# Leftover scripts

#tracker_outputs = tracker.GetOutputList().values()
#for tracker_output in tracker_outputs:
    #print(tracker_output.Name)
    #if tracker_output.Name == "Unsteady Position":
        #tracker_unsteady_position_values = tracker_output[comp.CurrentTime]
        #tracker_unsteady_pos_x = tracker_unsteady_position_values[1]
        #tracker_unsteady_pos_y = tracker_unsteady_position_values[2]
        
#print(gridwarp_points_list)
# Published grid warp data.
# GridWarp[i]Point[j].X
# GridWarp[i]Point[j].Y

#gridwarp.SetInput("")

#print(gridwarp_points_list)
#for point in gridwarp_points_list:
    #point_values = gridwarp.GetInput(point)
    #point_x = point_values[1]
    #point_y = point_values[2]

    #print(point_x, point_y)

    #point_num = int(point.replace("Point ", ""))
    #print(point_num)
    #gridwarp.GetInput(point).SetExpression(f"Point({point_x}, {point_y})")
    #gridwarp.Set

#gridwarp.GetInput("")

#return gridwarp_points_list