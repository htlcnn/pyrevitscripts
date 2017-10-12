# -*- coding: utf-8 -*-
__title__ = 'Select Same\nSchedule Mark Rebar'
__author__ = 'htl'
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
selection = uidoc.Selection.PickObject(Autodesk.Revit.UI.Selection.ObjectType.Element,
                                           RebarFilter(), 'Pick Rebar')
rebar = rpw.db.Element.from_id(selection.ElementId).unwrap()
same_schedule_mark = rpw.db.Collector(of_category='Rebar',
                                      view=doc.ActiveView,
                                      where=lambda x: x.ScheduleMark==rebar.ScheduleMark)
rids = List[rpw.DB.ElementId](same_schedule_mark.element_ids)
uidoc.Selection.SetElementIds(rids)
