import ScriptEnv
from math import sin, cos, pi
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject=oDesktop.GetActiveProject()
oDesign=oProject.GetActiveDesign()
oEditor=oDesign.SetActiveEditor("3D Modeler")

def trace(L0, dL, N, M):
   
    orientations=[(cos(i*2*pi/N),sin(i*2*pi/N)) for i in range(M)]
    x, y = 0, 0
    points=[(x,y)]
    for i,(u,v) in enumerate(orientations):
        x=x+(L0+i*dL)*u
        y=y+(L0+i*dL)*v
        points.append((x,y))
    
    return points

def factor(L0, N):
    points=trace(L0 , 1, N, N)
    pA=points[0]
    pB=points[-1]
    return abs(pA[1]-pB[1])
    
class createSpiral():
    def __init__(self, L0, ds, N, M, W=3, H=1):
        self.points=["NAME:PolylinePoints"]
        self.segments=["NAME:PolylineSegments"]
        self.index=0
        
        dL=ds/factor(L0,N)
        
        for x, y in trace(L0, dL, N, M):
            self.setPoint(x,y)
        
        self.create(W, H)
        
    def setPoint(self, x, y):
        self.points.append(["NAME:PLPoint","X:=","{}mm".format(x),"Y:=", "{}mm".format(y),"Z:=", "0mm"])
        if self.index is not 0:
            self.segments.append(["NAME:PLSegment","SegmentType:=","Line","StartIndex:=", self.index-1,"NoOfPoints:=",2])
        self.index+=1       
        
    def create(self, width, height):
        oEditor.CreatePolyline(["NAME:PolylineParameters","IsPolylineCovered:=",True,"IsPolylineClosed:=",False, self.points, self.segments,["NAME:PolylineXSection","XSectionType:=","Rectangle","XSectionOrient:=","Auto","XSectionWidth:=","{}mm".format(width),"XSectionTopWidth:=","0mm","XSectionHeight:=","{}mm".format(height),"XSectionNumSegments:=","0","XSectionBendType:=","Corner"]],["NAME:Attributes","Name:=","Polyline1","Flags:=","","Color:=","(96 211 244)","Transparency:=",0.5,"PartCoordinateSystem:=","Global","UDMId:=","","MaterialValue:=","\"copper\"","SurfaceMaterialValue:=","\"\"","SolveInside:=",False,"IsMaterialEditable:=",True,"UseMaterialAppearance:=",False,"IsLightweight:=",False])
        
createSpiral(10, 4, 5, 24, 3, 1)
oEditor.FitAll()