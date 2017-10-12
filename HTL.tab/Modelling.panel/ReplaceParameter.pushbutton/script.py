# -*- coding: utf-8 -*-
__title__ = 'Replace\nBeam Parameter'
__author__ = 'htl'

import sys
import rpw
from rpw import doc
from rpw.ui.forms import Label, TextBox, Button, ComboBox, FlexForm
from pprint import pprint

try:
    beams = rpw.db.Collector(of_category='OST_Structural Framing',
                            of_class='FamilyInstance',
                            view=doc.ActiveView).wrapped_elements
except:
    sys.exit()

editable = {p.name: p.name for p in beams[0].parameters.all
                 if not p.IsReadOnly and p.StorageType==rpw.DB.StorageType.String}

components = [ComboBox('parameter', editable),
              Label('Replace:'),
              TextBox('old'),
              Label('With:'),
              TextBox('new'),
              Button('Replace'),
            ]

ff = FlexForm('Replace Beam Parameter values', components)
ff.show()

if ff.values:
    for beam in beams:
        p = beam.parameters[ff.values['parameter']]
        new_name = p.value.replace(ff.values['old'], ff.values['new'])
        with rpw.db.Transaction('rename beam {} to {}'.format(p.value, new_name)):
            p.value = new_name
