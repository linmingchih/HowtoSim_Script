# Environment Setting for WFM. Don't Revise It.
import os, sys, clr

clr.AddReference('System.Windows.Forms') 
import System.Windows.Forms as WinForms 
#WinForms.MessageBox.Show('Debug')

code_dir=os.path.dirname(__file__)
dll_dir=''
for i in code_dir.split('/'):
    if i != 'Win64':
        dll_dir+=i+'/'
    else:
        dll_dir+='Win64/common/IronPython/DLLs'
        break
       
sys.path.append(dll_dir)

clr.AddReference('IronPython.Wpf')
os.chdir(code_dir)
import wpf
from System.Windows import Window

from Box_Gen_M import buildBlock
class MyWindow(Window):
    def __init__(self):
        wpf.LoadComponent(self, 'Box_Gen_V.xaml')
        
    def Button_Click(self, sender, e):
        x=self.xsz.Text
        y=self.ysz.Text
        z=self.zsz.Text
        buildBlock(x,y,z, oDesktop)
        pass

# Invoke GUI in AEDT. Don't Revise It.

if __name__ == '__main__':
    
	window = MyWindow()
	window.ShowDialog()
    
