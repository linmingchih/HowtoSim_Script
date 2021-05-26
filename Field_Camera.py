# coding=UTF-8
import os, sys, re, math, json, time, clr

win64_dir = oDesktop.GetExeDir()
dll_dir = os.path.join(win64_dir, 'common/IronPython/DLLs')
sys.path.append(dll_dir)
clr.AddReference('IronPython.Wpf')

import wpf
from System.Windows import Window
from System.Windows.Controls import ListBoxItem
from System.Windows.Forms import OpenFileDialog, SaveFileDialog, DialogResult, FolderBrowserDialog
os.chdir(os.path.dirname(__file__))


import ScriptEnv

ScriptEnv.Initialize("AnsoftHfss.HfssScriptInterface")
oProject = oDesktop.GetActiveProject()
oDesign = oProject.GetActiveDesign()
oEditor=oDesign.SetActiveEditor('3D Modeler')

class solutions():
    def __init__(self):
        oProject = oDesktop.GetActiveProject()
        self.oDesign = oProject.GetActiveDesign()
        
    def getReportType(self):
        oModule=self.oDesign.GetModule("ReportSetup")
        return oModule.GetAvailableReportTypes()

    def getAvailableSolution(self, ReportType):
        oModule=self.oDesign.GetModule("ReportSetup")
        return oModule.GetAvailableSolutions(ReportType)
    
    def getFrequency(self, Solution):
        oModule=self.oDesign.GetModule("Solutions")
        return oModule.GetSolveRangeInfo(Solution)
        
    def getVariations(self, Solution):
        oModule=self.oDesign.GetModule("Solutions")
        return oModule.GetAvailableVariations(Solution)

class boundingbox():
    def __init__(self):
        self.bb=[float(i) for i in oEditor.GetModelBoundingBox()]
    
    def getBoundary(self):
        return list(zip(self.bb[0:3], self.bb[3:6]))
    
    def getCenter(self):
        return [(i+j)/2 for i,j in zip(self.bb[0:3], self.bb[3:6])]
    
class fieldCut():
    def __init__(self):
        self.deleteCS()
        self.unit=oEditor.GetModelUnits()
    
    def createCS(self, _origin):
        origin=[str(i)+self.unit for i in _origin]
        
        oEditor.CreateRelativeCS(["NAME:RelativeCSParameters","Mode:=","Axis/Position","OriginX:=",origin[0],"OriginY:=",origin[1],"OriginZ:=",origin[2],"XAxisXvec:=","1mm","XAxisYvec:=","0mm","XAxisZvec:=","0mm","YAxisXvec:=","0mm","YAxisYvec:=","1mm","YAxisZvec:=","0mm"],["NAME:Attributes","Name:=","FCCS"])
        

    def deleteCS(self):
        try:
            oEditor.Delete(["NAME:Selections","Selections:=","FCCS"])
        except:
            pass
            
    def createField(self, solution="Setup1:LastAdaptive", frequency='65GHz', quantity='Mag_E', plane='YZ'):
        oModule = oDesign.GetModule("FieldsReporter")
        try:
            oModule.DeleteFieldPlot(["fieldcam"])
        except:
            pass
          
        oModule.CreateFieldPlot(["NAME:fieldcam","SolutionName:=", solution,"QuantityName:=",quantity,"PlotFolder:=","field","UserSpecifyName:=",0,"UserSpecifyFolder:=",0,"StreamlinePlot:=",False,"AdjacentSidePlot:=",False,"FullModelPlot:=",False,"IntrinsicVar:=","Freq=\'{}\'Phase=\'0deg\'".format(frequency),"PlotGeomInfo:=",[1,"Surface","CutPlane",1,"FCCS:{}".format(plane)],"FilterBoxes:=",[0],["NAME:PlotOnSurfaceSettings","Filled:=",False,"IsoValType:=","Fringe","SmoothShade:=",True,"AddGrid:=",False,"MapTransparency:=",True,"Refinement:=",0,"Transparency:=",0,"SmoothingLevel:=",0,["NAME:Arrow3DSpacingSettings","ArrowUniform:=",True,"ArrowSpacing:=",0,"MinArrowSpacing:=",0,"MaxArrowSpacing:=",0],"GridColor:=",[255,255,255]]],"Field")
    
    def moveCS(self, _coordinate):
        co=[str(i)+self.unit for i in _coordinate]
        oEditor.ChangeProperty(["NAME:AllTabs",["NAME:Geometry3DCSTab",["NAME:PropServers","FCCS"],["NAME:ChangedProps",["NAME:Origin","X:=", co[0],"Y:=", co[1],"Z:=", co[2]]]]])

    def changePhase(self, phase):
        oDesign.ChangeProperty(["NAME:AllTabs",["NAME:FieldsPostProcessorTab",["NAME:PropServers","FieldsReporter:fieldcam"],["NAME:ChangedProps",["NAME:Phase","Value:=","{}deg".format(phase)]]]])

