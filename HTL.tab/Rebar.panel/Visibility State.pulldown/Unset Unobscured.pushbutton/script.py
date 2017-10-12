# -*- coding: utf-8 -*-
__title__ = 'Unset Unobscured'
__author__ = 'htl'
import sys
import rpw
from rpw import doc, uidoc
import Autodesk


class CategoriesFilter(Autodesk.Revit.UI.Selection.ISelectionFilter):
    def __init__(self, names):
        self.names = names
    def AllowElement(self, element):
        return element.Category.Name in self.names


def select_by_category(prompt='Pick Objects', *names):
    references = uidoc.Selection.PickObjects(Autodesk.Revit.UI.Selection.ObjectType.Element,
                                           CategoriesFilter(names), prompt)
    return [rpw.db.Element.from_id(reference.ElementId) for reference in references]

def select_rebars():
    sel = rpw.ui.Selection()
    if sel:
        sel = [rpw.db.Element.from_id(eid) for eid in sel.element_ids]
        sel = [e for e in sel if e.Category.Name=='Structural Rebar']
        return sel
    else:
        try:
            elements = select_by_category('Pick Rebars','Structural Rebar')
            return elements
        except:
            sys.exit()

rebars = select_rebars()

with rpw.db.Transaction('Unset Rebars Unobscured in Active View'):
    for rebar in rebars:
        rebar.SetUnobscuredInView(doc.ActiveView, False)

