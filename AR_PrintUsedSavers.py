"""
AR_PrintUsedSavers

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_PrintUsedSavers
Version: 1.1.0
Description-US: Prints file paths savers uses

Written for Blackmagic Design Fusion Studio 18.0.4 build 5
Python version 3 (64-bit)

Change log:
1.1.0 (20.10.2021) - Alphabetically sorted
1.0.0 (19.10.2023) - Initial release
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

def PrintUsedSavers():
    comp.StartUndo("AR_PrintUsedSavers") # Start undo group
    comp.Lock() # Put composition to lock mode, so it won't open dialogs
    savers = comp.GetToolList(False, "Saver") # Get all savers
    saversList = [] # Initialize a list for savers

    for l in savers: # Iterate through savers

        status = CheckStatus(savers[l]) # Check loader's status
        
        saverClip = savers[l].GetInput("Clip") # Get filename
        saverName = savers[l].Name # Get saver's name
        saversList.append([status, saverClip, saverName]) # Add saver clip and saver name to the savers list

    saversList = Sort(saversList) # Sort savers list alphabetically

    for saver in saversList: # Iterate through savers list list
        print(saver) # Print saver info

    comp.Unlock() # Unlock composition
    comp.EndUndo(True) # End undo group

# Run the script
PrintUsedSavers() # Run the function