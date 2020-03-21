"""
AR_DisableAllSavers

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_DisableAllSavers
Description-US: This script will disable all savers in active composition.
Written for Fusion 16.0 beta 22 build 22
"""
#Installation path: %appdata%\Roaming\Blackmagic Design\Fusion\Scripts\Comp
# Functinons
def DisableAllSavers():
    comp.StartUndo("AR_DisableAllSavers") # Start undo group
    savers = comp.GetToolList(False, "Saver") # Get savers
    for s in savers: # For each saver
        savers[s].SetAttrs({'TOOLB_PassThrough' : True}) # Set pass through on
    comp.EndUndo(True) # End undo group
DisableAllSavers() # Run the function