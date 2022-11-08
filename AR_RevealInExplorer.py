"""
AR_RevealInExplorer

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_RevealInExplorer
Version: 1.0.1
Description-US: Opens saver's or loader's media input in the explorer

Written for Blackmagic Design Fusion Studio 18.0.4 build 5
Python version 3 (64-bit)

Change log:
1.0.1 (08.11.2022) - Semantic versioning
1.0.0 (04.10.2021) - Initial release
"""

# Installation path: %appdata%\Roaming\Blackmagic Design\Fusion\Scripts\Tool

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

# Run the script
OpenFolder() # Run the function