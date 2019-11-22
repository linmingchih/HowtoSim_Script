
import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.GetActiveProject()
oDesign = oProject.GetActiveDesign()
oEditor = oDesign.SetActiveEditor("3D Modeler")
unit=oEditor.GetModelUnits()
def getpts(pts_list):
    pts=[]
    segs=[]
    n=0
    for x, y, z in pts_list:
        _x, _y, _z = str(x)+unit, str(y)+unit, str(z)+unit
        pts.append(["NAME:PLPoint","X:=", _x,"Y:=", _y,"Z:=", _z])
        
    for i in range(len(pts)-1):
        segs.append(["NAME:PLSegment","SegmentType:=","Line","StartIndex:=",i,"NoOfPoints:=",2])
        
    return pts, segs

def create_polyline(pts_list, name):
    pts, segs=getpts(pts_list)

    oEditor.CreatePolyline(
        [
            "NAME:PolylineParameters",
            "IsPolylineCovered:="	, True,
            "IsPolylineClosed:="	, False,
            ["NAME:PolylinePoints"] + pts,
            ["NAME:PolylineSegments"] + segs,
            [
                "NAME:PolylineXSection",
                "XSectionType:="	, "None",
                "XSectionOrient:="	, "Auto",
                "XSectionWidth:="	, "0mm",
                "XSectionTopWidth:="	, "0mm",
                "XSectionHeight:="	, "0mm",
                "XSectionNumSegments:="	, "0",
                "XSectionBendType:="	, "Corner"
            ]
        ], 
        [
            "NAME:Attributes",
            "Name:="		, name,
            "Flags:="		, "",
            "Color:="		, "(157 249 158)",
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

def createspiral(a, b, pitch, sw, st, N):
    pts=[]
    z=0
    for x, y in [(-a, -b), (a, -b), (a, b), (-a, b)]*N:
        pts.append((x, y, z))
        z+=pitch/4
    create_polyline(pts, 'trace1')
    
    pts=[]
    z=sw
    for x, y in [(-a, -b), (a, -b), (a, b), (-a, b)]*N:
        pts.append((x, y, z))
        z+=pitch/4        
    create_polyline(pts, 'trace2')
    
    oEditor.Connect(
        [
            "NAME:Selections",
            "Selections:="		, 'trace1, trace2'
        ])
    oEditor.ThickenSheet(
        [
            "NAME:Selections",
            "Selections:="		, "trace1",
            "NewPartsModelFlag:="	, "Model"
        ], 
        [
            "NAME:SheetThickenParameters",
            "Thickness:="		, str(-st)+unit,
            "BothSides:="		, True
        ])

createspiral(3, 2, 1, 0.5, 0.1, 10)    
    