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

#Replace MyWindow class from Visual Studio
def buildBlock(x,y,z):
    #import ScriptEnv
    #ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
    #oDesktop.RestoreWindow()
    oProject = oDesktop.GetActiveProject()
    oDesign = oProject.GetActiveDesign()
    oEditor = oDesign.SetActiveEditor("3D Modeler")
    oEditor.CreateBox(
        [
            "NAME:BoxParameters",
            "XPosition:="		, "0mm",
            "YPosition:="		, "0mm",
            "ZPosition:="		, "0mm",
            "XSize:="		, x,
            "YSize:="		, y,
            "ZSize:="		, z
        ], 
        [
            "NAME:Attributes",
            "Name:="		, "Box1",
            "Flags:="		, "",
            "Color:="		, "(143 175 143)",
            "Transparency:="	, 0,
            "PartCoordinateSystem:=", "Global",
            "UDMId:="		, "",
            "MaterialValue:="	, "\"vacuum\"",
            "SurfaceMaterialValue:=", "\"\"",
            "SolveInside:="		, True,
            "IsMaterialEditable:="	, True,
            "UseMaterialAppearance:=", False,
            "IsLightweight:="	, False
        ])
    oEditor.FitAll()

class MyWindow(Window):
    def __init__(self):
        wpf.LoadComponent(self, 'Box_Gen.xaml')
        
    def Button_Click(self, sender, e):
        x=self.xsz.Text
        y=self.ysz.Text
        z=self.zsz.Text
        buildBlock(x,y,z)
        pass


# Invoke GUI in AEDT. Don't Revise It.
if __name__ == '__main__':
	window = MyWindow()
	window.ShowDialog()
