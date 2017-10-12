# -*- coding: utf-8 -*-
# __title__ = 'Assign\nRebar Partition'
__author__ = 'htl'
import sys
import clr
clr.AddReference('RevitAPI')
import Autodesk
import Autodesk.Revit.DB as DB

import rpw
from rpw import doc, uidoc
from rpw.ui.forms import Label, ComboBox, Button, FlexForm
from Autodesk.Revit.DB import (BoundingBoxIntersectsFilter, Outline, ElementId,
                               Options, Solid, UV, FaceIntersectionFaceResult,
                               GeometryInstance, SetComparisonResult, XYZ, GeometryObject, GeometryElement)

from System.Collections.Generic import List

# class CategoriesFilter(Autodesk.Revit.UI.Selection.ISelectionFilter):
#     def __init__(self, names):
#         self.names = names
#     def AllowElement(self, element):
#         return element.Category.Name in self.names


# def select_by_category(*names):
#     selection = uidoc.Selection.PickObject(Autodesk.Revit.UI.Selection.ObjectType.Element,
#                                            CategoriesFilter(names), 'Pick Beam')
#     return rpw.db.Element.from_id(selection.ElementId)

# try:
#     element = select_by_category('Structural Rebar')
# except:
#     sys.exit()

# print(sys.path)
# components = [Label('Parameter to assign partition:'),
#             ComboBox('parameter', {p.name: p.name for p in element.parameters.all}),
#             Button('Assign Partition')]
# ff = FlexForm('Assign Partition based on Host parameter', components)
# ff.show()
# if ff.values:
#     p_name = ff.values['parameter']
# else:
#     sys.exit()

# rebars = rpw.db.Collector(of_category='Rebar', view=doc.ActiveView,
#                           where=lambda x: rpw.db.Element.from_id(x.GetHostId()).Category.Name==element.Category.Name)
# rids = List[rpw.DB.ElementId]()

# with rpw.db.Transaction('Set Partition By Host'):
#     for bar in rebars:
#         if rpw.db.Element.from_id(bar.GetHostId()).parameters[p_name].value == element.parameters[p_name].value:
#             rids.Add(bar.Id)
#             rpw.db.Element(bar).parameters['Partition'].value = element.parameters[p_name].value

# uidoc.Selection.SetElementIds(rids)





def get_faces(element):
    op = Options()
    geo_element = element.Geometry[op]
    for geo_object in geo_element:
        if type(geo_object) == Solid and geo_object.Faces.Size > 0:
            return geo_object.Faces
        elif type(geo_object) == GeometryInstance:
            for go in geo_object.GetInstanceGeometry():
                if type(go) == Solid and go.Faces.Size > 0:
                    return go.Faces

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

import sys
sys.path.append(r'C:\Program Files\Dynamo\Dynamo Core\1.3')
sys.path.append(r'C:\Program Files\Dynamo\Dynamo Core\1.3\libg_221')


clr.AddReference('RevitNodes')
import Revit
clr.ImportExtensions(Revit.GeometryConversion)

clr.AddReference('ProtoGeometry')
clr.AddReference('LibG.ProtoInterface')

from Autodesk.DesignScript.Geometry import Surface



def calculate_cross_area(host_element, cross_element):
    host_faces = get_faces(host_element)
    cross_element_faces = get_faces(cross_element)
    cross_faces_area = []
    for host_face in host_faces:
        # curve = ''
        # print([(curve, host_face.Intersect(cross_face, curve)) for cross_face in cross_element_faces])
        host_face = host_face.Convert()[0]
        for cross_face in cross_element_faces:
            cross_face = cross_face.Convert()[0]
            if host_face.DoesIntersect(cross_face):
                intersection = list(host_face.Intersect(cross_face))[0]
                if type(intersection) == Surface:
                    cross_faces_area.append(intersection.Area)
    return sum(cross_faces_area)

