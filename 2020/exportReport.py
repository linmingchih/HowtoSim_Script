# ----------------------------------------------
# Script Recorded by ANSYS Electronics Desktop Version 2020.1.0
# 20:37:40  Jun 11, 2020
# ----------------------------------------------
import clr, sys, os
sys.path.append('C:/Program Files/AnsysEM/AnsysEM19.4/Win64/common/IronPython/DLLs')
sys.path.append('C:/Program Files/AnsysEM/AnsysEM19.5/Win64/common/IronPython/DLLs')
sys.path.append('C:/Program Files/AnsysEM/AnsysEM20.1/Win64/common/IronPython/DLLs')
sys.path.append('C:/Program Files/AnsysEM/AnsysEM20.2/Win64/common/IronPython/DLLs')
clr.AddReference('IronPython.Wpf')
from System.Windows.Forms import FolderBrowserDialog, DialogResult

import ScriptEnv

ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.GetActiveProject()
oDesign = oProject.GetActiveDesign()
oModule = oDesign.GetModule("ReportSetup")

dialog = FolderBrowserDialog()
project_folder = os.path.dirname(oProject.GetPath()).replace('/', '\\')
dialog.SelectedPath = project_folder

if dialog.ShowDialog() == DialogResult.OK:
    path = dialog.SelectedPath
    for report in oModule.GetAllReportNames():
        AddWarningMessage("Export {}.jpg".format(report))
        oModule.ExportImageToFile(report, "{}/{}.jpg".format(path, report), 8000, 4000)
else:
    pass

