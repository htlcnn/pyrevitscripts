# -*- coding: utf-8 -*-
import clr
import rpw
from rpw.ui.forms import Button, ComboBox, FlexForm, CheckBox, Label, TextBox, Separator
from rpw import doc

clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import (Outline, BoundingBoxIntersectsFilter, JoinGeometryUtils,
                               FilteredElementCollector, ElementId)

def get_elements(family, selected=False):
    if selected:
        selection = rpw.ui.Selection()
        if family == "floor":
            ret =  rpw.db.Collector(of_category='OST_Floors', is_type=False,
                                    where=lambda x: x.Id in selection.get_element_ids())
        elif family == "wall":
            ret = rpw.db.Collector(of_category='OST_Walls', is_type=False,
                                   where=lambda x: x.Id in selection.get_element_ids())
        elif family == "column":
            ret = rpw.db.Collector(of_category="OST_StructuralColumns", is_type=False,
                                   where=lambda x: x.Id in selection.get_element_ids())
        elif family == "beam":
            ret = rpw.db.Collector(of_category="OST_StructuralFraming", is_type=False,
                                   where=lambda x: x.Id in selection.get_element_ids())
        elif family == "generic_model":
            ret = rpw.db.Collector(of_category="OST_GenericModel", is_type=False,
                                   where=lambda x: x.Id in selection.get_element_ids())
        return ret
    else:
        if family == "floor":
            return rpw.db.Collector(of_category='OST_Floors', is_type=False)
        elif family == "wall":
            return rpw.db.Collector(of_category='OST_Walls', is_type=False)
        elif family == "column":
            return rpw.db.Collector(of_category="OST_StructuralColumns", is_type=False)
        elif family == "beam":
            return rpw.db.Collector(of_category="OST_StructuralFraming", is_type=False)
        elif family == "generic_model":
            return rpw.db.Collector(of_category="OST_GenericModel", is_type=False)

def multijoin(fam1, fam2, selected=False):
    fam1 = fam1.lower()
    fam2 = fam2.lower()
    with rpw.db.Transaction("join {} and {}".format(fam1, fam2).upper()):
        elements1 = get_elements(fam1, selected)
        for e1 in elements1.get_elements():
            bb = e1.BoundingBox[doc.ActiveView]
            outline = Outline(bb.Min, bb.Max)
            bbfilter = BoundingBoxIntersectsFilter(outline)
            elements2 = get_elements(fam2, selected)
            elements2.WherePasses(bbfilter)
            for e2 in elements2:
                try:
                    JoinGeometryUtils.JoinGeometry(doc, e1, e2)
                except Autodesk.Revit.Exceptions.ArgumentException:
                    pass


components = [Label('Cut Elements:'),
            ComboBox('cut_element', {'Sàn': 'floor',
                                     'Cột': 'column',
                                     'Dầm': 'beam',
                                     'Tường': 'wall',
                                     'Generic Model': 'generic_model',}),
            Separator(),
            Label('Elements to join:'),
            CheckBox('join_floor', 'Sàn'),
            CheckBox('join_column', 'Cột'),
            CheckBox('join_beam', 'Dầm'),
            CheckBox('join_wall', 'Tường'),
            CheckBox('join_generic_model', 'Generic Model'),
            Button('Join')]

if rpw.ui.Selection():
    selected = True
else:
    selected = False

ff = FlexForm("Join cấu kiện", components)
ff.show()

if ff.values:
    cut_element = ff.values['cut_element']

    for k, v in ff.values.items():
        if k.startswith('join_') and v == True:
            multijoin(cut_element, k.replace('join_', ''), selected)
