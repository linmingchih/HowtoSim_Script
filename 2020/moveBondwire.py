import os, sys, re, clr
import math, cmath
import collections
import json
win64_dir = oDesktop.GetExeDir()
dll_dir = os.path.join(win64_dir, 'common/IronPython/DLLs')
sys.path.append(dll_dir)
clr.AddReference('IronPython.Wpf')

import wpf
from System.Windows import Window, Visibility
from System.Windows.Controls import ListBoxItem
from System.Windows.Forms import OpenFileDialog, SaveFileDialog, DialogResult, FolderBrowserDialog
os.chdir(os.path.dirname(__file__))

oProject = oDesktop.GetActiveProject()
oDesign = oProject.GetActiveDesign()
oEditor = oDesign.GetActiveEditor()
oDesktop.ClearMessages("", "", 2)
#Functions---------------------------------------------------------------------|
def switch(bw_name):
    unit = 	oEditor.GetActiveUnits()
    start_layer = oEditor.GetPropertyValue("BaseElementTab", bw_name, 'Start Layer')
    end_layer = oEditor.GetPropertyValue("BaseElementTab", bw_name, 'End Layer')
    pt0 = oEditor.GetPropertyValue("BaseElementTab", bw_name, 'Pt0').split(',')
    pt1 = oEditor.GetPropertyValue("BaseElementTab", bw_name, 'Pt1').split(',')
    
    try:
        oEditor.ChangeProperty(
            [
                "NAME:AllTabs",
                [
                    "NAME:BaseElementTab",
                    [
                        "NAME:PropServers", 
                        bw_name
                    ],
                    [
                        "NAME:ChangedProps",
                        [
                            "NAME:Start Layer",
                            "Value:="		, end_layer
                        ]
                    ]
                ]
            ])
        oEditor.ChangeProperty(
            [
                "NAME:AllTabs",
                [
                    "NAME:BaseElementTab",
                    [
                        "NAME:PropServers", 
                        bw_name
                    ],
                    [
                        "NAME:ChangedProps",
                        [
                            "NAME:End Layer",
                            "Value:="		, start_layer
                        ]
                    ]
                ]
            ])
        oEditor.ChangeProperty(
            [
                "NAME:AllTabs",
                [
                    "NAME:BaseElementTab",
                    [
                        "NAME:PropServers", 
                        bw_name
                    ],
                    [
                        "NAME:ChangedProps",
                        [
                            "NAME:Pt0",
                            "X:="			, "{}{}".format(pt1[0], unit),
                            "Y:="			, "{}{}".format(pt1[1], unit)
                        ]
                    ]
                ]
            ])
        oEditor.ChangeProperty(
            [
                "NAME:AllTabs",
                [
                    "NAME:BaseElementTab",
                    [
                        "NAME:PropServers", 
                        bw_name
                    ],
                    [
                        "NAME:ChangedProps",
                        [
                            "NAME:Pt1",
                            "X:="			, "{}{}".format(pt0[0], unit),
                            "Y:="			, "{}{}".format(pt0[1], unit)
                        ]
                    ]
                ]
            ])
        AddWarningMessage('{} is switched!'.format(bw_name))
    except:
        AddWarningMessage('{} failed in switching!'.format(bw_name))




def change(bondwire_name, direction, distance):
    pt0 = oEditor.GetPropertyValue("BaseElementTab", bondwire_name, 'pt0')
    pt1 = oEditor.GetPropertyValue("BaseElementTab", bondwire_name, 'pt1')
    x0, y0 = map(float, pt0.strip().split(','))
    x1, y1 = map(float, pt1.strip().split(','))
    if direction == "Move in x":
        x, y = x1 + distance, y1
    
    elif direction == "Move in y":
        x, y = x1, y1 + distance
    
    elif direction == "Move along":
        length = math.sqrt((x1-x0)**2+(y1-y0)**2)
        x, y = x1 + distance*(x1-x0)/(length), y1 + distance*(y1-y0)/(length)
    
    elif direction == "Switch Pts":
        switch(bondwire_name)
        return None
    
    else:
        pass

    oEditor.ChangeProperty(
        [
            "NAME:AllTabs",
            [
                "NAME:BaseElementTab",
                [
                    "NAME:PropServers", 
                    bondwire_name
                ],
                [
                    "NAME:ChangedProps",
                    [
                        "NAME:Pt1",
                        "X:="			, "{}mm".format(x),
                        "Y:="			, "{}mm".format(y)
                    ]
                ]
            ]
        ])

def getProfile():
    profile = {}
    for bondwire_name in oEditor.FindObjects('Type', 'bondwire'):
        name = oEditor.GetPropertyValue("BaseElementTab", bondwire_name, 'Profile')
        try:
            profile[name]+=[bondwire_name]
        except:
            profile[name]=[bondwire_name]
    
    return profile   
#GUI---------------------------------------------------------------------------|

class MyWindow(Window):
    def __init__(self):
        wpf.LoadComponent(self, 'MoveBondWire.xaml')

        try:
            with open('movebw.json') as f:
                data = json.load(f)
            self.direction_cb.Text = data['direction']
            self.dist_tb.Text = data['dist']
        except:
            pass
        
        self.profiles = getProfile()
        for i in self.profiles:
            self.profile_cb.Items.Add(i)        

    def direction_cb_SelectionChanged(self, sender, e):
        if self.direction_cb.SelectedItem.Content == 'Switch Pts':
            self.dist_tb.Visibility =  Visibility.Hidden
            self.move_bt.Content = 'Switch'
        else:
            self.dist_tb.Visibility =  Visibility.Visible
            self.move_bt.Content = 'Move'            
    
    def dist_tb_TextChanged(self, sender, e):
        pass

    
    def move_bt_Click(self, sender, e):
        selected = oEditor.GetSelections()
        for i in selected:
            change(i, self.direction_cb.Text, float(self.dist_tb.Text))
        
        data = {'direction': self.direction_cb.Text, 
                'dist': self.dist_tb.Text}
        with open('movebw.json', 'w') as f:
            json.dump(data, f, indent=4)
            
        oEditor.Select(selected)

    
    def profile_cb_SelectionChanged(self, sender, e):
        AddWarningMessage(str(self.profiles[self.profile_cb.SelectedValue]))
        oEditor.Select(self.profiles[self.profile_cb.SelectedValue])
'''
class MyWindow(Window):
    def __init__(self):
        wpf.LoadComponent(self, 'moveBondwire.xaml')
        try:
            with open('movebw.json') as f:
                data = json.load(f)
            self.direction_cb.Text = data['direction']
            self.dist_tb.Text = data['dist']
        except:
            pass
        
        self.profiles = getProfile()
        for i in self.profiles:
            self.profile_cb.Items.Add(i)

    def Button_Click(self, sender, e):
        selected = oEditor.GetSelections()
        for i in selected:
            change(i, self.direction_cb.Text, float(self.dist_tb.Text))
        
        data = {'direction': self.direction_cb.Text, 
                'dist': self.dist_tb.Text}
        with open('movebw.json', 'w') as f:
            json.dump(data, f, indent=4)
            
        oEditor.Select(selected)
        
    def profile_cb_SelectionChanged(self, sender, e):
        AddWarningMessage(str(self.profiles[self.profile_cb.SelectedValue]))
        oEditor.Select(self.profiles[self.profile_cb.SelectedValue])

    def direction_cb_SelectionChanged(self, sender, e):
        if self.direction_cb.SelectedValue == "Switch Pts":
            self.dist_tb.IsEnabled= False
'''            
#Code End----------------------------------------------------------------------|       
MyWindow().ShowDialog()

