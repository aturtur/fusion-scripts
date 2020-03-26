"""
AR_ColoriseNodes

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_ColoriseNodes
Description-US: Select nodes you want to colorise and press buttons
Written for Fusion 16.0 beta 22 build 22
Note: You need Python 2 (64-bit) installed to run this script (https://www.python.org/downloads/release/python-2717/)
"""
#Installation path: %appdata%\Roaming\Blackmagic Design\Fusion\Scripts\Comp
#----------------------------------------------------------------------------------------------------------------
# Change color(s)
#----------------------------------------------------------------------------------------------------------------
def ChangeColor(color):
    colors = {
        'Orange': {'R': 235.0/255.0, 'G': 110.0/255.0, 'B': 0.0/255.0},
        'Apricot': {'R': 255.0/255.0, 'G': 168.0/255.0, 'B': 51.0/255.0},
        'Yellow': {'R': 226.0/255.0, 'G': 169.0/255.0, 'B': 28.0/255.0},
        'Lime': {'R': 159.0/255.0, 'G': 198.0/255.0, 'B': 21.0/255.0},
        'Olive': {'R': 95.0/255.0, 'G': 153.0/255.0, 'B': 32.0/255.0},
        'Green': {'R': 64.0/255.0, 'G': 143.0/255.0, 'B': 101.0/255.0},
        'Teal': {'R': 0.0/255.0, 'G': 152.0/255.0, 'B': 153.0/255.0},
        'Navy': {'R': 21.0/255.0, 'G': 98.0/255.0, 'B': 132.0/255.0},
        'Blue': {'R': 121.0/255.0, 'G': 168.0/255.0, 'B': 208.0/255.0},
        'Purple': {'R': 153.0/255.0, 'G': 115.0/255.0, 'B': 160.0/255.0},
        'Violet': {'R': 149.0/255.0, 'G': 75.0/255.0, 'B': 205.0/255.0},
        'Pink': {'R': 233.0/255.0, 'G': 140.0/255.0, 'B': 181.0/255.0},
        'Tan': {'R': 185.0/255.0, 'G': 176.0/255.0, 'B': 151.0/255.0},
        'Beige': {'R': 198.0/255.0, 'G': 160.0/255.0, 'B': 119.0/255.0},
        'Brown': {'R': 153.0/255.0, 'G': 102.0/255.0, 'B': 0.0/255.0},
        'Chocolate': {'R': 140.0/255.0, 'G': 90.0/255.0, 'B': 63.0/255.0}
    }
    tools = comp.GetToolList(True) # Get selected nodes
    #print colors[color]
    for t in tools: # For each selected node
        if color == 'Clear':
            tools[t].TileColor = None
        else:
            tools[t].TileColor = colors[color]
    pass
#----------------------------------------------------------------------------------------------------------------
# Creating user interface
#----------------------------------------------------------------------------------------------------------------
ui = fu.UIManager
disp = bmd.UIDispatcher(ui)
dlg = disp.AddWindow({ "WindowTitle": "Colorise nodes", "ID": "MyWin", "Geometry": [ 100, 100, 200, 500 ], },
    [
        # {'R' : 235/255, 'G' : 110/255, 'B' : 0/255}
        ui.VGroup({ "Spacing": 5, },
        [
            ui.Button({ "Text": "Clear", "ID": "Clear" }),
            ui.Button({ "Text": "Orange", "ID": "Orange" }),
            ui.Button({ "Text": "Apricot", "ID": "Apricot" }),
            ui.Button({ "Text": "Yellow", "ID": "Yellow" }),
            ui.Button({ "Text": "Lime", "ID": "Lime" }),
            ui.Button({ "Text": "Olive", "ID": "Olive" }),
            ui.Button({ "Text": "Green", "ID": "Green" }),
            ui.Button({ "Text": "Teal", "ID": "Teal" }),
            ui.Button({ "Text": "Navy", "ID": "Navy" }),
            ui.Button({ "Text": "Blue", "ID": "Blue" }),
            ui.Button({ "Text": "Purple", "ID": "Purple" }),
            ui.Button({ "Text": "Violet", "ID": "Violet" }),
            ui.Button({ "Text": "Pink", "ID": "Pink" }),
            ui.Button({ "Text": "Tan", "ID": "Tan" }),
            ui.Button({ "Text": "Beige", "ID": "Beige" }),
            ui.Button({ "Text": "Brown", "ID": "Brown" }),
            ui.Button({ "Text": "Chocolate", "ID": "Chocolate" })
        ]),
    ])
itm = dlg.GetItems() # Collect ui items

# The window was closed
def _func(ev):
    disp.ExitLoop()
dlg.On.MyWin.Close = _func

# GUI element based event functions
def _func(ev):
    comp.StartUndo("Colorise Nodes")
    ChangeColor(ev['who'])
    comp.EndUndo(True)
dlg.On.Clear.Clicked = _func
dlg.On.Orange.Clicked = _func
dlg.On.Apricot.Clicked = _func
dlg.On.Yellow.Clicked = _func
dlg.On.Lime.Clicked = _func
dlg.On.Olive.Clicked = _func
dlg.On.Green.Clicked = _func
dlg.On.Teal.Clicked = _func
dlg.On.Navy.Clicked = _func
dlg.On.Blue.Clicked = _func
dlg.On.Purple.Clicked = _func
dlg.On.Violet.Clicked = _func
dlg.On.Pink.Clicked = _func
dlg.On.Tan.Clicked = _func
dlg.On.Beige.Clicked = _func
dlg.On.Brown.Clicked = _func
dlg.On.Chocolate.Clicked = _func

# Dialog things
dlg.Show()
disp.RunLoop()
dlg.Hide()