# -*- coding: utf-8 -*-
# __title__ = 'Assign\nRebar Partition'
__author__ = 'htl'

import clr
import codecs
import re
import sys


clr.AddReference('PresentationFramework')
from Microsoft.Win32 import OpenFileDialog

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
    for i in m:
        print(','.join(i))
