# -*- coding: utf-8 -*-
__title__ = 'Add Parameters'
__author__ = 'htl'

import clr
import codecs
import re

clr.AddReference('PresentationFramework')
from Microsoft.Win32 import OpenFileDialog

clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')

from Autodesk.Revit.DB import *
import rpw

def get_sp_file():
    dialog = OpenFileDialog()
    dialog.Title = "Select Shared Parameters file"
    dialog.Filter = "TXT|*.txt"
    if not dialog.ShowDialog():
        return

    with codecs.open(dialog.FileName, 'r', 'utf-16') as f:
        data = f.read()
        if '# This is a Revit shared parameter file.' not in data:
            return
    return dialog.FileName

def add_shared_parameters(sp_file, params, categories):
    uiapp = __revit__
    uidoc = uiapp.ActiveUIDocument
    app = uiapp.Application
    doc = uidoc.Document
    with rpw.db.Transaction('Add Shared Parameters'):
        for p in params:
            app.SharedParametersFilename = sp_file.name
            definition_file = app.OpenSharedParameterFile()
            group = definition_file.Groups.Item['UDIC-KetCau']
            definition = group.Definitions.Item[p]
            try:
                category_set = CategorySet()
                for cat in categories:
                    if type(cat) == BuiltInCategory:
                        bi_cat = Category.GetCategory(doc, cat)
                        category_set.Insert(bi_cat)
                    else:
                        category_set.Insert(cat)
                instance_binding = InstanceBinding(category_set)
                binding_map = doc.ParameterBindings
                binding_map.Insert(definition, instance_binding,
                                   BuiltInParameterGroup.PG_CONSTRUCTION)
            except Exception as e:
                pass

def main():
    uiapp = __revit__
    uidoc = uiapp.ActiveUIDocument
    app = uiapp.Application
    doc = uidoc.Document
    sp_file_path = get_sp_file()
    if not sp_file_path:
        return
    with codecs.open(sp_file_path, 'r', 'utf-16') as sp_file:
        p1 = ['UDIC_Formwork_Type', 'UDIC_Formwork_Area', 'UDIC_Formwork_Hostname',
              'UDIC_Formwork_Hostcategory', 'UDIC_Formwork_Level']
        c1 = [BuiltInCategory.OST_GenericModel]
        add_shared_parameters(sp_file, p1, c1)

        p2 = ['UDIC_FormworkArea_Side', 'UDIC_FormworkArea_Bottom', 'UDIC_Name']
        c2 = [
              BuiltInCategory.OST_Floors, BuiltInCategory.OST_GenericModel,
              BuiltInCategory.OST_StructuralColumns, BuiltInCategory.OST_StructuralFoundation,
              BuiltInCategory.OST_StructuralFraming, BuiltInCategory.OST_Walls
             ]
        add_shared_parameters(sp_file, p2, c2)


if __name__ == '__main__':
    main()
