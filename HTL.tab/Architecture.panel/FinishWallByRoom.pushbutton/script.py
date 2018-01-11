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
import System


class CategoriesFilter(Selection.ISelectionFilter):
    def __init__(self, names):
        self.names = names
    def AllowElement(self, element):
        return element.Category.Name in self.names


def select_objects_by_category(*names):
    prompt = 'Pick {}'.format(', '.join(names))
    references = uidoc.Selection.PickObjects(Selection.ObjectType.Element,
                                           CategoriesFilter(names), prompt)
    return (rpw.db.Element.from_id(reference.ElementId) for reference in references)


def select_object_by_category(name):
    prompt = 'Pick {}'.format(name)
    reference = uidoc.Selection.PickObject(Selection.ObjectType.Element,
                                           CategoriesFilter(name), prompt)
    return rpw.db.Element.from_id(reference.ElementId)


def get_boundaries(room):
    opt = SpatialElementBoundaryOptions()
    opt.SpatialElementBoundaryLocation = SpatialElementBoundaryLocation.Finish
    opt.StoreFreeBoundaryFaces = False
    return room.GetBoundarySegments(opt)


def curveloop_from_boundary(boundary):
    curveloop = CurveLoop()
    for segment in boundary:
        curveloop.Append(segment.GetCurve())
    return curveloop


def form():
    wall_types = rpw.db.Collector(of_category='Walls', is_type=True,
                                  where=lambda x: x.GetParameters('Width')).get_elements()
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

def is_inside_room(curveloop, room):
    for curve in curveloop:
        end0 = curve.GetEndPoint(0)
        end1 = curve.GetEndPoint(1)
        if room.IsPointInRoom(end0) and room.IsPointInRoom(end1):
            continue
        else:
            return False
    return True


def create_finish_wall(room, wall_type, wall_height):
    offset_distance = wall_type.parameters['Width'].AsDouble() * 0.5
    boundary_loops = get_boundaries(room)
    # print(boundary_loops)
    for boundary in boundary_loops:
        curveloop = curveloop_from_boundary(boundary)

        offset_curveloop = CurveLoop.CreateViaOffset(curveloop, offset_distance,
                                                     curveloop.GetPlane().Normal)
        if not is_inside_room(offset_curveloop, room):
            offset_curveloop = CurveLoop.CreateViaOffset(curveloop, -offset_distance,
                                                         curveloop.GetPlane().Normal)
        new_walls = []
        with rpw.db.Transaction('Create Finish Wall'):
            for curve in offset_curveloop:
                new_wall = Wall.Create(doc, curve, wall_type.Id, room.LevelId,
                                       wall_height/304.8, 0, False, False)
                new_walls.append(new_wall)
        with rpw.db.Transaction('Join old-new walls'):
            for idx, new_wall in enumerate(new_walls):
                old_wall = doc.GetElement(boundary[idx].ElementId)
                if old_wall:
                    try:
                        JoinGeometryUtils.JoinGeometry(doc, old_wall, new_wall)
                    except Exception as e:
                        print(e)
        with rpw.db.Transaction('Delete short walls'):
            for new_wall in new_walls:
                length = new_wall.LookupParameter('Length').AsDouble() * 304.8
                if length < 50:
                    doc.Delete(new_wall.Id)


def main():
    try:
        wall_type, wall_height = form()
        rooms = select_objects_by_category('Rooms')
        for room in rooms:
            create_finish_wall(room, wall_type, wall_height)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
