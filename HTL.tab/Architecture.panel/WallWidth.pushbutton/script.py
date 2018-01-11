# -*- coding: utf-8 -*-
__title__ = 'Wall Width'
__author__ = 'htl'
import clr
clr.AddReference('RevitAPI')

import rpw
from htl import selection


def main():
    uiapp = __revit__
    uidoc = uiapp.ActiveUIDocument
    app = uiapp.Application
    doc = uidoc.Document

    try:
        elements = selection.select_objects_by_category('Windows', 'Doors')
    except:
        return
    with rpw.db.Transaction('Update parameter'):
        for e in elements:
            host_type_id = e.Host.GetTypeId()
            host_type = doc.GetElement(host_type_id)
            width = host_type.Width
            e.LookupParameter('UDIC_Wall_Width').Set(width)


if __name__ == '__main__':
    main()
