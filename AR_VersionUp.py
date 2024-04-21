"""
AR_VersionUp

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_VersionUp
Version: 1.1.0
Description-US: Change easily between different versions

Written for Blackmagic Design Fusion Studio 18.0.4 build 5
Python version 3 (64-bit)

Change log:
1.1.0 (21.04.2024) - Rework
1.0.2 (07.03.2024) - Cleaning etc
1.0.1 (08.11.2022) - Semantic versioning
1.0.0 (04.10.2021) - Initial release
"""

# Installation path: %appdata%\Roaming\Blackmagic Design\Fusion\Scripts\Comp
# File path syntax example: ..\VERSIONS\ProjectName_v001\..\..\ProjectName_v001_0000.tif

#----------------------------------------------------------------------------------------------------------------
# Libraries
#----------------------------------------------------------------------------------------------------------------
import os
import re

#----------------------------------------------------------------------------------------------------------------
# Global variables
#----------------------------------------------------------------------------------------------------------------
pattern = "(?:[^a-zA-Z]|^)v\d{1,4}(?:[^a-zA-Z]|$)" # Searches v1, v01, v001, v0001 types of versioning
tries   = 50 # Amount of tries
#----------------------------------------------------------------------------------------------------------------
# Functions
#----------------------------------------------------------------------------------------------------------------
# Check does the file exist
def CheckFile(filePath):
    if os.path.exists(filePath):
        return True
    else:
        return False

def UpdateFilePath(filePath, position):
    path = os.path.normpath(filePath) # Normalize path
    splittedPath = path.split(os.sep) # Split path
    updatedPath = [] # Initialize a list for updated path
    for part in splittedPath: # Iterate through splitted parts
        found = re.findall(pattern, part) # Get versioning part
        if len(found) != 0: # If version found
            rawVersion = found[0]
            version = re.findall(r"\d+", rawVersion)[0] # Parse digits
            zpad = len(version) # Get zero padding size
            number = int(version) # Get version number without zero padding
            updatedNumber = position # Get updated version number
            updatedVersion = str(updatedNumber).zfill(zpad) # Get updated version with zero padding
            updatedRawVersion = re.sub(r"\d+", updatedVersion, rawVersion) # Replace old version with updated version
            part = part.replace(rawVersion, updatedRawVersion) # Replace part with updated version
        updatedPath.append(part) # Add part to the list        
    resultPath = os.path.sep.join(updatedPath) # Join path
    return resultPath

def GetCurrentVersion(filePath):
    path = os.path.normpath(filePath) # Normalize path
    splittedPath = path.split(os.sep) # Split path
    for part in splittedPath: # Iterate through splitted parts
        found = re.findall(pattern, part) # Get versioning part
        if len(found) != 0: # If version found
            rawVersion = found[0]
            version = re.findall(r"\d+", rawVersion)[0] # Parse digits
            number = int(version) # Get version number without zero padding
            return number

# Refresh tool toggling pass through parameter on and off
def Refresh(tool):
    currentState = tool.GetAttrs()['TOOLB_PassThrough'] # Store tool's current state
    tool.SetAttrs({'TOOLB_PassThrough' : True}) # Set pass through on
    tool.SetAttrs({'TOOLB_PassThrough' : False}) # Set pass through off
    tool.SetAttrs({'TOOLB_PassThrough' : currentState}) # Put back old setting
    return None

#----------------------------------------------------------------------------------------------------------------
# Button functions
#----------------------------------------------------------------------------------------------------------------
def LatestRun():
    """ Tries to get the newest version """
    tools = comp.GetToolList(True, "Loader") # Get selected loaders
    for t in tools: # For each selected loader
        filePath = tools[t].GetInput("Clip") # Loader's clip's file path

        for i in range(1, tries + 1): # Try
            latest = GetCurrentVersion(filePath) + i
            customPath = UpdateFilePath(filePath, latest)

            if CheckFile(customPath) == True: # If file exist
                tools[t].SetInput("Clip", customPath + "")
                tools[t].SetInput("Clip", customPath) # Update loader's clip

        Refresh(tools[t]) # Refresh the loader
    pass

