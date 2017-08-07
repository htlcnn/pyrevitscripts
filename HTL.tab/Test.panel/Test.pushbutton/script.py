from pprint import pprint
from scriptutils import this_script

import os
import clr
clr.AddReference('IronPython.Wpf')
clr.AddReference("PresentationFramework")
clr.AddReference('PresentationCore')

from IronPython.Modules import Wpf as wpf

from System import Uri
from System.Windows import Window
from System.Windows.Media.Imaging import BitmapImage
from System.IO import StringReader

script_path = '\\'.join(this_script.info.script_file.split('\\')[:-1])
xaml_path = os.path.join(script_path, 'xaml.xaml')
with open(xaml_path) as f:
    xaml = f.read()

class MyWindow(Window):
    def __init__(self):
        wpf.LoadComponent(self, StringReader(xaml))

    def OnLoad(self, sender, e):
        # self.image1.Source = os.path.join(script_path, 'icon.png')
        pass

    def ApplyButton_Click(self, sender, e):
        pass

    def ComboBox_SelectionChanged(self, sender, e):
        pass


w = MyWindow()
w.Title = "Auto Foundation"
w.Width = 300
img_path = BitmapImage(Uri(os.path.join(script_path, 'icon.png')))
w.image1.Source = img_path
w.image1.Width = 32
w.Show()
