"""
AR_OpenProjectFolder
Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_OpenFolder
Description-US: Open the composition's folder
Written for Fusion 16.2 build 22
Note: You need Python 2 (64-bit) installed to run this script (https://www.python.org/downloads/release/python-2717/)
"""
#Installation path: %appdata%\Roaming\Blackmagic Design\Fusion\Scripts\Comp
# Libraries
import os, re
import subprocess

# Functions
def OpenProjectFolder():
    path = comp.GetAttrs()['COMPS_FileName'] # Get composition's file path
    folder = os.path.dirname(path) # Get folder path
    #os.startfile(folder) # Open the folder
    subprocess.Popen(["explorer", "/select,", path]) # Open the folder and select the file
OpenProjectFolder() # Run the function