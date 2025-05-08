"""
AR_ClearViews

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Clear Views
Version: 1.0.0
Description-US: Clears all views (preview windows).

Written for Blackmagic Design Fusion Studio 19.1.3 build 5.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp
  
Changelog:
1.0.0 (04.02.2025) - Initial release.
"""
# Libraries
...


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()


# Functions
def clear_previews() -> None:
    """Clears preview windows, also both A and B buffers."""
    
    node = comp.AddTool("Background")
    windowlist = comp.GetFrameList()
    previews = comp.GetPreviewList()

    for window in windowlist.values():

        # Left preview window.
        left = previews['LeftView'].View
        left.SetBuffer(0)  # A buffer.
        window.ViewOn(node, 1)
        left.SetBuffer(1)  # B buffer.
        window.ViewOn(node, 1)
        left.SetBuffer(0)

        # Right preview window.
        right = previews['RightView'].View
        right.SetBuffer(0)
        window.ViewOn(node, 2)
        right.SetBuffer(1)
        window.ViewOn(node, 2)
        right.SetBuffer(0)

        # Second monitor.
        window.ViewOn(node, 3)

    node.Delete()


def main() -> None:
    """The main function."""

    clear_previews()


if __name__ == "__main__":
    main()