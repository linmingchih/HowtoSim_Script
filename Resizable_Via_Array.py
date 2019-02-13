config='''
import os, sys, re, clr

m=re.search('(.*Win64)', __file__)
dll_dir=m.group(1)+'/common/IronPython/DLLs'
sys.path.append(dll_dir)
clr.AddReference('IronPython.Wpf')
import wpf
from System.Windows import Window

os.chdir(os.path.dirname(__file__))

#import System.Windows.Forms as WinForms 
#WinForms.MessageBox.Show('Debug')
'''
exec(config)

class duplicateVia():

    def __init__(self):
        oProject = oDesktop.GetActiveProject()
        self.oDesign = oProject.GetActiveDesign()
        self.oEditor = self.oDesign.GetActiveEditor()
        self.activeUnits = self.oEditor.GetActiveUnits()
        
    def setProperty(self, x_name, x_value, y_name, y_value):
        vars=self.oDesign.GetVariables()
        self.x_name, self.y_name=x_name, y_name
        if x_name not in vars:        
            self.oDesign.ChangeProperty(
                [
                    "NAME:AllTabs",
                    [
                        "NAME:DefinitionParameterTab",
                        [
                            "NAME:PropServers", 
                            "Instance:"+self.oDesign.GetName()
                        ],
                        [
                            "NAME:NewProps",
                            [
                                "NAME:"+x_name,
                                "PropType:="		, "VariableProp",
                                "UserDef:="		, True,
                                "Value:="		, x_value
                            ]
                        ]
                    ]
                ])
        
        if y_name not in vars:        
            self.oDesign.ChangeProperty(
                [
                    "NAME:AllTabs",
                    [
                        "NAME:DefinitionParameterTab",
                        [
                            "NAME:PropServers", 
                            "Instance:"+self.oDesign.GetName()
                        ],
                        [
                            "NAME:NewProps",
                            [
                                "NAME:"+y_name,
                                "PropType:="		, "VariableProp",
                                "UserDef:="		, True,
                                "Value:="		, y_value
                            ]
                        ]
                    ]
                ])        
            
    def duplicate(self, m, n):
        if self.oEditor.GetSelections()==[]:
            AddErrorMessage("Please select a via first!")
            return None
        
        else:
            item=self.oEditor.GetSelections()[0]
        
        cs=self.oEditor.GetPropertyValue("BaseElementTab",item, "Location")
        x0,y0=cs.split(',')
        
        mymatrix=[]
        for i in range(m):
            self.oEditor.Duplicate(
                [
                    "NAME:options",
                    "count:="		, n
                ], 
                [
                    "NAME:elements", 
                    item
                ], [0, 0])

            mymatrix.append(self.oEditor.GetSelections()[1:])
        
 
        for i,m in enumerate(mymatrix):
            for j,n in enumerate(m):
                locx='({0}{1}+{2}*{3})'.format(x0,self.activeUnits,i,self.x_name)
                locy='({0}{1}+{2}*{3})'.format(y0,self.activeUnits,j,self.y_name)
                self._changeLocation(n,locx,locy)
        self.oEditor.Delete([item])
        
    def _changeLocation(self, item, x, y):
        self.oEditor.ChangeProperty(
            [
                "NAME:AllTabs",
                [
                    "NAME:BaseElementTab",
                    [
                        "NAME:PropServers", 
                        item
                    ],
                    [
                        "NAME:ChangedProps",
                        [
                            "NAME:Location",
                            "X:="			, x,
                            "Y:="			, y
                        ]
                    ]
                ]
            ])        


#Replace MyWindow class from Visual Studio
class MyWindow(Window):
    def __init__(self):
        wpf.LoadComponent(self, 'Resizable_Via_Array.xaml')
        
    def Button_Click(self, sender, e):
        dv=duplicateVia()
        dv.setProperty(self.Nx.Text, self.Vx.Text, self.Ny.Text, self.Vy.Text)            
        dv.duplicate(int(self.Cx.Text), int(self.Cy.Text))

# Invoke GUI in AEDT. Don't Revise It.
if __name__ == '__main__':
	window = MyWindow()
	window.ShowDialog()
