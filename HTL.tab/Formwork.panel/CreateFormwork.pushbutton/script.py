# -*- coding: utf-8 -*-
__title__ = 'Create Formwork'
__author__ = 'htl'
from itertools import chain
import sys
import clr
clr.AddReference('RevitAPI')
import Autodesk

import rpw
from rpw import doc, uidoc
from rpw.ui.forms import Label, TextBox, Button, FlexForm
from Autodesk.Revit.DB import *

from System.Collections.Generic import List

from htl import selection


def get_faces(element):
    faces = []
    solids = get_solids(element)
    for solid in solids:
        faces.extend(list(solid.Faces))
    return faces


def get_solids(element):
    op = Options()
    geo_element = element.Geometry[op]
    ret = []
    for geo_object in geo_element:
        if type(geo_object) == Solid and geo_object.Faces.Size > 0:
            ret.append(geo_object)
        elif type(geo_object) == GeometryInstance:
            for go in geo_object.GetInstanceGeometry():
                if type(go) == Solid and go.Faces.Size > 0:
                    ret.append(go)
    return ret


def get_crossing_element(host_element, cross_category, offset):
    bb = host_element.BoundingBox[doc.ActiveView]
    min_offset = XYZ(1, 1, 1).Multiply(-offset)
    max_offset = XYZ(1, 1, 1).Multiply(offset)
    outline = Outline(bb.Min + min_offset, bb.Max + max_offset)
    bbfilter = BoundingBoxIntersectsFilter(outline)
    crossing_elements = rpw.db.Collector(of_category=cross_category, is_type=False)
    x_ids = List[ElementId]()
    x_ids.Add(host_element.Id)
    crossing_elements.Excluding(x_ids)
    crossing_elements.WherePasses(bbfilter)
    return crossing_elements


def get_crossing_elements(host_element, offset):
    floors = get_crossing_element(host_element, 'Floors', offset)
    walls = get_crossing_element(host_element, 'Walls', offset)
    columns = get_crossing_element(host_element, 'Structural Columns', offset)
    beams = get_crossing_element(host_element, 'Structural Framing', offset)

    # filter generic models, exclude Formwork
    generic_models = get_crossing_element(host_element, 'Generic Model', offset)
    generic_models = generic_models.ToElements()
    gm = []
    for e in generic_models:
        name = e.LookupParameter('UDIC_Name').AsString()
        if name and 'Formwork' in name:
                continue
        gm.append(e)
    return chain(floors, walls, columns, beams, gm)


def create_formwork(face, thickness, cross_solids):
    normal = face.ComputeNormal(UV())
    angle_radian = normal.AngleTo(XYZ().BasisZ)
    angle = round(angle_radian * 180 / 3.14)
    if angle < 90:
        return
    elif angle == 180:
        angle_text = "Bottom"
    else:
        angle_text = "Side"

    formwork = GeometryCreationUtilities.CreateExtrusionGeometry(face.GetEdgesAsCurveLoops(),
                                                                normal, thickness/304.8)
    for solid in cross_solids:
        BooleanOperationsUtils.ExecuteBooleanOperationModifyingOriginalSolid(formwork, solid, BooleanOperationsType.Difference)
    return formwork, angle_text


def main():
    components = [Label('Thickness (mm)'),
                  TextBox('thickness'),
                  Button('Create Formwork')
                  ]
    ff = FlexForm('Create Formwork', components)
    ff.show()

    try:
        thickness = int(ff.values['thickness'])
        if not thickness:
            return
    except:
        return

    try:
        elements = selection.select_objects_by_category('Structural Framing', 'Structural Columns',
                                                        'Floors', 'Generic Models', 'Walls')
    except:
        return

    for element in elements:
        host_faces = get_faces(element)
        host_solids = get_solids(element)

        cross_elements = get_crossing_elements(element, thickness/304.8)
        cross_solids = []
        for cross_element in cross_elements:
            cross_solids.extend(get_solids(cross_element))
        if len(host_solids) > 1:
            cross_solids.extend(host_solids)

        host_name = element.LookupParameter('UDIC_Name').AsString()

        host_category = element.Category.Name
        if host_category == 'Structural Columns':
            param = 'Base Level'
        elif host_category == 'Structural Framing':
            param = 'Reference Level'
        elif host_category == 'Floors':
            param = 'Level'
        elif host_category == 'Walls':
            param = 'Base Constraint'
        elif host_category == 'Generic Models':
            param = 'Level'
        formwork_level = element.LookupParameter(param).AsValueString()

        with rpw.db.Transaction('Create formwork for {}'.format(element.Id)):
            for face in host_faces:
                try:
                    formwork, angle_text = create_formwork(face, thickness, cross_solids)
                except Exception as e:
                    continue

                area = formwork.Volume/(thickness/304.8)
                if area == 0:
                    continue
                ds = DirectShape.CreateElement(doc, ElementId(BuiltInCategory.OST_GenericModel))
                ds.SetShape([formwork])
                ds.LookupParameter('UDIC_Name').Set('Formwork {}'.format(element.Id))
                ds.LookupParameter('UDIC_Formwork_Type').Set(angle_text)
                if host_name:
                    ds.LookupParameter('UDIC_Formwork_Hostname').Set(host_name)
                ds.LookupParameter('UDIC_Formwork_Hostcategory').Set(host_category)
                ds.LookupParameter('UDIC_Formwork_Level').Set(formwork_level)
                ds.LookupParameter('UDIC_Formwork_Area').Set(area)


if __name__ == '__main__':
    main()
