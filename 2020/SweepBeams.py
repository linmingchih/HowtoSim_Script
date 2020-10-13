import os, sys, re, clr
import math, cmath
import collections

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
import os
oProject = oDesktop.GetActiveProject()
oDesign = oProject.GetActiveDesign()

def readBeams(code_dir):
    result = collections.OrderedDict()
    beam_list = []
    for beam_file in [os.path.join(code_dir, f) for f in os.listdir(code_dir) if f.endswith('.csv')]:
        with open(beam_file) as f:
            try:
                for line in list(f)[1:]:
                    port_name, mag, phase = line.strip().split(',')
                    mag = mag[:-1]
                    phase = phase[:-3]
                    
                    try:
                        result[port_name][0].append(mag)
                        result[port_name][1].append(phase)
                    except:
                        result[port_name] = ([mag], [phase])
                beam_list.append(os.path.basename(beam_file))
            except:
                pass    
    return result, beam_list
    
def output(x, unit='W'):
    def create(x):
        index, value = x[0]
        if len(x)>1:
            y = create(x[1:])        
            return 'if(beamID=={},{},({}))'.format(index, value, y) 
        else:
            return 'if(beamID=={},{},0)'.format(index, value)    
    
    return create(list(enumerate(x))) + unit
    
def setExcitations(code_dir):
    setBeamID()
    code, beam_list = readBeams(code_dir)
    
    with open(os.path.join(code_dir, 'mapping.txt'), 'w') as f:
        for i, name in enumerate(beam_list):
            f.writelines('{}:{}\n'.format(i, name))    
    
    x=[[    "IncludePortPostProcessing:=", False,
            "SpecifySystemPower:="	, False
        ]]
    
    for i in code:
        mag = output(code[i][0], 'W')
        phase = output(code[i][1], 'deg')
        x.append(
        [
            "Name:="		, i,
            "Magnitude:="		, mag,
            "Phase:="		, phase
        ])
        N=len(code[i][0])

    oModule = oDesign.GetModule("Solutions")    
    oModule.EditSources(x)
    msg = '{} beams are set successfully'.format(N)
    AddWarningMessage(msg)
    return msg
    
def resetExcitations():
    oModule = oDesign.GetModule("BoundarySetup")
    x=[[    "IncludePortPostProcessing:=", False,
            "SpecifySystemPower:="	, False
        ]]
        
    for i in oModule.GetExcitations()[::2]:
        x.append(
        [
            "Name:="		, i,
            "Magnitude:="		, "0W",
            "Phase:="		, "0deg"
        ])
        
    oModule = oDesign.GetModule("Solutions")    
    oModule.EditSources(x)
    msg = 'All excitations are reset to 0W/0deg.'
    AddWarningMessage(msg)
    return msg

def setBeamID():
    if 'beamID' not in oDesign.GetProperties("LocalVariableTab", "LocalVariables"):   
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
                        "NAME:NewProps",
                        [
                            "NAME:beamID",
                            "PropType:="		, "PostProcessingVariableProp",
                            "UserDef:="		, True,
                            "Value:="		, "0"
                        ]
                    ]
                ]
            ])
    else:
        pass
    
#GUI---------------------------------------------------------------------------|
class MyWindow(Window):
    def __init__(self):
        wpf.LoadComponent(self, 'SweepBeams.xaml')
        self.N = 0
        
    def folder_tb_TextChanged(self, sender, e):
        try:
            result, beam_list=readBeams(self.folder_tb.Text)
            self.N = len(result[result.keys()[0]][0])
            self.message_tb.Text = '{} beam(s) are selected!'.format(self.N)
            self.message_tb.Text += '\n'.join(beam_list)
        except:
            self.message_tb.Text = 'There are no beams!'
            
    
    def set_bt_Click(self, sender, e):
        if self.N == 0:
            self.message_tb.Text = 'No beams are selected!'
        else:
            msg = setExcitations(self.folder_tb.Text)
            self.message_tb.Text = msg
    
    def reset_bt_Click(self, sender, e):
        msg = resetExcitations()    
        self.message_tb.Text = msg
        
    def folder_tb_PreviewMouseDoubleClick(self, sender, e):
        dialog = FolderBrowserDialog()
        if self.folder_tb:
            dialog.SelectedPath = self.folder_tb.Text
        else:
            dialog.SelectedPath = 'c:\\'

        if dialog.ShowDialog() == DialogResult.OK:
            self.folder_tb.Text =  dialog.SelectedPath  
        else:
            pass
        
#Code End----------------------------------------------------------------------|       
MyWindow().ShowDialog()

