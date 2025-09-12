"""
AR_CopyPathToClipboard

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Copy Path To Clipboard
Version: 1.0.0
Description-US: Copies selected tool(s) path(s) to the clipboard.

Written for Blackmagic Design Fusion Studio 19.1 build 34.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Dependencies:
    - Pyperclip

Changelog:
1.0.0 (08.05.2025) - Initial release.
"""
# Libraries
import pyperclip


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()


# Functions
def copy_tools_paths(tools) -> None:
    """Copies given tool(s) path(s) to the clipboard."""

    now = comp.CurrentTime
    paths = []
    usd_tools = ["uLoader", "uVolume", "uImagePlane", "uMaterialX"]

    for tool in tools:
        if tool.ID == "Loader" or tool.ID == "Saver":
            paths.append(tool.Clip[now])
        if tool.ID == "SurfaceAlembicMesh":
            paths.append(tool.Filename[now])
        if tool.ID == "SurfaceFBXMesh":
            paths.append(tool.ImportFile[now])
        if tool.ID == "FileLUT":
            paths.append(tool.LUTFile[now])
        if tool.ID in usd_tools:
            if tool.ID == "uMaterialX":
                paths.append(tool.MaterialFile[now])
            else:
                paths.append(tool.Filename[now])

    clipboard = ("\n").join(paths)
    pyperclip.copy(clipboard)


def main() -> None:
    """The main function."""

    tools = comp.GetToolList(True).values()
    copy_tools_paths(tools)


if __name__ == "__main__":
    main()