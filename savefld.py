import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.GetActiveProject()
oDesign = oProject.GetActiveDesign()
oEditor = oDesign.SetActiveEditor("3D Modeler")

def getBoundaryofSheet(rect):
    fid=oEditor.GetFaceIDsOfSheet(rect)

    vid=oEditor.GetVertexIDsFromFace(fid[0])
    pos=[oEditor.GetVertexPosition(i) for i in vid]
    x,y,z=zip(*pos)
    x=[float(i) for i in x]
    y=[float(i) for i in y]
    z=[float(i) for i in z]
    
    boundary=([min(x), min(y), min(z)],[max(x), max(y), max(z)])
    return boundary

def getBoundaryofBox(obj):
    vid=oEditor.GetVertexIDsFromObject(obj)

    pos=[oEditor.GetVertexPosition(i) for i in vid]
    x,y,z=zip(*pos)
    x=[float(i) for i in x]
    y=[float(i) for i in y]
    z=[float(i) for i in z]
    
    boundary=([min(x), min(y), min(z)],[max(x), max(y), max(z)])
    return boundary

def savefld(solution, freq, boundary, fld_file, resolution=(1,1,1)):
    unit=oEditor.GetModelUnits()

    range_min=['{}{}'.format(i, unit) for i in boundary[0]]
    range_max=['{}{}'.format(i, unit) for i in boundary[1]]
    res=['{}{}'.format(i, unit) for i in resolution]
    
    oModule = oDesign.GetModule("FieldsReporter")
    oModule.ExportOnGrid(fld_file, range_min, range_max, res, solution, ["Freq:=", freq, "Phase:=", "0deg"], True, "Cartesian",["0mm","0mm","0mm"],False)

#b1=getBoundaryofBox('Box1')
#AddWarningMessage(str(b1))
#savefld('Setup1:LastAdaptive', '2500000000', b1, 'd:/demo/box1.fld',(2,2,2))

#b2=getBoundaryofSheet('Rectangle1')
#AddWarningMessage(str(b2))
#savefld('Setup1:LastAdaptive', '2500000000', b2, 'd:/demo/sheet.fld',(1,1,1))