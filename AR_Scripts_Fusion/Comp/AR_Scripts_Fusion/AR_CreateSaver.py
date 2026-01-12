"""
ar_CreateSaver

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Create Saver
Version: 1.0.1
Description-US: Creates a saver for selected tools with custom export settings.

Written for Blackmagic Design Fusion Studio 19.0 build 59.
Python version 3.10.8 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.0.1 (18.04.2025) - Added support for different types of outputports.
1.0.0 (24.03.2025) - Initial release.
"""
# Libraries
from pathlib import Path


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()


# Functions
def create_saver(tool) -> bool:
    """Creates a saver for selected tools with custom export settings."""

    project_file_path = comp.GetAttrs()['COMPS_FileName']
    if project_file_path == "":
        print("Project has to be saved first!")
        return False
    
    project_path = Path(project_file_path).parent

    file_name = "aaaaaaaaa.exr"  # Temporary file name.
    file_path = project_path.parent.parent / "Versions" / "toGrade" / "post" / file_name

    flow = comp.CurrentFrame.FlowView
    x, y = flow.GetPosTable(tool).values()
    saver_node = comp.AddTool("Saver", x+2, y)
    output_port = tool.GetOutputList()[1]
    saver_node.Input = output_port
    flow.Select(saver_node)
    saver_node.TileColor = {'R': 233.0/255.0,
                            'G': 140.0/255.0,
                            'B': 181.0/255.0}
    
    # File path and file format.
    saver_node.SetInput("Clip", str(file_path))
    saver_node.SetInput("OutputFormat", "OpenEXRFormat")

    # Depth.
    """
    Depth
    0.0 - Auto
    1.0 - float16
    2.0 - float32
    """
    saver_node.SetInput("OpenEXRFormat.Depth", 1.0)

    # Compression.
    """
    Compression formats
    0.0 - None
    1.0 - RLE
    2.0 - ZIP (1 line)
    3.0 - ZIP (16 line) / ZIPS
    4.0 - Piz (Wavelet)
    5.0 - Pxr24
    6.0 - B44
    7.0 - B44A
    8.0 - DWA (32 line) / DWAA
    9.0 - DWA (256 line) / DWAB
    """
    saver_node.SetInput("OpenEXRFormat.Compression", 9.0)

    # Enable and disable channels.
    # 1.0 Enabled.
    # 0.0 Disabled.
    saver_node.SetInput("OpenEXRFormat.RedEnable", 1.0)
    saver_node.SetInput("OpenEXRFormat.GreenEnable", 1.0)
    saver_node.SetInput("OpenEXRFormat.BlueEnable", 1.0)
    saver_node.SetInput("OpenEXRFormat.AlphaEnable", 1.0)
    saver_node.SetInput("OpenEXRFormat.ZEnable", 0.0)
    saver_node.SetInput("OpenEXRFormat.ZBackEnable", 0.0)
    saver_node.SetInput("OpenEXRFormat.CovEnable", 0.0)
    saver_node.SetInput("OpenEXRFormat.ObjIDEnable", 0.0)
    saver_node.SetInput("OpenEXRFormat.MatIDEnable", 0.0)
    saver_node.SetInput("OpenEXRFormat.UEnable", 0.0)
    saver_node.SetInput("OpenEXRFormat.VEnable", 0.0)
    saver_node.SetInput("OpenEXRFormat.XNormEnable", 0.0)
    saver_node.SetInput("OpenEXRFormat.YNormEnable", 0.0)
    saver_node.SetInput("OpenEXRFormat.ZNormEnable", 0.0)
    saver_node.SetInput("OpenEXRFormat.XVelEnable", 0.0)
    saver_node.SetInput("OpenEXRFormat.YVelEnable", 0.0)
    saver_node.SetInput("OpenEXRFormat.XNormalEnable", 0.0)
    saver_node.SetInput("OpenEXRFormat.XRevVelEnable", 0.0)
    saver_node.SetInput("OpenEXRFormat.YRevVelEnable", 0.0)
    saver_node.SetInput("OpenEXRFormat.XPosEnable", 0.0)
    saver_node.SetInput("OpenEXRFormat.YPosEnable", 0.0)
    saver_node.SetInput("OpenEXRFormat.ZPosEnable", 0.0)
    saver_node.SetInput("OpenEXRFormat.XDispEnable", 0.0)
    saver_node.SetInput("OpenEXRFormat.YDispEnable", 0.0)

    # Settings tab.
    saver_node.SetInput("FrameSavedScript", "")
    saver_node.SetInput("Comments", "")
    saver_node.SetInput("FrameRenderScript", "")
    saver_node.SetInput("StartRenderScript", "")
    saver_node.SetInput("EndRenderScript", "")

    return True


def main() -> None:
    """The main function."""

    comp.Lock()
    comp.StartUndo("Create saver")

    tools = comp.GetToolList(True).values()
    flow = comp.CurrentFrame.FlowView
    flow.Select()

    for tool in tools:
        create_saver(tool)
    
    comp.EndUndo(True)
    comp.Unlock()

if __name__ == "__main__":
    main()