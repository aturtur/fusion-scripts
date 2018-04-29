# Fusion Script - Change version [v0.05] by @aturtur
# Installation path: %appdata%\Blackmagic Design\Fusion\Scripts\Comp
# File path syntax example: ..\VERSIONS\ProjectName_v001\..\..\ProjectName_v001_0000.tif
#
# HOW TO USE:  - Select loaders you want to change and press buttons
#------------------------------------------------------------------------------------------------------------------------------------------------
# Import libraries
#------------------------------------------------------------------------------------------------------------------------------------------------
import os, re
import platform as pf

#------------------------------------------------------------------------------------------------------------------------------------------------
# Global variables
#------------------------------------------------------------------------------------------------------------------------------------------------
delimiter = "_v" # String that indicates version delimiter

#------------------------------------------------------------------------------------------------------------------------------------------------
# Functions
#------------------------------------------------------------------------------------------------------------------------------------------------
# Get correct separator depending what operating system user is using
def GetSep():
    if pf.system() == "Windows": # If os is windwos
        return "\\" # Return \
    else: # Is os is something else (mac or linux)
        return "/" # Return /

# Get version number from a file path
def GetVersion(filePath):
    versionList = re.findall(delimiter+"\d+",filePath) # Search delimiter+digits (e.g. _v001) string in file path and store those in a [list]
    rawVersion = re.compile(delimiter).split(versionList[len(versionList)-1])[1] # Version number with zero padding [string]
    #zeroPaddingSize = len(rawVersion) # How many zeros version number has [integer]
    version = int(rawVersion) # Version number without zero padding [integer]
    return version, rawVersion # (e.g. 1, 001)

# Get a file name from a file path
def FileName(filePath):
    splitted = filePath.rsplit(GetSep()) # Split file path
    fullFileName = splitted[len(splitted)-1] # Full file name with extension [string]
    firstPart = re.compile(delimiter+"\d+").split(fullFileName)[0] # File name first part before delimiter+digits [string]
    fileName = firstPart+delimiter+GetVersion(filePath)[1] # Base file name without extras [string]
    lastPart = re.compile(delimiter+"\d+").split(fullFileName)[1] # File name last part after delimiter+digits [string]
    return fullFileName, firstPart, lastPart, fileName # [string]

""" Some unnecessary functions I wanted to keep
# Get the current folde path and name from a full file path
def CurrentFolder(filePath):
    splitted = filePath.split(GetSep()) # Split file path to folders
    folderName = splitted[len(splitted)-2] # Folder name [string]
    folderPath = os.path.abspath(os.path.join(filePath,"..")) # Current folder path
    return folderPath, folderName # [string]

# Get parent folder path and name from a full file path
def ParentFolder(filePath):
    parentFolderPath = os.path.abspath(os.path.join(filePath,"../.."))
    parentFolderName = os.path.basename(parentFolderPath)
    return parentFolderPath, parentFolderName
"""

# Get master folder (e.g. ../ projectname_v001)
def MasterFolder(filePath):
    search = FileName(filePath)[3] # Search with file name
    splitted = filePath.split(GetSep()) # Split file path to folders
    pos = 0 # Initialize starting position
    firstPos = 0
    for s in splitted:
        find = "".join(re.findall(search, s))
        if find == search:
            if firstPos == 0:
                firstPos = pos
                break
        pos = pos + 1 # Moving forward
    folder = splitted[:firstPos+1]
    masterFolderPath = GetSep().join(folder) # Join list with os specific path separator
    masterParentFolderPath = os.path.abspath(os.path.join(masterFolderPath,".."))
    return masterFolderPath, masterParentFolderPath # [string]

# Searches given file path to check different versions
def GetVersions(searchPath, search):
    modSearch = search+delimiter # Add delimiter to search string
    versions = [] # List of collected versions
    items = os.listdir(searchPath) # Items to go through
    for i in items: # Loop through every file in folder
        find = "".join(re.findall(modSearch, i)) # Search
        if find == modSearch: # If it matches
            versions.append(GetVersion(i)[0]) # Put version to versions list
        versions = list(set(versions)) # Remove duplicates
        versions.sort() # Sort list
    return versions # [list]

""" Some unnecessary function I wanted to keep
# Finds out folders between current file and master folder
def FoldersBetween(filePath):
    search = FileName(filePath)[3] # Search base file name
    splitted = filePath.split(GetSep()) # Split file path to folders
    pos = 0 # Initialize starting position
    firstPos = 0 # First found position
    lastPos = 0 # Last found position
    for s in splitted:
        find = "".join(re.findall(search, s))
        if find == search:
            if firstPos == 0:
                firstPos = pos
            else:
                lastPos = pos
        pos = pos + 1 # Moving forward
    count = lastPos-firstPos-1 # How many folders there are between master folder and file
    foldersBetween = splitted[firstPos+1:] # Trim list from start
    foldersBetween = foldersBetween[:-1] # Trim list from end
    foldersBetweenPath = GetSep().join(foldersBetween) # Join list with os specific path separator
    if count <= 0: # If there is no folders between
        return "" # Return empty string
    else:
        return GetSep()+foldersBetweenPath # Return between path
"""

