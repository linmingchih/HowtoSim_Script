solution = "Setup1 : LastAdaptive"
freq = "5GHz"

#------------------------------------------------------------------------------
# Code Begining
#------------------------------------------------------------------------------
import os
os.chdir(os.path.dirname(__file__))

import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oDesktop.ClearMessages("", "", 2)
oProject = oDesktop.GetActiveProject()
oDesign = oProject.GetActiveDesign()
oEditor = oDesign.SetActiveEditor("3D Modeler")

unit = oEditor.GetModelUnits()

def drawPlane(name, xyz_list):
    points = []
    for x, y, z in xyz_list:
        x , y, z = str(x) + unit, str(y) + unit, str(z) + unit
        points.append(["NAME:PLPoint", "X:=", x, "Y:=", y, "Z:=", z])
    points.append(points[0])
    
    segments = [["NAME:PLSegment", "SegmentType:=", "Line",	"StartIndex:=", i,"NoOfPoints:=", 2] for i in range(len(xyz_list))]

    return oEditor.CreatePolyline(
        [
            "NAME:PolylineParameters",
            "IsPolylineCovered:="	, True,
            "IsPolylineClosed:="	, True,
            [
                "NAME:PolylinePoints",
            ] + points,
            [
                "NAME:PolylineSegments",
            ] + segments,
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
            "Flags:="		, "NonModel#",
            "Color:="		, "(143 175 143)",
            "Transparency:="	, 0.9,
            "PartCoordinateSystem:=", "Global",
            "UDMId:="		, "",
            "MaterialValue:="	, "\"vacuum\"",
            "SurfaceMaterialValue:=", "\"\"",
            "SolveInside:="		, True,
            "ShellElement:="	, False,
            "ShellElementThickness:=", "0mm",
            "IsMaterialEditable:="	, True,
            "UseMaterialAppearance:=", False,
            "IsLightweight:="	, False
        ])

def getRadiatedPower(plane_name):
    oModule = oDesign.GetModule("FieldsReporter")
    oModule.CalcStack("clear")
    oModule.EnterQty("Poynting")
    oModule.CalcOp("Real")
    oModule.EnterSurf(plane_name)
    oModule.CalcOp("NormalComponent")
    oModule.CalcOp("Integrate")
    oModule.ClcEval(solution, 
        [
            "Freq:="		, freq,
            "Phase:="		, "0deg"
        ], "Fields")
    oModule.CalculatorWrite("./temp.fld", 
        [
            "Solution:="		, solution
        ], 
        [
            "Freq:="		, freq,
            "Phase:="		, "0deg"
        ])
    oModule.CalcStack("clear")
    with open("./temp.fld") as f:
        return f.readlines()[1]

total_power = 0
faces = []
for n, face in enumerate(oEditor.GetSelections(), 1):
    z = [oEditor.GetVertexPosition(v) for v in oEditor.GetVertexIDsFromFace(face[4:])]   
    name = drawPlane('face_{}'.format(n), z)
    power = float(getRadiatedPower(name))
    total_power += power
    AddWarningMessage('{}: {}W'.format(name, power))
    faces.append(name)

oEditor.Delete(
[
    "NAME:Selections",
    "Selections:="		, ','.join(faces)
])

AddWarningMessage('Total Radiated Power: {}W'.format(total_power))
