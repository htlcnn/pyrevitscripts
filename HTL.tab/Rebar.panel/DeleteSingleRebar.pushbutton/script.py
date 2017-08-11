# -*- coding: utf-8 -*-
__title__ = 'Delete\nSingle Rebars'
__author__ = 'htl'

import clr
clr.AddReference('RevitAPI')

import Autodesk

import rpw
from rpw import doc

single_rebars = rpw.db.Collector(of_class=Autodesk.Revit.DB.Structure.Rebar, view=doc.ActiveView,
                    where=lambda x: x.LayoutRule==Autodesk.Revit.DB.Structure.RebarLayoutRule.Single)

with rpw.db.Transaction('Delete single rebars'):
    for bar in single_rebars:
        doc.Delete(bar.Id)
