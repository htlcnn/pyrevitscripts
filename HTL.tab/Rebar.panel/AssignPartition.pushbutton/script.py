# -*- coding: utf-8 -*-
'''
Assign Rebar Partition by Host's parameter value: UDIC_Name
'''
__title__ = 'Assign\nRebar Partition'
__author__ = 'htl'
import sys
import clr
clr.AddReference('RevitAPI')
import Autodesk

import rpw
from rpw import doc, uidoc
from rpw.ui.forms import Label, ComboBox, Button, FlexForm

from System.Collections.Generic import List

class CategoriesFilter(Autodesk.Revit.UI.Selection.ISelectionFilter):
    def __init__(self, names):
        self.names = names
    def AllowElement(self, element):
        return element.Category.Name in self.names


def select_by_category(*names):
    selection = uidoc.Selection.PickObject(Autodesk.Revit.UI.Selection.ObjectType.Element,
                                           CategoriesFilter(names), 'Pick Objects')
    return rpw.db.Element.from_id(selection.ElementId)

workset_table = doc.GetWorksetTable()
active_ws_id = workset_table.GetActiveWorksetId()

element = select_by_category('Structural Framing', 'Structural Columns', 'Floors', 'Generic Models')

# components = [Label('Parameter to assign partition:'),
#             ComboBox('parameter', {p.name: p.name for p in element.parameters.all}),
#             Button('Assign Partition')]
# ff = FlexForm('Assign Partition based on Host parameter', components)
# ff.show()
# if ff.values:
#     p_name = ff.values['parameter']
# else:
#     sys.exit()

rebars = rpw.db.Collector(of_category='Rebar', is_type=False,
                          where=lambda x: rpw.db.Element.from_id(x.GetHostId()).Category.Name==element.Category.Name \
                          and x.WorksetId==active_ws_id)
rids = List[rpw.DB.ElementId]()

with rpw.db.Transaction('Set Partition By Host'):
    for bar in rebars:
        if rpw.db.Element.from_id(bar.GetHostId()).parameters['UDIC_Name'].value == element.parameters['UDIC_Name'].value:
            rids.Add(bar.Id)
            rpw.db.Element(bar).parameters['Partition'].value = element.parameters['UDIC_Name'].value

uidoc.Selection.SetElementIds(rids)
