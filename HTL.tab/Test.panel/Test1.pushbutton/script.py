# -*- coding: utf-8 -*-

import clr
clr.AddReference('RevitAPI')
import Autodesk

import rpw
from rpw import doc, uidoc
from System.Collections.Generic import List


class RebarFilter(Autodesk.Revit.UI.Selection.ISelectionFilter):
    def AllowElement(self, element):
        if element.Category.Name == 'Structural Rebar':
            return True
        else:
            return False

def select_rebar():
    selection = uidoc.Selection.PickObject(Autodesk.Revit.UI.Selection.ObjectType.Element,
                                           RebarFilter(), 'Pick Rebar')
    rebar = rpw.db.Element.from_id(selection.ElementId).unwrap()
    rebar_id = rebar.Id.IntegerValue
    curves = rebar.GetCenterlineCurves(False, False, False,
                                    rpw.DB.Structure.MultiplanarOption.IncludeOnlyPlanarCurves, 0)
    curve_array = rpw.DB.CurveArray()

    for curve in curves:
        curve_array.Append(curve)

    with rpw.db.Transaction('Create detail curve array'):
        dca = doc.Create.NewDetailCurveArray(doc.ActiveView, curve_array)

    ids = List[rpw.DB.ElementId]()
    for dc in dca:
        ids.Add(dc.Id)

    with rpw.db.Transaction('Create group'):
        group = doc.Create.NewGroup(ids)

    # Pick Point
    sp = rpw.db.Collector(of_class='SketchPlane', where=lambda x: x.OwnerViewId==doc.ActiveView.Id)[0]
    plane = sp.GetPlane()
    with rpw.db.Transaction('Set Work plane'):
        new_sp = rpw.DB.SketchPlane.Create(doc, plane)
        uidoc.ActiveView.SketchPlane = new_sp
    point = uidoc.Selection.PickPoint('Pick point to place rebar detail')

    ids.Add(group.Id)
    old_loc = group.Location.Point
    move_sector = point.Subtract(old_loc)
    with rpw.db.Transaction('Move group'):
        rpw.DB.ElementTransformUtils.MoveElements(doc, ids, move_sector)


    # spacing = int(round(rebar.MaxSpacing * 304.8))
    # rebar_type = rpw.db.Element.from_id(rebar.GetTypeId())
    # diameter = int(round(rebar_type.BarDiameter * 304.8, 0))
    # spacing_text = '{}a{}'.format(diameter, spacing)
    # schedule_mark = rebar.ScheduleMark
    # return rebar_id, schedule_mark, spacing_text

select_rebar()
