"""
AR_CopyToolNameToClipboard

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Copy Tool Name To Clipboard
Version: 1.0.0
Description-US: Copies selected tool(s) name(s) to the clipboard.

Written for Blackmagic Design Fusion Studio 19.1 build 34.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Dependencies:
    - Pyperclip

Changelog:
1.0.0 (13.11.2024) - Initial release.
"""
# Libraries
import pyperclip


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()


# Functions
def copy_tools_names(tools) -> None:
    """Disables given saver."""

    names = []
    for tool in tools:
        names.append(tool.Name)
    
    clipboard = ("\n").join(names)
    pyperclip.copy(clipboard)


def main() -> None:
    """The main function."""

    tools = comp.GetToolList(True).values()
    copy_tools_names(tools)


if __name__ == "__main__":
    main()