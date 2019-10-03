import json
import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.GetActiveProject()
oDesign = oProject.GetActiveDesign()
oEditor = oDesign.SetActiveEditor("Layout")

stackup=[]
objs=[]
stackup.append(('layers',len(oEditor.GetStackupLayerNames())))
stackup.append(('nets',len(oEditor.GetNets())))

types=['bondwire','pin', 'via', 'rect', 'arc', 'line', 'poly', 'plg', 'circle void', 'line void','rect void', 'poly void', 'plg void', 'text', 'cell', 'Measurement', 'Port', 'Port Instance', 'Port','Instance Port', 'Edge Port', 'component', 'CS', 'S3D']

total=0
for t in types:
    num=len(oEditor.FindObjects('Type', t))
    objs.append((t,num))
    total+=num
    

oDesktop.ClearMessages('','',2)
objs.sort(key=lambda tup: tup[1])

for i,j in stackup[::-1]:
    if j>0:
        AddInfoMessage('{}: {}'.format(i,j))
AddInfoMessage('*'*10+'Objects Count'+'*'*10)

for i,j in objs[::-1]:
    if j>0:
        AddInfoMessage('{}: {}'.format(i,j))
AddInfoMessage('*'*30)

AddWarningMessage('Objects Total: {}'.format(total))


