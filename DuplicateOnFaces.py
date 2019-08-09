import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.GetActiveProject()
oDesign = oProject.GetActiveDesign()
oEditor = oDesign.SetActiveEditor("3D Modeler")

objs=oEditor.GetSelections()

fcs=[]

for i in range (1,len(objs),1) :
    oFaceIDs = oEditor.GetFaceIDs(str(objs[i]))
    oVertexIDs = oEditor.GetVertexIDsFromFace(str(oFaceIDs[0]))
    oEditor.CreateFaceCS(["NAME:FaceCSParameters",["NAME:Origin","IsAttachedToEntity:=",True,"EntityID:=",int(oFaceIDs[0]),"FacetedBodyTriangleIndex:=",-1,"TriangleVertexIndex:=",-1,"PositionType:=","FaceCenter","UParam:=",0,"VParam:=",0,"XPosition:=","0","YPosition:=","0","ZPosition:=","0"],"MoveToEnd:=",False,"FaceID:=",int(oFaceIDs[0]),["NAME:AxisPosn","IsAttachedToEntity:=",True,"EntityID:=",int(oVertexIDs[0]),"FacetedBodyTriangleIndex:=",-1,"TriangleVertexIndex:=",-1,"PositionType:=","OnVertex","UParam:=",0,"VParam:=",0,"XPosition:=","0","YPosition:=","0","ZPosition:=","0"],"WhichAxis:=","X"],["NAME:Attributes","Name:=","FaceCS"+objs[i],"PartName:=",objs[i]])
    fcs.append("FaceCS"+objs[i])

for j in fcs:
    oEditor.Copy(["NAME:Selections","Selections:=",str(objs[0])])
    oEditor.SetWCS(["NAME:SetWCSParameter","Working Coordinate System:=",j,"RegionDepCSOk:=",False])
    oEditor.Paste()
