"""
ar_DisableAllSavers

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Disable All Savers
Version: 1.0.2
Description-US: Disables all savers in the active composition.

Written for Blackmagic Design Fusion Studio 19.0 build 59.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.0.2 (25.09.2024) - Modified code to follow more PEP 8 recommendations.
1.0.1 (08.11.2022) - Semantic versioning.
1.0.0 (26.04.2022) - Initial release.
"""
# Libraries
...


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()


# Functions
def disable_saver(saver) -> None:
    """Disables given saver."""

    saver.SetAttrs({'TOOLB_PassThrough' : True})


def main() -> None:
    """The main function."""

    comp.StartUndo("Disable savers")
    savers = comp.GetToolList(False, "Saver").values()

    for saver in savers:
        disable_saver(saver)
        
    comp.EndUndo(True)


if __name__ == "__main__":
    main()