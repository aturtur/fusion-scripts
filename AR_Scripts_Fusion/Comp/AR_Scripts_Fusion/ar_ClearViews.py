"""
ar_ClearViews

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Clear Views
Version: 1.1.0
Description-US: Clears all views (preview windows).\nShift: Clear B buffers.

Written for Blackmagic Design Fusion Studio 19.1.3 build 5.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp
  
Changelog:
1.1.0 (23.01.2025) - With SHIFT key modifier will clear only B buffers.
1.0.0 (04.02.2025) - Initial release.
"""
# Libraries
...


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()

try:
    key_modifiers = key_modifiers
except Exception:
    key_modifiers = None

ALT: str = "ALT"
CTRL: str = "CTRL"
SHIFT: str = "SHIFT"


# Functions
def clear_previews(key_modifiers: list) -> None:
    """Clears preview windows, also both A and B buffers."""
    
    node = comp.AddTool("Background")
    windowlist = comp.GetFrameList()
    previews = comp.GetPreviewList()

    for window in windowlist.values():

        # Clear all views.
        if not key_modifiers:
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

        # Clear only B buffers.
        if SHIFT in key_modifiers:
            # Left preview window.
            left = previews['LeftView'].View
            left.SetBuffer(1)  # B buffer.
            window.ViewOn(node, 1)
            left.SetBuffer(0)

            # Right preview window.
            right = previews['RightView'].View
            right.SetBuffer(1)
            window.ViewOn(node, 2)
            right.SetBuffer(0)

    node.Delete()


def main() -> None:
    """The main function."""

    clear_previews(key_modifiers)


if __name__ == "__main__":
    main()