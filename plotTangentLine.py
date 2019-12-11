import math
import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.GetActiveProject()
oDesign = oProject.GetActiveDesign()
oEditor = oDesign.SetActiveEditor("3D Modeler")
unit=oEditor.GetModelUnits()

def createline(pt0, pt1):
    oEditor.CreatePolyline(
        [
            "NAME:PolylineParameters",
            "IsPolylineCovered:="	, True,
            "IsPolylineClosed:="	, False,
            [
                "NAME:PolylinePoints",
                [
                    "NAME:PLPoint",
                    "X:="			, "{}{}".format(pt0[0], unit),
                    "Y:="			, "{}{}".format(pt0[1], unit),
                    "Z:="			, "{}{}".format(pt0[2], unit)
                ],
                [
                    "NAME:PLPoint",
                    "X:="			, "{}{}".format(pt1[0], unit),
                    "Y:="			, "{}{}".format(pt1[1], unit),
                    "Z:="			, "{}{}".format(pt1[2], unit)
                ]
            ],
            [
                "NAME:PolylineSegments",
                [
                    "NAME:PLSegment",
                    "SegmentType:="		, "Line",
                    "StartIndex:="		, 0,
                    "NoOfPoints:="		, 2
                ]
            ],
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
            "Name:="		, "Polyline2",
            "Flags:="		, "",
            "Color:="		, "(255 0 0)",
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



sel=oEditor.GetSelections()
pt_ID=sel[1][6:]
AddWarningMessage('pt_ID:{}'.format(pt_ID))

pt_position=oEditor.GetVertexPosition(pt_ID)
x0, y0, z0=map(float, pt_position)

face_ID=sel[0][4:]
AddWarningMessage('face_ID:{}'.format(face_ID))
positions_on_face=[]

for i in oEditor.GetVertexIDsFromFace(face_ID):
    position = oEditor.GetVertexPosition(i)
  
    positions_on_face+=[map(float, position)]


def calculate_angle(v1, v2):
    a=(v1[0]*v2[0]+v1[1]*v2[1]+v1[2]*v2[2])
    b1=abs(math.sqrt(v1[0]*v1[0]+v1[1]*v1[1]+v1[2]*v1[2]))
    b2=abs(math.sqrt(v2[0]*v2[0]+v2[1]*v2[1]+v2[2]*v2[2]))

    return abs(a/(b1*b2))

angle=[]
for n in range(len(positions_on_face)-1):
    x1, y1, z1=positions_on_face[n]
    x2, y2, z2=positions_on_face[n+1]
    v1=(x1-x0, y1-y0, z1-z0)
    v2=(x2-x1, y2-y1, z2-z1)
    angle+=[(calculate_angle(v1, v2), n, x1, y1, z1)]

angle.sort()
angle=angle[::-1]
ptA=angle[0]
for i in angle[1:]:
    if abs(i[1]-ptA[1])<3:
        continue
    else:
        ptB=i
        break

createline(pt_position, ptA[2:])
createline(pt_position, ptB[2:])

