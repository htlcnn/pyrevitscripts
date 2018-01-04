# -*- coding: utf-8 -*-
# __title__ = 'Assign\nRebar Partition'
__author__ = 'htl'
import os
import re
import clr

# clr.AddReference('RevitAPI')
# import Autodesk


# def get_hdd_serial_number():
#     path = System.IO.Path.GetPathRoot(System.Environment.SystemDirectory).strip('\\')
#     query = "ASSOCIATORS OF {Win32_LogicalDisk.DeviceID='%s'} WHERE ResultClass=Win32_DiskPartition" % path

#     searcher = ManagementObjectSearcher(query)
#     partition_info = str(list(searcher.Get())[0])

#     pattern = re.compile(r'.+"Disk #(\d).+')
#     partition_number = re.findall(pattern, partition_info)[0]

#     searcher1 = ManagementObjectSearcher('SELECT * FROM Win32_DiskDrive')
#     searcher2 = ManagementObjectSearcher('SELECT * FROM Win32_PhysicalMedia')

#     for wmi_hd, wmi_pm in zip(searcher1.Get(), searcher2.Get()):
#         if wmi_hd['DeviceID'].endswith(partition_number):
#             return wmi_pm['SerialNumber'].strip()

# secret_key = 'htl'
# hdd_serial = get_hdd_serial_number()

import System

import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')

from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
import rpw

from htl import selection


uiapp = __revit__
uidoc = uiapp.ActiveUIDocument
app = uiapp.Application
doc = uidoc.Document


# print(System.Enum.GetValues(BuiltInCategory))
print([(c.Name, c.CategoryType) for c in doc.Settings.Categories])

# elements = selection.select_objects_by_category('Structural Rebar')

# for e in elements:
#     print(dir(e.Location))
    # sda = e.GetShapeDrivenAccessor()
    # print(sda.GetDistributionPath().Length)

# ref = uidoc.Selection.PickObject(Selection.ObjectType.Face)

# e = doc.GetElement(ref.ElementId)
# face = e.GetGeometryObjectFromReference(ref)

# plane = face.GetSurface()
# with rpw.db.Transaction('Set Workplane'):
#     sp = SketchPlane.Create(doc, plane)
#     doc.ActiveView.SketchPlane = sp
#     # doc.ActiveView.ShowActiveWorkPlane()

# p1 = uidoc.Selection.PickPoint(Selection.ObjectSnapTypes.Endpoints|Selection.ObjectSnapTypes.Midpoints)
# p2 = uidoc.Selection.PickPoint(Selection.ObjectSnapTypes.Endpoints|Selection.ObjectSnapTypes.Midpoints)

# print(p1, p2)


# def main():
#     print("Main")

# if __name__=='__main__':
#     import sys
#     sys.path.append(r'E:\Setup\UCE\Autodesk\Revit\pyRevit extensions\htl.extension\HTL.tab\Test.panel\Test.pushbutton')
#     clr.AddReferenceToFile('htladdin.dll')
#     print(sys.path)
#     import htladdin
    # addin = HTLAddin('test')
    # print(addin.execute())
