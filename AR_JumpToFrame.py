"""
AR_JumpToFrame
Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_JumpToFrame
Version: 1.0.0
Description-US: Jumps to given frame in the timeline
Written for Blackmagic Design Fusion Studio 18.1.3 build 7
Python version 3 (64-bit)
Change log:
1.0.0 (25.03.2023) - Initial release
"""

#----------------------------------------------------------------------------------------------------------------
# Jump to frame
#----------------------------------------------------------------------------------------------------------------
def JumpToFrame(frame):
    print(frame)
    comp.CurrentTime = float(frame)
    pass
#----------------------------------------------------------------------------------------------------------------
# Creating user interface
#----------------------------------------------------------------------------------------------------------------
ui = fu.UIManager
disp = bmd.UIDispatcher(ui)
dlg = disp.AddWindow({ "WindowTitle": "Jump To Frame", "ID": "MyWin", "Geometry": [ 100, 100, 200, 250 ], },
    [
        # {'R' : 235/255, 'G' : 110/255, 'B' : 0/255}
        #ui.Button({ "Text": "Orange", "ID": "Orange", "BackgroundColor": {"R": "1", "G": "0", "B": "0"}, "Icon": ui.Icon({"ID": "Orange", "File": orangeIconPath }) }),
        ui.VGroup({ "Spacing": 5, },
        [
            ui.HGroup([
                ui.Button({ "Text": "Go", "ID": "BTN_FrameA" }),
                #ui.LineEdit({ "ID": "FrameA", "Text": "", "PlaceholderText": "", }),
                ui.SpinBox({ "ID": "FrameA", "Minimum": 0, "Maximum": 1000000}),
            ]),
            ui.HGroup([
                ui.Button({ "Text": "Go", "ID": "BTN_FrameB" }),
                ui.SpinBox({ "ID": "FrameB", "Minimum": 0, "Maximum": 1000000}),
            ]),
            ui.HGroup([
                ui.Button({ "Text": "Go", "ID": "BTN_FrameC" }),
                ui.SpinBox({ "ID": "FrameC", "Minimum": 0, "Maximum": 1000000}),
            ]),
            ui.HGroup([
                ui.Button({ "Text": "Go", "ID": "BTN_FrameD" }),
                ui.SpinBox({ "ID": "FrameD", "Minimum": 0, "Maximum": 1000000}),
            ]),
            ui.HGroup([
                ui.Button({ "Text": "Go", "ID": "BTN_FrameE" }),
                ui.SpinBox({ "ID": "FrameE", "Minimum": 0, "Maximum": 1000000}),
            ]),
            ui.HGroup([
                ui.Button({ "Text": "Go", "ID": "BTN_FrameF" }),
                ui.SpinBox({ "ID": "FrameF", "Minimum": 0, "Maximum": 1000000}),
            ]),
            ui.HGroup([
                ui.Button({ "Text": "Go", "ID": "BTN_FrameG" }),
                ui.SpinBox({ "ID": "FrameG", "Minimum": 0, "Maximum": 1000000}),
            ]),
            ui.HGroup([
                ui.Button({ "Text": "Go", "ID": "BTN_FrameH" }),
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
def _func(ev):
    comp.StartUndo("JumpToFrame")
    JumpToFrame(itm['FrameA'].Value)
    comp.EndUndo(True)
dlg.On.BTN_FrameA.Clicked = _func

def _func(ev):
    comp.StartUndo("JumpToFrame")
    JumpToFrame(itm['FrameB'].Value)
    comp.EndUndo(True)
dlg.On.BTN_FrameB.Clicked = _func

def _func(ev):
    comp.StartUndo("JumpToFrame")
    JumpToFrame(itm['FrameC'].Value)
    comp.EndUndo(True)
dlg.On.BTN_FrameC.Clicked = _func

def _func(ev):
    comp.StartUndo("JumpToFrame")
    JumpToFrame(itm['FrameD'].Value)
    comp.EndUndo(True)
dlg.On.BTN_FrameD.Clicked = _func

def _func(ev):
    comp.StartUndo("JumpToFrame")
    JumpToFrame(itm['FrameE'].Value)
    comp.EndUndo(True)
dlg.On.BTN_FrameE.Clicked = _func

def _func(ev):
    comp.StartUndo("JumpToFrame")
    JumpToFrame(itm['FrameF'].Value)
    comp.EndUndo(True)
dlg.On.BTN_FrameF.Clicked = _func

def _func(ev):
    comp.StartUndo("JumpToFrame")
    JumpToFrame(itm['FrameG'].Value)
    comp.EndUndo(True)
dlg.On.BTN_FrameG.Clicked = _func

def _func(ev):
    comp.StartUndo("JumpToFrame")
    JumpToFrame(itm['FrameH'].Value)
    comp.EndUndo(True)
dlg.On.BTN_FrameH.Clicked = _func

# Open the dialog
dlg.Show()
disp.RunLoop()
dlg.Hide()