# ----------------------------------------------
# Script Recorded by ANSYS Electronics Desktop Version 2021.1.0
# 13:27:00  Apr 16, 2021
# ----------------------------------------------
import ScriptEnv
import json, os
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oDesktop.ClearMessages("","",2)
oProject = oDesktop.GetActiveProject()
oDesign = oProject.GetActiveDesign()
oEditor = oDesign.SetActiveEditor("Layout")
os.chdir(os.path.dirname(__file__))
db = {}
layerinfo = {}
for layer in oEditor.GetStackupLayerNames():
    info = oEditor.GetLayerInfo(layer)
    if 'Type: signal' in info:
        lower_elevation = info[-1].split(':')[-1].strip()
        try:
            x = float(lower_elevation[:-2])
        except:
            x = float(lower_elevation[:-3])
        layerinfo[layer] = x
        db[layer] = []
    else:
        continue
    
    for i in oEditor.FindObjects('Layer', layer):
        otype = oEditor.GetPropertyValue('BaseElementTab', i, 'Type')
        if otype in ['Pin', 'Via']:
            location = oEditor.GetPropertyValue('BaseElementTab', i, 'Location')
        elif otype in ['line', 'poly']:
            location = oEditor.GetPropertyValue('BaseElementTab', i, 'Pt0')
        else:
            continue
        
        x, y = [float(j) for j in location.split(',')]
        net = oEditor.GetPropertyValue('BaseElementTab', i, 'Net')
        db[layer].append((x, y, net, otype))

with open('rename.json', 'w') as f:
    json.dump((layerinfo, db), f, indent=4)
    AddWarningMessage('Completed!')