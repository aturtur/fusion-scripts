"""
AR_SelectAllLoaders

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_SelectAllLoaders
Description-US: Selects all loader nodes
Written for Fusion 16.2 build 22
Note: You need Python 2 (64-bit) installed to run this script (https://www.python.org/downloads/release/python-2717/)
"""
#Installation path: %appdata%\Roaming\Blackmagic Design\Fusion\Scripts\Comp
def SelectAllLoaders():
    loaders = comp.GetToolList(False, "Loader") # Get all loaders
    flow = comp.CurrentFrame.FlowView # Get flow view
    flow.Select() # Deselect all
    for l in loaders: # For each loader
        flow.Select(loaders[l], True) # Select the loader
SelectAllLoaders() # Run the function