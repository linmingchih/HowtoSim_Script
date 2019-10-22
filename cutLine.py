import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.GetActiveProject()
oDesign = oProject.GetActiveDesign()
oEditor = oDesign.SetActiveEditor("3D Modeler")
unit=oEditor.GetModelUnits()

def func(edge):
    p0, p1=edge
    x0, y0, z0=map(float,p0)
    x1, y1, z1=map(float,p1)
    p=((x0+x1)/2, (y0+y1)/2, (z0+z1)/2)
    v=((x1-x0),(y1-y0),(z1-z0))
    return (p,v)

def getAll():
    objs=[]
    totalobjects = oEditor.GetNumObjects()
    for i in range(totalobjects):
        objs.append(oEditor.GetObjectName(i))
    return objs

edges=oEditor.GetSelections()
AddWarningMessage(str(edges))
edge_vertex=[oEditor.GetVertexIDsFromEdge(float(i[4:])) for i in edges] 
vertex_location=[(oEditor.GetVertexPosition(i),oEditor.GetVertexPosition(j)) for i,j in edge_vertex]

for p, v in map(func, vertex_location):
    old_name=oDesign.GetName()
    oProject.CopyDesign(old_name)
    oProject.Paste()
    oDesign=oProject.GetActiveDesign()
    new_name=oDesign.GetName()

    oDesign=oProject.SetActiveDesign(old_name)
    oEditor = oDesign.SetActiveEditor("3D Modeler")
    oEditor.SetWCS(
        [
            "NAME:SetWCS Parameter",
            "Working Coordinate System:=", "Global",
            "RegionDepCSOk:="	, False
        ])
    oEditor.CreateRelativeCS(
        [
            "NAME:RelativeCSParameters",
            "Mode:="		, "Axis/Position",
            "OriginX:="		, "{}{}".format(p[0],unit),
            "OriginY:="		, "{}{}".format(p[1],unit),
            "OriginZ:="		, "{}{}".format(p[2],unit),
            "XAxisXvec:="		, "{}{}".format(v[0],unit),
            "XAxisYvec:="		, "{}{}".format(v[1],unit),
            "XAxisZvec:="		, "{}{}".format(v[2],unit),
            "YAxisXvec:="		, "0mm",
            "YAxisYvec:="		, "0mm",
            "YAxisZvec:="		, "1mm"
        ], 
        [
            "NAME:Attributes",
            "Name:="		, "cutCS"
        ])

    oEditor.Split(
        [
            "NAME:Selections",
            "Selections:="		,','.join(getAll()),
            "NewPartsModelFlag:="	, "Model"
        ], 
        [
            "NAME:SplitToParameters",
            "SplitPlane:="		, "YZ",
            "WhichSide:="		, "NegativeOnly",
            "ToolType:="		, "PlaneTool",
            "ToolEntityID:="	, -1,
            "SplitCrossingObjectsOnly:=", False,
            "DeleteInvalidObjects:=", True
        ])
    #-------------------


    oDesign=oProject.SetActiveDesign(new_name)
    oEditor = oDesign.SetActiveEditor("3D Modeler")    
    oEditor.SetWCS(
        [
            "NAME:SetWCS Parameter",
            "Working Coordinate System:=", "Global",
            "RegionDepCSOk:="	, False
        ])
    oEditor.CreateRelativeCS(
        [
            "NAME:RelativeCSParameters",
            "Mode:="		, "Axis/Position",
            "OriginX:="		, "{}{}".format(p[0],unit),
            "OriginY:="		, "{}{}".format(p[1],unit),
            "OriginZ:="		, "{}{}".format(p[2],unit),
            "XAxisXvec:="		, "{}{}".format(v[0],unit),
            "XAxisYvec:="		, "{}{}".format(v[1],unit),
            "XAxisZvec:="		, "{}{}".format(v[2],unit),
            "YAxisXvec:="		, "0mm",
            "YAxisYvec:="		, "0mm",
            "YAxisZvec:="		, "1mm"
        ], 
        [
            "NAME:Attributes",
            "Name:="		, "cutCS"
        ])

    oEditor.Split(
        [
            "NAME:Selections",
            "Selections:="		,','.join(getAll()),
            "NewPartsModelFlag:="	, "Model"
        ], 
        [
            "NAME:SplitToParameters",
            "SplitPlane:="		, "YZ",
            "WhichSide:="		, "PositiveOnly",
            "ToolType:="		, "PlaneTool",
            "ToolEntityID:="	, -1,
            "SplitCrossingObjectsOnly:=", False,
            "DeleteInvalidObjects:=", True
        ])    
    #---------------------------------
