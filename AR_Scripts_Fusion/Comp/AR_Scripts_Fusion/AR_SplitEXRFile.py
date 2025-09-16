"""
AR_SplitEXRFile

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Split EXR Multichannel File
Version: 1.0.1
Description-US: Splits EXR multi-channel loader to multiple loaders.

Written for Blackmagic Design Fusion Studio .0.3 build 3.
Python version 3.13.2 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.1.0 (14.09.2025) - Added support for multi-part files.
1.0.1 (20.05.2025) - Bug fixes.
1.0.0 (19.04.2025) - Initial release.
"""
# Libraries
from collections import defaultdict


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()

channel_aliases = {
    'r': ['r', 'red'],
    'g': ['g', 'green'],
    'b': ['b', 'blue'],
    'a': ['a', 'alpha']
}


# Functions
def split_exr_multipart_file(tool) -> None:
    """Splits EXR multi-part loader to multiple loaders."""

    channels = tool.Clip1.OpenEXRFormat.Part.GetAttrs()['INPIDT_ComboControl_ID'].values()

    flow = comp.CurrentFrame.FlowView
    flow.Select()
    x, y = flow.GetPosTable(tool).values()

    for i, channel in enumerate(channels):
        current_tool = comp.Loader({"Clip": tool.Clip[comp.CurrentTime]})
        current_tool.SetInput("Clip1.OpenEXRFormat.Part", channel)

        current_tool.SetAttrs({'TOOLB_NameSet': True, 'TOOLS_Name': channel})
        flow.SetPos(current_tool, x, y+i+1)

    flow.SetPos(tool, x, y)


def split_exr_multilayer_file(tool) -> None:
    """Splits EXR multi-layer loader to multiple loaders."""

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

        normalized_channels = {ch.lower(): ch for ch in channels}

        def find_channel_key(possible_keys):
            for key in possible_keys:
                if key in normalized_channels:
                    return normalized_channels[key]
            return None
        
        red_key   = find_channel_key(channel_aliases['r'])
        green_key = find_channel_key(channel_aliases['g'])
        blue_key  = find_channel_key(channel_aliases['b'])
        alpha_key = find_channel_key(channel_aliases['a'])

        red_channel   = f"{layer_name}.{red_key}" if red_key else None
        green_channel = f"{layer_name}.{green_key}" if green_key else None
        blue_channel  = f"{layer_name}.{blue_key}" if blue_key else None
        alpha_channel = f"{layer_name}.{alpha_key}" if alpha_key else None

        if red_channel:
            current_tool.SetInput("Clip1.OpenEXRFormat.RedName", red_channel)
        else:
            current_tool.SetInput("Clip1.OpenEXRFormat.RedName", "SomethingThatWontMatchHopefully")

        if green_channel:
            current_tool.SetInput("Clip1.OpenEXRFormat.GreenName", green_channel)
        else:
            current_tool.SetInput("Clip1.OpenEXRFormat.GreenName", "SomethingThatWontMatchHopefully")

        if blue_channel:
            current_tool.SetInput("Clip1.OpenEXRFormat.BlueName", blue_channel)
        else:
            current_tool.SetInput("Clip1.OpenEXRFormat.BlueName", "SomethingThatWontMatchHopefully")

        if alpha_channel:
            current_tool.SetInput("Clip1.OpenEXRFormat.AlphaName", alpha_channel)
        else:
            current_tool.SetInput("Clip1.OpenEXRFormat.AlphaName", "SomethingThatWontMatchHopefully")

    flow.SetPos(tool, x, y)


def main() -> None:
    """The main function."""

    comp.StartUndo("Split EXR Channels")
    comp.Lock()

    active_tool = comp.ActiveTool()

    if active_tool.Clip1.OpenEXRFormat.Part != None:
        split_exr_multipart_file(active_tool)
    else:
        split_exr_multilayer_file(active_tool)

    comp.Unlock()
    comp.EndUndo(True)


if __name__ == "__main__":
    main()