import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.GetActiveProject()
oDesign = oProject.GetActiveDesign()
oEditor = oDesign.SetActiveEditor("3D Modeler")
unit=oEditor.GetModelUnits()

loc=[]
with open('d:/demo/location.csv') as f:
    for line in f.readlines():
        loc.append(line.strip().split(','))

sel=oEditor.GetSelections()
for x,y,z in loc:        
    oEditor.Copy(
        [
            "NAME:Selections",
            "Selections:="		, ','.join(sel)
        ])
    modulename=oEditor.Paste()
    oEditor.Move(
        [
            "NAME:Selections",
            "Selections:="		, ','.join(modulename),
            "NewPartsModelFlag:="	, "Model"
        ], 
        [
            "NAME:TranslateParameters",
            "TranslateVectorX:="	, x+unit,
            "TranslateVectorY:="	, y+unit,
            "TranslateVectorZ:="	, z+unit
        ])
