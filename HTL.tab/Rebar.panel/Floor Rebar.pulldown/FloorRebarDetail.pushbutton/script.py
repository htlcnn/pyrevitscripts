# -*- coding: utf-8 -*-
__title__='Floor Rebar\nDetail'
__author__='htl'
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
    rebar_type = rpw.db.Element.from_id(rebar.GetTypeId())
    diameter = int(round(rebar_type.BarDiameter * 304.8, 0))
    spacing_text = '{}a{}'.format(diameter, spacing)
    schedule_mark = rebar.ScheduleMark
    return rebar_id, schedule_mark, spacing_text


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
    rebar_id, schedule_mark, spacing_text = select_rebar()
    point = uidoc.Selection.PickPoint('Pick point to place rebar detail')
    with rpw.db.Transaction():
        if not symbol.IsActive:
            symbol.Activate()
        detail = doc.Create.NewFamilyInstance(point, symbol, doc.ActiveView)
        if detail:
            edit_detail_parameter(detail, rebar_id, schedule_mark, spacing_text)


def edit_detail_parameter(detail, rebar_id, schedule_mark, spacing_text):
    e = rpw.db.Element(detail)
    e.parameters['Rebar ID'] = rebar_id
    e.parameters['Rebar Schedule Mark'] = schedule_mark
    e.parameters['Rebar Spacing'] = spacing_text

while True:
    try:
        place_detail()
    except Autodesk.Revit.Exceptions.OperationCanceledException:
        break
