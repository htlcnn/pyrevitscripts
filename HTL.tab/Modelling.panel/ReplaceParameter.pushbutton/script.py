# -*- coding: utf-8 -*-
__title__ = 'Replace\nParameter Value'
__author__ = 'htl'

import sys
import rpw
from rpw import doc
from rpw.ui.forms import Label, TextBox, Button, ComboBox, FlexForm
from pprint import pprint

selection = rpw.ui.Selection()

if not selection:
  try:
      elements = rpw.db.Collector(of_class='FamilyInstance',
                              view=doc.ActiveView).wrapped_elements
  except:
      sys.exit()
else:
  elements = selection.wrapped_elements

editable = {p.name: p.name for p in elements[0].parameters.all
                 if not p.IsReadOnly and p.StorageType==rpw.DB.StorageType.String}

components = [ComboBox('parameter', editable),
              Label('Replace:'),
              TextBox('old'),
              Label('With:'),
              TextBox('new'),
              Button('Replace'),
            ]

ff = FlexForm('Replace Parameter values', components)
ff.show()

if ff.values:
    for element in elements:
      try:
          p = element.parameters[ff.values['parameter']]
          if ff.values['old'] in p.value:
            new_name = p.value.replace(ff.values['old'], ff.values['new'])
            with rpw.db.Transaction('Rename {} to {}'.format(p.value, new_name)):
                p.value = new_name
      except Exception, e:
          print(e)
          pass
