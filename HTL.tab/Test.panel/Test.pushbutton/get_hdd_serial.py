import System
import clr
import os
import re

def get_hdd_serial_number():
    path = System.IO.Path.GetPathRoot(System.Environment.SystemDirectory).strip('\\')
    query = "ASSOCIATORS OF {Win32_LogicalDisk.DeviceID='%s'} WHERE ResultClass=Win32_DiskPartition" % path

    searcher = ManagementObjectSearcher(query)
    partition_info = str(list(searcher.Get())[0])

    pattern = re.compile(r'.+"Disk #(\d).+')
    partition_number = re.findall(pattern, partition_info)[0]

    searcher1 = ManagementObjectSearcher('SELECT * FROM Win32_DiskDrive')
    searcher2 = ManagementObjectSearcher('SELECT * FROM Win32_PhysicalMedia')

    for wmi_hd, wmi_pm in zip(searcher1.Get(), searcher2.Get()):
        if wmi_hd['DeviceID'].endswith(partition_number):
            return wmi_pm['SerialNumber'].strip()

secret_key = 'fjeiowjfklsdeoiu'
hdd_serial = get_hdd_serial_number()
