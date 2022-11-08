"""
AR_SelectAllLoaders

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_SelectAllLoaders
Version: 1.0.0
Description-US: Selects all loader nodes in the active project

Written for Blackmagic Design Fusion Studio 18.0.4 build 5
Python version 3 (64-bit)

Change log:
1.0.0 (08.11.2022) - Initial release
"""

# Installation path: %appdata%\Roaming\Blackmagic Design\Fusion\Scripts\Comp

# Functions
def SelectAllLoaders():
    loaders = comp.GetToolList(False, "Loader") # Get all loaders
    flow = comp.CurrentFrame.FlowView # Get flow view
    flow.Select() # Deselect all
    for l in loaders: # For each loader
        flow.Select(loaders[l], True) # Select the loader

# Run the script
SelectAllLoaders() # Run the function