class CategoriesFilter(Autodesk.Revit.UI.Selection.ISelectionFilter):
    def __init__(self, names):
        self.names = names
    def AllowElement(self, element):
        return element.Category.Name in self.names


def select_by_category(*names):
    prompt = 'Pick {}'.format(', '.join(names))
    references = uidoc.Selection.PickObjects(Autodesk.Revit.UI.Selection.ObjectType.Element,
                                           CategoriesFilter(names), prompt)
    return [rpw.db.Element.from_id(reference.ElementId) for reference in references]


def get_crossing_elements(host_element):
    bb = host_element.BoundingBox[doc.ActiveView]
    outline = Outline(bb.Min + XYZ(-100, -100, -100), bb.Max + XYZ(100, 100, 100))
    # outline = Outline(bb.Min, bb.Max)
    crossing_elements = []
    bbfilter = BoundingBoxIntersectsFilter(outline)

    crossing_floors = rpw.db.Collector(of_category='Floors', is_type=False)
    x_ids = List[ElementId]()
    x_ids.Add(host_element.Id)
    crossing_floors.Excluding(x_ids)
    crossing_floors.WherePasses(bbfilter)
    crossing_elements.extend(crossing_floors)

    crossing_walls = rpw.db.Collector(of_category='Walls', is_type=False,
                                      where=lambda x: x.LookupParameter('Structural').AsValueString() == 'Yes')
    x_ids = List[ElementId]()
    x_ids.Add(host_element.Id)
    crossing_walls.Excluding(x_ids)
    crossing_walls.WherePasses(bbfilter)
    crossing_elements.extend(crossing_walls)

    crossing_columns = rpw.db.Collector(of_category='Structural Columns')
    x_ids = List[ElementId]()
    x_ids.Add(host_element.Id)
    crossing_columns.Excluding(x_ids)
    crossing_columns.WherePasses(bbfilter)
    crossing_elements.extend(crossing_columns)

    crossing_beams = rpw.db.Collector(of_category='Structural Framing')
    x_ids = List[ElementId]()
    x_ids.Add(host_element.Id)
    crossing_beams.Excluding(x_ids)
    crossing_beams.WherePasses(bbfilter)
    crossing_elements.extend(crossing_beams)

    return crossing_elements

# try:
#     selected_elements = select_by_category('Structural Framing')
# except Autodesk.Revit.Exceptions.OperationCanceledException:
#     sys.exit()

# for host_element in selected_elements:
#     host_faces = get_faces(host_element)
#     cross_elements = get_crossing_elements(host_element)
#     total_formwork_subtract_area = 0
#     for cross_element in cross_elements:
#         print('Host: {}, cross: {}'.format(host_element.Id, cross_element.Id))
#         print(calculate_cross_area(host_element, cross_element))
#         print('-'*20)
#         total_formwork_subtract_area += calculate_cross_area(host_element, cross_element)
#     print(total_formwork_subtract_area)
#     print('-'*40)


# import math
# angle in radians
# angle = XYZ(0,0,1).AngleTo(XYZ(1,1,1))
# radian to degree
# print(angle, angle * 180 / math.pi)

e1_id = 396584
e2_id = 399115
# e2_id = 396782

e1 = rpw.db.Element.from_int(e1_id)
e2 = rpw.db.Element.from_int(e2_id)

faces1 = get_faces(e1)
faces2 = get_faces(e2)


# cfaces1 = [face for face in faces1 if type(face)==DB.CylindricalFace]
# cfaces2 = [face for face in faces2]

print(sys.path)
print(Revit.GeometryConversion.RevitToProtoFace.ToProtoType(list(faces1)[0], False))
# cfaces1 = [face for face in faces1 if type(face)==DB.CylindricalFace]
# cfaces2 = [face for face in faces2 if type(face)==DB.CylindricalFace]

# for face1 in cfaces1:
#     for face2 in cfaces2:
#         f= face1.Intersect(face2,)
#         print(f)