# Update file path with given version number
def GetNewPath(filePath, version):
    oldVersion = GetVersion(filePath)[1] # Old version
    zeroPadding = len(oldVersion) # Zero padding
    newVersion = delimiter+str(version).zfill(zeroPadding) # New version with zero padding
    #foldersBetween = FoldersBetween(filePath) # Folders between file and master folder
    newPath = re.sub(r""+delimiter+oldVersion, newVersion, filePath) # New full file path
    return newPath # [string]

# Get latest version number
def LatestVersion(versions):
    latestVersion = max(versions)
    return latestVersion # [integer]

# Return newer version
def VersionUp(versions, currentVersion):
    upList = [v for v in versions if v > currentVersion] # Collect higher versions than current version
    if not upList: # If list is empty
        up = currentVersion # Current version is latest
    else:
        up = min(upList)
    return up # [integer]

# Return older version
def VersionDown(versions, currentVersion):
    downList = [v for v in versions if v < currentVersion] # Collect lower versions than current version
    if not downList: # If list is empty
        down = currentVersion # Current version is oldest
    else:
        down = max(downList)
    return down # [integer]

# Refresh tool toggling pass through parameter on and off
def Refresh(t):
    d = t.GetAttrs()['TOOLB_PassThrough'] # Store tool's current state
    t.SetAttrs({'TOOLB_PassThrough' : True}) # Set pass through on
    t.SetAttrs({'TOOLB_PassThrough' : False}) # Set pass through off
    t.SetAttrs({'TOOLB_PassThrough' : d}) # Put back old setting
    return None
#------------------------------------------------------------------------------------------------------------------------------------------------
# Run
#------------------------------------------------------------------------------------------------------------------------------------------------
def LatestRun():
    tools = comp.GetToolList(True, "Loader") # Get selected loaders
    for t in tools: # For each selected loader
        filePath = tools[t].GetInput("Clip") # Loader's clip's file path
        #--------------------------
        masterFolder = MasterFolder(filePath)[1]
        versions = GetVersions(masterFolder, FileName(filePath)[1])
        latestVersion = LatestVersion(versions)
        latestPath = GetNewPath(filePath, latestVersion)
        #--------------------------
        tools[t].SetInput("Clip", latestPath) # Update loader's clip
        Refresh(tools[t]) # Refresh the loader
    pass

def VersionUpRun():
    tools = comp.GetToolList(True, "Loader") # Get selected loaders
    for t in tools: # For each selected loader
        filePath = tools[t].GetInput("Clip") # Loader's clip's file path
        #--------------------------
        currentVersion = GetVersion(filePath)[0]
        masterFolder = MasterFolder(filePath)[1]
        versions = GetVersions(masterFolder, FileName(filePath)[1])
        newVersion = VersionUp(versions, currentVersion)
        newPath = GetNewPath(filePath, newVersion)
        #--------------------------
        tools[t].SetInput("Clip", newPath) # Update loader's clip
        Refresh(tools[t]) # Refresh the loader
    pass

def VersionDownRun():
    tools = comp.GetToolList(True, "Loader") # Get selected loaders
    for t in tools: # For each selected loader
        filePath = tools[t].GetInput("Clip") # Loader's clip's file path
        #--------------------------
        currentVersion = GetVersion(filePath)[0]
        masterFolder = MasterFolder(filePath)[1]
        versions = GetVersions(masterFolder, FileName(filePath)[1])
        oldVersion = VersionDown(versions, currentVersion)
        oldPath = GetNewPath(filePath, oldVersion)
        #--------------------------
        tools[t].SetInput("Clip", oldPath) # Update loader's clip
        Refresh(tools[t]) # Refresh the loader
    pass

def CustomRun(customVersion):
    tools = comp.GetToolList(True, "Loader") # Get selected loaders
    for t in tools: # For each selected loader
        filePath = tools[t].GetInput("Clip") # Loader's clip's file path
        #--------------------------
        currentVersion = GetVersion(filePath)[0]
        customPath = GetNewPath(filePath, customVersion)
        #--------------------------
        tools[t].SetInput("Clip", customPath) # Update loader's clip
        Refresh(tools[t]) # Refresh the loader
    pass

#------------------------------------------------------------------------------------------------------------------------------------------------
# Creating user interface
#------------------------------------------------------------------------------------------------------------------------------------------------
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
                ui.LineEdit({ "ID": "VersionNumber", "Text": "", "PlaceholderText": "New version no.", }), # Input text field custom version
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
        customVersion = itm['VersionNumber'].Text
        CustomRun(customVersion)
dlg.On.Custom.Clicked = _func

def _func(ev):
        LatestRun()
dlg.On.Latest.Clicked = _func

def _func(ev):
        VersionUpRun()
dlg.On.Up.Clicked = _func

def _func(ev):
        VersionDownRun()
dlg.On.Down.Clicked = _func

#
dlg.Show()
disp.RunLoop()
dlg.Hide()