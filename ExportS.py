import ScriptEnv, os
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.GetActiveProject()
oDesign = oProject.GetActiveDesign()
name=oProject.GetName()
prj_dir=oProject.GetPath()
data_dir=prj_dir+'/'+'data'
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

oModule=oDesign.GetModule("BoundarySetup")
N=oModule.GetNumExcitations()

oModule = oDesign.GetModule("Solutions")
oModule.ExportNetworkData("", ["Setup1:Sweep"], 3, "{}/{}.s{}p".format(data_dir, name, N), ["All"], True, 50, "S", -1, 0, 15, True, False, False)
oDesign.ExportProfile("Setup1", "", "{}/{}.prof".format(data_dir,name))
