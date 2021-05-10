# coding=UTF-8
#User Input--------------------------------------------------------
solution = "Setup1 : LastAdaptive"
freq = "28e9"
code_dir = "D:/demo/code1"

#Don't Revise Code Below-------------------------------------------
from math import log10
import os
import time
import json
import itertools
import ScriptEnv
t0 = time.time()

ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.GetActiveProject()
oDesign = oProject.GetActiveDesign()
oDesktop.ClearMessages("","",2)

try:
    oModule.DeleteAllReports()
except:
    pass
    
def getrE():
    oModule = oDesign.GetModule("ReportSetup")
    arr = oModule.GetSolutionDataPerVariation(  
        "Far Fields", 
        solution, 
        [
            "Context:="		, "RG"
        ],
        ['Freq:=', [freq]], 
        ["RealizedGainTotal"])

    rETotal = [x for x in arr[0].GetRealDataValues("RealizedGainTotal")]
    if len(rETotal) != 65341:
        raise Exception("Theta, Phi範圍錯誤!")
    return rETotal
    
def setExcitation(csv_path):
    oModule = oDesign.GetModule("BoundarySetup")
    ports = [i.replace(':1', '') for i in oModule.GetExcitations()[::2]]
    x = {name: ("0W", "0deg") for name in ports}

    try:
        with open(csv_path) as f:
            text = f.readlines()

        for i in text[1:]:
            try:
                source, magnitude, phase = i.split(',')
                x[source.replace(':1', '')] = (magnitude, phase)
            except:
                pass

        oModule = oDesign.GetModule("Solutions")
        y = []
        for name in x:
            magnitude, phase = x[name]
            y.append([
                "Name:="   , name,
                "Magnitude:="     , magnitude,
                "Phase:="     , phase
            ])

        oModule.EditSources(
            [
                [
                    "IncludePortPostProcessing:=", False,
                    "SpecifySystemPower:=" , False
                ],
            ] + y)

        for name in x:
            magnitude, phase = x[name]
        AddWarningMessage('Load "{}" successfully!'.format(csv_path))

    except:
        AddErrorMessage('Load "{}" failed!'.format(csv_path))

oModule = oDesign.GetModule("RadField")

if "RG" not in oModule.GetChildNames():
    oModule.InsertInfiniteSphereSetup(
        [
            "NAME:RG",
            "UseCustomRadiationSurface:=", False,
            "CSDefinition:="	, "Theta-Phi",
            "Polarization:="	, "Linear",
            "ThetaStart:="		, "0deg",
            "ThetaStop:="		, "180deg",
            "ThetaStep:="		, "1deg",
            "PhiStart:="		, "-180deg",
            "PhiStop:="		, "180deg",
            "PhiStep:="		, "1deg",
            "UseLocalCS:="		, False
        ])




data = []
for i in os.listdir(code_dir):
    csv_path = os.path.join(code_dir, i)
    setExcitation(csv_path)
    data.append(getrE())
    
max_table = list(map(max, zip(*data)))

with open('RealizedGain.tab', 'w') as f:
    f.writelines('Phi[deg],Theta[deg],RealizedGain[db/sr]\n')
    
    for Er, (phi, theta) in zip(max_table, itertools.product(range(-180,181), range(0,181),)):
        #maxU = 10*log10(Er**2/377/2) + 30
        f.writelines('{}\t{}\t{}\n'.format(phi, theta, Er))

oModule = oDesign.GetModule("ReportSetup")
avaiulable_solution = oModule.GetAvailableSolutions("Modal")

oModule = oDesign.GetModule("Solutions")

if "RG : Table" in avaiulable_solution:
    oModule.DeleteImportData(["RG:Table"])

oProject.Save()   
oModule.ImportTable('RealizedGain.tab', "RG", "Table", True, True, ["Phi", "Theta", "RealizedGain"], [True, True, False])
oModule = oDesign.GetModule("ReportSetup")
oModule.CreateReport("RG Plot", "Modal Solution Data", "3D Polar Plot", "RG : Table", [], 
	[
		"Tb(Phi):="		, ["All"],
		"Tb(Theta):="		, ["All"]
	], 
	[
		"Phi Component:="	, "Tb(Phi)",
		"Theta Component:="	, "Tb(Theta)",
		"Mag Component:="	, ["Tb(RealizedGain)"]
	])


