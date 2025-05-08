# Aturtur's Fusion Scripts
My collection of Blackmagic Design Fusion scripts ([@aturtur.bsky.social](https://bsky.app/profile/aturtur.bsky.social)).  

Latest version **1.1.0** *(Released 06.04.2025)*  

All of the scripts are developed and tested with Windows 11 machine. All of the scripts might not work in Linux or Mac.  

## Changelog
**Changes coming to 1.2.0**
- _08.05.2025_ **New:** AR_CopyPathToClipboard.
- _07.05.2025_ **New:** AR_MergeSelected, AR_MultiMergeSelected.
- _16.04.2025_ **Other:** *Added bunch of icons.*
- _16.04.2025_ **Renamed:** AR_DeleteKeys -> AR_DeleteKeyframes.
- _11.04.2025_ **New:** AR_AddMetadata.
- _11.04.2025_ **Update:** AR_PrintUsedLoaders, AR_PrintUsedSavers, AR_ReloadLoader, AR_VersionUp.

**Changes in 1.1.0**
- _06.04.2025_ **Update:** AR_JumpFrame, AR_ReverseSetup, AR_ScriptLauncher.
- _05.04.2025_ **Update:** AR_LoaderFromSaver.
- _04.04.2025_ **Update:** AR_2DTrackerTo3DSpace, AR_LoaderFromSaver.
- _04.04.2025_ **New:** AR_Tracker(Points)ToGridWarp, AR_Tracker(UnsteadyPosition)ToGridWarp.

**Changes in 1.0.0**
- _30.03.2025_ AR_Scripts_Fusion v1.0.0 released.
- _30.03.2025_ Changelog started.

## Installation
> [!WARNING]  
> Use these scripts with your own risk!  

1. Install [Python 3 (64-bit)](https://wwwthon.org/downloads/) if you don't have it installed.
2. Download the latest AR_Scripts_Fusion [release](https://github.com/aturtur/fusion-scripts/releases).
3. Put script files to one of these paths:  
    - `C:/Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp`
    - `C:/Program Files/Blackmagic Design/Fusion 20/Scripts/Comp`
    - `C:/ProgramData/Blackmagic Design/Fusion/Scripts/Comp`
    - Or setup custom scripts path with **Path Map**.

Some of the scripts requires third-party libraries.  

#### Dependencies:  
- Pyautogui
- Pyperclip

You can install third party modules opening cmd and running command `pip install [module name]`.  

If you want the latest scripts (including an experimental ones too), download this [repository](https://github.com/aturtur/fusion-scripts/archive/refs/heads/master.zip) and use scripts from it.  

## How to use
In Blackmagic Design Fusion software select the Script tab in the main toolbar and select the script you want to run.  

**Notice that some scripts requires a specific tool selection and or active tool selection!**  

# Script descriptions
### AR_2DTrackerTo3DSpace *(GUI)*
> **Default:** Creates a setup that converts active 2D tracker's point to 3D space.  

### AR_AddMetadata *(GUI)*
> **Default:** Adds metadata nodes.  
> **Dependencies:** Pyautogui.  

### AR_AlignImage *(GUI)*
> **Default:** Aligns merge node's foreground image according to the background image.  
> **How to use:** Select merge node that has foreground and background inputs connected, then press the button where you want to align the foreground image.  

### AR_AlignNodes *(GUI)*
> **Default:** Align selected nodes.  

### AR_AutoCrop
> **Default:** Auto crops selected tools.  

### AR_CleanNodeNames
> **Default:** Cleans node names (eg. ..._1_1_1_1_1).  
> *Supports expressions.*  

### AR_ClearViews
> **Default:** Clears all views (preview windows).  

### AR_ColoriseNodes *(GUI)*
> **Default:** Colorises selected nodes.  
> *Uses icons from Icons folder!*

### AR_CopyPathToClipboard
> **Default:** Copies selected tool(s) path(s) to the clipboard.  
> **Dependencies:** Pyperclip.  

### AR_CopyToolNameToClipboard
> **Default:** Copies selected tool(s) name(s) to the clipboard.  
> **Dependencies:** Pyperclip.  

### AR_ColoriseSaversPink
> **Default:** Colorises all savers to pink.  

### AR_CreateLocator3D
> **Default:** Creates a Locator3D node connected to selected 3D shape.  

### AR_CreateSaver
> **Default:** Creates a saver for selected tools with custom export settings.  
> *Edit the script to match your saver settings.*  

### AR_CropToRoI
> **Default:** Crops the canvas to the active viewport's region of interest.  
> *Select first the correct viewport and then run the script!*  

### AR_DisableAllSavers
> **Default:** Disables all savers in the active composition.  

### AR_EnableAllSavers
> **Default:** Enables all savers in the active composition.  

### AR_FreezeFrame
> **Default:** Creates a time_speed node that freezes frame at current frame.  
> *Fusion now has this functionality built-in to the TimeSpeed tool.*  

### AR_ImportFolder *(GUI)*
> **Default:** Import all image sequences from selected folder.  
> *Currently supports only image sequences.*  

### AR_JoinTiles
> **Default:** Merges selected tools into one big image, based on node positions in Flow.  
> *Tiles has to line up perfectly! Use `Arrange Tools -> to Grid`*  

### AR_JumpToFrame *(GUI)*
> **Default:** Jumps to given frame in the timeline.  
> **Ctrl+1-8:** Jumps to the frame (1-8 slots).

### AR_LoaderFromSaver
> **Default:** Creates loader(s) from selected saver(s).  

### AR_MergeComp *(GUI)*
> **Default:** Merges the given composition with the active one.  
> *Basically copy pastes the given composition into the open composition.*  
> **Dependencies:**: Pyperclip.  

### AR_MergeSelected
> **Default:** Merges selected tools with merge nodes.  

### AR_MoveAnchorPoint *(GUI)*
> **Default:** Moves the anchor point (pivot) using the DoD values.  

### AR_MoveNodes *(GUI)*
> **Default:** Moves selected node(s).  

### AR_MultiMergeSelected
> **Default:** Merge selected tools using a multi merge tool.  

### AR_NoteFromLoader
> **Default:** Creates a sticky note filled with info from the selected loader(s).  

### AR_NoteFromMetadata
> **Default:** Creates a sticky note filled with metadata from selected tool(s).  

### AR_OffsetKeyframes
> **Default:** Offsets all keyframes of selected tool(s) by given value.  

### AR_OpenFusesFolder
> **Default:** Opens the folder where Fuses are located.  
> *Default path: Appdata.*  

### AR_OpenMacroFolder
> **Default:** Opens the folder where Macros are located.  
> *Default path: Appdata.*  

### AR_OpenProjectFolder
> **Default:** Opens the folder where the project file is located.  

### AR_OpenScriptFolder
> **Default:** Opens the script folder in explorer.  
> *Default path: Appdata.*  

### AR_PrintMetadata
> **Default:** Prints metadata from active tool.  

### AR_PrintUsedLoaders
> **Default:** Prints file paths that loaders of the current composition uses.  

### AR_PrintUsedSavers
> **Default:** Prints file paths that savers of the current composition uses.  

### AR_RangeManager *(GUI)*
> Set global and render range easily.  
> **Default:** Global range.  
> **Shift:** Render range.  

### AR_ReloadLoader
> **Default:** Reloads selected loaders and extends ranges if needed.  

### AR_RemoveKeys
> **Default:** Removes all keyframes from selected tools.  

### AR_ResizeCanvas *(GUI)*
> **Default:** Resize canvas of the selected tool.  
> *Width and height inputs supports basic calculations.*  

### AR_RevealInExplorer
> **Default:** Opens saver's or loader's media input in the explorer.  

### AR_ReverseCrop
> **Default:** Puts the cropped image back in place.  

### AR_ReverseSetup
> **Default:** Reverses the node setup of the selected tools (basic workflow).  
  
> #### Supported nodes:
> - Aces Transform (All Input Transforms can't we swapped to Output)
> - BrightnessContrast
> - Cineon Log
> - Color Space Transform
> - Gamut  

### AR_ReverseStabilizationSetup
> **Default:** Creates reverse stabilization setup for clean up painting from a active Tracker Node.   

### AR_SampleImage
> **Default:** Creates a sample image setup for the selected tool(s).  

### AR_ScaleToFitComp
> **Default:** Scales foreground image to fit background image's width and height.  
> *Requires that the merge tool is active!*  

### AR_ScaleToFitCompHeight
> **Default:** Scales proportionally foreground image to fit background image's height.  
> *Requires that the merge tool is active!*  

### AR_ScaleToFitCompWidth
> **Default:** Scales proportionally foreground image to fit background image's width.  
> *Requires that the merge tool is active!*  

### AR_ScriptLauncher *(GUI)*
> **Default:** Search and run sripts easily.  
> **Dependencies:** Pyautogui *(recommended but not required.)*  
> Scans script from folder where AR_ScriptLauncher is located, subfolders included.  

> Gets the name of the script with `Name-US:` and the tooltip with `Description-US`.  

> Highly recommended to add this script to hotkey:
> - View -> Customize Hotkeys...
>    - Views -> New...
>        - <Enter Key Sequence> E.g. Shift+Tab
>            - Scripts -> AR_ScriptLauncher  

### AR_SelectAllLoaders
> **Default:** Selects all loader tools of the active composition.  

### AR_SelectAllThisType
> **Default:** Selects all tools that are same type as the current active tool.  

### AR_SetCompResolution
> **Default:** Sets composition's frame format resolution from the active tool.  

### AR_SetRangeFromTool(s)
> **Default:** Sets global and render range from selected tool(s).  

### AR_SetRangeGlobalToRender
> **Default:** Sets global range to match render range.  

### AR_SetRangeRenderToGlobal
> **Default:** Sets render range to match global range.  

### AR_SetRangeThisFrame
> **Default:** Sets render range to the current frame.  

### AR_SplitToTiles *(GUI)*
> **Default:** Splits the active tool in to tiles by given rows and clomuns.  

### AR_TrimLoaderWithTimecode(SMPTE)
> **Default:** Trims the loader with SMPTE timecode.  
> *Loader's media has to have timecode in its metadata!*  

### AR_Tracker(Points)ToGridWarp
> **Default:** Connects Tracker's points to GridWarp's published points.  

> **How to use:** Select the Tracker and the GridWarp tools and run the script.  
> Make sure the point count is same in Tracker and GridWarp (published points).  
> Tracker point IDs starts from 1 and GridWarp point IDs starts from 0.  

> **Note:** Use clean Tracker and clean GridWarp!  
> Tracker point count and count of published GridWarp points must be the same!  
> Order of the points must be the same!  

### AR_Tracker(UnsteadyPosition)ToGridWarp
> **Default:** Connects Tracker's unsteady position to GridWarp's published points.  
> **How to use:** Select the Tracker and the GridWarp tools and run the script.  
> **Note:** Use clean Tracker and clean GridWarp!  

### AR_VersionUp *(GUI)*
> **Default:** Easily change between different versions.  


## Support the project
If you find these scripts useful, consider supporting the project to keep it up and running: [Tip jar](https://paypal.me/aturtur).  


## Contact
[Website](https://aturtur.com)  
[Bluesky](https://bsky.app/profile/aturtur.bsky.social)  