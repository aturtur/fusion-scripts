"""
AR_EnableAllSavers

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_EnableAllSavers
Description-US: This script enables all savers in active composition.
Written for Fusion 16.0 beta 22 build 22
Note: You need Python 2 (64-bit) installed to run this script (https://www.python.org/downloads/release/python-2717/)
"""
#Installation path: %appdata%\Roaming\Blackmagic Design\Fusion\Scripts\Comp
# Functinons
def DisableAllSavers():
    comp.StartUndo("AR_DisableAllSavers") # Start undo group
    savers = comp.GetToolList(False, "Saver") # Get savers
    for s in savers: # For each saver
        savers[s].SetAttrs({'TOOLB_PassThrough' : False}) # Set pass through off
    comp.EndUndo(True) # End undo group
DisableAllSavers() # Run the function