"""
AR_OpenFolder

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_OpenFolder
Description-US: Open savers / loaders file path's folder
Written for Fusion 16.2 build 22
"""
#Installation path: %appdata%\Roaming\Blackmagic Design\Fusion\Scripts\Comp
# Libraries
import os, re
import subprocess

# Functions
def OpenFolder():
    savers = comp.GetToolList(True, "Saver") # Get selected savers
    loaders = comp.GetToolList(True, "Loader") # Get selected loaders
    for s in savers: # For each selected saver
        path = savers[s].GetInput("Clip") # Get file path from saver
        folder = os.path.dirname(path) # Get folder path
        os.startfile(folder) # Open the folder
    for l in loaders: # For each selected loader
        path = loaders[l].GetInput("Clip") # Get file path from loader
        subprocess.Popen(["explorer", "/select,", path]) # Open the folder and select the file
OpenFolder() # Run the function