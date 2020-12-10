import os, sys, re, clr
import math, cmath
import collections
import copy

clr.AddReferenceByName('Microsoft.Office.Interop.Excel, Version=11.0.0.0, Culture=neutral, PublicKeyToken=71e9bce111e9429c')
from Microsoft.Office.Interop import Excel

win64_dir = oDesktop.GetExeDir()
dll_dir = os.path.join(win64_dir, 'common/IronPython/DLLs')
sys.path.append(dll_dir)
clr.AddReference('IronPython.Wpf')

import wpf
from System.Windows import Window
from System.Windows.Controls import ListBoxItem
from System.Windows.Forms import OpenFileDialog, SaveFileDialog, DialogResult, FolderBrowserDialog
os.chdir(os.path.dirname(__file__))

#Functions---------------------------------------------------------------------|
oProject = oDesktop.GetActiveProject()
oDesign = oProject.GetActiveDesign()
oEditor = oDesign.SetActiveEditor("3D Modeler")
oModule = oDesign.GetModule("ModelSetup")

def get3DCmpInstance():
    cmpdefs = oEditor.Get3DComponentDefinitionNames()
    return [oEditor.Get3DComponentInstanceNames(i)[0] for i in cmpdefs]

def getMatrix(filepath, x="G5:K10"):
    ex = Excel.ApplicationClass()   
    ex.DisplayAlerts = False
    workbook = ex.Workbooks.Open(filepath)
    ws = workbook.Worksheets[1]
    matrix = []
    color_map = {}
    n = 1
    info = {}
    rowindex = 0
    temp = []
    for cell in ws.Range(x):
        if str(cell.Interior.Color) in color_map:
            colorID = color_map[str(cell.Interior.Color)]
        else:
            colorID = 'type'+str(n)
            n+=1
            color_map[str(cell.Interior.Color)] = colorID
        
        if colorID not in info:
            info[colorID] = [cell.Value()]
        else:
            info[colorID].append(cell.Value())

        if str(cell.Row) != rowindex:
            if temp:
                matrix.append(temp)

            temp = [colorID]
            rowindex = str(cell.Row)
        else:
            temp.append(colorID)
    if temp:
        matrix.append(temp)
        
    return matrix, info
    
#GUI---------------------------------------------------------------------------|
class MyWindow(Window):
    def __init__(self):
        wpf.LoadComponent(self, 'BuildArray.xaml')
        self.set_sp.Children.Clear()

    def file_tb_MouseDoubleClick(self, sender, e):
        dialog = OpenFileDialog()
        dialog.Filter = "EXCEL files (*.xlsx)|*.xlsx"

        if dialog.ShowDialog() == DialogResult.OK:
            self.xlsx_path = dialog.FileName
            self.file_tb.Text = self.xlsx_path
            AddWarningMessage(self.xlsx_path)
        else:
            pass
            
    def read_bt_Click(self, sender, e):
        try:
            self.matrix, info = getMatrix(self.xlsx_path, self.range_tb.Text)
            self.data_tb.Text = '\n-----Matrix-----\n'
            for i in self.matrix:
                self.data_tb.Text += str(i) +'\n'
            self.data_tb.Text += '\n-----Type-----\n'
            for i in info:
                self.data_tb.Text += '{}:{}\n'.format(i, info[i])

            self.data = {}

            self.set_sp.Children.Clear()

            for i in sorted(info.keys()):
                x = copy.copy(self.name_lb)
                x.Content = i
                self.set_sp.Children.Add(x)

                x = copy.copy(self.cmp_cb)
                for j in get3DCmpInstance():
                    x.Items.Add(j)
                    x.SelectedIndex = 0
                self.set_sp.Children.Add(x)
                
                self.data[i] = x
        except:
            self.data_tb.Text = 'Failed to read excel range! Try again.'
            
    def array_bt_Click(self, sender, e):
        try:
            oModule.DeleteArray()
        except:
            pass
            
        result = {}
        mapping = {i: self.data[i].Text for i in self.data}
        
        for m, row in enumerate(self.matrix):
            for n, element in enumerate(row):
                try:
                    result[mapping[element]] +=', [{},{}]'.format(m+1, n+1) 
                except:
                    result[mapping[element]] = '[{},{}]'.format(m+1, n+1)
        
        assignment=[]
        for i in result:
            assignment.append(i+':=')
            assignment.append([result[i]])
            
        oModule.AssignArray(
            [
                "NAME:A",
                "Name:="		, "A",
                "UseAirObjects:="	, True,
                "RowMasterBnd:="	, "{}_LatticePair1".format(get3DCmpInstance()[0]),
                "ColumnMasterBnd:="	, "{}_LatticePair2".format(get3DCmpInstance()[0]),
                "RowDimension:="	, len(self.matrix),
                "ColumnDimension:="	, max([len(i) for i in self.matrix]),
                "Visible:="		, True,
                "RenderType:="		, 0,
                "Padding:="		, 0,
                [
                    "NAME:Cells",
                ] + assignment,
                [
                    "NAME:Rotation"
                ],
                "Active:="		, "All",
                [
                    "NAME:PostProcessingCells"
                ],
                "Colors:="		, []
            ])
    
        self.Close()
#Code End----------------------------------------------------------------------|       
MyWindow().ShowDialog()

