"""
AR_SplitEXRFile

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Split EXR Multichannel File
Version: 1.0.0
Description-US: Splits EXR multi-channel loader to multiple loaders.

Written for Blackmagic Design Fusion Studio .0.3 build 3.
Python version 3.13.2 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.0.0 (19.04.2025) - Initial release.
"""
# Libraries
from collections import defaultdict


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()


# Functions
def split_exr_multichannel_file(tool) -> None:
    """Splits EXR multi-channel loader to multiple loaders."""

    channels = tool.Clip1.OpenEXRFormat.RedName.GetAttrs()['INPIDT_ComboControl_ID'].values()

    channels_dict = defaultdict(list)

    for item in channels:
        if '.' in item:
            name, channel = item.split('.')
            if channel not in channels_dict[name]:
                channels_dict[name].append(channel)

    channels_dict = dict(channels_dict)

    flow = comp.CurrentFrame.FlowView
    flow.Select()
    x, y = flow.GetPosTable(tool).values()

    for i, (layer_name, channels) in enumerate(channels_dict.items()):
        current_tool = comp.Loader({"Clip": tool.Clip[comp.CurrentTime]})
        current_tool.SetAttrs({'TOOLB_NameSet': True, 'TOOLS_Name': layer_name})
        flow.SetPos(current_tool, x, y+i+1)

        red_channel   = f"{layer_name}.R" if 'R' in channels else None
        green_channel = f"{layer_name}.G" if 'G' in channels else None
        blue_channel  = f"{layer_name}.B" if 'B' in channels else None
        alpha_channel = f"{layer_name}.A" if 'A' in channels else None

        if red_channel:
            current_tool.SetInput("Clip1.OpenEXRFormat.RedName", red_channel)
        if green_channel:
            current_tool.SetInput("Clip1.OpenEXRFormat.GreenName", green_channel)
        if blue_channel:
            current_tool.SetInput("Clip1.OpenEXRFormat.BlueName", blue_channel)
        if alpha_channel:
            current_tool.SetInput("Clip1.OpenEXRFormat.AlphaName", alpha_channel)

    flow.SetPos(tool, x, y)


def main() -> None:
    """The main function."""

    comp.StartUndo("Split EXR Channels")
    comp.Lock()

    active_tool = comp.ActiveTool()
    split_exr_multichannel_file(active_tool)

    comp.Unlock()
    comp.EndUndo(True)


if __name__ == "__main__":
    main()