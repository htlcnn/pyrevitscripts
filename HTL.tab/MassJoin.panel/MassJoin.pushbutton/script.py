# -*- coding: utf-8 -*-
import clr
import rpw
from rpw.ui.forms import Button, ComboBox, FlexForm, CheckBox, Label, TextBox, Separator
from rpw import doc

clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import Outline, BoundingBoxIntersectsFilter, JoinGeometryUtils

def get_elements(family):
    if family == "floor":
        return rpw.db.Collector(of_class="Floor")
    elif family == "wall":
        return rpw.db.Collector(of_class="Wall")
    elif family == "column":
        return rpw.db.Collector(of_category="OST_StructuralColumns", of_class="FamilyInstance")
    elif family == "beam":
        return rpw.db.Collector(of_category="OST_StructuralFraming", of_class="FamilyInstance")

def multijoin(fam1, fam2):
    fam1 = fam1.lower()
    fam2 = fam2.lower()
    with rpw.db.Transaction("join {} and {}".format(fam1, fam2)):
        elements1 = get_elements(fam1)
        for e1 in elements1:
            bb = e1.BoundingBox[doc.ActiveView]
            outline = Outline(bb.Min, bb.Max)
            bbfilter = BoundingBoxIntersectsFilter(outline)
            elements2 = get_elements(fam2)
            elements2.WherePasses(bbfilter)
            for e2 in elements2:
                try:
                    JoinGeometryUtils.JoinGeometry(doc, e1, e2)
                except Autodesk.Revit.Exceptions.ArgumentException:
                    pass


components = [Label('Cut Elements:'),
            ComboBox('cut_element', {'Tường': 'wall', 'Cột': 'column', 'Dầm': 'beam', 'Sàn': 'floor'}),
            Separator(),
            Label('Elements to join:'),
            CheckBox('join_wall', 'Tường'),
            CheckBox('join_column', 'Cột'),
            CheckBox('join_beam', 'Dầm'),
            CheckBox('join_floor', 'Sàn'),
            Button('Join')]

ff = FlexForm("Join cấu kiện trong view hiện tại", components)
ff.show()

if ff.values:
    cut_element = ff.values['cut_element']

    for k, v in ff.values.items():
        if k.startswith('join_') and v == True:
            multijoin(cut_element, k.replace('join_', ''))
