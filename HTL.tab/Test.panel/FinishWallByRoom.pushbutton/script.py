# -*- coding: utf-8 -*-
__title__ = 'Create Finish Walls\nBy Room'
__author__ = 'htl'
import sys
import clr
clr.AddReference('RevitAPI')

import rpw
from rpw import doc, uidoc
from rpw.ui.forms import ComboBox, Button, Label, FlexForm, TextBox
import Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import Selection
from itertools import izip


class CategoriesFilter(Selection.ISelectionFilter):
    def __init__(self, names):
        self.names = names
    def AllowElement(self, element):
        return element.Category.Name in self.names


def select_objects_by_category(*names):
    prompt = 'Pick {}'.format(', '.join(names))
    references = uidoc.Selection.PickObjects(Selection.ObjectType.Element,
                                           CategoriesFilter(names), prompt)
    return [rpw.db.Element.from_id(reference.ElementId) for reference in references]


def select_object_by_category(name):
    prompt = 'Pick {}'.format(name)
    reference = uidoc.Selection.PickObject(Selection.ObjectType.Element,
                                           CategoriesFilter(name), prompt)
    return rpw.db.Element.from_id(reference.ElementId)


def get_boundaries(room):
    ret = []
    for segments in room.GetBoundarySegments(SpatialElementBoundaryOptions()):
        for segment in segments:
            wall = doc.GetElement(segment.ElementId)
            curve = segment.GetCurve()
            ret.append((wall, curve))
    return ret


def form():
    wall_types = rpw.db.Collector(of_category='Walls', is_type=True,
                                  where=lambda x: x.GetParameters('Width')).wrapped_elements
    components = [Label('Finish wall type:'),
                  ComboBox('wall_type_id',
                           {wt.parameters['Type Name'].AsString(): wt.Id for wt in wall_types}),
                  Label('Finish wall height (mm):'),
                  TextBox('wall_height'),
                  Button('Create Finish Walls')]

    ff = FlexForm('Create Finish Walls', components)
    ff.show()
    if ff.values['wall_type_id'] and ff.values['wall_height']:
        try:
            wall_type = rpw.db.Element.from_id(ff.values['wall_type_id'])
            wall_height = float(ff.values['wall_height'])
            return wall_type, wall_height
        except:
            return


def create_finish_wall(wall_type, wall_height):
    room = select_object_by_category('Rooms')
    offset_distance = wall_type.parameters['Width'].AsDouble() * 0.5
    new_walls = []
    boundaries = get_boundaries(room)
    with rpw.db.Transaction('Create Finish Wall'):
        for wall, curve in boundaries:
            new_curve = curve.CreateOffset(-offset_distance, XYZ().BasisZ)
            new_wall = Wall.Create(doc, new_curve, wall_type.Id, room.LevelId,
                                   wall_height/304.8, 0, 0, 0)
            new_walls.append(new_wall)
    with rpw.db.Transaction('Join old-new walls'):
        for idx, new_wall in enumerate(new_walls):
            old_wall = boundaries[idx][0]
            try:
                JoinGeometryUtils.JoinGeometry(doc, old_wall, new_wall)
            except Exception as e:
                print(e)


def main():
    try:
        wall_type, wall_height = form()
    except Exception as e:
        return

    while True:
        try:
            create_finish_wall(wall_type, wall_height)
        except Exception as e:
            break


if __name__ == '__main__':
    main()
