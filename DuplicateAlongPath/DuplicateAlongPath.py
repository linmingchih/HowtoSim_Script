config='''import os, sys, re, clr, math
try:
    dll_dir='C:/Program Files/AnsysEM/AnsysEM19.3/Win64/common/IronPython/DLLs'
    if not os.path.isdir(dll_dir):
        raise Exception 
except:
    m=re.search('(.*Win64)', __file__)
    dll_dir=m.group(1)+'/common/IronPython/DLLs'
finally:
    sys.path.append(dll_dir)
    clr.AddReference('IronPython.Wpf')  
    
    import wpf
    from System.Windows import Window
    os.chdir(os.path.dirname(__file__))
'''
exec(config)
oProject = oDesktop.GetActiveProject()
oDesign = oProject.GetActiveDesign()
oEditor = oDesign.SetActiveEditor("3D Modeler")

#Code Start-----------------------------------
class line():
    def __init__(self, v0, v1):
        self.v0=v0
        self.v1=v1
        self.l=[v1[0]-v0[0],v1[1]-v0[1],v1[2]-v0[2]]   
        self.length=math.sqrt(sum([i*i for i in self.l]))

    def _move(self, dl):
        if dl>self.length:
            return False
        
        v0, v1=self.v0, self.v1
        t=dl/self.length
        
        v0=(v0[0]+t*self.l[0], v0[1]+t*self.l[1], v0[2]+t*self.l[2])
        self.v0=v0
        self.l=[v1[0]-v0[0],v1[1]-v0[1],v1[2]-v0[2]]
        self.length=math.sqrt(sum([i*i for i in self.l])) 
        return True
    
    def getLoc(self, dl, offset):
        result=[]
        if self._move(offset):
            result.append(self.v0)
        else:
            return result, round(self.length,15)
        
        while self._move(dl):
            result.append(self.v0)
        else:
            return result, round(self.length,15)

def getLocations(x, dl):
    results=[]
    surplus=dl
    for i in range(len(x)-1):
        y=line(x[i], x[i+1])
        locs, surplus=y.getLoc(dl, dl-surplus)
        results+=locs
    
    return results
    
def polylinePoints(plines):
    points=[]
    for pline in plines:
        for i in oEditor.GetVertexIDsFromObject(pline):
            u=oEditor.GetVertexPosition(i)
            px = map(float, u)
            if points and px == points[-1]:
                pass
            else:
                points.append(px)
            
    p0=points[0]
    points=[[i[0]-p0[0], i[1]-p0[1], i[2]-p0[2]] for i in points[0:]]
    return points

class MyWindow(Window):
    def __init__(self):
        wpf.LoadComponent(self, 'DuplicateAlongPath.xaml')
        oDesktop.ClearMessages("", "", 2)        
        try:
            selections=oEditor.GetSelections()
            self.path.Text=str(selections[1:])
            self.objects.Text=selections[0]
            self.selections=selections
        except:
            raise Exception('Please Select "object" and then "polyline"!')
        
    def duplicate_Click(self, sender, e):
        objects=self.objects
        path=self.path
        pitch=self.pitch
        unit=oEditor.GetModelUnits()
        
        points=polylinePoints(self.selections[1:])        
        if not self.onVertex.IsChecked:
            points=getLocations(points, float(self.pitch.Text))
           
        for u in points[1:]:
            oEditor.Copy(["NAME:Selections","Selections:=",self.objects.Text])
            name=oEditor.Paste()
            for j in name:
                oEditor.Move(["NAME:Selections","Selections:=",j,"NewPartsModelFlag:=","Model"],["NAME:TranslateParameters","TranslateVectorX:=","{}{}".format(u[0], unit),"TranslateVectorY:=","{}{}".format(u[1], unit),"TranslateVectorZ:=","{}{}".format(u[2], unit)])
                
#Code End-------------------------------------        
MyWindow().ShowDialog()

