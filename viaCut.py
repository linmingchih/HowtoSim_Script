from math import sin, cos, pi, sqrt
class vector():
    def __init__(self, x=1, y=0):       
        self.x=x
        self.y=y
        
    def __repr__(self):
        return '{},{}'.format(self.x, self.y)
    
    def __add__(self, other):
        x0=self.x+other.x
        y0=self.y+other.y
        return vector(x0,y0)
    
    def __sub__(self, other):
        x0=self.x-other.x
        y0=self.y-other.y
        return vector(x0,y0)
    
    def __mul__(self, k):
        x0=self.x*k
        y0=self.y*k
        return vector(x0,y0)
     
    def __neg__(self):
        x0=self.x*-1
        y0=self.y*-1
        return vector(x0,y0)        
    
    def rotate90(self):
        x0=self.x*cos(pi/2)-self.y*sin(pi/2)
        y0=self.x*sin(pi/2)+self.y*cos(pi/2)
        return vector(x0,y0)

    def mag(self):
        return sqrt(self.x*self.x+self.y*self.y)
        
    def unit(self):
        k=self.mag()
        x0=self.x/k
        y0=self.y/k
        return vector(x0,y0)
    
    def get(self):
        return self.x, self.y

class cutRect():
    def __init__(self, pt0, pt1):
        self.v0=vector(pt0[0],pt0[1])
        self.v1=vector(pt1[0],pt1[1])
        self.dist=(self.v0-self.v1).mag()
        
    def get(self, w, h):
        u=(self.v1-self.v0).unit()
        v=u.rotate90()
        p0=u*w+v*h+self.v1
        p1=u*w-v*h+self.v1
        p2=-u*w-v*h+self.v0
        p3=-u*w+v*h+self.v0
        return [p0.get(), p1.get(), p2.get(), p3.get()]
    
class viaCut():
    def __init__(self, oProject):
        self.projectname=oProject.GetName()
        self.oDesign = oProject.GetActiveDesign()
        self.oEditor = self.oDesign.GetActiveEditor()
        self.unit=self.oEditor.GetActiveUnits()
        
    def _getLocation(self,name):
        loc=self.oEditor.GetPropertyValue('BaseElementTab', name, 'Location')
        return [float(i) for i in loc.split(',')]
        
    def _getNet(self, name):
        return self.oEditor.GetPropertyValue('BaseElementTab', name, 'Net')  
        
        
    def preprocess(self):
        
        sel=self.oEditor.GetSelections()

        via1, via2, via3 =sel[0], sel[1], sel[2]
        self.cR=cutRect(self._getLocation(via1), self._getLocation(via2))
            
        netpath=lambda x:self.projectname+':'+self._getNet(x)
        self.diff1=netpath(via1)
        self.diff2=netpath(via2)
        self.ref=netpath(via3)
            
        return 'diffnets:\n{}\n{}\n\nrefnet:\n{}'.format(self._getNet(via1),self._getNet(via2),self._getNet(via3))

        
    def showCutRegion(self, w=1, h=1):
        self.region=self.cR.get(w,h)
        p0, p1, p2, p3=self.region
        try:
            self.oEditor.Delete(["cutRegion"])
        except:
            pass
        self.oEditor.CreatePolygon(["NAME:Contents","polyGeometry:=",["Name:=","cutRegion","LayerName:=","Postprocessing","lw:=","0","n:=",4,"U:=","mm","x:=",p0[0],"y:=",p0[1],"x:=",p1[0],"y:=",p1[1],"x:=",p2[0],"y:=",p2[1],"x:=",p3[0],"y:=",p3[1],"x:=",p0[0],"y:=",p0[1]]])
        
    
    def genCutDesign(self, name):        
        p0, p1, p2, p3=self.region
        
        self.oEditor.CutOutSubDesign(["NAME:Params","Name:=",name,"EMDesign:=",True,"SubDesign:=",False,"Within:=",True,"Without:=",False,"AutoGenExtent:=",False,"Expansion:=",0.1,"RoundCorners:=",True,"Increments:=",1,"InPlace:=",False,"ExtentSel:=",[],["NAME:Nets","net:=",[self.ref,True],"net:=",[self.diff1,True],"net:=",[self.diff2,True]],"Extent:=",["cw:=",False,"cl:=",True,"pt:=",["U:=",self.unit,"x:=",p0[0],"y:=",p0[1],"x:=",p1[0],"y:=",p1[1],"x:=",p2[0],"y:=",p2[1],"x:=",p3[0],"y:=",p3[1],"x:=",p0[0],"y:=",p0[1]]]])
  

config='''import os, sys, re, clr

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

class MyWindow(Window):
    def __init__(self, oDesktop):
        wpf.LoadComponent(self, 'viaCut.xaml')
        oProject = oDesktop.GetActiveProject()
        self.vC=viaCut(oProject)
        try:
            self.tbMessage.Text=self.vC.preprocess()
            self.vC.showCutRegion(2,1)
            #self.tbMessage.Background=Colors.White
        except:
            self.tbMessage.Text='''Error! Vias are not correctly selected!\n
Please select 2 differential vias and then 1 ground via with Ctrl+Click before open this tool.'''
   
    def Button_Click(self, sender, e):
        self.vC.genCutDesign(self.tbCutName.Text)
        self.Close()
    
    def checkValid(self, sender, e):
        try:
            w=float(self.tbW.Text)
            l=float(self.tbL.Text)
            self.vC.showCutRegion(w,l)            
            1/len(self.tbCutName.Text)
            self.btCut.IsEnabled=True
        except Exception as e:
            self.btCut.IsEnabled=False
            

if __name__ == '__main__':
        window = MyWindow(oDesktop)
        window.ShowDialog()
