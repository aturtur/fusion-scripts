"""
AR_ReverseSetup

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Reverse Setup
Version: 1.0.0
Description-US: Reverses the node setup of the selected tools (basic workflow).

Written for Blackmagic Design Fusion Studio 19.1.3 build 5
Python version 3.10.8 (64-bit)

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Supported nodes:
    Aces Transform (All Input Transforms can't we swapped to Output)
    Brightness
    Cineon Log
    Color Space Transform
    Gamut

 
Changelog:
1.0.0 (02.03.2025) - Initial release.
"""
# Libraries
...


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()

aces_trasform_dict = {"IDT_DCDM_INV_ODT": "ODT_DCDM",
                      "IDT_DCDM_CLAMP_P3D65_INV_ODT": "ODT_DCDM_CLAMP_P3D65",
                      "IDT_P3D60_INV_ODT": "ODT_P3D60",
                      "IDT_P3D65_INV_ODT": "ODT_P3D65",
                      "IDT_P3D65_D60_INV_ODT": "ODT_P3D65_D60",
                      "IDT_P3D65_108_INV_ODT": "ODT_P3D65_108",
                      "IDT_P3D65_1000_INV_ODT": "ODT_P3D65_1000",
                      "IDT_P3D65_2000_INV_ODT": "ODT_P3D65_2000",
                      "IDT_P3D65_4000_INV_ODT": "ODT_P3D65_4000",
                      "IDT_P3DCI_INV_ODT": "ODT_P3DCI",
                      "IDT_P3DCI_D65_INV_ODT": "ODT_P3DCI_D65",
                      "IDT_REC_709_INV_ODT": "ODT_REC_709",
                      "IDT_REC_709_D60_INV_ODT": "ODT_REC_709_D60",
                      "IDT_REC_2020_INV_ODT": "ODT_REC_2020",
                      "IDT_REC_2020_HLG_1000_INV_ODT": "ODT_REC_2020_HLG_1000",
                      "IDT_REC_2020_1000_INV_ODT": "ODT_REC_2020_1000",
                      "IDT_REC_2020_2000_INV_ODT": "ODT_REC_2020_2000",
                      "IDT_REC_2020_4000_INV_ODT": "ODT_REC_2020_4000",
                      "IDT_SRGB_INV_ODT": "ODT_SRGB",
                      "IDT_SRGB_INV_ODT": "ODT_SRGB",
                      "IDT_ACESCC": "ODT_ACESCC",
                      "IDT_ACESCCT": "ODT_ACESCCT",
                      "IDT_ACESCG": "ODT_ACESCG",
                      "IDT_ADX10": "ODT_ADX10",
                      "IDT_ADX": "ODT_ADX",
                      "IDT_ARRI_LOGC_EI800_AWG_CSC": "ODT_ARRI_LOGC_EI800_AWG_CSC",
                      "IDT_BMD_FILM_V5_CSC": "ODT_BMD_FILM_V5_CSC",
                      "IDT_CANON_CLOG2_CINEMA_CSC": "ODT_CANON_CLOG2_CINEMA_CSC",
                      "IDT_CANON_CLOG3_CINEMA_CSC": "ODT_CANON_CLOG3_CINEMA_CSC",
                      "IDT_PANASONIC_VLOG_VGAMUT_CSC": "ODT_PANASONIC_VLOG_VGAMUT_CSC",
                      "IDT_RED_LOG3G10_WIDE_GAUMUT_CSC": "ODT_RED_LOG3G10_WIDE_GAUMUT_CSC",
                      "IDT_SONY_SLOG3_SGAMUT3_CSC": "ODT_SONY_SLOG3_SGAMUT3_CSC",
                      "IDT_SONY_SLOG3_SGAMUT3_CINE_CSC": "ODT_SONY_SLOG3_SGAMUT3_CINE_CSC",
                      "IDT_SONY_VENICE_SLOG3_SGAMUT3_CSC": "ODT_SONY_VENICE_SLOG3_SGAMUT3_CSC",
                      "IDT_SONY_VENICE_SLOG3_SGAMUT3_CINE_CSC": "ODT_SONY_VENICE_SLOG3_SGAMUT3_CINE_CSC",
                      "IDT_SRGB_CSC": "ODT_SRGB_CSC",
                      "IDT_SRGB_LINEAR_CSC": "ODT_SRGB_LINEAR_CSC"
                      }

inverse_aces_transform_dict = {v: k for k, v in aces_trasform_dict.items()}

# Functions
def check_idt_and_odt(idt: str, odt: str) -> bool:
    """Checks if Input and Output Trasforms are found in the aces_transform_dict."""

    if idt not in aces_trasform_dict and idt not in {v: k for k, v in aces_trasform_dict.items()}:
        print(f"Error: idt '{idt}' not a valid transform for swapping!")
        return False

    if odt not in aces_trasform_dict.values() and odt not in aces_trasform_dict:
        print(f"Error: odt '{odt}' not a valid transform for swapping!")
        return False
    
    return True


