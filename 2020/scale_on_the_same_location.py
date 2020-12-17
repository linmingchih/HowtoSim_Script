oProject = oDesktop.GetActiveProject()
oDesign = oProject.GetActiveDesign()
oEditor = oDesign.SetActiveEditor("3D Modeler")
unit = oEditor.GetModelUnits()
scale = 1.25

def draw(points):
    pts = []
    segs = []
    n = 0
    for x, y, z in points:    
        pts.append([
                        "NAME:PLPoint",
                        "X:="			, "{}{}".format(x, unit),
                        "Y:="			, "{}{}".format(y, unit),
                        "Z:="			, "{}{}".format(z, unit)
                    ])
        segs.append([
                        "NAME:PLSegment",
                        "SegmentType:="		, "Line",
                        "StartIndex:="		, n,
                        "NoOfPoints:="		, 2
                    ])
        n += 1
        
    oEditor.CreatePolyline(
        [
            "NAME:PolylineParameters",
            "IsPolylineCovered:="	, True,
            "IsPolylineClosed:="	, True,
            [
                "NAME:PolylinePoints",

            ] + pts ,
            [
                "NAME:PolylineSegments",

            ] + segs,
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
            "Name:="		, "Polyline1",
            "Flags:="		, "",
            "Color:="		, "(143 175 143)",
            "Transparency:="	, 0,
            "PartCoordinateSystem:=", "Global",
            "UDMId:="		, "",
            "MaterialValue:="	, "\"copper\"",
            "SurfaceMaterialValue:=", "\"\"",
            "SolveInside:="		, False,
            "ShellElement:="	, False,
            "ShellElementThickness:=", "0mm",
            "IsMaterialEditable:="	, True,
            "UseMaterialAppearance:=", False,
            "IsLightweight:="	, False
        ])


for obj in oEditor.GetSelections():
    x_list = []
    y_list = []
    z_list = []
    for v in oEditor.GetVertexIDsFromObject(obj):
        x, y, z = oEditor.GetVertexPosition(v)
        x_list.append(float(x))
        y_list.append(float(y))
        z_list.append(float(z))
    AddWarningMessage(str(x_list))
    x0, y0, z0 = (sum(x_list)/len(x_list), sum(y_list)/len(y_list), sum(z_list)/len(z_list))
    
    line = []
    for x, y, z in zip(x_list, y_list, z_list):
        line.append(((x - x0)*scale + x0,
                     (y - y0)*scale + y0,
                     (z - z0)*scale + z0))
    AddWarningMessage(str(line))
    try:
        draw(line)
    except:
        pass
    