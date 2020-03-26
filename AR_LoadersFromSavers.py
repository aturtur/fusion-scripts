"""
AR_LoadersFromSavers

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_LoadersFromSavers
Description-US: Select savers that you want to make to loaders and run the script
Written for Fusion 16.0 beta 22 build 22
Note: You need Python 2 (64-bit) installed to run this script (https://www.python.org/downloads/release/python-2717/)
"""
#Installation path: %appdata%\Roaming\Blackmagic Design\Fusion\Scripts\Comp
# Libraries
import os, re
import ntpath
from os import listdir

# Functions
def find(name, path):
    pattern = '^'+name+'\d' # Search file name and accept digit right after name
    for file in listdir(path): # Iterate through files
        search = re.match(pattern, file) # Search
        if search: # If acceptable file name found
            return os.path.join(path, file) # Return file path
def LoadersFromSavers():
    comp.StartUndo("AR_LoadersFromSavers") # Start undo group
    comp.Lock() # Put composition to lock mode, so it won't open dialogs
    savers = comp.GetToolList(True, "Saver") # Get selected savers
    for s in savers: # For each selected saver
        flow = comp.CurrentFrame.FlowView # Get flow view
        x, y = flow.GetPosTable(savers[s]).values() # Get node's position
        loader = comp.AddTool("Loader", x+2, y) # Add loader
        path = savers[s].GetInput("Clip") # Get file path from saver
        folder = os.path.dirname(path) # Get folder path
        file = ntpath.basename(path) # Get file name with extension
        extension = os.path.splitext(path)[1] # Get extension
        if extension == ".mov": # If movie file
            loader.SetInput("Clip", path) # Get savers path to loader
        else: # If image sequence
            name = file.replace(extension, "") # Get file name without extension
            loader.SetInput("Clip", find(name, folder)) # Get savers path to loader
    comp.Unlock() # Unlock composition
    comp.EndUndo(True) # End undo group
LoadersFromSavers() # Run the function