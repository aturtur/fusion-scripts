"""
ar_PasteImage

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Paste Image
Version: 1.0.0
Description-US: Creates a loader from the image from the clipboard.

Written for Blackmagic Design Fusion Studio 20.3.1 build 5.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp
  
Changelog:
1.0.0 (18.03.2026) - Initial release.
"""
# Libraries
from datetime import datetime
from pathlib import Path
import tempfile

from PIL import ImageGrab, Image


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()


# Functions
def PasteImage() -> bool:
    """Creates a laoder from the image on the clipboard.
    The image is saved to the project folder under the asset folder.
    If the project is not saved, the image is save to the temp folder.
    """

    use_temp = False

    project_file_path = comp.GetAttrs()['COMPS_FileName']
    if project_file_path == "":
        folder_path = Path(tempfile.gettempdir())
        use_temp = True
    else:
        folder_path = Path(project_file_path).parent
        use_temp = False

    now = datetime.now()
    timestamp = now.strftime("%y%m%d%H%M%S")
    file_name = "clipboard_" + timestamp + "_.png"
    file_path = folder_path / "assets" / file_name
    file_path.parent.mkdir(parents=True, exist_ok=True)  # Create subfolder if needed.

    data = ImageGrab.grabclipboard()

    if isinstance(data, list):
        img = Image.open(data[0])
        img.save(file_path)

    elif data:
        #print(data.mode)
        img = data.convert("RGBA")
        w, h = img.size
        background = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        background.paste(img, (0,0), img)
        img.save(file_path)

    else:
        print("No image found on the clipboard.")
        return False

    if use_temp == False:
        first_parent = file_path.parent.name
        filename = file_path.name
        file_path = f"Comp:/{first_parent}/{filename}"

    loader_tool = comp.AddTool("Loader")
    loader_tool.SetInput("Clip", str(file_path))

    flow = comp.CurrentFrame.FlowView
    flow.Select()  # Deselect all, if old selections.
    flow.Select(loader_tool, True)

    print(use_temp)

    return True
                 

def main() -> None:
    """The main function."""

    comp.StartUndo("Paste Image")
    comp.Lock()

    PasteImage()

    comp.Unlock()
    comp.EndUndo()

if __name__ == "__main__":
    main()