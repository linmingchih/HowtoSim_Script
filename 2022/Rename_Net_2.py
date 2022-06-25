import json, os

# from win32com import client
# oApp = client.Dispatch("Ansoft.ElectronicsDesktop.2022.1")
# oDesktop = oApp.GetAppDesktop()
# oDesktop.RestoreWindow()

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
                                                "XPosition:=","{:.6f}{}".format(x, unit), 
                                                "YPosition:=","{:.6f}{}".format(y, unit), 
                                                "ZPosition:=","{:.6f}{}".format(z, unit)
                                                ])
        for name in names:
            if 'fill' in name or 'airbox' in name or 'UNNAMED' in name:
                continue
            if name not in result[net]:
                result[net].append(name)


total = len(result)
n = 0
for net in result:
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
                    ] + result[net],
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

AddWarningMessage(str(result['GND']))
oDesktop.AddMessage(oProject.GetName(), oDesign.GetName(),0,'Completed!')
