"""
ar_PasteColor

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Paste Color
Version: 1.0.0
Description-US: Creates a background with the hex color from the clipboard.

Written for Blackmagic Design Fusion Studio 20.3.1 build 5.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

to do: muokkaa käyttämään pyperclip moduulia:
    data = pyperclip.paste()
  
Changelog:
1.0.0 (18.03.2026) - Initial release.
"""
# Libraries
import win32clipboard
import re


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()


# Functions
def process_string(string):
    """Process the given string."""

    if string.startswith("#"):
        string = string.lstrip("#")

    return hex_to_float(string)


def get_clipboard() -> str:
    """Checks what kind of data is copied to the clipboard (files, image, text)
    and if it is in text format, return the data.
    """

    win32clipboard.OpenClipboard()

    if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_HDROP):
        result = "files"
    elif win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_BITMAP):
        result = "image"
    elif win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_UNICODETEXT):
        result = "text"
    else:
        result = "unknown"

    if result == "text":
        try:
            data = win32clipboard.GetClipboardData()
        except:
            data = None

    win32clipboard.CloseClipboard()
    return data


def rgb_to_float(rgb_int) -> list:
    """Converts rgb integer values (255) to rgb float values (0.0-1.0)."""

    return [c / 255.0 for c in rgb_int]


def hex_to_float(hex_color) -> list:
    """Converts hex color (#ffffff) to rgb float values (0.0-1.0)."""

    return [int(hex_color[i:i+2], 16)/255.0 for i in (0, 2, 4)]


def hsl_to_float(hsl_int) -> list:
    """Converts hsl values to rgb float values."""
    return [hsl_int[0]/360.0, hsl_int[1]/100.0, hsl_int[2]/100.0]


def float_to_hex(r, g, b) -> str:
    """Converts rgb gloat values to hex color."""

    return "#{:02X}{:02X}{:02X}".format(int(r*255), int(g*255), int(b*255))


def create_background_tool(color) -> bool:
    """Creates a background tool with te given color."""

    background_tool = comp.AddTool("Background")
    background_tool.SetInput("TopLeftRed", color[0])
    background_tool.SetInput("TopLeftGreen", color[1])
    background_tool.SetInput("TopLeftBlue", color[2])
    #background_tool.SetAttrs({'TOOLS_Name': name})

    return True


def main() -> None:
    """The main function."""

    comp.StartUndo("Paste Color")

    clipboard = get_clipboard()
    if clipboard:
        splitted_data = re.split(r"[-,\s]+", clipboard)
        for string in splitted_data:
            color = process_string(string)
            create_background_tool(color)

    comp.EndUndo(True)


if __name__ == "__main__":
    main()