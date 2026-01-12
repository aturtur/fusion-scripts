"""
ar_CreateLocator3D

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Create Locator3D
Version: 1.0.0
Description-US: Creates a Locator3D node connected to selected 3D shape.

Written for Blackmagic Design Fusion Studio 19.0 build 59.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.0.0 (05.02.2025) - Initial realease.
"""
# Libraries
...


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()

threed_objects = ["SurfaceAlembicMesh",
                  "SurfaceFBXMesh",
                  "Cube3D",
                  "ImagePlane3D",
                  "LightProjector",
                  "Shape3D",
                  "Text3D"]


# Functions
def create_locator3d(shape) -> any:
    """Creates a Locator3D node that is connected to the given 3D Shape node."""

    locator3d = comp.AddTool("Locator3D")
    
    locator3d.Transform3DOp.Translate.X.ConnectTo(shape.Transform3DOp.Translate.X)
    locator3d.Transform3DOp.Translate.Y.ConnectTo(shape.Transform3DOp.Translate.Y)
    locator3d.Transform3DOp.Translate.Z.ConnectTo(shape.Transform3DOp.Translate.Z)

    locator3d.Transform3DOp.Rotate.X.ConnectTo(shape.Transform3DOp.Rotate.X)
    locator3d.Transform3DOp.Rotate.Y.ConnectTo(shape.Transform3DOp.Rotate.Y)
    locator3d.Transform3DOp.Rotate.Z.ConnectTo(shape.Transform3DOp.Rotate.Z)

    return locator3d


def create_transform(locator3d) -> any:
    """Creates a transform node that is connected to the given Locator3D node."""

    transform = comp.AddTool("Transform")
    transform.Center.ConnectTo(locator3d.Position)

    return transform


def main() -> None:
    """The main function."""

    comp.StartUndo("Locator3D")
    tools = comp.GetToolList(True).values()

    for tool in tools:
        if tool.ID in threed_objects:
            locator3d = create_locator3d(tool)
            transform = create_transform(locator3d)

    comp.EndUndo(True)


if __name__ == "__main__":
    main()
