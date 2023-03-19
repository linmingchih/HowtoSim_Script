# from win32com import client
# oApp = client.Dispatch("Ansoft.ElectronicsDesktop.2022.2")
# oDesktop = oApp.GetAppDesktop()
# oDesktop.RestoreWindow()
# AddWarningMessage = print


import json, os

oDesktop.ClearMessages("","",2)
oProject = oDesktop.GetActiveProject()
oDesign = oProject.GetActiveDesign()
oEditor = oDesign.SetActiveEditor("Layout")
folder = os.chdir(os.path.dirname(__file__))
folder = r'D:\OneDrive - ANSYS, Inc\Customer2023\2023_03_19_vianexech_renaming'

unit_map = {'nm':1e-9, 'um':1e-6, 'mm':1e-3, 'mil':2.54e-5}
scale = unit_map[oEditor.GetActiveUnits()]

db = {}
layerinfo = {}
for layer in oEditor.GetStackupLayerNames():
    info = oEditor.GetLayerInfo(layer)
    if 'Type: signal' in info:
        lower_elevation = info[-1].split(':')[-1].strip()
        try:
            value = lower_elevation[:-2]
            unit = lower_elevation[-2:]
            x = float(value)*unit_map[unit]
        except:
            value = lower_elevation[:-3]
            unit = lower_elevation[-3:]
            x = float(value)*unit_map[unit]
        
        layerinfo[layer] = x
        db[layer] = []
    else:
        continue
    
    for i in oEditor.FindObjects('Layer', layer):
        otype = oEditor.GetPropertyValue('BaseElementTab', i, 'Type')
        if otype in ['Pin', 'Via']:
            location = oEditor.GetPropertyValue('BaseElementTab', i, 'Location')
        elif otype in ['line', 'poly']:
            location = oEditor.GetPropertyValue('BaseElementTab', i, 'Pt1')
        else:
            continue
        
        x, y = [float(j)*scale for j in location.split(',')]
        net = oEditor.GetPropertyValue('BaseElementTab', i, 'Net')
        db[layer].append((x, y, net, otype))

with open(os.path.join(folder, 'rename.json'), 'w') as f:
    json.dump((layerinfo, db), f, indent=4)
    AddWarningMessage('Completed!')