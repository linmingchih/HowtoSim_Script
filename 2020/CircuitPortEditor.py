import os, sys, re, clr
import copy
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
from System.Windows.Forms import Button, CheckBox, Form, Label, ListBox

os.chdir(os.path.dirname(__file__))

#Functions---------------------------------------------------------------------|
import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.GetActiveProject()
oDesign = oProject.GetActiveDesign()
oEditor = oDesign.GetActiveEditor()
unit = oEditor.GetActiveUnits()

scale_map = {'mm':1e-3, 'um':1e-6}
scale = scale_map[unit]
#AddWarningMessage(str(scale))

def getComponents():
    return oEditor.FindObjects('Type', 'component')

def getCompPinInfo():
    data = {}
    for comp in oEditor.FindObjects('Type', 'component'):
        data[comp]=[]
        for i in oEditor.GetComponentPins(comp):
            net = oEditor.GetPropertyValue("BaseElementTab", i, "Net")
            Location = oEditor.GetPropertyValue("BaseElementTab", i, "Location")
            x, y = map(float, Location.split(','))
            start_layer = oEditor.GetPropertyValue("BaseElementTab", i, "Start Layer")
            data[comp].append((i, net, x, y, start_layer))
    return data

    
#GUI---------------------------------------------------------------------------|

class MyWindow(Window):
    def __init__(self):
        wpf.LoadComponent(self, 'CircuitPortEditor.xaml')
        
        self.components = getComponents()
        for i in self.components:
            self.component_cb.Items.Add(i)
        self.component_cb.SelectedIndex=0
        
        for i in oEditor.FindObjects('Type', 'PinGroup'):
            self.reference_cb.Items.Add(i)        
        
        for i in oEditor.GetNets():
            self.reference_cb.Items.Add(i)
           
        self.reference_cb.SelectedIndex=0

        self.data = getCompPinInfo()
        self.show_pins_not_on_net()
        
    def show_pins_not_on_net(self):

        self.pins_lb.Items.Clear()
        pins = []
        for pin, net, _, _, _ in self.data[self.component_cb.SelectedValue]:
            if net != self.reference_cb.SelectedValue:
                pins.append(pin+':'+net)
        
        for i in pins:
            cb = copy.deepcopy(self.pin_cb)
            cb.Content=str(i)
            self.pins_lb.Items.Add(cb)
       
    def component_cb_SelectionChanged(self, sender, e):
        try:
            self.show_pins_not_on_net()
        except:
            pass

    
    def reference_cb_SelectionChanged(self, sender, e):
        try:
            self.show_pins_not_on_net()
        except:
            pass

    def pins_lb_PreviewMouseRightButtonDown(self, sender, e):
        for i in self.pins_lb.SelectedItems:
            i.IsChecked= not i.IsChecked
            
    def create_bt_Click(self, sender, e):
        checked_cbs = [i.Content.split(':')[0] for i in self.pins_lb.Items if i.IsChecked]
        checked_pins=[]
        
        for i in checked_cbs:
            for j in self.data[self.component_cb.SelectedValue]:
                if j[0] == i:
                    checked_pins.append(j)
        
        if self.reference_cb.SelectedValue in oEditor.FindObjects('Type', 'PinGroup'):
            for i in checked_pins:
                #AddWarningMessage(str(i))
                
                if i[0].startswith(self.component_cb.SelectedValue) and i[0].endswith(i[1]):
                    port_name = i[0]
                elif self.component_cb.SelectedValue + '-' in i[0]:
                    port_name = i[0].replace('-','.') + '.' + i[1]
                elif i[1] == '':
                    AddWarningMessage('Ignore {}: No Net assignment!'.format(i[0]))
                    continue
                else:
                    port_name = "{}.{}.{}".format(self.component_cb.SelectedValue, i[0], i[1])
                
                AddWarningMessage('port_name:'+port_name)
                
                oEditor.ToggleViaPin(
                    [
                        "NAME:elements", 
                        i[0]
                    ])
                oEditor.AddPinGroupRefPort([port_name], [self.reference_cb.SelectedValue])                
        
        else:
            reference_pins=[i for i in self.data[self.component_cb.SelectedValue] if i[1] == self.reference_cb.SelectedValue]
                   
            for i in checked_pins:
                info=[]
                x0, y0 = i[2], i[3]
                for j in reference_pins:
                    x1, y1 = j[2], j[3]
                    distance = math.sqrt((x1-x0)**2 + (y1-y0)**2)
                    info.append((distance, i, j))
                
                info.sort()
                _, i, j = info[0]
            
                oEditor.CreateCircuitPort(
                    [
                        "NAME:Location",
                        "PosLayer:="		, i[4],
                        "X0:="			, i[2]*scale,
                        "Y0:="			, i[3]*scale,
                        "NegLayer:="		, j[4],
                        "X1:="			, j[2]*scale,
                        "Y1:="			, j[3]*scale
                    ])
                oDesign.ChangeProperty(
                    [
                        "NAME:AllTabs",
                        [
                            "NAME:EM Design",
                            [
                                "NAME:PropServers", 
                                "Excitations:Port1"
                            ],
                            [
                                "NAME:ChangedProps",
                                [
                                    "NAME:Port",
                                    "Value:="		, "{}.{}.{}".format(self.component_cb.SelectedValue, i[0], i[1])
                                ]
                            ]
                        ]
                    ])
                
#Code End----------------------------------------------------------------------|       
MyWindow().ShowDialog()

