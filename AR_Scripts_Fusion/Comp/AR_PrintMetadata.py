"""
AR_PrintMetadata

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Print Metadata
Version: 1.0.3
Description-US: Prints metadata from active tool.

Written for Blackmagic Design Fusion Studio 19.0 build 59.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.0.3 (30.03.2025) - Name fix.
1.0.2 (06.11.2024) - Changed print to use f-string.
1.0.1 (25.09.2024) - Modified code to follow more PEP 8 recommendations.
1.0.0 (20.10.2023) - Initial release.
"""
# Libraries
...


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()


# Functions
def print_metadata() -> None:
    """Prints meta data of the active tool to the console."""

    metadata = comp.ActiveTool.Output[comp.CurrentTime].Metadata
    for key, value in metadata.items():
        print(f"{key} = {value}")


def main() -> None:
    """The main function."""

    print_metadata()


if __name__ == "__main__":
    main()