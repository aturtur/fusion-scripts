"""
AR_EnableAllSavers

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_EnableAllSavers
Version: 1.0.1
Description-US: Enables all savers in the active composition

Written for Blackmagic Design Fusion Studio 18.0.4 build 5
Python version 3 (64-bit)

Change log:
1.0.1 (08.11.2022) - Semantic versioning
1.0.0 (26.04.2022) - Initial release
"""

# Installation path: %appdata%\Roaming\Blackmagic Design\Fusion\Scripts\Comp

# Functions
def EnableAllSavers():
    comp.StartUndo("AR_EnableAllSavers") # Start undo group
    savers = comp.GetToolList(False, "Saver") # Get savers
    for s in savers: # For each saver
        savers[s].SetAttrs({'TOOLB_PassThrough' : False}) # Set pass through off
    comp.EndUndo(True) # End undo group

# Run the script
EnableAllSavers() # Run the function