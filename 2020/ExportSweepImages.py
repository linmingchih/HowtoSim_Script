# ----------------------------------------------
# Script Recorded by ANSYS Electronics Desktop Version 2020.1.0
# 14:13:54  Apr 25, 2020
# ----------------------------------------------
import ScriptEnv
import time
from itertools import product
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.GetActiveProject()
oDesign = oProject.GetActiveDesign()
oEditor = oDesign.SetActiveEditor("3D Modeler")

inbox='''
tw1:["0.2mm","0.3mm","0.4mm"]
tw2:["0.2mm","0.3mm","0.4mm"]
ay:["1.5mm","1.7mm","1.9mm"]
gap:["0.18mm","0.2mm"]
'''
path='d:/demo'

def sweeplist(inbox):
    data = {}
    for i in inbox.splitlines():
        try:
            x, y = i.strip().split(':')
            data[x.strip()] = eval(y.strip())
        except:
            pass
        
    result=(dict(zip(data.keys(), values)) for values in product(*data.values()))
    return list(result)

slist = sweeplist(inbox)
#AddWarningMessage(str(slist))

for i in slist:
    AddWarningMessage(str(i))
    for key in i:
        oDesign.ChangeProperty(
            [
                "NAME:AllTabs",
                [
                    "NAME:LocalVariableTab",
                    [
                        "NAME:PropServers", 
                        "LocalVariables"
                    ],
                    [
                        "NAME:ChangedProps",
                        [
                            "NAME:{}".format(key),
                            "Value:="		, "{}".format(i[key])
                        ]
                    ]
                ]
            ])
    oDesktop.RefreshJobMonitor()
    oEditor.FitAll()
    pngname=str(i).replace('{','').replace('}','').replace(':','=')
    oEditor.ExportModelImageToFile(
    '{}/{}.png'.format(path, pngname),
    0,
    0,
    [   "NAME:SaveImageParams",
        "ShowAxis:=" , "True",
        "ShowGrid:=" , "True",
        "ShowRuler:=" , "True",
        "ShowRegion:=" , "Default",
        "Selections:=" , ""
        "Orientation:=" , "Trimetric"])