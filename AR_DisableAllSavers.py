"""
AR_DisableAllSavers

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_DisableAllSavers
Version: 1.0.1
Description-US: Disables all savers in the active composition

Written for Blackmagic Design Fusion Studio 18.0.4 build 5
Python version 3 (64-bit)

Change log:
1.0.1 (08.11.2022) - Semantic versioning
1.0.0 (26.04.2022) - Initial release
"""

# Installation path: %appdata%\Roaming\Blackmagic Design\Fusion\Scripts\Comp

# Functions
def DisableAllSavers():
    comp.StartUndo("AR_DisableAllSavers") # Start undo group
    savers = comp.GetToolList(False, "Saver") # Get savers
    for s in savers: # For each saver
        savers[s].SetAttrs({'TOOLB_PassThrough' : True}) # Set pass through on
    comp.EndUndo(True) # End undo group

# Run the script
DisableAllSavers() # Run the function