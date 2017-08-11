# -*- coding: utf-8 -*-
# from pprint import pprint
# from scriptutils import this_script

# import os
# import clr
# clr.AddReference('IronPython.Wpf')
# clr.AddReference("PresentationFramework")
# clr.AddReference('PresentationCore')

# from IronPython.Modules import Wpf as wpf

# from System import Uri
# from System.Windows import Window
# from System.Windows.Media.Imaging import BitmapImage
# from System.IO import StringReader

# script_path = '\\'.join(this_script.info.script_file.split('\\')[:-1])
# xaml_path = os.path.join(script_path, 'xaml.xaml')
# with open(xaml_path) as f:
#     xaml = f.read()

# class MyWindow(Window):
#     def __init__(self):
#         wpf.LoadComponent(self, StringReader(xaml))

#     def OnLoad(self, sender, e):
#         # self.image1.Source = os.path.join(script_path, 'icon.png')
#         pass

#     def ApplyButton_Click(self, sender, e):
#         pass

#     def ComboBox_SelectionChanged(self, sender, e):
#         pass


# w = MyWindow()
# w.Title = "Auto Foundation"
# w.Width = 300
# img_path = BitmapImage(Uri(os.path.join(script_path, 'icon.png')))
# w.image1.Source = img_path
# w.image1.Width = 32
# w.Show()


import clr
clr.AddReference('RevitAPI')
import Autodesk

import rpw
from rpw import doc, uidoc


class RebarFilter(Autodesk.Revit.UI.Selection.ISelectionFilter):
    def AllowElement(self, element):
        if element.Category.Name == 'Structural Rebar':
            return True
        else:
            return False


def on_document_change(sender, e):
    global added_element_ids
    added_element_ids.extend(e.GetAddedElementIds())
    Press.PostMessage(_revit_window.Handle, Press.KEYBOARD_MSG['WM_KEYDOWN'], Keys.Escape, 0);
    Press.PostMessage( _revit_window.Handle, Press.KEYBOARD_MSG['WM_KEYDOWN'], Keys.Escape, 0 );


def select_rebar():
    selection = uidoc.Selection.PickObject(Autodesk.Revit.UI.Selection.ObjectType.Element,
                                           RebarFilter(), 'Pick Rebar')
    rebar = rpw.db.Element.from_id(selection.ElementId).unwrap()
    rebar_id = rebar.Id.IntegerValue
    spacing = int(round(rebar.MaxSpacing * 304.8))
    diameter = rebar.Name.split(' : ')[0]
    spacing_text = '{}a{}'.format(diameter, spacing)
    number = rebar.ScheduleMark
    return rebar_id, number, spacing_text


def place_detail():
    doc.Application.DocumentChanged += on_document_change
    added_element_ids = []
    symbol = rpw.db.Collector(of_class='FamilySymbol',
                              where=lambda x: x.FamilyName=='UDIC - Floor Rebar Symbol')[0]

    # Pick Point
    sp = rpw.db.Collector(of_class='SketchPlane', where=lambda x: x.OwnerViewId==doc.ActiveView.Id)[0]
    plane = sp.GetPlane()
    with rpw.db.Transaction('Set Work plane'):
        new_sp = rpw.DB.SketchPlane.Create(doc, plane)
        uidoc.ActiveView.SketchPlane = new_sp

    rebar_id, number, spacing_text = select_rebar()

    point = uidoc.Selection.PickPoint('Pick point to place rebar detail')

    with rpw.db.Transaction():
        detail = doc.Create.NewFamilyInstance(point, symbol, doc.ActiveView)
        if detail:
            edit_detail_parameter(detail, rebar_id, number, spacing_text)


def edit_detail_parameter(detail, rebar_id, number, spacing_text):
    e = rpw.db.Element(detail)
    e.parameters['Rebar ID'] = rebar_id
    e.parameters['Rebar Number'] = number
    e.parameters['Rebar Spacing'] = spacing_text

while True:
    try:
        place_detail()
    except Autodesk.Revit.Exceptions.OperationCanceledException:
        break



# rebar = rpw.db.Element.from_id(selection.ElementId).unwrap()

# rb_curves = rebar.GetCenterlineCurves(False, False, False,
#                             Autodesk.Revit.DB.Structure.MultiplanarOption.IncludeOnlyPlanarCurves,
#                             0)

# ca = rpw.DB.CurveArray()

# for curve in rb_curves:
#     ca.Append(curve)

# with rpw.db.Transaction('Create Detail Line'):
#     new_ca = doc.Create.NewDetailCurveArray(doc.ActiveView, ca)





# print(f.FamilyCategory.Name)
# pprint(dir(f))

