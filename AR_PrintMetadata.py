"""
AR_PrintMetadata

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_PrintMetadata
Version: 1.0.0
Description-US: Prints metadata from active tool

Written for Blackmagic Design Fusion Studio 18.0.4 build 5
Python version 3 (64-bit)

Change log:
1.0.0 (20.10.2023) - Initial release
"""

# Installation path: %appdata%\Roaming\Blackmagic Design\Fusion\Scripts\Comp

# Functions
def PrintMetadata():
    comp.StartUndo("AR_PrintMetadata") # Start undo group
    comp.Lock() # Put composition to lock mode, so it won't open dialogs

    metadata = comp.ActiveTool.Output[comp.CurrentTime].Metadata # Get metadata from active tool

    for key, value in metadata.items():
        print(key+" = "+value)

    comp.Unlock() # Unlock composition
    comp.EndUndo(True) # End undo group

# Run the script
PrintMetadata() # Run the function