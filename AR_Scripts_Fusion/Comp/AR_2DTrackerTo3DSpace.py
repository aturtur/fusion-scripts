"""
AR_2DTrackerTo3DSpace

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: 2D Tracker To 3D Space
Version: 1.0.0
Description-US: Creates a setup that converts selected 2D trackers data to 3D space.

Currenty uses only the first tracker of the tracker tool.  

Written for Blackmagic Design Fusion Studio 19.1.4 build 6.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.0.0 (06.10.2024) - Initial realease.
"""
# Libraries
import os


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()


# Functions
def tracker_to_3d_space(tracker) -> None:
    """Creates a setup that converts 2D tracker data to 3D space."""

    # AoV type: Horizontal.
    #Shape3D1.Transform3DOp.Translate.X = (Tracker1.TrackedCenter1.X-0.5) * -(Transform3DOp.Translate.Z * (math.tan(Camera3D1.AoV * (math.pi / 180) * 0.5) * 2.0))
    #Shape3D1.Transform3DOp.Translate.Y = (Tracker1.TrackedCenter1.Y-0.5) * -(Transform3DOp.Translate.Z * (2 * math.atan(math.tan(Camera3D1.AoV * (math.pi / 180) / 2) / (Camera3D1.ApertureW / Camera3D1.ApertureH))))

    # AoV type: Vertical.
    #Shape3D1.Transform3DOp.Translate.X = (Tracker1.TrackedCenter1.X-0.5) * -(Transform3DOp.Translate.Z * (2 * math.tan(Camera3D1.AoV * (math.pi / 180) * 0.5) * (Camera3D1.ApertureW / Camera3D1.ApertureH)))
    #Shape3D1.Transform3DOp.Translate.Y = (Tracker1.TrackedCenter1.Y-0.5) * -(Transform3DOp.Translate.Z * (math.tan(Camera3D1.AoV * (math.pi / 180) * 0.5) * 2.0))

    # Tracker.
    tracker_name = tracker.Name

    # Camera3D.
    camera3d = comp.AddTool("Camera3D")
    camera3d_name = camera3d.Name

    # Shape3D.
    shape3d = comp.AddTool("Shape3D")
    shape3d_name = shape3d.Name
    shape3d.SetInput("Shape", "SurfaceSphereInputs")
    shape3d.Transform3DOp.Translate.X.SetExpression(f"({tracker_name}.TrackedCenter1.X-0.5) * -(Transform3DOp.Translate.Z * (2 * math.tan({camera3d_name}.AoV * (math.pi / 180) * 0.5) * ({camera3d_name}.ApertureW / {camera3d_name}.ApertureH)))")
    shape3d.Transform3DOp.Translate.Y.SetExpression(f"({tracker_name}.TrackedCenter1.Y-0.5) * -(Transform3DOp.Translate.Z * (math.tan({camera3d_name}.AoV * (math.pi / 180) * 0.5) * 2.0))")
    shape3d.SetInput("Transform3DOp.Translate.Z", -10)
    
    # Connect nodes.
    camera3d.SceneInput = shape3d.Output

    return None


def main() -> None:
    """The main function."""

    comp.StartUndo("Tracker to 3D space")
    tools = comp.GetToolList(True).values()

    for tool in tools:
        if tool.ID == "Tracker":
            tracker_to_3d_space(tool)

    comp.EndUndo(True)


if __name__ == "__main__":
    main()