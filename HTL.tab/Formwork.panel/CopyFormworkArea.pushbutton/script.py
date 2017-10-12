# -*- coding: utf-8 -*-
__title__ = 'Copy\nFormwork Area'
__author__ = 'htl'
import sys
import clr
clr.AddReference('RevitAPI')

import rpw
from rpw import doc, uidoc
import Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import Selection
from itertools import izip


class CategoriesFilter(Selection.ISelectionFilter):
    def __init__(self, names):
        self.names = names
    def AllowElement(self, element):
        return element.Category.Name in self.names


def select_objects_by_category(*names):
    prompt = 'Pick {}'.format(', '.join(names))
    references = uidoc.Selection.PickObjects(Selection.ObjectType.Element,
                                           CategoriesFilter(names), prompt)
    return (rpw.db.Element.from_id(reference.ElementId) for reference in references)


def main():
    elements = select_objects_by_category('Floors', 'Structural Columns',
                                          'Structural Framing', 'Structural Foundations', 'Walls')
    with rpw.db.Transaction('Copy formwork area'):
        for element in elements:
            side_area = element.parameters['SOFiSTiK_FormworkArea_Side'].value
            bottom_area = element.parameters['SOFiSTiK_FormworkArea_Bottom'].value
            element.parameters['UDIC_FormworkArea_Side'].value = side_area
            element.parameters['UDIC_FormworkArea_Bottom'].value = bottom_area


if __name__ == '__main__':
    main()
