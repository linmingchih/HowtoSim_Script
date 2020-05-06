# ----------------------------------------------
# Script Recorded by ANSYS Electronics Desktop Version 2020.1.0
# 14:23:14  May 06, 2020
# ----------------------------------------------
import ScriptEnv
from math import pi, cos, sin
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.GetActiveProject()
oDesign = oProject.GetActiveDesign()
oEditor = oDesign.SetActiveEditor("3D Modeler")

N = 10
unit = 'mm'
x0, y0 = 0, 0
length = 10
angle = 30
width = 0.5
height = 0.2

def segment(N):
    result = []
    for i in range(N):
        result.append([
            "NAME:PLSegment",
            "SegmentType:="		, "Line",
            "StartIndex:="		, i,
            "NoOfPoints:="		, 2
        ])
    return result

def pts(N, length, angle):
    x, y, z = x0, y0, 0
    theta=angle*2*pi/360
    result=[]
    for i in range(N+1):
        result.append([
				"NAME:PLPoint",
				"X:="			, "{}{}".format(x, unit),
				"Y:="			, "{}{}".format(y, unit),
				"Z:="			, "{}{}".format(z, unit)
			])
        x+=length*cos(theta)
        y+=length*sin(theta)
        theta*=-1
    return result
    

oEditor.CreatePolyline(
	[
		"NAME:PolylineParameters",
		"IsPolylineCovered:="	, True,
		"IsPolylineClosed:="	, False,
		[
			"NAME:PolylinePoints"
		] + pts(N, length, angle),
		[
			"NAME:PolylineSegments",

		] + segment(N),
		[
			"NAME:PolylineXSection",
			"XSectionType:="	, "Rectangle",
			"XSectionOrient:="	, "Auto",
			"XSectionWidth:="	, "{}{}".format(width, unit),
			"XSectionTopWidth:="	, "{}{}".format(width, unit),
			"XSectionHeight:="	, "{}{}".format(height, unit),
			"XSectionNumSegments:="	, "0",
			"XSectionBendType:="	, "Corner"
		]
	], 
	[
		"NAME:Attributes",
		"Name:="		, "Polyline1",
		"Flags:="		, "",
		"Color:="		, "(255 175 143)",
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


