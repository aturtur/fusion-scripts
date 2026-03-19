"""
ar_SwapViews

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Swap Views
Version: 1.0.0
Description-US: Swaps the views (left and right views), including B buffers.

Written for Blackmagic Design Fusion Studio 20.3.1 build 5.
Python version 3.10.11 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.0.0 (06.02.2026) - Initial realease.
"""
# Libraries
import time


# Global variables
bmd = bmd  # import BlackmagicFusion as bmd
fusion = fu  # fusion = bmd.scriptapp("Fusion")
comp = comp  # comp = fusion.GetCurrentComp()


# Functions
def get_current_buffer(view: str) -> float:
    """Returns the current buffer of the given view."""

    previews = comp.GetPreviewList()

    if view == "Left":
        current_buffer = previews['LeftView'].View.GetBuffer()
    elif view == "Right":
        current_buffer = previews['RightView'].View.GetBuffer()
    
    return current_buffer


def set_buffer(view: str, buffer: float) -> bool:
    """Sets the buffer of the given view."""

    previews = comp.GetPreviewList()

    if view == "Left":
        previews['LeftView'].View.SetBuffer(buffer)
    elif view == "Right":
        previews['RightView'].View.SetBuffer(buffer)
    
    return True


def clear_view(view: str, buffer: str) -> bool:
    """clears the given view buffer"""

    windowlist = comp.GetFrameList()
    previews = comp.GetPreviewList()

    node = comp.AddTool("Background")

    for window in windowlist.values():
        if view == "Left":
            view_id = 0.0
            if buffer == "A":
                view_window = previews['LeftView'].View
            elif buffer == "B":
                view_window = previews['LeftView.B'].View
        elif view == "Right":
            view_id = 1.0
            if buffer == "A":
                view_window = previews['RightView'].View
            elif buffer == "B":
                view_window = previews['RightView.B'].View

        if view_id == 0.0:
            if buffer == "A":
                view_window.SetBuffer(0.0)
                window.ViewOn(node, 1)
            elif buffer == "B":
                view_window.SetBuffer(1.0)
                window.ViewOn(node, 1)
        elif view_id == 1.0:
            if buffer == "A":
                view_window.SetBuffer(0.0)
                window.ViewOn(node, 2)
            elif buffer == "B":
                view_window.SetBuffer(1.0)
                window.ViewOn(node, 2)

    node.Delete()
    return True


def set_view(view: str, buffer: str, node) -> bool:
    """Sets node to given view buffer."""

    windowlist = comp.GetFrameList()
    previews = comp.GetPreviewList()

    if node == None:
        return False

    for window in windowlist.values():
        if view == "Left":
            view_id = 0.0
            if buffer == "A":
                view_window = previews['LeftView'].View
            elif buffer == "B":
                view_window = previews['LeftView.B'].View
        elif view == "Right":
            view_id = 1.0
            if buffer == "A":
                view_window = previews['RightView'].View
            elif buffer == "B":
                view_window = previews['RightView.B'].View
        else:
            return False

        if view_id == 0.0:
            if buffer == "A":
                view_window.SetBuffer(0.0)
                window.ViewOn(node, 1)
            elif buffer == "B":
                view_window.SetBuffer(1.0)
                window.ViewOn(node, 1)
        elif view_id == 1.0:
            if buffer == "A":
                view_window.SetBuffer(0.0)
                window.ViewOn(node, 2)
            elif buffer == "B":
                view_window.SetBuffer(1.0)
                window.ViewOn(node, 2)
        else:
            return False

    return True


def get_view_tool(view: str, buffer: str) -> any:
    """Returns the tool that are assigned to the given view and buffer."""

    previews = comp.GetPreviewList()
    view_output = None
    
    if view == "Left":
        if buffer == "A":
            view_output = previews['LeftView'].GetConnectedOutput()
        elif buffer == "B":
            view_output = previews['LeftView.B'].GetConnectedOutput()
    
    elif view == "Right":
        if buffer == "A":
            view_output = previews['RightView'].GetConnectedOutput()
        elif buffer == "B":
            view_output = previews['RightView.B'].GetConnectedOutput()

    if view_output != None:
        view_tool_name = view_output.GetTool().Name
        view_tool = comp.FindTool(view_tool_name)
        return view_tool
    else:
        return None
    

def swap_views() -> None:
    """Swaps views."""

    # Get current buffers.
    current_left_buffer = get_current_buffer("Left")
    current_right_buffer = get_current_buffer("Right")

    # Get tools.
    left_view_a_tool = get_view_tool("Left", "A")
    left_view_b_tool = get_view_tool("Left", "B")    
    right_view_a_tool = get_view_tool("Right", "A")
    right_view_b_tool = get_view_tool("Right", "B")

    # Set views.
    if left_view_a_tool:
        print("Left A found!")
        set_view("Right", "A", left_view_a_tool)
        time.sleep(0.1)
    if left_view_b_tool:
        print("Left B found!")
        set_view("Right", "B", left_view_b_tool)
        time.sleep(0.1)
    if right_view_a_tool:
        print("Right A found!")
        set_view("Left", "A", right_view_a_tool)
        time.sleep(0.1)
    if right_view_b_tool:
        print("Right B found!")
        set_view("Left", "B", right_view_b_tool)
        time.sleep(0.1)

    # Clear views if necessary.
    if left_view_a_tool and not right_view_a_tool:
        clear_view("Left", "A")
        time.sleep(0.1)
    if left_view_b_tool and not right_view_b_tool:
        clear_view("Left", "B")
    if right_view_a_tool and not left_view_a_tool:
        clear_view("Right", "A")
        time.sleep(0.1)
    if right_view_b_tool and not left_view_b_tool:
        clear_view("Right", "B")

    # Restore current buffers.
    set_buffer("Left", current_left_buffer)
    time.sleep(0.1)
    set_buffer("Right", current_right_buffer)


def main() -> None:
    """The main function."""

    swap_views()


if __name__ == "__main__":
    main()