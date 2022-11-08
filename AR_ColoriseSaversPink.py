"""
AR_ColoriseSaversPink

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_ColoriseSaversPink
Version: 1.0.0
Description-US: Colorises all savers to pink

Written for Blackmagic Design Fusion Studio 18.0.4 build 5
Python version 3 (64-bit)

Change log:
1.0.0 (08.11.2022) - Initial release
"""

# Installation path: %appdata%\Roaming\Blackmagic Design\Fusion\Scripts\Comp

# Functinons
def ColoriseSaversPink():
    comp.StartUndo("AR_ColoriseSaversPink") # Start undo group
    savers = comp.GetToolList(False, "Saver") # Get savers
    for s in savers: # For each saver
        savers[s].TileColor = {'R': 233.0/255.0, 'G': 140.0/255.0, 'B': 181.0/255.0} # Colorise node to pink
        #savers[s].SetAttrs({'TOOLB_PassThrough' : True}) # Set pass through on
    comp.EndUndo(True) # End undo group

# Run the script
ColoriseSaversPink() # Run the function