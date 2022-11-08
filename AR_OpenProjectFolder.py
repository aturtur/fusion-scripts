"""
AR_OpenProjectFolder

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_OpenProjectFolder
Version: 1.0.1
Description-US: Opens the folder where the project file is located

Written for Blackmagic Design Fusion Studio 18.0.4 build 5
Python version 3 (64-bit)

Change log:
1.0.1 (08.11.2022) - Semantic versioning
1.0.0 (26.04.2022) - Initial release
"""

# Installation path: %appdata%\Roaming\Blackmagic Design\Fusion\Scripts\Comp

# Libraries
import os, re
import subprocess

# Functions
def OpenProjectFolder():
    path = comp.GetAttrs()['COMPS_FileName'] # Get composition's file path
    folder = os.path.dirname(path) # Get folder path
    #os.startfile(folder) # Open the folder
    subprocess.Popen(["explorer", "/select,", path]) # Open the folder and select the file

# Run the script
OpenProjectFolder() # Run the function