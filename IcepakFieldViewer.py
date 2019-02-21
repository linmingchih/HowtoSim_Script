config='''import os, sys, re, clr


dll_dir=r'C:\Program Files\AnsysEM\AnsysEM19.3\Win64\common\IronPython\DLLs'
sys.path.append(dll_dir)
clr.AddReference('IronPython.Wpf')
import wpf
from System.Windows import Window

#os.chdir(os.path.dirname(__file__))

#import System.Windows.Forms as WinForms 
#WinForms.MessageBox.Show('Debug')
'''
exec(config)

class moveCut():
    def __init__(self, oDesktop):
        self.oProject = oDesktop.GetActiveProject()
        self.oDesign = self.oProject.GetActiveDesign()
        self.oEditor = self.oDesign.SetActiveEditor("3D Modeler")
        
        self.unit=self.oEditor.GetModelUnits()
        
        self.Pcenter=[str(i)+self.unit for i in self.getCenter()]
        if not self.checkCut():
            self.createXCut(self.Pcenter)
            self.createYCut(self.Pcenter)
            self.createZCut(self.Pcenter)
        
    def getCenter(self):
        x,y,z=self.getMinMax()
        xc=(x[0]+x[1])/2
        yc=(y[0]+y[1])/2        
        zc=(z[0]+z[1])/2
        return(xc, yc, zc)
        
    def getMinMax(self):   
        p=[float(i) for i in self.oEditor.GetModelBoundingBox()]
        return (p[0],p[3]),(p[1],p[4]),(p[2],p[5])

    def checkCut(self):
        try:
            self.oEditor.ChangeProperty(["NAME:AllTabs",["NAME:Geometry3DPlaneTab",["NAME:PropServers","xCut"],["NAME:ChangedProps",["NAME:Normal","X:=","1","Y:=","0","Z:=","0"]]]])
            return True
        except:
            return False
    
    def _createCut(self, name, position, normal):
        self.oEditor.CreateCutplane(["NAME:PlaneParameters","PlaneBaseX:=",position[0],"PlaneBaseY:=",position[1],"PlaneBaseZ:=",position[2],"PlaneNormalX:=",normal[0],"PlaneNormalY:=",normal[1],"PlaneNormalZ:=",normal[2]],["NAME:Attributes","Name:=",name,"Color:=","(143 175 143)"])
    
    def createXCut(self, position):
        self._createCut('xCut', position, ("1","0","0"))
    
    def createYCut(self, position):
        self._createCut('yCut', position, ("0","1","0"))    
    
    def createZCut(self, position):
        self._createCut('zCut', position, ("0","0","1"))

    def _move(self, name, x=0, y=0, z=0):
        x0=x if x else self.Pcenter[0]
        y0=x if y else self.Pcenter[1]
        z0=x if z else self.Pcenter[2]
        
        self.oEditor.ChangeProperty(["NAME:AllTabs",["NAME:Geometry3DPlaneTab",["NAME:PropServers",name],["NAME:ChangedProps",["NAME:Root point","X:=",x,"Y:=",y,"Z:=",z]]]])
        
    def moveX(self, loc):
        self._move('xCut', x=str(loc)+self.unit)
        
    def moveY(self, loc):
        self._move('yCut', y=str(loc)+self.unit)
        
    def moveZ(self, loc):
        self._move('zCut', z=str(loc)+self.unit)



class MyWindow(Window):
    def __init__(self, oDesktop):
        wpf.LoadComponent(self, 'IcepakFieldViewer.xaml')
        self.mC=moveCut(oDesktop)
        self._initSlider()
        
    def _initSlider(self):  
        (xm,xM),(ym,yM),(zm,zM)=self.mC.getMinMax()
        self.sliderX.Maximum=xM
        self.sliderX.Minimum=xm
        self.sliderY.Maximum=yM
        self.sliderY.Minimum=ym
        self.sliderZ.Maximum=zM
        self.sliderZ.Minimum=zm
        
        self.sliderX.Value, self.sliderY.Value, self.sliderZ.Value = self.mC.getCenter()
        
        self.sliderX.TickFrequency=(xM-xm)/100
        self.sliderY.TickFrequency=(yM-ym)/100        
        self.sliderZ.TickFrequency=(zM-zm)/100
        
    def sliderX_ValueChanged(self, sender, e):
        self.mC.moveX(self.sliderX.Value)
    
    def sliderY_ValueChanged(self, sender, e):
        self.mC.moveY(self.sliderY.Value)
    
    def sliderZ_ValueChanged(self, sender, e):
        self.mC.moveZ(self.sliderZ.Value)


if __name__ == '__main__':
    window = MyWindow(oDesktop)
    window.ShowDialog()
