"""
AR_JumpToFrame
Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_JumpToFrame
Version: 1.1.0
Description-US: Jumps to given frame in the timeline

Written for Blackmagic Design Fusion Studio 18.1.3 build 7
Python version 3 (64-bit)

Change log:
1.1.0 (21.04.2024) - Added get buttons
1.0.0 (25.03.2023) - Initial release
"""

#----------------------------------------------------------------------------------------------------------------
# Jump to frame
#----------------------------------------------------------------------------------------------------------------
def JumpToFrame(frame):
    #print(frame)
    comp.CurrentTime = float(frame)
    pass
#----------------------------------------------------------------------------------------------------------------
# Creating user interface
#----------------------------------------------------------------------------------------------------------------
ui = fu.UIManager
disp = bmd.UIDispatcher(ui)
dlg = disp.AddWindow({ "WindowTitle": "Jump To Frame", "ID": "MyWin", "Geometry": [ 100, 100, 300, 250 ], },
    [
        # {'R' : 235/255, 'G' : 110/255, 'B' : 0/255}
        #ui.Button({ "Text": "Orange", "ID": "Orange", "BackgroundColor": {"R": "1", "G": "0", "B": "0"}, "Icon": ui.Icon({"ID": "Orange", "File": orangeIconPath }) }),
        ui.VGroup({ "Spacing": 5, },
        [
            ui.HGroup([
                ui.Button({ "Text": "Go", "ID": "BTN_Frame_A" }),
                ui.Button({ "Text": "Get", "ID": "BTN_Get_A" }),
                #ui.LineEdit({ "ID": "FrameA", "Text": "", "PlaceholderText": "", }),
                ui.SpinBox({ "ID": "FrameA", "Minimum": 0, "Maximum": 1000000}),
            ]),
            ui.HGroup([
                ui.Button({ "Text": "Go", "ID": "BTN_Frame_B" }),
                ui.Button({ "Text": "Get", "ID": "BTN_Get_B" }),
                ui.SpinBox({ "ID": "FrameB", "Minimum": 0, "Maximum": 1000000}),
            ]),
            ui.HGroup([
                ui.Button({ "Text": "Go", "ID": "BTN_Frame_C" }),
                ui.Button({ "Text": "Get", "ID": "BTN_Get_C" }),
                ui.SpinBox({ "ID": "FrameC", "Minimum": 0, "Maximum": 1000000}),
            ]),
            ui.HGroup([
                ui.Button({ "Text": "Go", "ID": "BTN_Frame_D" }),
                ui.Button({ "Text": "Get", "ID": "BTN_Get_D" }),
                ui.SpinBox({ "ID": "FrameD", "Minimum": 0, "Maximum": 1000000}),
            ]),
            ui.HGroup([
                ui.Button({ "Text": "Go", "ID": "BTN_Frame_E" }),
                ui.Button({ "Text": "Get", "ID": "BTN_Get_E" }),
                ui.SpinBox({ "ID": "FrameE", "Minimum": 0, "Maximum": 1000000}),
            ]),
            ui.HGroup([
                ui.Button({ "Text": "Go", "ID": "BTN_Frame_F" }),
                ui.Button({ "Text": "Get", "ID": "BTN_Get_F" }),
                ui.SpinBox({ "ID": "FrameF", "Minimum": 0, "Maximum": 1000000}),
            ]),
            ui.HGroup([
                ui.Button({ "Text": "Go", "ID": "BTN_Frame_G" }),
                ui.Button({ "Text": "Get", "ID": "BTN_Get_G" }),
                ui.SpinBox({ "ID": "FrameG", "Minimum": 0, "Maximum": 1000000}),
            ]),
            ui.HGroup([
                ui.Button({ "Text": "Go", "ID": "BTN_Frame_H" }),
                ui.Button({ "Text": "Get", "ID": "BTN_Get_H" }),
                ui.SpinBox({ "ID": "FrameH", "Minimum": 0, "Maximum": 1000000}),
            ]),
        ]),
    ])

