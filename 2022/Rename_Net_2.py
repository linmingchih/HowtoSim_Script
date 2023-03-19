import json, os
from collections import defaultdict

# from win32com import client
# oApp = client.Dispatch("Ansoft.ElectronicsDesktop.2022.2")
# oDesktop = oApp.GetAppDesktop()
# oDesktop.RestoreWindow()

oDesktop.ClearMessages("","",2)
oProject = oDesktop.GetActiveProject()
oDesign = oProject.GetActiveDesign()
oEditor = oDesign.SetActiveEditor("3D Modeler")
os.chdir(os.path.dirname(__file__))

unit = oEditor.GetModelUnits()
unit_map = {'nm':1e-9, 'um':1e-6, 'mm':1e-3, 'mil':2.54e-5}
scale = unit_map[unit]


with open('rename.json') as f:
    layer_info, db = json.load(f)

result = defaultdict(list)
obj_net = defaultdict(set)

for layer in db:
    z = layer_info[layer]
    for obj in db[layer]:
        x, y, net, otype = obj
        names = oEditor.GetBodyNamesByPosition(["NAME:Parameters", 
                                                "XPosition:=","{:.6f}{}".format(x/scale, unit), 
                                                "YPosition:=","{:.6f}{}".format(y/scale, unit), 
                                                "ZPosition:=","{:.6f}{}".format(z/scale, unit)
                                                ])

        for name in names:
            result[net].append(name)
            obj_net[name].add(net)

new_result = defaultdict(list)
for net, names in result.items():
    for name in names:
        if len(obj_net[name]) == 1:
            new_result[net].append(name)


total = len(new_result)
#%%

n = 0
for net in new_result:
    oDesktop.ClearMessages("","",2)
    n+=1
    oDesktop.AddMessage(oProject.GetName(), oDesign.GetName(),0,'{}/{}'.format(n,total))
    
    try:
        oEditor.ChangeProperty(
            [
                "NAME:AllTabs",
                [
                    "NAME:Geometry3DAttributeTab",
                    [
                        "NAME:PropServers"                    
                    ] + new_result[net],
                    [
                        "NAME:ChangedProps",
                        [
                            "NAME:Name",
                            "Value:="		, net.replace('<', '_').replace('>', '_').replace('-', '_')
                        ]
                    ]
                ]
            ])
    except:
        pass


oDesktop.AddMessage(oProject.GetName(), oDesign.GetName(),0,'Completed!')