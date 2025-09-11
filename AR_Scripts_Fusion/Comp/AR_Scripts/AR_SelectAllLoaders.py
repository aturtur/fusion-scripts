"""
AR_SelectAllLoaders

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Select All Loaders
Version: 1.0.1
Description-US: Selects all loader tools of the active composition.

Written for Blackmagic Design Fusion Studio 19.0 build 59.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.0.1 (25.09.2024) - Modified code to follow more PEP 8 recommendations.
1.0.0 (08.11.2022) - Initial release.
"""
# Libraries
...


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()


# Functions
def select_all_loaders() -> None:
    """Selects all loaders of the composition in the flow view."""

    loaders = comp.GetToolList(False, "Loader").values()
    flow = comp.CurrentFrame.FlowView
    flow.Select() # Deselect all, if old selections

    for loader in loaders:
        flow.Select(loader, True)


def main() -> None:
    """The main function."""

    select_all_loaders()


if __name__ == "__main__":
    main()