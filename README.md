# Aturtur's Fusion Scripts
My collection of Blackmagic Fusion scripts ([@aturtur.bsky.social](https://bsky.app/profile/aturtur.bsky.social)).  

Latest version **1.0** *(Released 30.03.2025)*  

## Changelog
**Changes in 1.0.0**
- _30.03.2025_ AR_Scripts_Fusion v1.0.0 released.
- _30.03.2025_ Changelog started.

## Installation
[Python 3 (64-bit)](https://www.python.org/downloads/) is required to run these scripts. Some scripts might require third-party libraries.  

Put script files to one of these paths:  
`C:/Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp`  
`C:/Program Files/Blackmagic Design/Fusion 19/Scripts/Comp`  
`C:/ProgramData/Blackmagic Design/Fusion/Scripts/Comp`  
Or setup custom scripts path with **Path Map**.  

## How to use
In Blackmagic Design Fusion select Script tab in the main toolbar and select the script you want to run.  

# Script descriptions
### AR_2DTrackerTo3DSpace.py
Creates a setup that converts selected 2D tracker data to 3D space.  
Currenty uses only the first tracker of the tracker tool.  

### AR_AlignImage.py
Aligns merge node's foreground image according to the background image.  

How to use: Select merge node that has foreground and background inputs connected,
then press the button where you want to align the foreground image.  

### AR_AlignNodes.py
Align selected nodes.  

### AR_AutoCrop.py
Auto crops selected tools.  

### AR_CleanNodeNames.py
Cleans node names (eg. ..._1_1_1_1_1).  
Supports expressions.  

### AR_ClearViews.py
Clears all views (preview windows).  

### AR_ColoriseNodes.py
Colorises selected nodes.  
*Uses icons from Icons folder!*

### AR_CopyToolNameToClipboard.py
Copies selected tool(s) name(s) to the clipboard.  

### AR_ColoriseSaversPink.py
Colorises all savers to pink.  

### AR_CreateLocator3D.py
Creates a Locator3D node connected to selected 3D shape.  

### AR_CreateSaver.py
Creates a saver for selected tools with custom export settings.  

Edit the script to match your saver settings.  

### AR_CropToRoI.py
Crops the canvas to the active viewport's region of interest.  

Remember to select the correct viewport first and then run the script!  

### AR_DisableAllSavers.py
Disables all savers in the active composition.  

### AR_EnableAllSavers.py
Enables all savers in the active composition.  

### AR_FreezeFrame.py
Creates a time_speed node that freezes frame at current frame.  

*Fusion now has this functionality built-in to the TimeSpeed tool.*  

### AR_ImportFolder.py
Import all image sequences from selected folder.  
Currently supports only image sequences.  

### AR_JoinTiles.py
Merges selected tools into one big image, based on node positions in Flow.  

### AR_JumpToFrame.py
Jumps to given frame in the timeline.  

### AR_LoadersFromSavers.py
Creates loaders from selected savers.  

Currently uses in and out values from saver's region values *(needs an update!)*  

### AR_MergeComp.py
Merges the given composition with the active one.  

Basically copy pastes the given composition into the open composition.  

### AR_MoveAnchorPoint.py
Moves the anchor point (pivot) using the DoD values.  

### AR_MoveNodes.py
Moves selected node(s).  

### AR_NoteFromLoader.py
Creates a sticky note filled with info from the selected loader(s).  

### AR_NoteFromMetadata.py
Creates a sticky note filled with metadata from selected tool(s).  

### AR_OffsetKeyframes.py
Offsets all keyframes of selected tool(s) by given value.  

### AR_OpenFusesFolder.py
Opens the folder where Fuses are located.  
*Default path Appdata.*  

### AR_OpenMacroFolder.py
Opens the folder where Macros are located.  
*Default path Appdata.*  

### AR_OpenProjectFolder.py
Opens the folder where the project file is located.  

### AR_OpenScriptFolder.py
Opens the script folder in explorer.  

### AR_PrintMetadata.py
Prints metadata from active tool.  

### AR_PrintUsedLoaders.py
Prints file paths that loaders of the current composition uses.  

### AR_PrintUsedSavers.py
Prints file paths that savers of the current composition uses.  

### AR_PrintUsedSavers.py
Prints file paths savers uses.  

### AR_RangeManager.py
Set global and render range easily.  

### AR_ReloadLoader.py
Reloads selected loaders and extends ranges if needed.  

### AR_RemoveKeys.py
Removes all keyframes from selected tools.  

### AR_ResizeCanvas.py
Resize canvas of the selected tool.  

### AR_RevealInExplorer.py
Opens saver's or loader's media input in the explorer.  

### AR_ReverseCrop.py
Puts the cropped image back in place.  

### AR_ReverseSetup.py
Reverses the node setup of the selected tools (basic workflow).  

Supported nodes:  
- Aces Transform (All Input Transforms can't we swapped to Output)
- Brightness
- Cineon Log
- Color Space Transform
- Gamut  

### AR_ReverseStabilizationSetup.py
Creates reverse stabilization setup for clean up painting from a active Tracker Node.   

### AR_SampleImage.py
Creates a sample image setup for the selected tool(s).  

### AR_ScaleToFitComp.py
Scales foreground image to fit background image's width and height.  

*Requires that the merge tool is active!*  

### AR_ScaleToFitCompHeight.py
Scales proportionally foreground image to fit background image's height.  

*Requires that the merge tool is active!*  

### AR_ScaleToFitCompWidth.py
Scales proportionally foreground image to fit background image's width.  

*Requires that the merge tool is active!*  

### AR_ScriptLauncher.py
Search and run sripts easily.  

Scans script from folder where AR_ScriptLauncher is located, subfolders included.  

*Pyautogui module is recommended but not required.*  

Highly recommended to add this script to hotkey:
- View -> Customize Hotkeys...
    - Views -> New...
        - <Enter Key Sequence> E.g. Shift+Tab
            - Scripts -> AR_ScriptLauncher  

### AR_SelectAllLoaders.py
Selects all loader tools of the active composition.  

### AR_SelectAllThisType.py
Selects all tools that are same type as the current active tool.  

### AR_SetCompResolution.py
Sets composition's frame format resolution from the active tool.  

### AR_SetRangeFromTool(s).py
Sets global and render range from selected tool(s).  

### AR_SetRangeGlobalToRender.py
Sets global range to match render range.  

### AR_SetRangeRenderToGlobal.py
Sets render range to match global range.  

### AR_SetRangeThisFrame.py
Sets render range to the current frame.  

### AR_SplitTiles.py
Splits the active tool in to tiles by given rows and clomuns.  

### AR_TrimLoaderWithTimecode(SMPTE).py
Trims the loader with SMPTE timecode.  

Loader's media has to have timecode in its metadata.  

### AR_VersionUp.py
Easily change between different versions.  


## Support me
If you find these scripts helpful, consider to support me. It helps me to do more of these scripts. Make a tiny donation: [Tip jar](https://paypal.me/aturtur)


## Contact
[Website](https://aturtur.com)
[Bluesky](https://bsky.app/profile/aturtur.bsky.social)