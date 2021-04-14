# ----------------------------------------------
# Script Recorded by ANSYS Electronics Desktop Version 2021.1.0
# 1:55:23  Apr 15, 2021
# mingchih.lin@ansys.com
# ----------------------------------------------
import sys
import clr
clr.AddReference("System.Windows.Forms")

from System.Windows.Forms import DialogResult, OpenFileDialog
dialog = OpenFileDialog()
dialog.Title = 'Select CAD(.sat) File'
dialog.Filter = "sat files (*.sat)|*.sat"

if dialog.ShowDialog() == DialogResult.OK:
    sat_path = dialog.FileName
else:
    pass

import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oDesktop.ClearMessages("","",2)
oProject = oDesktop.GetActiveProject()
oProject.Save()
oDesign = oProject.GetActiveDesign()
design_name = oDesign.GetName()
oEditor = oDesign.SetActiveEditor("3D Modeler")

def getMaterial():
    result = {}
    for i in range(oEditor.GetNumObjects()):
        name = oEditor.GetObjectName(i)
        material = oEditor.GetPropertyValue('Geometry3DAttributeTab', name, 'Material').replace('"', '')
        color = oEditor.GetPropertyValue('Geometry3DAttributeTab', name, 'Color')
        result[name] = (material, color)
    return result

x = getMaterial()
def changeMaterial(name, material, color_code):
    oEditor.ChangeProperty(
        [
            "NAME:AllTabs",
            [
                "NAME:Geometry3DAttributeTab",
                [
                    "NAME:PropServers", 
                    name
                ],
                [
                    "NAME:ChangedProps",
                    [
                        "NAME:Material",
                        "Value:="		, "\"{}\"".format(material)
                    ]              
                ]
            ]
        ])
        
    code = int(color_code)
    R= code % 256
    G = ((code - R) % (256**2)) / 256
    B = (code - R - 256*G) / 256**2

    oEditor.ChangeProperty(
       [
          "NAME:AllTabs",
          [
             "NAME:Geometry3DAttributeTab",
             [
                "NAME:PropServers",
                name
             ],
             [
                "NAME:ChangedProps",
                [
                   "NAME:Color",
                   "R:="        , R,
                   "G:="        , G,
                   "B:="        , B
                ]
             ]
          ]
       ])
       
 
import re
m = re.search('(\d+)$', design_name)
if m:
    N = int(m.group(1))
else:
    N = 0

existing_designs = [i.GetName() for i in oProject.GetDesigns()]
new_design_name = re.sub('(\d+)$', str(N+1), design_name)
while new_design_name in existing_designs:
    N += 1
    new_design_name = re.sub('(\d+)$', str(N+1), design_name)

oProject.InsertDesign("HFSS", new_design_name, "DrivenTerminal", "")
AddWarningMessage('{} is created!'.format(new_design_name))

oDesign = oProject.GetActiveDesign()
oEditor = oDesign.SetActiveEditor("3D Modeler")     

oEditor.Import(
	[
		"NAME:NativeBodyParameters",
		"HealOption:="		, 0,
		"Options:="		, "-1",
		"FileType:="		, "UnRecognized",
		"MaxStitchTol:="	, -1,
		"ImportFreeSurfaces:="	, False,
		"GroupByAssembly:="	, False,
		"CreateGroup:="		, False,
		"STLFileUnit:="		, "Auto",
		"MergeFacesAngle:="	, 0.02,
		"HealSTL:="		, False,
		"ReduceSTL:="		, False,
		"ReduceMaxError:="	, 0,
		"ReducePercentage:="	, 100,
		"PointCoincidenceTol:="	, 1E-06,
		"CreateLightweightPart:=", False,
		"ImportMaterialNames:="	, False,
		"SeparateDisjointLumps:=", False,
		"SourceFile:="		, sat_path
	])
    
for name in x:
    try:
        material, color = x[name]
        changeMaterial(name, material, color)
    except:
        pass