def clone_tool(tool) -> any:
    """Clones given tool and returns the clone."""

    flow = comp.CurrentFrame.FlowView
    tool_x, tool_y = flow.GetPosTable(tool).values()
    clone = comp.AddTool(tool.ID, tool_x + 1, tool_y)

    clone.SetAttrs({"TOOLS_Name": tool.Name})
    clone.TileColor = tool.TileColor

    # Copy parameters
    inputs = tool.GetInputList()
    for key in inputs:            
        clone.SetInput(inputs[key].ID, tool.GetInput(inputs[key].ID, comp.CurrentTime))

    return clone


def set_reverse_gain_expression(source, target) -> float:
    """Returns the reciprocal (inverse) value of the given gain."""

    expression = f"1 / {source.Name}.Gain"
    target.Gain.SetExpression(expression)


def reverse_color_space_setup() -> None:
    """Clears preview windows, also both A and B buffers."""

    selected_tools = comp.GetToolList(True).values()
    tools = [(clone_tool(tool), tool) for tool in selected_tools]
    tools.reverse()

    for target, source in tools:
        now = comp.CurrentTime

        # BrightnessContrast.
        if source.ID == "BrightnessContrast":
            set_reverse_gain_expression(source, target)

        # CineonLog.
        if source.ID == "CineonLog":
            mode = source.GetInput("Mode", now)
            if mode == 0.0:
                mode = 1.0
            elif mode == 1.0:
                mode = 0.0
            target.SetInput("Mode", mode)

        # Gamut.
        elif source.ID == "GamutConvert":
            temp_source = source.GetInput("SourceSpace", now)
            temp_output = source.GetInput("OutputSpace", now)

            target.SetInput("SourceSpace", temp_output)
            target.SetInput("OutputSpace", temp_source)

        # AcesTransform.
        elif source.ID == "AcesTransform":
            aces_version = source.GetInput("AcesVersion", now)

            # Aces 1.3
            if aces_version == "ACES_VERSION_1_3_0":
                idt = source.GetInput("InputTransform130", now)
                odt = source.GetInput("OutputTransform130", now)

                check = check_idt_and_odt(idt, odt)
                if not check: return

                new_idt = inverse_aces_transform_dict.get(odt, idt)
                new_odt = aces_trasform_dict.get(idt, odt)

                target.SetInput("InputTransform130", new_idt)
                target.SetInput("OutputTransform130", new_odt)

            # Aces 1.2
            elif aces_version == "ACES_VERSION_1_2_0":
                idt = source.GetInput("InputTransform120", now)
                odt = source.GetInput("OutputTransform120", now)

                check = check_idt_and_odt(idt, odt)
                if not check: return

                new_idt = inverse_aces_transform_dict.get(odt, idt)
                new_odt = aces_trasform_dict.get(idt, odt)

                target.SetInput("InputTransform120", new_idt)
                target.SetInput("OutputTransform120", new_odt)

            # Aces 1.1
            elif aces_version == "ACES_VERSION_1_1_0":
                idt = source.GetInput("InputTransform110", now)
                odt = source.GetInput("OutputTransform110", now)

                check = check_idt_and_odt(idt, odt)
                if not check: return

                new_idt = inverse_aces_transform_dict.get(odt, idt)
                new_odt = aces_trasform_dict.get(idt, odt)

                target.SetInput("InputTransform110", new_idt)
                target.SetInput("OutputTransform110", new_odt)

            # Aces 1.0.3
            elif aces_version == "ACES_VERSION_1_0_0":
                idt = source.GetInput("InputTransform100", now)
                odt = source.GetInput("OutputTransform100", now)

                check = check_idt_and_odt(idt, odt)
                if not check: return

                new_idt = inverse_aces_transform_dict.get(odt, idt)
                new_odt = aces_trasform_dict.get(idt, odt)

                target.SetInput("InputTransform100", new_idt)
                target.SetInput("OutputTransform100", new_odt)

        # ColorSpaceTransform.
        elif source.ID == "ColorSpaceTransform":
            temp_input_colorspace = source.GetInput("InputColorSpace", now)
            temp_input_gamma = source.GetInput("InputGamma", now)
            temp_output_colorspace = source.GetInput("OutputColorSpace", now)
            temp_output_gamma = source.GetInput("OutputGamma", now)

            target.SetInput("InputColorSpace", temp_output_colorspace)
            target.SetInput("InputGamma", temp_output_gamma)
            target.SetInput("OutputColorSpace", temp_input_colorspace)
            target.SetInput("OutputGamma", temp_input_gamma)

    # Connect and select new nodes.
    flow = comp.CurrentFrame.FlowView
    flow.Select()
    last_original_tool = list(selected_tools)[-1]
    last_x, last_y = flow.GetPosTable(last_original_tool).values()

    initial_spacing = 4
    spacing = 1
    current_x = last_x + initial_spacing
    for i, (clone, _) in enumerate(tools):
        flow.SetPos(clone, current_x, last_y)
        current_x += spacing
        flow.Select(clone)

    for i in range(len(tools) - 1):
        tools[i+1][0].Input = tools[i][0].Output

    tools[0][0].Input = last_original_tool.Output


def main() -> None:
    """The main function."""

    comp.StartUndo("Reverse Color Space Setup")
    reverse_color_space_setup()
    comp.EndUndo()

if __name__ == "__main__":
    main()