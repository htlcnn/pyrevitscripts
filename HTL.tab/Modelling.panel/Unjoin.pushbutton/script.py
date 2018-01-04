# -*- coding: utf-8 -*-
__title__ = 'Unjoin Elements'
__author__ = 'htl'

import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
import rpw
from htl import selection

def main():
    uiapp = __revit__
    uidoc = uiapp.ActiveUIDocument
    doc = uidoc.Document
    cats = ['Structural Framing', 'Structural Columns', 'Structural Foundations',
            'Floors', 'Walls', 'Generic Models']
    elements = selection.select_objects_by_category(*cats)
    with rpw.db.Transaction('Unjoin all selected items'):
        for element in elements:
            joined_element_ids = JoinGeometryUtils.GetJoinedElements(doc, element)
            for joined_element_id in joined_element_ids:
                joined_element = doc.GetElement(joined_element_id)
                try:
                    JoinGeometryUtils.UnjoinGeometry(doc, element, joined_element)
                except Exception as e:
                    print(e)
                    pass

if __name__ == '__main__':
    main()
