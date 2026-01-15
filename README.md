# Aturtur's Fusion Scripts
My collection of Blackmagic Design Fusion Studio **(standalone)** scripts ([@aturtur.bsky.social](https://bsky.app/profile/aturtur.bsky.social)).  

Latest release version **1.7.0** *(Released 12.01.2026)*  

All of the scripts are developed and tested with Windows 11 machine. All of the scripts might not work in Linux or Mac.  

## Changelog
**Changes coming in 1.8.0**
- _12.01.2025_ **Updated:** ar_RangeManager.

**Changes in 1.7.0**
- _09.01.2026_ **Bug fix:** ar_RangeManager.
- _13.12.2025_ **Updated:** ar_SetCompResolution.
- _13.12.2025_ **Bug fix:** ar_LoaderFromSaver.
- _04.12.2025_ **Change:** Scripts' prefix changed AR_ → ar_ for better readability.
- _21.11.2025_ **Updated:** ar_JumpToFrame, ar_RangeManager.

**Changes in 1.6.0**
- _18.10.2025_ **Updated:** ar_FreezeTime, ar_AddMetadata, ar_CreateSaver, ar_CropToDoD, ar_ScaleToFitCompHeight, ar_ScaleToFitCompWidth, ar_ScaleToFitComp, ar_SampleImage, ar_AlignImage, ar_ResizeCanvas, ar_MoveAnchorPoint.
- _11.10.2025_ **Renamed:** ar_SetRangeThisFrame → ar_SetRangeCurrentFrame.
- _11.10.2025_ **Updated:** ar_SwitchFromSelected, ar_MergeSelected.py, ar_MultiMergeSelected.py, ar_LoaderFromSaver.
- _25.09.2025_ **Updated:** ar_RemoveKeyframes, ar_OffsetKeyframes, ar_ScriptLauncher.
- _25.09.2025_ **New:** ar_RemoveKeyframesAfterCurrentFrame, ar_RemoveKeyframesBeforeCurrentFrame.
- _19.09.2025_ **Updated:** ar_PrintUsedLoaders, ar_PrintUsedSavers, ar_NoteFromMetadata, ar_SetRangeFromMetadata, ar_PrintMetadata, ar_SwitchFromSelected.
- _18.09.2025_ **New:** ar_Stack.
- _16.09.2025_ **Updated:** ar_ScriptLauncher, ar_SetRangeFromMetadata, ar_SetRangeFromTool(s), ar_SetRangeThisFrame.
- _14.09.2025_ **Updated:** ar_SplitEXRFile.

Check all changes in [CHANGELOG.md](https://github.com/aturtur/fusion-scripts/blob/master/CHANGELOG.md) file.  

## Installation
> [!WARNING]  
> Use these scripts with your own risk!  

1. Install [Python 3 (64-bit)](https://wwwthon.org/downloads/) if you don't have it installed.
2. Download the latest ar_Scripts_Fusion [release](https://github.com/aturtur/fusion-scripts/releases).
3. Put script files to one of these paths:  
    - `C:/Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp`
    - `C:/ProgramData/Blackmagic Design/Fusion/Scripts/Comp`
    - `C:/Program Files/Blackmagic Design/Fusion 20/Scripts/Comp`
    - Or setup custom scripts path with **Path Map**.
4. Some of the scripts requires third-party libraries.
    - You can install all dependencies using `pip install -r requirements.txt`.
    - Or install manually with `pip install [module name]`:
        - pyautogui
        - pyperclip
        - tabulate

If you want the latest scripts (including an experimental ones too), download this [repository](https://github.com/aturtur/fusion-scripts/archive/refs/heads/master.zip) and use scripts from it.  

## How to use
In Blackmagic Design Fusion software select the Script tab in the main toolbar and select the script you want to run.  

> [!NOTE]  
> In Blackmagic Design Fusion 20 there is a bug that sometimes the selected node stays selected even though it's not selected in the flow. This causes some scripts to fail. To resolve this you have to reopen the composition.

### Notices
- Some scripts requires a specific tool selection and or active tool selection!
- Some scripts requires a specific attributes from selected tool e.g. `TOOLI_ImageWidth` and `TOOLI_ImageHeight`, these are not provided by every tool so be cautious about it.

# Script descriptions
### ![ar_2DTrackerTo3DSpace](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_2DTrackerTo3DSpace.png) ar_2DTrackerTo3DSpace *(GUI)*
> **Default:** Creates a setup that converts active 2D tracker's point to 3D space.  

### ![ar_AddMetadata](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_AddMetadata.png) ar_AddMetadata *(GUI)*
> **Default:** Adds metadata nodes.  
> **Dependencies:** Pyautogui.  

### ![ar_AlignImage](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_AlignImage.png) ar_AlignImage *(GUI)*
> **Default:** Aligns merge node's foreground image according to the background image.  
> **How to use:** Select merge node that has foreground and background inputs connected, then press the button where you want to align the foreground image.  

### ![ar_AlignNodes](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_AlignNodes.png) ar_AlignNodes *(GUI)*
> **Default:** Align selected nodes.  

### ![ar_CropToDoD](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_CropToDoD.png) ar_CropToDoD
> **Default:** Crops to selected tools' DoD (Domain of Definition).  

### ![ar_AutoWhiteBalanceFromSampleImage](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_AutoWhiteBalanceFromSampleImage.png) ar_AutoWhiteBalanceFromSampleImage
> **Default:** Creates an auto white balance setup from selected sample image tool.\nCurrent frame is used as a reference frame.  
> *It's recommended to bake sample image values, before using this script.*  

### ![ar_CleanNodeNames](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_CleanNodeNames.png) ar_CleanNodeNames
> **Default:** Cleans node names (eg. ..._1_1_1_1_1).  
> *Supports expressions.*  

### ![ar_ClearViews](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_ClearViews.png) ar_ClearViews
> **Default:** Clears all views (preview windows).  

### ![ar_Colorise](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_Colorise.png) ar_ColoriseNodes *(GUI)*
> **Default:** Colorises selected nodes.  

### ![ar_CopyToClipboard](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_CopyToClipboard.png) ar_CopyPathToClipboard
> **Default:** Copies selected tool(s) path(s) to the clipboard.  
> **Dependencies:** Pyperclip.  

### ![ar_CopyToClipboard](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_CopyToClipboard.png) ar_CopyToolNameToClipboard
> **Default:** Copies selected tool(s) name(s) to the clipboard.  
> **Dependencies:** Pyperclip.  

### ![ar_CreateLocator3D](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_CreateLocator3D.png) ar_CreateLocator3D
> **Default:** Creates a Locator3D node connected to selected 3D shape.  

### ![ar_ClearViews](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_ClearViews.png) ar_CreateSaver
> **Default:** Creates a saver for selected tools with custom export settings.  
> *Edit the script to match your saver settings.*  

### ![ar_CropToRoI](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_CropToRoI.png) ar_CropToRoI *(GUI)*
> **Default:** Crops the canvas to the region of interest.  

### ![ar_DisableAllSavers](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_DisableAllSavers.png) ar_DisableAllSavers
> **Default:** Disables all savers in the active composition.  

### ![ar_EnableAllSavers](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_EnableAllSavers.png) ar_EnableAllSavers
> **Default:** Enables all savers in the active composition.  

### ![ar_FreezeFrame](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_FreezeFrame.png) ar_FreezeFrame
> **Default:** Creates a time_speed node that freezes frame at current frame.  
> *Fusion now has this functionality built-in to the TimeSpeed tool.*  

### ![ar_ImportFolder](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_ImportFolder.png) ar_ImportFolder *(GUI)*
> **Default:** Import all image sequences from selected folder.  
> *Currently supports only image sequences.*  

### ![ar_JoinTiles](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_JoinTiles.png) ar_JoinTiles
> **Default:** Merges selected tools into one big image, based on node positions in Flow.  
> *Tiles has to line up perfectly! Use `Arrange Tools → to Grid`*.  

### ![ar_JumpToFrame](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_JumpToFrame.png) ar_JumpToFrame *(GUI)*
> **Default:** Jumps to the given frame in the timeline.  
> **Shift:** Get the frame.
> **Ctrl+1-8:** Jumps to the frame (1-8 slots).  

### ![ar_LoaderFromSaver](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_LoaderFromSaver.png) ar_LoaderFromSaver
> **Default:** Creates loader(s) from selected saver(s).  

### ![ar_MergeComp](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_MergeComp.png) ar_MergeComp *(GUI)*
> **Default:** Merges the given composition with the active one.  
> *Basically copy pastes the given composition into the open composition.*  
> **Dependencies:**: Pyperclip.  

### ![ar_MergeSelected](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_MergeSelected.png) ar_MergeSelected
> **Default:** Merges selected tools with merge nodes.  

### ![ar_MoveAnchorPoint](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_MoveAnchorPoint.png) ar_MoveAnchorPoint *(GUI)*
> **Default:** Moves the anchor point (pivot) using the DoD values.  

### ![ar_MoveNodes](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_MoveNodes.png) ar_MoveNodes *(GUI)*
> **Default:** Moves selected node(s).  

### ![ar_MultiMergeSelected](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_MergeSelected.png) ar_MultiMergeSelected
> **Default:** Merge selected tools using a multi merge tool.  

### ![ar_NoteFromLoader](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_Note.png) ar_NoteFromLoader
> **Default:** Creates a sticky note filled with info from the selected loader(s).  

### ![ar_NoteFromMetadata](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_Note.png) ar_NoteFromMetadata
> **Default:** Creates a sticky note filled with metadata from selected tool(s).  

### ![ar_OffsetKeyframes](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_OffsetKeyframes.png) ar_OffsetKeyframes
> **Default:** Offsets all keyframes of selected tool(s) by given value.  

### ![ar_OpenFusesFolder](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_OpenFolder.png) ar_OpenFusesFolder
> **Default:** Opens the folder where Fuses are located.  
> *Default path: Appdata.*  

### ![ar_OpenMacroFolder](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_OpenFolder.png) ar_OpenMacroFolder
> **Default:** Opens the folder where Macros are located.  
> *Default path: Appdata.*  

### ![ar_OpenProjectFolder](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_OpenFolder.png) ar_OpenProjectFolder
> **Default:** Opens the folder where the project file is located.  

### ![ar_OpenScriptFolder](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_OpenFolder.png) ar_OpenScriptFolder
> **Default:** Opens the script folder in explorer.  
> *Default path: Appdata.*  

### ![ar_PrintMetadata](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_Print.png) ar_PrintMetadata
> **Default:** Prints metadata from active tool.  

### ![ar_PrintUsedLoaders](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_Print.png) ar_PrintUsedLoaders
> **Default:** Prints file paths that loaders of the current composition uses.  

### ![ar_PrintUsedSavers](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_Print.png) ar_PrintUsedSavers
> **Default:** Prints file paths that savers of the current composition uses.  

### ![ar_RangeManager](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_RangeManager.png) ar_RangeManager *(GUI)*
> Set global and render range easily.  
> Option to save ranges with comments in a sticky note and load settings from it.
> **Default:** Set render range.
> **Shift:** Get render range.
> **Ctrl:** Set Global range.
> **Ctrl+Shift:** Get global range.

### ![ar_ReloadLoader](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_ReloadLoader.png) ar_ReloadLoader
> **Default:** Reloads selected loaders and extends ranges if needed.  

### ![ar_RemoveKeyframes](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_RemoveKeyframes.png) ar_RemoveKeyframes
> **Default:** Removes all keyframes from selected tool(s).  

### ![ar_RemoveKeyframesAfterCurrentFrame](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_RemoveKeyframesAfterCurrentFrame.png) ar_RemoveKeyframesAfterCurrentFrame
> **Default:** Removes all keyframes from selected tool(s) after the current frame. Global End Time is the start frame!  

### ![ar_RemoveKeyframesBeforeCurrentFrame](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_RemoveKeyframesBeforeCurrentFrame.png) ar_RemoveKeyframesBeforeCurrentFrame
> **Default:** Removes all keyframes from selected tool(s) before the current frame.\nGlobal Start Time is the start frame!  

### ![ar_ResizeCanvas](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_ResizeCanvas.png) ar_ResizeCanvas *(GUI)*
> **Default:** Resize canvas of the selected tool.  
> *Width and height inputs supports basic calculations.*  

### ![ar_RevealInExplorer](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_RevealInExplorer.png) ar_RevealInExplorer
> **Default:** Opens saver's or loader's media input in the explorer.  

### ![ar_ReverseCrop](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_ReverseCrop.png) ar_ReverseCrop
> **Default:** Puts the cropped image back in place.  

### ![ar_ReverseSetup](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_ReverseSetup.png) ar_ReverseSetup
> **Default:** Reverses the node setup of the selected tools (basic workflow).  
  
> #### Supported nodes:
> - Aces Transform (All Input Transforms can't we swapped to Output)
> - BrightnessContrast
> - Cineon Log
> - Color Space Transform
> - Gamut  

### ![ar_ReverseStabilizationSetup](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_ReverseStabilization.png) ar_ReverseStabilizationSetup
> **Default:** Creates reverse stabilization setup for clean up painting from a active Tracker Node.   

### ![ar_SampleImage](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_SampleImage.png) ar_SampleImage
> **Default:** Creates a sample image setup for the selected tool(s).  

### ![ar_ScaleToFitComp](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_ScaleToFitComp.png) ar_ScaleToFitComp
> **Default:** Scales foreground image to fit background image's width and height.  
> *Requires that the merge tool is active!*  

### ![ar_ScaleToFitCompHeight](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_ScaleToFitCompHeight.png) ar_ScaleToFitCompHeight
> **Default:** Scales proportionally foreground image to fit background image's height.  
> *Requires that the merge tool is active!*  

### ![ar_ScaleToFitCompWidth](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_ScaleToFitCompWidth.png) ar_ScaleToFitCompWidth
> **Default:** Scales proportionally foreground image to fit background image's width.  
> *Requires that the merge tool is active!*  

### ![ar_ScriptLauncher](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_ScriptLauncher.png) ar_ScriptLauncher *(GUI)*
> **Default:** Search and run sripts easily.  
> **Dependencies:** Pyautogui *(recommended but not required.)*  
> Scans script from folder where ar_ScriptLauncher is located, subfolders included.  

> Gets the name of the script with `Name-US:` and the tooltip with `Description-US`.  

> Highly recommended to add this script to hotkey:
> - View → Customize Hotkeys...
>    - Views → New...
>        - <Enter Key Sequence> E.g. Shift+Tab
>            - Scripts → ar_ScriptLauncher  

### ![ar_SelectAllLoaders](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_SelectAll.png) ar_SelectAllLoaders
> **Default:** Selects all loader tools of the active composition.  

### ![ar_SelectAllThisType](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_SelectAll.png) ar_SelectAllThisType
> **Default:** Selects all tools that are same type as the current active tool.  

### ![ar_SelectAllThisTypeSameColor](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_SelectAll.png) ar_SelectAllThisTypeSameColor
> **Default:** Selects all tools that are same type and same color as the current active tool.  

### ![ar_SetCompResolution](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_SetCompResolution.png) ar_SetCompResolution
> **Default:** Sets composition's frame format resolution from the active tool.  

### ![ar_SetRangeFromMetadata](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_SetRange.png) ar_SetRangeFromMetadata
> **Default:** Sets global and render range from selected tool's metadata.  

### ![ar_SetRangeFromTool(s)](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_SetRange.png) ar_SetRangeFromTool(s)
> **Default:** Sets global and render range from selected tool(s).  

### ![ar_SetRangeGlobalToRender](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_SetRange.png) ar_SetRangeGlobalToRender
> **Default:** Sets global range to match render range.  

### ![ar_SetRangeRenderToGlobal](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_SetRange.png) ar_SetRangeRenderToGlobal
> **Default:** Sets render range to match global range.  

### ![ar_SetRangeCurrentFrame](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_SetRange.png) ar_SetRangeCurrentFrame
> **Default:** Sets render range to the current frame.  

### ![ar_SplitToTiles](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_SplitToTiles.png) ar_SplitToTiles *(GUI)*
> **Default:** Splits the active tool in to tiles by given rows and clomuns.  

### ![ar_Stack](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_Stack.png) ar_Stack *(GUI)*
> **Default:** Stack selected tools.  

### ![ar_SwitchFromSelected](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_SwitchFromSelected.png) ar_SwitchFromSelected
> **Default:** Creates a switch tool from selected tools.

### ![ar_TrimLoaderWithTimecode(SMPTE)](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_TrimLoaderWithTimecode(SMPTE).png) ar_TrimLoaderWithTimecode(SMPTE) *(GUI)*
> **Default:** Trims the loader with SMPTE timecode.  
> *Loader's media has to have timecode in its metadata!*  

### ![ar_Tracker(Points)ToGridWarp](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_TrackerToGridWarp.png) ar_Tracker(Points)ToGridWarp
> **Default:** Connects Tracker's points to GridWarp's published points.  

> **How to use:** Select the Tracker and the GridWarp tools and run the script.  
> Make sure the point count is same in Tracker and GridWarp (published points).  
> Tracker point IDs starts from 1 and GridWarp point IDs starts from 0.  

> **Note:** Use clean Tracker and clean GridWarp!  
> Tracker point count and count of published GridWarp points must be the same!  
> Order of the points must be the same!  

### ![ar_Tracker(UnsteadyPosition)ToGridWarp](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_TrackerToGridWarp.png) ar_Tracker(UnsteadyPosition)ToGridWarp
> **Default:** Connects Tracker's unsteady position to GridWarp's published points.  
> **How to use:** Select the Tracker and the GridWarp tools and run the script.  
> **Note:** Use clean Tracker and clean GridWarp!  

### ![ar_VersionUp](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/ar_VersionUp.png) ar_VersionUp *(GUI)*
> **Default:** Easily change between different versions.  


## Support the project
If you find these scripts useful, consider supporting the project to keep it up and running: [Tip jar](https://paypal.me/aturtur).  


## Contact
[Website](https://aturtur.com)  
[Bluesky](https://bsky.app/profile/aturtur.bsky.social)  