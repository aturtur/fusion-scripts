"""
AR_VersionUp

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_VersionUp
Version: 1.2.0
Description-US: Change easily between different versions

Written for Blackmagic Design Fusion Studio 18.0.4 build 5
Python version 3 (64-bit)

Change log:
1.2.0 (22.04.2024)  - Added checkbox to keep loader's settings (trims and hold frames...)
                    - Added checkbox to print information to console
1.1.0 (21.04.2024)  - Rework, better algorithm
1.0.2 (07.03.2024)  - Cleaning etc
1.0.1 (08.11.2022)  - Semantic versioning
1.0.0 (04.10.2021)  -  Initial release
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
tries   = 50 # Amount of tries for looking newer or older version number
#----------------------------------------------------------------------------------------------------------------
# Functions
#----------------------------------------------------------------------------------------------------------------
# Check does the file exist
def CheckFile(filePath):
    if os.path.exists(filePath):
        return True
    else:
        return False

# Update file path
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

# Get current version from the file path
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

# Get loader's settings
def GetLoaderSettings(tool):
    settings = {} # Initialize a dictionary for storing settings

    settings['GlobalIn']      = tool.GlobalIn[1]
    settings['GlobalOut']     = tool.GlobalOut[1]
    settings['TrimIn']        = tool.ClipTimeStart[1]
    settings['TrimOut']       = tool.ClipTimeEnd[1]
    settings['HoldFirst']     = tool.HoldFirstFrame[1]
    settings['HoldLast']      = tool.HoldLastFrame[1]
    settings['Reverse']       = tool.Reverse[1]
    settings['Loop']          = tool.Loop[1]
    settings['MissingFrames'] = tool.MissingFrames[1]

    return settings

# Set loader's settings
def SetLoaderSettings(tool, settings):
    tool.GlobalIn[1]       = settings['GlobalIn']
    tool.GlobalOut[1]      = settings['GlobalOut']
    tool.ClipTimeStart[1]  = settings['TrimIn']
    tool.ClipTimeEnd[1]    = settings['TrimOut']
    tool.HoldFirstFrame[1] = settings['HoldFirst']
    tool.HoldLastFrame[1]  = settings['HoldLast']
    tool.Reverse[1]        = settings['Reverse']    
    tool.Loop[1]           = settings['Loop']       
    tool.MissingFrames[1]  = settings['MissingFrames']

    return True

#----------------------------------------------------------------------------------------------------------------
# Main functions
#----------------------------------------------------------------------------------------------------------------
def LatestRun(keepSettings, printData):
    """ Tries to get the newest version """
    tools = comp.GetToolList(True, "Loader") # Get selected loaders
    for t in tools: # For each selected loader
        loaderName = tools[t].Name # Get loader's name
        filePath = tools[t].GetInput("Clip") # Loader's clip's file path
        currentVersion = GetCurrentVersion(filePath) # Get current version

        newerFound = False
        latestValidPath = ""
        latestValidVersion = 0

        for i in range(1, tries + 1): # Try
            latestVersion = currentVersion + i
            updatedPath = UpdateFilePath(filePath, latestVersion)

            if CheckFile(updatedPath) == True: # If file exist
                
                latestValidPath = updatedPath
                latestValidVersion = latestVersion

                settings = GetLoaderSettings(tools[t]) # Get loader's settings

                tools[t].SetInput("Clip", updatedPath + "")
                tools[t].SetInput("Clip", updatedPath) # Update loader's clip

                if keepSettings: # If keepSettings is checked
                    SetLoaderSettings(tools[t], settings) # Set loader's settings
                
                newerFound = True
        
        if newerFound: # If newer version found
            Refresh(tools[t]) # Refresh the loader

            # Print some data to console
            if printData:
                print("%s - Updated from v%s to v%s" % (loaderName, currentVersion, latestValidVersion))
                print("\tOld path:\t\t%s" % filePath)
                print("\tUpdated path:\t%s" % latestValidPath)

        else: # If newer version not found
            # Print some errors to console
            if printData:
                print("%s - Newer version not found!" % loaderName)





    pass

def VersionUpRun(keepSettings, printData):
    """ Tries to get one newer version """
    tools = comp.GetToolList(True, "Loader") # Get selected loaders
    for t in tools: # For each selected loader
        loaderName = tools[t].Name # Get loader's name
        filePath = tools[t].GetInput("Clip") # Loader's clip's file path
        currentVersion = GetCurrentVersion(filePath) # Get current version

        for i in range(1, tries + 1): # Try
            versionUp = currentVersion + i
            updatedPath = UpdateFilePath(filePath, versionUp)

            if CheckFile(updatedPath) == True: # If file exist

                settings = GetLoaderSettings(tools[t]) # Get loader's settings

                tools[t].SetInput("Clip", updatedPath + "")
                tools[t].SetInput("Clip", updatedPath) # Update loader's clip

                if keepSettings: # If keepSettings is checked
                    SetLoaderSettings(tools[t], settings) # Set loader's settings

                Refresh(tools[t]) # Refresh the loader

                # Print some data to console
                if printData:
                    print("%s - Updated from v%s to v%s" % (loaderName, currentVersion, versionUp))
                    print("\tOld path:\t\t%s" % filePath)
                    print("\tUpdated path:\t%s" % updatedPath)

                break # Break the loop
        else:
            # Print some errors to console
            if printData:
                print("%s - Newer version not found!" % loaderName)
    pass

def VersionDownRun(keepSettings, printData):
    """ Tries to get one older version """
    tools = comp.GetToolList(True, "Loader") # Get selected loaders
    for t in tools: # For each selected loader
        loaderName = tools[t].Name # Get loader's name
        filePath = tools[t].GetInput("Clip") # Loader's clip's file path
        currentVersion = GetCurrentVersion(filePath) # Get current version

        for i in range(1, tries + 1): # Try
            versionDown = currentVersion - i
            updatedPath = UpdateFilePath(filePath, versionDown)

            if CheckFile(updatedPath) == True: # If file exist

                settings = GetLoaderSettings(tools[t]) # Get loader's settings

                tools[t].SetInput("Clip", updatedPath + "")
                tools[t].SetInput("Clip", updatedPath) # Update loader's clip

                if keepSettings: # If keepSettings is checked
                    SetLoaderSettings(tools[t], settings) # Set loader's settings

                Refresh(tools[t]) # Refresh the loader

                # Print some data to console
                if printData:
                    print("%s - Updated from v%s to v%s" % (loaderName, currentVersion, versionDown))
                    print("\tOld path:\t\t%s" % filePath)
                    print("\tUpdated path:\t%s" % updatedPath)

                break # Break the loop
        else:
            # Print some errors to console
            if printData:
                print("%s - Older version not found!" % loaderName)
    pass

def CustomRun(customVersion, keepSettings, printData):
    """ Tries to get specific version given by user """
    tools = comp.GetToolList(True, "Loader") # Get selected loaders
    for t in tools: # For each selected loader
        loaderName = tools[t].Name # Get loader's name
        filePath = tools[t].GetInput("Clip") # Loader's clip's file path
        currentVersion = GetCurrentVersion(filePath) # Get current version
        updatedPath = UpdateFilePath(filePath, customVersion)
        if CheckFile(updatedPath) == True: # If file exist

            settings = GetLoaderSettings(tools[t]) # Get loader's settings

            tools[t].SetInput("Clip", updatedPath + "")
            tools[t].SetInput("Clip", updatedPath) # Update loader's clip

            if keepSettings: # If keepSettings is checked
                SetLoaderSettings(tools[t], settings) # Set loader's settings

            Refresh(tools[t]) # Refresh the loader

            # Print some data to console
            if printData:
                print("%s - Updated from v%s to v%s" % (loaderName, currentVersion, customVersion))
                print("\tOld path:\t\t%s" % filePath)
                print("\tUpdated path:\t%s" % updatedPath)

        else:
            # Print some errors to console
            if printData:
                print("%s - Given version not found!" % loaderName)
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
            ui.HGroup(
            [
                ui.CheckBox({ "ID": "Cbox_Keep", "Text": "Keep settings"}),
                ui.CheckBox({ "ID": "Cbox_Print", "Text": "Print info"}),
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
    keepSettings = itm['Cbox_Keep'].Checked
    printData = itm['Cbox_Print'].Checked
    customVersion = itm['VersionNumber'].Value
    CustomRun(customVersion, keepSettings, printData)
dlg.On.Custom.Clicked = _func

def _func(ev):
    keepSettings = itm['Cbox_Keep'].Checked
    printData = itm['Cbox_Print'].Checked
    LatestRun(keepSettings, printData)
dlg.On.Latest.Clicked = _func

def _func(ev):
    keepSettings = itm['Cbox_Keep'].Checked
    printData = itm['Cbox_Print'].Checked
    VersionUpRun(keepSettings, printData)
dlg.On.Up.Clicked = _func

def _func(ev):
    keepSettings = itm['Cbox_Keep'].Checked
    printData = itm['Cbox_Print'].Checked
    VersionDownRun(keepSettings, printData)
dlg.On.Down.Clicked = _func

# Open the dialog
dlg.Show()
disp.RunLoop()
dlg.Hide()