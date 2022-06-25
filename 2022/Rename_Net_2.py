# ----------------------------------------------
# Script Recorded by ANSYS Electronics Desktop Version 2021.1.0
# 14:33:37  Apr 16, 2021
# ----------------------------------------------
import json, os
import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oDesktop.ClearMessages("","",2)
oProject = oDesktop.GetActiveProject()
oDesign = oProject.GetActiveDesign()
oEditor = oDesign.SetActiveEditor("3D Modeler")
os.chdir(os.path.dirname(__file__))
unit = oEditor.GetModelUnits()
with open('rename.json') as f:
    layer_info, db = json.load(f)

result = {}
for layer in db:
    z = layer_info[layer]
    for obj in db[layer]:
        x, y, net, otype = obj
        if net not in result:
            result[net] = []
        names = oEditor.GetBodyNamesByPosition(["NAME:Parameters", 
                                                "XPosition:=","{}{}".format(x, unit), 
                                                "YPosition:=","{}{}".format(y, unit), 
                                                "ZPosition:=","{}{}".format(z, unit)
                                                ])
        for name in names:
            if 'fill' in name or 'airbox' in name:
                continue
            if name not in result[net]:
                result[net].append(name)
total = len(result)
n = 0
for net in result:
    oDesktop.ClearMessages("","",2)
    n+=1
    oDesktop.AddMessage(oProject.GetName(), oDesign.GetName(),0,'{}/{}'.format(n,total))
    
    oEditor.ChangeProperty(
        [
            "NAME:AllTabs",
            [
                "NAME:Geometry3DAttributeTab",
                [
                    "NAME:PropServers"                    
                ] + result[net],
                [
                    "NAME:ChangedProps",
                    [
                        "NAME:Name",
                        "Value:="		, net.replace('<', '_').replace('>', '_')
                    ]
                ]
            ]
        ])

oDesktop.AddMessage(oProject.GetName(), oDesign.GetName(),0,'Completed!')
