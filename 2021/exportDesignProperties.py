import sys
import clr
clr.AddReference("System.Windows.Forms")

from System.Windows.Forms import DialogResult, SaveFileDialog
dialog = SaveFileDialog()
dialog.Title = "Export Design Properties"
dialog.Filter = "csv file (*.csv)|*.csv"

if dialog.ShowDialog() == DialogResult.OK:
    csv_path = dialog.FileName
    AddWarningMessage(csv_path)
else:
    pass

oProject = oDesktop.GetActiveProject()
oDesign = oProject.GetActiveDesign()

data = []
for key in oDesign.GetProperties('LocalVariableTab', "LocalVariables"):
    value = oDesign.GetPropertyValue('LocalVariableTab', "LocalVariables", key)
    data.append((key, value))

with open(csv_path, 'w') as f:
    for key, value in data:
        f.writelines('{}, {}\n'.format(key, value))