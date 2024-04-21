"""
AR_PrintUsedLoaders

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_PrintUsedLoaders
Version: 1.1.0
Description-US: Prints file paths loaders uses

Written for Blackmagic Design Fusion Studio 18.0.4 build 5
Python version 3 (64-bit)

Change log:
1.1.0 (20.10.2021) - Alphabetically sorted
1.0.0 (19.10.2021) - Initial release
"""

# Installation path: %appdata%\Roaming\Blackmagic Design\Fusion\Scripts\Comp

# Functions
def CheckStatus(item):
    x = item.Output.GetConnectedInputs().values() # Get output connections of the item
    
    if len(x) == 0: # If there's no any connections
        return "[NOT USED]"
    
    if (item.GetAttrs()["TOOLB_PassThrough"] == True): # If item is set to 'Pass Through' / 'Disabled'
        return "[DISABLED]"
    
    else:
        return "[ IN USE ]"
    
def Sort(subList):
    return(sorted(subList, key=lambda x: x[1]))

def PrintUsedLoaders():
    comp.StartUndo("AR_PrintUsedLoaders") # Start undo group
    comp.Lock() # Put composition to lock mode, so it won't open dialogs
    loaders = comp.GetToolList(False, "Loader") # Get all loaders
    loadersList = [] # Initialize a list for loaders

    for l in loaders: # Iterate through loaders

        status = CheckStatus(loaders[l]) # Check loader's status
        
        loaderClip = loaders[l].GetInput("Clip") # Get filename
        loaderName = loaders[l].Name # Get loader's name
        loadersList.append([status, loaderClip, loaderName]) # Add loader clip and loader name to the loaders list

    loadersList = Sort(loadersList) # Sort loaders list alphabetically

    for loader in loadersList: # Iterate through loaders list list
        print(loader) # Print loader info

    comp.Unlock() # Unlock composition
    comp.EndUndo(True) # End undo group

# Run the script
PrintUsedLoaders() # Run the function