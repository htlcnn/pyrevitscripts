# -*- coding: utf-8 -*-
__title__ = 'Rebar Filter'
__author__ = 'htl'

import clr
clr.AddReference('RevitAPI')
from System.Collections.Generic import List
import rpw
from rpw import doc, uidoc
from rpw.ui.forms import Label, ComboBox, Button, FlexForm

all_rebars = rpw.db.Collector(of_category='OST_Rebar', view=doc.ActiveView).elements
rebar_dict = {}
for rebar in all_rebars:
    host = rpw.db.Element.from_id(rebar.GetHostId())
    rebar_dict[host.Category.Name] = host.Category.Name

components = [Label('Filter by Host Category:'),
              ComboBox('host_category', rebar_dict),
              Button('Select Rebar')]

ff = FlexForm("Select Rebar", components)
ff.show()

if ff.values:
    category = ff.values['host_category']
    rebars = rpw.db.Collector(of_category='OST_Rebar',
                          where=lambda x: rpw.db.Element.from_id(x.GetHostId()).Category.Name==category,
                          view=doc.ActiveView)
    rebar_ids = List[rpw.DB.ElementId]()
    for rebar in rebars:
        rebar_ids.Add(rebar.Id)
    uidoc.Selection.SetElementIds(rebar_ids)
