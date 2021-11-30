import sys
import clr
clr.AddReference("System.Windows.Forms")

from System.Windows.Forms import DialogResult, OpenFileDialog
dialog = OpenFileDialog()
dialog.Multiselect = False
dialog.Title = "HFSS ffd to csv converter"
dialog.Filter = "csv file (*.csv)|*.csv"

if dialog.ShowDialog() == DialogResult.OK:
    csv_path = dialog.FileName
    
    with open(csv_path) as f:
        text = f.readlines()

    data = []
    for line in text:
        try:
            key, value = line.split(',')[0:2]
            data.append((key, value))
        except:
            pass
            
    oProject = oDesktop.GetActiveProject()
    oDesign = oProject.GetActiveDesign()
    for key, value in data:
        oDesign.ChangeProperty(
            [
                "NAME:AllTabs",
                [
                    "NAME:LocalVariableTab",
                    [
                        "NAME:PropServers", 
                        "LocalVariables"
                    ],
                    [
                        "NAME:ChangedProps",
                        [
                            "NAME:{}".format(key),
                            "Value:="		, value
                        ]
                    ]
                ]
            ])
else:
    pass