def VersionUpRun():
    """ Tries to get one newer version """
    tools = comp.GetToolList(True, "Loader") # Get selected loaders
    for t in tools: # For each selected loader
        filePath = tools[t].GetInput("Clip") # Loader's clip's file path

        for i in range(1, tries + 1): # Try
            versionUp = GetCurrentVersion(filePath) + i
            customPath = UpdateFilePath(filePath, versionUp)

            if CheckFile(customPath) == True: # If file exist
                tools[t].SetInput("Clip", customPath + "")
                tools[t].SetInput("Clip", customPath) # Update loader's clip
                Refresh(tools[t]) # Refresh the loader
                return # Break the loop
        else:
            print("Newer version not found!")
    pass

def VersionDownRun():
    """ Tries to get one older version """
    tools = comp.GetToolList(True, "Loader") # Get selected loaders
    for t in tools: # For each selected loader
        filePath = tools[t].GetInput("Clip") # Loader's clip's file path

        for i in range(1, tries + 1): # Try
            versionDown = GetCurrentVersion(filePath) - i
            customPath = UpdateFilePath(filePath, versionDown)

            if CheckFile(customPath) == True: # If file exist
                tools[t].SetInput("Clip", customPath + "")
                tools[t].SetInput("Clip", customPath) # Update loader's clip
                Refresh(tools[t]) # Refresh the loader
                return # Break the loop
        else:
            print("Older version not found!")
    pass

def CustomRun(customVersion):
    """ Tries to get specific version given by user """
    tools = comp.GetToolList(True, "Loader") # Get selected loaders
    for t in tools: # For each selected loader
        filePath = tools[t].GetInput("Clip") # Loader's clip's file path

        customPath = UpdateFilePath(filePath, customVersion)
        if CheckFile(customPath) == True: # If file exist
            tools[t].SetInput("Clip", customPath + "")
            tools[t].SetInput("Clip", customPath) # Update loader's clip
            Refresh(tools[t]) # Refresh the loader
        else:
            print("Given version not found!")
    pass
#----------------------------------------------------------------------------------------------------------------
# Creating user interface
#----------------------------------------------------------------------------------------------------------------
ui = fu.UIManager
disp = bmd.UIDispatcher(ui)
dlg = disp.AddWindow({ "WindowTitle": "Change Version", "ID": "MyWin", "Geometry": [ 100, 100, 225, 140 ], },
    [
        ui.VGroup({ "Spacing": 5, },
        [
            # GUI elements  
            #ui.VGap(),
            ui.HGroup(
            [
                ui.Button({ "Text": "^", "ID": "Up" }), # Button one version up
                ui.Button({ "Text": "v", "ID": "Down" }), # Button one version down
            ]),
            #ui.VGap(),
            ui.Button({ "Text": "Latest version", "ID": "Latest" }), # Button latest version
            ui.HGroup(
            [
                #ui.LineEdit({ "ID": "VersionNumber", "Text": "", "PlaceholderText": "New version no.", }), # Input text field custom version
                ui.SpinBox({ "ID": "VersionNumber", "Value":1, "Minimum":0, "Maximum":100000}), # Input text field custom version
                ui.Button({ "Text": "Custom", "ID": "Custom" }), # Button apply custom version
            ]),
        ]),
    ])

itm = dlg.GetItems() # Collect ui items

# The window was closed
def _func(ev):
    disp.ExitLoop()
dlg.On.MyWin.Close = _func

# GUI element based event functions
def _func(ev):
    customVersion = itm['VersionNumber'].Value
    #print("Custom Version: " + str(customVersion))
    CustomRun(customVersion)
dlg.On.Custom.Clicked = _func

def _func(ev):
    #print("Latest Version")
    LatestRun()
dlg.On.Latest.Clicked = _func

def _func(ev):
    #print("Version Up")
    VersionUpRun()
dlg.On.Up.Clicked = _func

def _func(ev):
    #print("Version Down")
    VersionDownRun()
dlg.On.Down.Clicked = _func

# Open the dialog
dlg.Show()
disp.RunLoop()
dlg.Hide()