# ----------------------------------------------
# Script Recorded by ANSYS Electronics Desktop Version 2020.2.0
# 3:01:19  Nov 20, 2020
# ----------------------------------------------
import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.GetActiveProject()
oDesign = oProject.GetActiveDesign()
oEditor = oDesign.SetActiveEditor('3D Modeler')
i = 0
while True:
    name = "{}{}_{}.png".format(oProject.GetPath(), oDesign.GetName(), i)
    oEditor.ExportModelImageToFile(name,
        0, 
        0,
        [
        "NAME:SaveImageParams",
        "ShowAxis:=" , "True",
        "ShowGrid:=" , "True",
        "ShowRuler:=" , "True",
        "ShowRegion:=" , "Default",
        "Selections:=" , ""
        "Orientation:=" , "Trimetric"
        ])
    i+=1
    oDesktop.PauseScript('{} is saved.\nPress "Stop" or "Resume"'.format(name))