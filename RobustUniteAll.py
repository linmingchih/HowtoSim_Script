'''
This script will sort size of models and then do Unite operation. It is more robust compared to default Unite Operation in HFSS2019U2
'''
import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.GetActiveProject()
oDesign = oProject.GetActiveDesign()
oEditor = oDesign.SetActiveEditor("3D Modeler")

def getsortedObjects():
    totalobjects = oEditor.GetNumObjects()
    data=[]
    for i in range(totalobjects):
        objectname = oEditor.GetObjectName(i)
        faces=oEditor.GetFaceIDs(objectname)
        area=0
        for j in faces:
            area+=float(oEditor.GetFaceArea(j))
        data.append((objectname, area))
    return sorted(data, key=lambda tup: tup[1])[::-1]


totalobjects =','.join([i for i,j in getsortedObjects()])


oEditor.Unite(
    [
        "NAME:Selections",
        "Selections:="		, totalobjects
    ], 
    [
        "NAME:UniteParameters",
        "KeepOriginals:="	, False
    ])

