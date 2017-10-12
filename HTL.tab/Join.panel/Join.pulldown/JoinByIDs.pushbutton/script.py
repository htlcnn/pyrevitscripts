# -*- coding: utf-8 -*-
__title__ = 'Join by IDs'
__author__ = 'htl'
import clr
import rpw
from rpw import doc
from rpw.ui.forms import Label, Button, TextBox, FlexForm

clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import (Outline, BoundingBoxIntersectsFilter, JoinGeometryUtils,
                               FilteredElementCollector, ElementId)

selected = rpw.ui.Selection()

def multijoin(fam1, fam2, selected=False):
    fam1 = fam1.lower()
    fam2 = fam2.lower()
    with rpw.db.Transaction("join {} and {}".format(fam1, fam2).upper()):
        elements1 = get_elements(fam1, selected)
        for e1 in elements1.elements:
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


components = [Label('Host Element ID:'),
            TextBox('host_id'),
            Label('Element IDs to be joined (comma separated):'),
            TextBox('joined_ids'),
            Button('Join')]

ff = FlexForm("Join by IDs", components)
ff.show()

if ff.values and ff.values['host_id']:
    host_id = ff.values['host_id']
    host_element = rpw.db.Element.from_int(int(host_id)).unwrap()
    with rpw.db.Transaction('Join IDs {} with {}'.format(ff.values['joined_ids'], host_id)):
        for eid in ff.values['joined_ids'].split(','):
            joined_element = rpw.db.Element.from_int(int(eid)).unwrap()
            JoinGeometryUtils.JoinGeometry(doc, host_element, joined_element)
