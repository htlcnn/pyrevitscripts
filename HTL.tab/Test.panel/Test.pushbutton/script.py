# -*- coding: utf-8 -*-
# __title__ = 'Assign\nRebar Partition'
__author__ = 'htl'

import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')

from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
import rpw
from rpw.ui.forms import Label, CheckBox, Button, TextBox, FlexForm

uiapp = __revit__
uidoc = uiapp.ActiveUIDocument
app = uiapp.Application
doc = uidoc.Document

def on_click(sender, e):
    checkbox = sender
    grid = checkbox.Parent
    textbox = grid.Children[2]
    if checkbox.IsChecked:
        textbox.IsEnabled = True
    else:
        textbox.IsEnabled = False

components = [
              CheckBox('create_elements', 'Create Formwork Elements', on_click=on_click),
              Label('Thickness (mm)'),
              TextBox('thickness', IsEnabled=False),
              Button('Create Formwork'),
             ]
ff = FlexForm('Create Formwork', components)

ff.show()
