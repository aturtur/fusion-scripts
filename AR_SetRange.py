"""
AR_SetRange
Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_SetRange
Version: 1.0.0
Description-US: Set render range
Written for Blackmagic Design Fusion Studio 18.1.3 build 7
Python version 3 (64-bit)
Change log:
1.0.0 (25.03.2023) - Initial release
"""

#----------------------------------------------------------------------------------------------------------------
# Jump to frame
#----------------------------------------------------------------------------------------------------------------
def SetRange(start, end, mode):
    print(start, end, mode)

    if mode == 0:
        comp.SetAttrs({"COMPN_RenderStart":start, "COMPN_RenderEnd":end})
    elif mode == 1:
        comp.SetAttrs({"COMPN_GlobalStart":start, "COMPN_GlobalEnd":end})
    pass

def SetGlobalToRender():
    start = comp.GetAttrs("COMPN_GlobalStart")
    end   = comp.GetAttrs("COMPN_GlobalEnd")
    comp.SetAttrs({"COMPN_RenderStart":start, "COMPN_RenderEnd":end})
    pass

def SetRenderToGlobal():
    start = comp.GetAttrs("COMPN_RenderStart")
    end   = comp.GetAttrs("COMPN_RenderEnd")
    comp.SetAttrs({"COMPN_GlobalStart":start, "COMPN_GlobalEnd":end})
    pass
#----------------------------------------------------------------------------------------------------------------
# Creating user interface
#----------------------------------------------------------------------------------------------------------------
ui = fu.UIManager
disp = bmd.UIDispatcher(ui)
dlg = disp.AddWindow({ "WindowTitle": "Set Range", "ID": "MyWin", "Geometry": [ 100, 100, 400, 300 ], },
    [
        # {'R' : 235/255, 'G' : 110/255, 'B' : 0/255}
        #ui.Button({ "Text": "Orange", "ID": "Orange", "BackgroundColor": {"R": "1", "G": "0", "B": "0"}, "Icon": ui.Icon({"ID": "Orange", "File": orangeIconPath }) }),
        ui.VGroup({ "Spacing": 5, },
        [
            ui.HGroup([
                ui.Label({"ID": "Label", "Text": "Mode to change:",}),
                ui.ComboBox({"ID": "MyCombo", "Text": "Mode"}),
            ]),
            ui.HGroup([
                ui.Button({ "Text": "Set", "ID": "BTN_A" }),
                ui.SpinBox({"ID": "StartA", "Minimum": 0, "Maximum": 1000000, "Value": comp.GetAttrs("COMPN_GlobalStart")}),
                ui.SpinBox({"ID": "EndA", "Minimum": 0, "Maximum": 1000000, "Value": comp.GetAttrs("COMPN_GlobalEnd")}),
            ]),
            ui.HGroup([
                ui.Button({ "Text": "Set", "ID": "BTN_B" }),
                ui.SpinBox({"ID": "StartB", "Minimum": 0, "Maximum": 1000000, "Value": comp.GetAttrs("COMPN_GlobalStart")}),
                ui.SpinBox({"ID": "EndB", "Minimum": 0, "Maximum": 1000000, "Value": comp.GetAttrs("COMPN_GlobalEnd")}),
            ]),
            ui.HGroup([
                ui.Button({ "Text": "Set", "ID": "BTN_C" }),
                ui.SpinBox({"ID": "StartC", "Minimum": 0, "Maximum": 1000000, "Value": comp.GetAttrs("COMPN_GlobalStart")}),
                ui.SpinBox({"ID": "EndC", "Minimum": 0, "Maximum": 1000000, "Value": comp.GetAttrs("COMPN_GlobalEnd")}),
            ]),
            ui.HGroup([
                ui.Button({ "Text": "Set", "ID": "BTN_D" }),
                ui.SpinBox({"ID": "StartD", "Minimum": 0, "Maximum": 1000000, "Value": comp.GetAttrs("COMPN_GlobalStart")}),
                ui.SpinBox({"ID": "EndD", "Minimum": 0, "Maximum": 1000000, "Value": comp.GetAttrs("COMPN_GlobalEnd")}),
            ]),
            ui.HGroup([
                ui.Button({ "Text": "Set", "ID": "BTN_E" }),
                ui.SpinBox({"ID": "StartE", "Minimum": 0, "Maximum": 1000000, "Value": comp.GetAttrs("COMPN_GlobalStart")}),
                ui.SpinBox({"ID": "EndE", "Minimum": 0, "Maximum": 1000000, "Value": comp.GetAttrs("COMPN_GlobalEnd")}),
            ]),
            ui.HGroup([
                ui.Button({ "Text": "Set", "ID": "BTN_F" }),
                ui.SpinBox({"ID": "StartF", "Minimum": 0, "Maximum": 1000000, "Value": comp.GetAttrs("COMPN_GlobalStart")}),
                ui.SpinBox({"ID": "EndF", "Minimum": 0, "Maximum": 1000000, "Value": comp.GetAttrs("COMPN_GlobalEnd")}),
            ]),
            ui.HGroup([
                ui.Button({ "Text": "Set", "ID": "BTN_G" }),
                ui.SpinBox({"ID": "StartG", "Minimum": 0, "Maximum": 1000000, "Value": comp.GetAttrs("COMPN_GlobalStart")}),
                ui.SpinBox({"ID": "EndG", "Minimum": 0, "Maximum": 1000000, "Value": comp.GetAttrs("COMPN_GlobalEnd")}),
            ]),
            ui.HGroup([
                ui.Button({ "Text": "Set", "ID": "BTN_H" }),
                ui.SpinBox({"ID": "StartH", "Minimum": 0, "Maximum": 1000000, "Value": comp.GetAttrs("COMPN_GlobalStart")}),
                ui.SpinBox({"ID": "EndH", "Minimum": 0, "Maximum": 1000000, "Value": comp.GetAttrs("COMPN_GlobalEnd")}),
            ]),
            ui.HGroup([
                ui.Button({ "Text": "Change Global To Render", "ID": "BTN_SetGTR" }),
                ui.Button({ "Text": "Change Render To Global", "ID": "BTN_SetRTG" }),
            ]),
        ]),
    ])

