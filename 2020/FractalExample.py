# ----------------------------------------------
# Script Recorded by ANSYS Electronics Desktop Version 2020.1.0
# 19:45:19  Apr 23, 2020
# ----------------------------------------------
import ScriptEnv
from math import sin, cos, pi
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.GetActiveProject()
oDesign = oProject.GetActiveDesign()
oEditor = oDesign.SetActiveEditor("3D Modeler")

r=1
unit='mm'
n=3

models=[]
def triangle(x,y,r):
    name=oEditor.CreateRegularPolygon(
        [
            "NAME:RegularPolygonParameters",
            "IsCovered:="		, True,
            "XCenter:="		, "{}{}".format(x, unit),
            "YCenter:="		, "{}{}".format(y, unit),
            "ZCenter:="		, "0mm",
            "XStart:="		, "{}{}".format(x+r, unit),
            "YStart:="		, "{}{}".format(y, unit),
            "ZStart:="		, "0mm",
            "NumSides:="		, "3",
            "WhichAxis:="		, "Z"
        ], 
        [
            "NAME:Attributes",
            "Name:="		, "Polygon1",
            "Flags:="		, "",
            "Color:="		, "(255 128 0)",
            "Transparency:="	, 0,
            "PartCoordinateSystem:=", "Global",
            "UDMId:="		, "",
            "MaterialValue:="	, "\"copper\"",
            "SurfaceMaterialValue:=", "\"\"",
            "SolveInside:="		, True,
            "IsMaterialEditable:="	, True,
            "UseMaterialAppearance:=", False,
            "IsLightweight:="	, False
        ])

    return name


def fractal(n, x, y, r):
    global models
    if n == 0:
        models.append(triangle(x, y, r))
    else:
        fractal(n-1, x-r*cos(0*pi/3), y-r*sin(0*pi/3), r/2)
        fractal(n-1, x-r*cos(2*pi/3), y-r*sin(2*pi/3), r/2)
        fractal(n-1, x-r*cos(4*pi/3), y-r*sin(4*pi/3), r/2)
        models.append(triangle(x, y, r))
        
    
triangle(0,0,-r)
fractal(n,0,0,r/2)

tool = ','.join(models)
AddWarningMessage(tool)

oEditor.Subtract(
	[
		"NAME:Selections",
		"Blank Parts:="		, "Polygon1",
		"Tool Parts:="		, tool
	], 
	[
		"NAME:SubtractParameters",
		"KeepOriginals:="	, False
	])     