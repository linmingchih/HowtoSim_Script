config='''import os, sys, re, clr
from math import log, sqrt, exp
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

class createDiff():
    def __init__(self, oDesktop):
        self.oProject = oDesktop.GetActiveProject()
        self.oDesign = self.oProject.GetActiveDesign()
        self.oEditor = self.oDesign.SetActiveEditor("3D Modeler")
        self.oEditor.SetModelUnits(["NAME:UnitsParameter","Units:=","mil","Rescale:=",False])
        self.unit='mil'

        self.AddCopper()
        self.objectName=[]
  
    def AddCopper(self):
        oDefinitionManager = self.oProject.GetDefinitionManager()
        if not oDefinitionManager.DoesMaterialExist("copper"):
            oDefinitionManager.EditMaterial("copper",["NAME:copper","CoordinateSystemType:=","Cartesian","BulkOrSurfaceType:=",1,["NAME:PhysicsTypes","set:=",["Electromagnetic","Thermal","Structural"]],["NAME:AttachedData",["NAME:MatAppearanceData","property_data:=","appearance_data","Red:=",242,"Green:=",140,"Blue:=",102]],"permeability:=","0.999991","conductivity:=","58000000","thermal_conductivity:=","400","mass_density:=","8933","specific_heat:=","385","youngs_modulus:=","120000000000","poissons_ratio:=","0.38","thermal_expansion_coeffcient:=","1.77e-05"])

    def AddMaterial(self, dk):
        oDefinitionManager = self.oProject.GetDefinitionManager()
        x=oDefinitionManager.AddMaterial(["NAME:material","CoordinateSystemType:=","Cartesian","BulkOrSurfaceType:=",1,["NAME:PhysicsTypes","set:=",["Electromagnetic"]],"permittivity:=",str(dk)])
        
        return x
            
    def createBox(self, name, origin, size, material='"vacuum"', solveInside=True, color="(255 128 64)"):
        origin=tuple(str(i)+self.unit for i in origin)
        size=tuple(str(i)+self.unit for i in size)
        
        x=self.oEditor.CreateBox(["NAME:BoxParameters","XPosition:=", origin[0],"YPosition:=", origin[1],"ZPosition:=", origin[2],"XSize:=",size[0],"YSize:=",size[1],"ZSize:=",size[2]],["NAME:Attributes","Name:=", name,"Flags:=","","Color:=",color,"Transparency:=",0.5,"PartCoordinateSystem:=",'Global',"UDMId:=","","MaterialValue:=",material,"SurfaceMaterialValue:=","\"\"","SolveInside:=",solveInside,"IsMaterialEditable:=",True,"UseMaterialAppearance:=",False,"IsLightweight:=",False])
        
        return x
    
    def createSub(self, length, width, height, dk):
        self.length=length        
        
        sub_name=self.AddMaterial(dk)
        name=self.createBox('sub',(0,-width/2,0),(length,width,-height), color="(143 175 143)", material='"{}"'.format(sub_name))
        self.objectName.append(name)
        
        name=self.createBox('gnd',(0,-width/2,-height),(length,width,-0.1), material='"copper"', solveInside=False)
        self.objectName.append(name)
        
        name=self.createBox('air',(0,-width/2,-height-0.1),(length,width,width/2), color="(128 128 255)")    
        self.objectName.append(name)         
        
    def createPair(self, width, gap, thickness):

        name=self.createBox('traceP',(0,-gap/2,0),(self.length,-width,thickness), material='"copper"', solveInside=False)
        self.objectName.append(name)
        name=self.createBox('traceN',(0,+gap/2,0),(self.length,+width,thickness), material='"copper"', solveInside=False)
        self.objectName.append(name)            

    def group(self):
        self.oEditor.CreateGroup(["NAME:GroupParameter","ParentGroupID:=","Model","Parts:=",','.join(self.objectName),"SubmodelInstances:=","","Groups:=",""])
        self.objectName=[]
        self.oEditor.FitAll()



class MyWindow(Window):
    def __init__(self, oDesktop):
        wpf.LoadComponent(self, 'CreateZdiff.xaml')
        self.calculate(self, None)
        self.x=createDiff(oDesktop)
        
    def textBox1_MouseEnter(self, sender, e):
        self.lb1.Content='Trace Width(mil)'
    
    def textBox_MouseEnter(self, sender, e):
        self.lb1.Content='Trace Separation(mil)'
    
    def tb_dk_MouseEnter(self, sender, e):
        self.lb1.Content='Relative Dielectric Constant'
    
    def tb_H_MouseEnter(self, sender, e):
        self.lb1.Content='Dielectric Thickness(mil)'
    
    def tb_T_MouseEnter(self, sender, e):
        self.lb1.Content='Trace Thickness(mil)'
    
    def calculate(self, sender, e):
        try:
            w=float(self.textBox1.Text)
            dk=float(self.tb_dk.Text)
            d=float(self.textBox.Text)
            h=float(self.tb_H.Text)
            t=float(self.tb_T.Text)
            zdiff=round((174/sqrt(dk+1.41))*log(5.98*h/(0.8*w+t))*(1-0.48*exp(-0.96*d/h)),3)
            self.lb2.Content='Zdiff: '+str(zdiff)+' (ohm)'
        except:

            self.lb2.Content='Calculation Failed!'  
    
    def Rectangle_MouseEnter(self, sender, e):
        self.lb1.Content=''
    
    def Button_Click(self, sender, e):
        l=float(self.tb_l.Text)
        w=float(self.tb_w.Text)
        h=float(self.tb_H.Text)
        dk=float(self.tb_dk.Text)
        wt=float(self.textBox1.Text)
        gt=float(self.textBox.Text)
        ht=float(self.tb_T.Text)
        self.x.createSub(l,w,h, dk)
        self.x.createPair(wt,gt,ht)
        self.x.group()


if __name__ == '__main__':
    window = MyWindow(oDesktop)
    window.ShowDialog()