# -*- coding: utf-8 -*-
__title__ = 'Select Beam\nBy Name'
__author__ = 'htl'
import clr
clr.AddReference('RevitAPI')
import Autodesk

import rpw
from rpw import doc, uidoc
from rpw.ui.forms import Label, TextBox, Button, FlexForm

from System.Collections.Generic import List

workset_table = doc.GetWorksetTable()
active_ws_id = workset_table.GetActiveWorksetId()

components = [Label('UDIC Name:'),
              TextBox('name'),
              Button('Select All')]

ff = FlexForm('Select by Name', components)
ff.show()

if ff.values:
    s = rpw.db.Collector(is_type=False, view=doc.ActiveView,
                         where=lambda x: x.WorksetId==active_ws_id \
                                         and x.LookupParameter('UDIC_Name') \
                                         and x.LookupParameter('UDIC_Name').AsString()==ff.values['name'])
    sids = List[rpw.DB.ElementId](s.element_ids)
    uidoc.Selection.SetElementIds(sids)
