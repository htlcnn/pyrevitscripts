# -*- coding: utf-8 -*-
__title__ = 'Create Lintel'
__author__ = 'htl'
import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

import rpw
from rpw.ui.forms import Label, TextBox, Button, ComboBox, FlexForm
from htl import selection

uiapp = __revit__
uidoc = uiapp.ActiveUIDocument
app = uiapp.Application
doc = uidoc.Document

def create_lintel(host, l1, l2, beam_type):
    host_height = doc.GetElement(host.GetTypeId()).LookupParameter('Height').AsDouble()
    host_width = doc.GetElement(host.GetTypeId()).LookupParameter('Width').AsDouble()
    level = doc.GetElement(host.Host.LevelId)
    beam_height = beam_type.LookupParameter('h').AsDouble()
    lintel_location_point = host.Location.Point + XYZ(0, 0, host_height + beam_height)
    host_location_curve = host.Host.Location.Curve
    l1 = l1/304.8
    l2 = l2/304.8
    if isinstance(host_location_curve, Line):
        wall_direction = host.Host.Location.Curve.Direction
        start = lintel_location_point - (l1 + host_width/2) * wall_direction
        end = lintel_location_point + (l2 + host_width/2) * wall_direction
        beam_location = Line.CreateBound(start, end)
        curve = clr.Reference[Curve](beam_location)
        overloads = (Curve, FamilySymbol, Level, Structure.StructuralType)
        with rpw.db.Transaction('create lintel'):
            beam = doc.Create.NewFamilyInstance.Overloads[overloads](beam_location, beam_type, level, Structure.StructuralType.Beam)

def main():

    try:
        elements = selection.select_objects_by_category('Windows', 'Doors')
    except:
        return
    all_beam_types = rpw.db.Collector(of_category='Structural Framing', is_type=True).get_elements(wrapped=False)
    components = [
                  Label('Lintel (Beam) Type:'),
                  ComboBox('beam_type', {b.LookupParameter('Type Name').AsString(): b for b in all_beam_types}),
                  Label('L1:'),
                  TextBox('l1'),
                  Label('L2:'),
                  TextBox('l2'),
                  Button('Create Lintels')
                 ]

    ff = FlexForm('Create Lintels', components)
    ff.show()

    if ff.values:
        beam_type = ff.values['beam_type']
        try:
            l1 = float(ff.values['l1'])
            l2 = float(ff.values['l2'])
        except:
            return
        if not beam_type.IsActive:
            with rpw.db.Transaction('Activate Beam Type'):
                beam_type.Activate()
        for e in elements:
            create_lintel(e, l1, l2, beam_type)

if __name__ == '__main__':
    main()
