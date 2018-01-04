# -*- coding: utf-8 -*-
__title__ = 'Join Interference'
__author__ = 'htl'

import clr
import codecs
import re
import sys
import itertools

clr.AddReference('PresentationFramework')
from Microsoft.Win32 import OpenFileDialog

clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')

from Autodesk.Revit.DB import *
import rpw

def get_interference():
    dialog = OpenFileDialog()
    dialog.Title = "Select interference report"
    dialog.Filter = "HTML|*.html"
    if not dialog.ShowDialog():
        sys.exit()

    with codecs.open(dialog.FileName, 'r', 'utf-16') as f:
        data = f.read()
        if 'Interference Report' not in data:
            sys.exit()
        pattern = re.compile(r'<td>.+id (\d+)\s+</td>\s+<td>.+id (\d+)\s+</td>\s+')
        m = re.findall(pattern, data)
        ret = []
        for key, group in itertools.groupby(m, lambda x: x[0]):
            li = [key]
            for i in group:
                li.append(i[1])
            ret.append(li)
        return ret

def main():
    uiapp = __revit__
    uidoc = uiapp.ActiveUIDocument
    app = uiapp.Application
    doc = uidoc.Document
    interferences = get_interference()
    for line in interferences:
        host = line[0]
        others = line[1:]
        with rpw.db.Transaction('Join IDs {} with {}'.format(host, others)):
            for other in others:
                host_eid = ElementId(int(host))
                host_element = doc.GetElement(host_eid)
                other_eid = ElementId(int(other))
                other_element = doc.GetElement(other_eid)
                JoinGeometryUtils.JoinGeometry(doc, host_element, other_element)

if __name__ == '__main__':
    main()