#Code Start-----------------------------------
class MyWindow(Window):
    def __init__(self):
        wpf.LoadComponent(self, 'Field_Camera.xaml')
        
        self.bb=boundingbox()
        self.coordinate=self.bb.getCenter()
        
        self.plane='YZ'
        self.fc=fieldCut()
        self.fc.createCS(self.coordinate)

        self.solu=solutions()
        s=self.solu.getAvailableSolution("Fields")
        for i in s:
            self.solution_CB.Items.Add(i)
        self.solution_CB.SelectedIndex = 0

        try:
            with open('quantity.json', 'r') as fp:
                self.quantity = json.load(fp)
        except:
            self.quantity=["Mag_E", "Mag_H", "Mag_Jvol", "Mag_Jsurf", "ComplexMag_E", "ComplexMag_H", "ComplexMag_Jvol","ComplexMag_Jsurf", "Vector_E", "Vector_H","Vector_Jvol", "Vector_Jsurf", "Vector_RealPoynting","Local_SAR", "Average_SAR"]
            with open('quantity.json', 'w') as fp:
                json.dump(self.quantity, fp, sort_keys=True, indent=4)  
        
        for i in self.quantity:
            self.quantity_CB.Items.Add(i)
        self.quantity_CB.SelectedIndex = 0
        
        self.plane='YZ'
        self.createField()
        x,y,z=self.bb.getBoundary()
        self.position_SB.Minimum=x[0]
        self.position_SB.Maximum=x[1]
        self.position_SB.Value=self.coordinate[0]
        
        
    def createField(self):
        _solution=self.solution_CB.SelectedItem
        _frequency=str(float(self.frequency_CB.SelectedItem)/1e9)+'GHz'
        _quantity=self.quantity_CB.SelectedItem

        _plane=self.plane
        try:
            self.fc.createField(_solution, _frequency, _quantity, _plane)
        except:
            pass
        
    def solution_CB_SelectionChanged(self, sender, e):
        for f in self.solu.getFrequency(self.solution_CB.SelectedItem):
            self.frequency_CB.Items.Add(f)
        self.frequency_CB.SelectedIndex = 0
        

    
    def frequency_CB_SelectionChanged(self, sender, e):
        self.createField()

    
    def variation_CB_SelectionChanged(self, sender, e):
        pass

    def quantity_CB_SelectionChanged(self, sender, e):
        self.createField()

    
    def Slider_ValueChanged(self, sender, e):
        pass

    
    def shot_BT_Click(self, sender, e):
        dialog = SaveFileDialog()
        dialog.Filter = "Image(*.png)|*.png"
        dialog.FileName=self.quantity_CB.Text+'_'+self.plane+'_'+str(self.position_SB.Value)
        if dialog.ShowDialog() == DialogResult.OK:
            options=['NAME:SaveImageParams','ShowAxis:=','Default','ShowGrid:=','Default','ShowRuler:=','Default']
            oEditor.ExportModelImageToFile(dialog.FileName, 1200, 900, options)
    
    def add_BT_Click(self, sender, e):
        self.quantity.append(self.quantity_TB.Text)
        with open('quantity.json', 'w') as fp:
            json.dump(self.quantity, fp, sort_keys=True, indent=4) 
        
        self.quantity_CB.Items.Clear()
        for i in self.quantity:
            self.quantity_CB.Items.Add(i)
        self.quantity_CB.SelectedIndex = 0
    
    def del_BT_Click(self, sender, e):
        try:
            self.quantity.remove(self.quantity_CB.SelectedItem)
            with open('quantity.json', 'w') as fp:
                json.dump(self.quantity, fp, sort_keys=True, indent=4) 
        except:
            pass
            
        self.quantity_CB.Items.Clear()
        for i in self.quantity:
            self.quantity_CB.Items.Add(i)
        self.quantity_CB.SelectedIndex = 0            
            
            
    def X_RB_Checked(self, sender, e):
        self.plane='YZ'
        self.position_SB.Value=self.coordinate[0]
        x,y,z=self.bb.getBoundary()

        self.position_SB.Minimum=x[0]
        self.position_SB.Maximum=x[1]

        self.createField()
        
    def Y_RB_Checked(self, sender, e):
        self.plane='XZ'
        self.position_SB.Value=self.coordinate[1]
        x,y,z=self.bb.getBoundary()
        self.position_SB.Minimum=y[0]
        self.position_SB.Maximum=y[1]

        self.createField()
    
    def Z_RB_Checked(self, sender, e):
        self.plane='XY'
        self.position_SB.Value=self.coordinate[2]
        x,y,z=self.bb.getBoundary()
        self.position_SB.Minimum=z[0]
        self.position_SB.Maximum=z[1]

        self.createField()
    
    def position_SB_ValueChanged(self, sender, e):
        if self.X_RB.IsChecked:
            self.coordinate[0]=self.position_SB.Value
        elif self.Y_RB.IsChecked:
            self.coordinate[1]=self.position_SB.Value            
        else:
            self.coordinate[2]=self.position_SB.Value
            
        self.fc.moveCS(self.coordinate)
        self.value_Label.Content=str(round(self.position_SB.Value,6)) 

    def phase_SB_ValueChanged(self, sender, e):
        print(sender.Value)
        self.fc.changePhase(sender.Value)
        
    def Window_Closing(self, sender, e):
        ReleaseDesktop()
        pass


        
def ReleaseDesktop():
    from Ansys.Ansoft.CoreCOMScripting.Util import COMUtil
    COMUtil.PInvokeProxyAPI.ReleaseCOMObjectScope(0)


MyWindow().Show()
oDesktop.PauseScript("Field Camera is opened!")

