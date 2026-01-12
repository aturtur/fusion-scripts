"""
ar_ColoriseSaversPink

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Colorise Savers Pink
Version: 1.0.1
Description-US: Colorises all savers to pink.

Written for Blackmagic Design Fusion Studio 19.0 build 59.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.0.1 (20.09.2024) - Modified code to follow more PEP 8 recommendations.
1.0.0 (08.11.2022) - Initial release.
"""
# Libraries
...


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()

colors = {
    'Orange': {'R': 235.0/255.0, 'G': 110.0/255.0, 'B': 0.0/255.0},
    'Apricot': {'R': 255.0/255.0, 'G': 168.0/255.0, 'B': 51.0/255.0},
    'Yellow': {'R': 226.0/255.0, 'G': 169.0/255.0, 'B': 28.0/255.0},
    'Lime': {'R': 159.0/255.0, 'G': 198.0/255.0, 'B': 21.0/255.0},
    'Olive': {'R': 95.0/255.0, 'G': 153.0/255.0, 'B': 32.0/255.0},
    'Green': {'R': 64.0/255.0, 'G': 143.0/255.0, 'B': 101.0/255.0},
    'Teal': {'R': 0.0/255.0, 'G': 152.0/255.0, 'B': 153.0/255.0},
    'Navy': {'R': 21.0/255.0, 'G': 98.0/255.0, 'B': 132.0/255.0},
    'Blue': {'R': 121.0/255.0, 'G': 168.0/255.0, 'B': 208.0/255.0},
    'Purple': {'R': 153.0/255.0, 'G': 115.0/255.0, 'B': 160.0/255.0},
    'Violet': {'R': 149.0/255.0, 'G': 75.0/255.0, 'B': 205.0/255.0},
    'Pink': {'R': 233.0/255.0, 'G': 140.0/255.0, 'B': 181.0/255.0},
    'Tan': {'R': 185.0/255.0, 'G': 176.0/255.0, 'B': 151.0/255.0},
    'Beige': {'R': 198.0/255.0, 'G': 160.0/255.0, 'B': 119.0/255.0},
    'Brown': {'R': 153.0/255.0, 'G': 102.0/255.0, 'B': 0.0/255.0},
    'Chocolate': {'R': 140.0/255.0, 'G': 90.0/255.0, 'B': 63.0/255.0}
}


# Functions
def colorise_tool(tool, color: dict[str, float]) -> None:
    """Colorises all savers to pink."""

    tool.TileColor = color


def main() -> None:
    """The main function."""

    savers = comp.GetToolList(False, "Saver").values()

    for saver in savers:
        colorise_tool(saver, colors['Pink'])
        

if __name__ == "__main__":
    main()