import clr
clr.AddReference('RevitAPI')
import Autodesk
from Autodesk.Revit.UI import Selection
import rpw
from rpw import uidoc


from System.Collections.Generic import List

class CategoriesFilter(Selection.ISelectionFilter):
    def __init__(self, names):
        self.names = names
    def AllowElement(self, element):
        return element.Category.Name in self.names


def select_objects_by_category(*names):
    prompt = 'Pick {}'.format(', '.join(names))
    references = uidoc.Selection.PickObjects(Selection.ObjectType.Element,
                                           CategoriesFilter(names), prompt)
    return (rpw.db.Element.from_id(reference.ElementId).unwrap() for reference in references)


def select_object_by_category(name):
    prompt = 'Pick {}'.format(name)
    reference = uidoc.Selection.PickObject(Selection.ObjectType.Element,
                                           CategoriesFilter(name), prompt)
    return rpw.db.Element.from_id(reference.ElementId).unwrap()