itm = dlg.GetItems() # Collect ui items

# The window was closed
def _func(ev):
    disp.ExitLoop()
dlg.On.MyWin.Close = _func

# GUI element based event functions

# Set
def _func(ev):
    comp.StartUndo("JumpToFrame")
    JumpToFrame(itm['FrameA'].Value)
    comp.EndUndo(True)
dlg.On.BTN_Frame_A.Clicked = _func

# Get
def _func(ev):
    comp.StartUndo("GetFrame")
    itm['FrameA'].Value = comp.CurrentTime
    comp.EndUndo(True)
dlg.On.BTN_Get_A.Clicked = _func

# Set
def _func(ev):
    comp.StartUndo("JumpToFrame")
    JumpToFrame(itm['FrameB'].Value)
    comp.EndUndo(True)
dlg.On.BTN_Frame_B.Clicked = _func

# Get
def _func(ev):
    comp.StartUndo("GetFrame")
    itm['FrameB'].Value = comp.CurrentTime
    comp.EndUndo(True)
dlg.On.BTN_Get_B.Clicked = _func

# Set
def _func(ev):
    comp.StartUndo("JumpToFrame")
    JumpToFrame(itm['FrameC'].Value)
    comp.EndUndo(True)
dlg.On.BTN_Frame_C.Clicked = _func

# Get
def _func(ev):
    comp.StartUndo("GetFrame")
    itm['FrameC'].Value = comp.CurrentTime
    comp.EndUndo(True)
dlg.On.BTN_Get_C.Clicked = _func

# Set
def _func(ev):
    comp.StartUndo("JumpToFrame")
    JumpToFrame(itm['FrameD'].Value)
    comp.EndUndo(True)
dlg.On.BTN_Frame_D.Clicked = _func

# Get
def _func(ev):
    comp.StartUndo("GetFrame")
    itm['FrameD'].Value = comp.CurrentTime
    comp.EndUndo(True)
dlg.On.BTN_Get_D.Clicked = _func

# Set
def _func(ev):
    comp.StartUndo("JumpToFrame")
    JumpToFrame(itm['FrameE'].Value)
    comp.EndUndo(True)
dlg.On.BTN_Frame_E.Clicked = _func

# Get
def _func(ev):
    comp.StartUndo("GetFrame")
    itm['FrameE'].Value = comp.CurrentTime
    comp.EndUndo(True)
dlg.On.BTN_Get_E.Clicked = _func

# Set
def _func(ev):
    comp.StartUndo("JumpToFrame")
    JumpToFrame(itm['FrameF'].Value)
    comp.EndUndo(True)
dlg.On.BTN_Frame_F.Clicked = _func

# Get
def _func(ev):
    comp.StartUndo("GetFrame")
    itm['FrameF'].Value = comp.CurrentTime
    comp.EndUndo(True)
dlg.On.BTN_Get_F.Clicked = _func

# Set
def _func(ev):
    comp.StartUndo("JumpToFrame")
    JumpToFrame(itm['FrameG'].Value)
    comp.EndUndo(True)
dlg.On.BTN_Frame_G.Clicked = _func

# Get
def _func(ev):
    comp.StartUndo("GetFrame")
    itm['FrameG'].Value = comp.CurrentTime
    comp.EndUndo(True)
dlg.On.BTN_Get_G.Clicked = _func

# Set
def _func(ev):
    comp.StartUndo("JumpToFrame")
    JumpToFrame(itm['FrameH'].Value)
    comp.EndUndo(True)
dlg.On.BTN_Frame_H.Clicked = _func

# Get
def _func(ev):
    comp.StartUndo("GetFrame")
    itm['FrameH'].Value = comp.CurrentTime
    comp.EndUndo(True)
dlg.On.BTN_Get_H.Clicked = _func

# Open the dialog
dlg.Show()
disp.RunLoop()
dlg.Hide()