# -*- coding: utf-8 -*-
__title__ = 'Update Formwork Comments'
__author__ = 'htl'
from itertools import chain
import sys
import clr
clr.AddReference('RevitAPI')
import Autodesk

import rpw
from rpw import doc, uidoc
from rpw.ui.forms import Label, TextBox, Button, FlexForm
from Autodesk.Revit.DB import *

from System.Collections.Generic import List

from htl import selection


def main():
    try:
        formworks = selection.select_objects_by_category('Generic Models')
    except:
        return

    with rpw.db.Transaction('update parameter'):
        for formwork in formworks:
            formwork_name = formwork.LookupParameter('UDIC_Name').AsString()
            eid = int(formwork_name.split()[-1])
            host = rpw.db.Element.from_int(eid)

            # host_category = host.Category.Name
            # if host_category == 'Structural Columns':
            #     param = 'Base Level'
            # elif host_category == 'Structural Framing':
            #     param = 'Reference Level'
            # elif host_category == 'Floors':
            #     param = 'Level'
            # elif host_category == 'Walls':
            #     param = 'Base Constraint'
            # elif host_category == 'Generic Models':
            #     param = 'Level'
            param = 'Comments'

            # formwork_level = host.LookupParameter(param).AsValueString()
            # formwork.LookupParameter('UDIC_Formwork_Level').Set(formwork_level)
            comments = host.LookupParameter(param).AsString()
            if comments:
                formwork.LookupParameter('Comments').Set(comments)


if __name__ == '__main__':
    main()
