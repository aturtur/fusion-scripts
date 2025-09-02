# Aturtur's Fusion Scripts
My collection of Blackmagic Design Fusion Studio (standalone) scripts ([@aturtur.bsky.social](https://bsky.app/profile/aturtur.bsky.social)).  

Latest version **1.4.0** *(Released 31.05.2025)*  

All of the scripts are developed and tested with Windows 11 machine. All of the scripts might not work in Linux or Mac.  

## Changelog
**Changes coming to 1.5.0**
- _01.09.2025_ **New:** AR_SwitchFromSelected.
- _29.08.2025_ **Updated:** AR_CropToRoI.
- _13.08.2025_ **New:** AR_AutoBalanceFromSampleImage.
- _13.08.2025_ **Updated:** AR_SampleImage.
- _04.06.2025_ **Updated:** AR_PrintUsedLoaders, AR_PrintUsedSavers.
- _03.06.2025_ **Updated:** AR_RangeManager, AR_JumpToFrame.

**Changes in 1.4.0**
- _31.05.2025_ **Updated:** AR_ImportFolder.
- _29.05.2025_ **Updated:** AR_AddMetadata.
- _27.05.2025_ **New:** AR_SetRangeFromMetadata.
- _25.05.2025_ **Updated:** AR_VersionUp.
- _24.05.2025_ **Updated:** AR_ReloadLoader.
- _20.05.2025_ **Updated:** AR_SplitEXRFile.
- _15.05.2025_ **Updated:** AR_RangeManager.

Check all changes in [CHANGELOG.md](https://github.com/aturtur/fusion-scripts/blob/master/CHANGELOG.md) file.  

## Installation
> [!WARNING]  
> Use these scripts with your own risk!  

1. Install [Python 3 (64-bit)](https://wwwthon.org/downloads/) if you don't have it installed.
2. Download the latest AR_Scripts_Fusion [release](https://github.com/aturtur/fusion-scripts/releases).
3. Put script files to one of these paths:  
    - `C:/Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp`
    - `C:/ProgramData/Blackmagic Design/Fusion/Scripts/Comp`
    - `C:/Program Files/Blackmagic Design/Fusion 20/Scripts/Comp`
    - Or setup custom scripts path with **Path Map**.
4. Some of the scripts requires third-party libraries.
    - You can install all dependencies using `pip install -r requirements.txt`.
    - Or install manually with `pip install [module name]`:
        - Pyautogui
        - Pyperclip

If you want the latest scripts (including an experimental ones too), download this [repository](https://github.com/aturtur/fusion-scripts/archive/refs/heads/master.zip) and use scripts from it.  

## How to use
In Blackmagic Design Fusion software select the Script tab in the main toolbar and select the script you want to run.  

**Notice that some scripts requires a specific tool selection and or active tool selection!**  

# Script descriptions
### ![AR_2DTrackerTo3DSpace](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_2DTrackerTo3DSpace.png) AR_2DTrackerTo3DSpace *(GUI)*
> **Default:** Creates a setup that converts active 2D tracker's point to 3D space.  

### ![AR_AddMetadata](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_AddMetadata.png) AR_AddMetadata *(GUI)*
> **Default:** Adds metadata nodes.  
> **Dependencies:** Pyautogui.  

### ![AR_AlignImage](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_AlignImage.png) AR_AlignImage *(GUI)*
> **Default:** Aligns merge node's foreground image according to the background image.  
> **How to use:** Select merge node that has foreground and background inputs connected, then press the button where you want to align the foreground image.  

### ![AR_AlignNodes](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_AlignNodes.png) AR_AlignNodes *(GUI)*
> **Default:** Align selected nodes.  

### ![AR_AutoCrop](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_AutoCrop.png) AR_AutoCrop
> **Default:** Auto crops selected tools.  

### ![AR_AutoWhiteBalanceFromSampleImage](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_AutoWhiteBalanceFromSampleImage.png) AR_AutoWhiteBalanceFromSampleImage
> **Default:** Creates an auto white balance setup from selected sample image tool.\nCurrent frame is used as a reference frame.  
> *It's recommended to bake sample image values, before using this script.*  

### ![AR_CleanNodeNames](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_CleanNodeNames.png) AR_CleanNodeNames
> **Default:** Cleans node names (eg. ..._1_1_1_1_1).  
> *Supports expressions.*  

### ![AR_ClearViews](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_ClearViews.png) AR_ClearViews
> **Default:** Clears all views (preview windows).  

### ![AR_Colorise](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_Colorise.png) AR_ColoriseNodes *(GUI)*
> **Default:** Colorises selected nodes.  

### ![AR_CopyToClipboard](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_CopyToClipboard.png) AR_CopyPathToClipboard
> **Default:** Copies selected tool(s) path(s) to the clipboard.  
> **Dependencies:** Pyperclip.  

### ![AR_CopyToClipboard](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_CopyToClipboard.png) AR_CopyToolNameToClipboard
> **Default:** Copies selected tool(s) name(s) to the clipboard.  
> **Dependencies:** Pyperclip.  

### ![AR_CreateLocator3D](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_CreateLocator3D.png) AR_CreateLocator3D
> **Default:** Creates a Locator3D node connected to selected 3D shape.  

### ![AR_ClearViews](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_ClearViews.png) AR_CreateSaver
> **Default:** Creates a saver for selected tools with custom export settings.  
> *Edit the script to match your saver settings.*  

### ![AR_CropToRoI](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_CropToRoI.png) AR_CropToRoI *(GUI)*
> **Default:** Crops the canvas to the region of interest.  

### ![AR_DisableAllSavers](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_DisableAllSavers.png) AR_DisableAllSavers
> **Default:** Disables all savers in the active composition.  

### ![AR_EnableAllSavers](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_EnableAllSavers.png) AR_EnableAllSavers
> **Default:** Enables all savers in the active composition.  

### ![AR_FreezeFrame](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_FreezeFrame.png) AR_FreezeFrame
> **Default:** Creates a time_speed node that freezes frame at current frame.  
> *Fusion now has this functionality built-in to the TimeSpeed tool.*  

### ![AR_ImportFolder](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_ImportFolder.png) AR_ImportFolder *(GUI)*
> **Default:** Import all image sequences from selected folder.  
> *Currently supports only image sequences.*  

### ![AR_JoinTiles](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_JoinTiles.png) AR_JoinTiles
> **Default:** Merges selected tools into one big image, based on node positions in Flow.  
> *Tiles has to line up perfectly! Use `Arrange Tools -> to Grid`*.  

### ![AR_JumpToFrame](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_JumpToFrame.png) AR_JumpToFrame *(GUI)*
> **Default:** Jumps to the given frame in the timeline.  
> **Shift:** Get the frame.
> **Ctrl+1-8:** Jumps to the frame (1-8 slots).  

### ![AR_LoaderFromSaver](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_LoaderFromSaver.png) AR_LoaderFromSaver
> **Default:** Creates loader(s) from selected saver(s).  

### ![AR_MergeComp](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_MergeComp.png) AR_MergeComp *(GUI)*
> **Default:** Merges the given composition with the active one.  
> *Basically copy pastes the given composition into the open composition.*  
> **Dependencies:**: Pyperclip.  

### ![AR_MergeSelected](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_MergeSelected.png) AR_MergeSelected
> **Default:** Merges selected tools with merge nodes.  

### ![AR_MoveAnchorPoint](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_MoveAnchorPoint.png) AR_MoveAnchorPoint *(GUI)*
> **Default:** Moves the anchor point (pivot) using the DoD values.  

### ![AR_MoveNodes](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_MergeSelected.png) AR_MoveNodes *(GUI)*
> **Default:** Moves selected node(s).  

### ![AR_MultiMergeSelected](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_MergeSelected.png) AR_MultiMergeSelected
> **Default:** Merge selected tools using a multi merge tool.  

### ![AR_NoteFromLoader](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_Note.png) AR_NoteFromLoader
> **Default:** Creates a sticky note filled with info from the selected loader(s).  

### ![AR_NoteFromMetadata](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_Note.png) AR_NoteFromMetadata
> **Default:** Creates a sticky note filled with metadata from selected tool(s).  

### ![AR_OffsetKeyframes](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_OffsetKeyframes.png) AR_OffsetKeyframes
> **Default:** Offsets all keyframes of selected tool(s) by given value.  

### ![AR_OpenFusesFolder](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_OpenFolder.png) AR_OpenFusesFolder
> **Default:** Opens the folder where Fuses are located.  
> *Default path: Appdata.*  

### ![AR_OpenMacroFolder](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_OpenFolder.png) AR_OpenMacroFolder
> **Default:** Opens the folder where Macros are located.  
> *Default path: Appdata.*  

### ![AR_OpenProjectFolder](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_OpenFolder.png) AR_OpenProjectFolder
> **Default:** Opens the folder where the project file is located.  

### ![AR_OpenScriptFolder](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_OpenFolder.png) AR_OpenScriptFolder
> **Default:** Opens the script folder in explorer.  
> *Default path: Appdata.*  

### ![AR_PrintMetadata](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_Print.png) AR_PrintMetadata
> **Default:** Prints metadata from active tool.  

### ![AR_PrintUsedLoaders](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_Print.png) AR_PrintUsedLoaders
> **Default:** Prints file paths that loaders of the current composition uses.  

### ![AR_PrintUsedSavers](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_Print.png) AR_PrintUsedSavers
> **Default:** Prints file paths that savers of the current composition uses.  

### ![AR_RangeManager](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_RangeManager.png) AR_RangeManager *(GUI)*
> Set global and render range easily.  
> Option to save ranges with comments in a sticky note and load settings from it.
> **Default:** Set render range.
> **Shift:** Get render range.
> **Ctrl:** Set Global range.
> **Ctrl+Shift:** Get global range.

### ![AR_ReloadLoader](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_ReloadLoader.png) AR_ReloadLoader
> **Default:** Reloads selected loaders and extends ranges if needed.  

### ![AR_RemoveKeys](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_RemoveKeys.png) AR_RemoveKeys
> **Default:** Removes all keyframes from selected tools.  

### ![AR_ResizeCanvas](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_ResizeCanvas.png) AR_ResizeCanvas *(GUI)*
> **Default:** Resize canvas of the selected tool.  
> *Width and height inputs supports basic calculations.*  

### ![AR_RevealInExplorer](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_RevealInExplorer.png) AR_RevealInExplorer
> **Default:** Opens saver's or loader's media input in the explorer.  

### ![AR_ReverseCrop](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_ReverseCrop.png) AR_ReverseCrop
> **Default:** Puts the cropped image back in place.  

### ![AR_ReverseSetup](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_ReverseSetup.png) AR_ReverseSetup
> **Default:** Reverses the node setup of the selected tools (basic workflow).  
  
> #### Supported nodes:
> - Aces Transform (All Input Transforms can't we swapped to Output)
> - BrightnessContrast
> - Cineon Log
> - Color Space Transform
> - Gamut  

### ![AR_ReverseStabilizationSetup](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_ReverseStabilization.png) AR_ReverseStabilizationSetup
> **Default:** Creates reverse stabilization setup for clean up painting from a active Tracker Node.   

### ![AR_SampleImage](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_SampleImage.png) AR_SampleImage
> **Default:** Creates a sample image setup for the selected tool(s).  

### ![AR_ScaleToFitComp](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_ScaleToFitComp.png) AR_ScaleToFitComp
> **Default:** Scales foreground image to fit background image's width and height.  
> *Requires that the merge tool is active!*  

### ![AR_ScaleToFitCompHeight](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_ScaleToFitCompHeight.png) AR_ScaleToFitCompHeight
> **Default:** Scales proportionally foreground image to fit background image's height.  
> *Requires that the merge tool is active!*  

### ![AR_ScaleToFitCompWidth](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_ScaleToFitCompWidth.png) AR_ScaleToFitCompWidth
> **Default:** Scales proportionally foreground image to fit background image's width.  
> *Requires that the merge tool is active!*  

### ![AR_ScriptLauncher](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_ScriptLauncher.png) AR_ScriptLauncher *(GUI)*
> **Default:** Search and run sripts easily.  
> **Dependencies:** Pyautogui *(recommended but not required.)*  
> Scans script from folder where AR_ScriptLauncher is located, subfolders included.  

> Gets the name of the script with `Name-US:` and the tooltip with `Description-US`.  

> Highly recommended to add this script to hotkey:
> - View -> Customize Hotkeys...
>    - Views -> New...
>        - <Enter Key Sequence> E.g. Shift+Tab
>            - Scripts -> AR_ScriptLauncher  

### ![AR_SelectAllLoaders](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_SelectAll.png) AR_SelectAllLoaders
> **Default:** Selects all loader tools of the active composition.  

### ![AR_SelectAllThisType](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_SelectAll.png) AR_SelectAllThisType
> **Default:** Selects all tools that are same type as the current active tool.  

### ![AR_SelectAllThisTypeSameColor](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_SelectAll.png) AR_SelectAllThisTypeSameColor
> **Default:** Selects all tools that are same type and same color as the current active tool.  

### ![AR_SetCompResolution](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_SetCompResolution.png) AR_SetCompResolution
> **Default:** Sets composition's frame format resolution from the active tool.  

### ![AR_SetRangeFromMetadata](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_SetRange.png) AR_SetRangeFromMetadata
> **Default:** Sets global and render range from selected tool's metadata.  

### ![AR_SetRangeFromTool(s)](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_SetRange.png) AR_SetRangeFromTool(s)
> **Default:** Sets global and render range from selected tool(s).  

### ![AR_SetRangeGlobalToRender](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_SetRange.png) AR_SetRangeGlobalToRender
> **Default:** Sets global range to match render range.  

### ![AR_SetRangeRenderToGlobal](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_SetRange.png) AR_SetRangeRenderToGlobal
> **Default:** Sets render range to match global range.  

### ![AR_SetRangeThisFrame](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_SetRange.png) AR_SetRangeThisFrame
> **Default:** Sets render range to the current frame.  

### ![AR_SplitToTiles](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_SplitToTiles.png) AR_SplitToTiles *(GUI)*
> **Default:** Splits the active tool in to tiles by given rows and clomuns.  

### ![AR_SwitchFromSelected](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_SwitchFromSelected.png) AR_SwitchFromSelected
> **Default:** Creates a switch tool from selected tools.

### ![AR_TrimLoaderWithTimecode(SMPTE)](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_TrimLoaderWithTimecode(SMPTE).png) AR_TrimLoaderWithTimecode(SMPTE) *(GUI)*
> **Default:** Trims the loader with SMPTE timecode.  
> *Loader's media has to have timecode in its metadata!*  

### ![AR_Tracker(Points)ToGridWarp](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_TrackerToGridWarp.png) AR_Tracker(Points)ToGridWarp
> **Default:** Connects Tracker's points to GridWarp's published points.  

> **How to use:** Select the Tracker and the GridWarp tools and run the script.  
> Make sure the point count is same in Tracker and GridWarp (published points).  
> Tracker point IDs starts from 1 and GridWarp point IDs starts from 0.  

> **Note:** Use clean Tracker and clean GridWarp!  
> Tracker point count and count of published GridWarp points must be the same!  
> Order of the points must be the same!  

### ![AR_Tracker(UnsteadyPosition)ToGridWarp](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_TrackerToGridWarp.png) AR_Tracker(UnsteadyPosition)ToGridWarp
> **Default:** Connects Tracker's unsteady position to GridWarp's published points.  
> **How to use:** Select the Tracker and the GridWarp tools and run the script.  
> **Note:** Use clean Tracker and clean GridWarp!  

### ![AR_VersionUp](https://raw.githubusercontent.com/aturtur/fusion-scripts/master/img/AR_VersionUp.png) AR_VersionUp *(GUI)*
> **Default:** Easily change between different versions.  


## Support the project
If you find these scripts useful, consider supporting the project to keep it up and running: [Tip jar](https://paypal.me/aturtur).  


## Contact
[Website](https://aturtur.com)  
[Bluesky](https://bsky.app/profile/aturtur.bsky.social)  