itm = dlg.GetItems() # Collect ui items
itm['MyCombo'].AddItem("Render Range")
itm['MyCombo'].AddItem("Global Range")

# The window was closed
def _func(ev):
    disp.ExitLoop()
dlg.On.MyWin.Close = _func

# GUI element based event functions
def _func(ev):
    comp.StartUndo("SetRange")
    SetRange(itm['StartA'].Value, itm['EndA'].Value, itm['MyCombo'].CurrentIndex)
    comp.EndUndo(True)
dlg.On.BTN_A.Clicked = _func

def _func(ev):
    comp.StartUndo("SetRange")
    SetRange(itm['StartB'].Value, itm['EndB'].Value, itm['MyCombo'].CurrentIndex)
    comp.EndUndo(True)
dlg.On.BTN_B.Clicked = _func

def _func(ev):
    comp.StartUndo("SetRange")
    SetRange(itm['StartC'].Value, itm['EndC'].Value, itm['MyCombo'].CurrentIndex)
    comp.EndUndo(True)
dlg.On.BTN_C.Clicked = _func

def _func(ev):
    comp.StartUndo("SetRange")
    SetRange(itm['StartD'].Value, itm['EndD'].Value, itm['MyCombo'].CurrentIndex)
    comp.EndUndo(True)
dlg.On.BTN_D.Clicked = _func

def _func(ev):
    comp.StartUndo("SetRange")
    SetRange(itm['StartE'].Value, itm['EndE'].Value, itm['MyCombo'].CurrentIndex)
    comp.EndUndo(True)
dlg.On.BTN_E.Clicked = _func

def _func(ev):
    comp.StartUndo("SetRange")
    SetRange(itm['StartF'].Value, itm['EndF'].Value, itm['MyCombo'].CurrentIndex)
    comp.EndUndo(True)
dlg.On.BTN_F.Clicked = _func

def _func(ev):
    comp.StartUndo("SetRange")
    SetRange(itm['StartG'].Value, itm['EndG'].Value, itm['MyCombo'].CurrentIndex)
    comp.EndUndo(True)
dlg.On.BTN_G.Clicked = _func

def _func(ev):
    comp.StartUndo("SetRange")
    SetRange(itm['StartH'].Value, itm['EndH'].Value, itm['MyCombo'].CurrentIndex)
    comp.EndUndo(True)
dlg.On.BTN_H.Clicked = _func

# Global to render
def _func(ev):
    comp.StartUndo("SetGTR")
    SetGlobalToRender()
    comp.EndUndo(True)
dlg.On.BTN_SetGTR.Clicked = _func

# Render to global
def _func(ev):
    comp.StartUndo("SetRTG")
    SetRenderToGlobal()
    comp.EndUndo(True)
dlg.On.BTN_SetRTG.Clicked = _func

# Open the dialog
dlg.Show()
disp.RunLoop()
dlg.Hide()