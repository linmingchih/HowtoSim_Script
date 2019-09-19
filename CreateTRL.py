import re
import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()

oProject = oDesktop.GetActiveProject()
oDesign = oProject.GetActiveDesign()
  
def getMicroStripInfo(netlist):
    
    with open(netlist) as f:
        text=f.read().replace('\n+',' ').splitlines()
    
    sub={}
    for i in text:
        m=re.search('.SUB\s(.*?)\s.*H=(.*) Er=(.*) TAND=(.*) TANM=(.*) MSat=(.*) MRem=(.*) HU=(.*) MET1=(.*) T1=(.*)\)',i)
        if m:
            sub[m.group(1)]={'H':m.group(2), 'Er':m.group(3), 'TanD':m.group(4), 
                'TANM':m.group(5),'MSat':m.group(6),'MRem':m.group(7),'HU':m.group(8),
                'MET1':m.group(9),'T1':m.group(10)}
    trl={}
    for i in text:
        m=re.search('(.*?)\s.*W=(.*) P=(.*) COMPONENT=TRL SUBSTRATE=(.*)',i)
        if m:
            trl[m.group(1)]={'W':m.group(2), 'P':m.group(3),'SUBSTRATE':m.group(4)}
            
    mcpl={}
    for i in text:
        m=re.search('(.*?)\s.*W=(.*) SP=(.*) P=(.*) SUBSTRATE=(.*) NL=2 COMPONENT=mcpl',i)
        if m:
            mcpl[m.group(1)]={'W':m.group(2), 'SP':m.group(3),'P':m.group(4),'SUBSTRATE':m.group(5)}
    
    return {'sub':sub, 'trl':trl, 'mcpl':mcpl}
    
def createtrl(name, trl, sub):
    oProject = oDesktop.NewProject()
    oProject.InsertDesign("HFSS", name, "DrivenModal", "")
    oDesign = oProject.SetActiveDesign(name)
    oEditor = oDesign.SetActiveEditor("3D Modeler")
    
    oDefinitionManager = oProject.GetDefinitionManager()    
    oDefinitionManager.AddMaterial(
        [
            "NAME:sub",
            "CoordinateSystemType:=", "Cartesian",
            "BulkOrSurfaceType:="	, 1,
            [
                "NAME:PhysicsTypes",
                "set:="			, ["Electromagnetic"]
            ],
            "permittivity:="	, sub['Er'],
            "dielectric_loss_tangent:=", sub['TanD']
        ])  
    oEditor.CreateBox(
        [
            "NAME:substrate",
            "XPosition:="		, "0mm",
            "YPosition:="		, "-10*{:.9f}".format(float(trl['W'])/2.0),
            "ZPosition:="		, "0mm",
            "XSize:="		, trl['P'],
            "YSize:="		, "20*{:.9f}".format(float(trl['W'])/2.0),
            "ZSize:="		, '-{}'.format(sub['H'])
        ], 
        [
            "NAME:Attributes",
            "Name:="		, "Box1",
            "Flags:="		, "",
            "Color:="		, "(157 249 158)",
            "Transparency:="	, 0,
            "PartCoordinateSystem:=", "Global",
            "UDMId:="		, "",
            "MaterialValue:="	, "\"sub\"",
            "SurfaceMaterialValue:=", "\"\"",
            "SolveInside:="		, True,
            "IsMaterialEditable:="	, True,
            "UseMaterialAppearance:=", False,
            "IsLightweight:="	, False
        ])


    oDefinitionManager.AddMaterial(
        [
            "NAME:metal",
            "CoordinateSystemType:=", "Cartesian",
            "BulkOrSurfaceType:="	, 1,
            [
                "NAME:PhysicsTypes",
                "set:="			, ["Electromagnetic"]
            ],
            "conductivity:="	, "{}".format(1e8/float(sub['MET1']))
        ])
    oEditor.CreateBox(
        [
            "NAME:BoxParameters",
            "XPosition:="		, "0",
            "YPosition:="		, "-{:.9f}".format(float(trl['W'])/2.0),
            "ZPosition:="		, "0",
            "XSize:="		, trl['P'],
            "YSize:="		, "{:.9f}".format(float(trl['W'])),
            "ZSize:="		, sub['T1']
        ], 
        [
            "NAME:Attributes",
            "Name:="		, "line",
            "Flags:="		, "",
            "Color:="		, "(255 0 128)",
            "Transparency:="	, 0,
            "PartCoordinateSystem:=", "Global",
            "UDMId:="		, "",
            "MaterialValue:="	, "\"metal\"",
            "SurfaceMaterialValue:=", "\"\"",
            "SolveInside:="		, True,
            "IsMaterialEditable:="	, True,
            "UseMaterialAppearance:=", False,
            "IsLightweight:="	, False
        ])
    oEditor.CreateRectangle(
        [
            "NAME:RectangleParameters",
            "IsCovered:="		, True,
            "XStart:="		, "0mm",
            "YStart:="		, "-10*{:.9f}".format(float(trl['W'])/2.0),
            "ZStart:="		, "-{}".format(sub['H']),
            "Width:="		, trl['P'],
            "Height:="		, "20*{:.9f}".format(float(trl['W'])/2.0),
            "WhichAxis:="		, "Z"
        ], 
        [
            "NAME:Attributes",
            "Name:="		, "gnd",
            "Flags:="		, "",
            "Color:="		, "(255 0 128)",
            "Transparency:="	, 0,
            "PartCoordinateSystem:=", "Global",
            "UDMId:="		, "",
            "MaterialValue:="	, "\"vacuum\"",
            "SurfaceMaterialValue:=", "\"\"",
            "SolveInside:="		, True,
            "IsMaterialEditable:="	, True,
            "UseMaterialAppearance:=", False,
            "IsLightweight:="	, False
        ])
    oModule = oDesign.GetModule("BoundarySetup")
    oModule.AssignPerfectE(
        [
            "NAME:PerfE",
            "Objects:="		, ["gnd"],
            "InfGroundPlane:="	, False
        ])
        
    oEditor.FitAll()

oDesign.ExportNetlist('','trlmodel.net')       
info=getMicroStripInfo('trlmodel.net')
AddWarningMessage(str(info))

for i in info['trl']:
    subname=info['trl'][i]['SUBSTRATE']
    createtrl(i, info['trl'][i], info['sub'][subname])

