# coding=utf-8
import os, re, sys, clr, json, math, logging, random, time
from itertools import combinations
os.chdir(os.path.dirname(__file__))
logging.basicConfig(filename='gui.log', filemode='w', encoding='utf-8', level=logging.DEBUG)
clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')

from System import Drawing, Array, ComponentModel, Diagnostics, IO
from System.Drawing import Color
from System.Windows import Forms
import System.Object as object
import System.String as string
from System.Windows.Forms import DialogResult, OpenFileDialog ,SaveFileDialog, FolderBrowserDialog, MessageBox
#----------------------------------------------------------------------------
import ScriptEnv

import clr

clr.AddReference('Ansys.Ansoft.Edb')
clr.AddReference('Ansys.Ansoft.SimSetupData')
import Ansys.Ansoft.Edb as edb
import Ansys.Ansoft.Edb.Definition as edbd

ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oDesktop.ClearMessages("", "", 2)
oProject = oDesktop.GetActiveProject()
oDesign = oProject.GetActiveDesign()
oEditor = oDesign.GetActiveEditor()

oDefinitionManager = oProject.GetDefinitionManager()
oBondwireManager = oDefinitionManager.GetManager("Bondwire") 
DB = edb.Database.Attach(int(oProject.GetEDBHandle()))

def changeJEDECType(bondwirenames, profile, jtype):
    jvalue = {1: "Cadence APD/Allegro:JEDEC4Bondwire",
              2: "Cadence APD/Allegro:JEDEC5Bondwire"}
   
    oEditor.ChangeProperty(
        [
            "NAME:AllTabs",
            [
                "NAME:BaseElementTab",
                [
                    "NAME:PropServers", 
                ] + bondwirenames,
                [
                    "NAME:ChangedProps",
                    [
                        "NAME:Type",
                        "Value:="		, jvalue[jtype]
                    ],
                    [
                        "NAME:Profile",
                        "Value:="		, "\"{}\"".format(profile)
                    ]                    
                ]
            ]
        ])
       
def getExistingProfiles():
    return oBondwireManager.GetNames()

def getCategory():
    category = {}
    for p in oBondwireManager.GetNames():
        category[p] = []    
 
    for i in oEditor.FindObjects('type', 'bondwire'):
        profile = oEditor.GetPropertyValue('BaseElementTab', i, 'Profile')[1:-1]
        try:
            category[profile] +=[i]
        except:
            category[profile] = [i]
    
    return category
       
def getProfileInfo():
    result = {i:(-1, '0', '0', '0') for i in getCategory()}
    for i in oBondwireManager.GetNames():
        data = oBondwireManager.GetData(i) 
        bondwire_type = data[2]
        if bondwire_type not in [1, 2]:
            continue
        h = data[8][0][:-2]
        a = data[10][0][:-3]
        b = data[12][0][:-3]
        result[i] = (bondwire_type, h, a, b)     
    return result
    
def removeProfile(names):
    for name in names:
        oBondwireManager.Remove(name, True, "", "Project")


def addProfile(name, profile_type, h="500", a="90", b="30"):
    # profile_type 1:Jedec4Bondwire, 2:Jedec4Bondwire

    oBondwireManager.Add(
        [
            "NAME:{}".format(name),
            "Type:="		, profile_type,
            "ModifiedOn:="		, str(time.time()).split('.')[0],
            "Library:="		, "",
            "h:="			, [h+'um'],
            "a:="			, [a+'deg'],
            "b:="			, [b+'deg']
        ])
    if profile_type == 1:
        result = edbd.Jedec4BondwireDef.Create(DB, name, float(h)*1e-6)
    elif profile_type == 2:
        result = edbd.Jedec5BondwireDef.Create(DB, name, float(h)*1e-6, float(a), float(b))
    
    setBondwireProfile(name, profile_type)
    AddWarningMessage('{} is added!'.format(name))
    return result
      
def setBondwireProfile(name, profile_type):     
    x = getCategory()
    bondwires = x[name]
    if bondwires:
        changeJEDECType(bondwires, name, profile_type)

def editProfile(name, profile_type, h='500', a='90', b='30'):
    # profile_type 1:Jedec4Bondwire, 2:Jedec4Bondwire
    a = '90' if a == '' else a
    b = '30' if b == '' else b
    
    if name not in getExistingProfiles():
        addProfile(name, profile_type, h, a, b)
    else:
        oBondwireManager.Edit(name, 
            [
                "NAME:{}".format(name),
                "Type:="		, profile_type,
                "ModifiedOn:="		, str(time.time()).split('.')[0],
                "Library:="		, "",
                "h:="			, [h+'um'],
                "a:="			, [a+'deg'],
                "b:="			, [b+'deg']
            ])
    if profile_type == 1:
        result = edbd.Jedec4BondwireDef.Create(DB, name, float(h)*1e-6)
    elif profile_type == 2:
        result = edbd.Jedec5BondwireDef.Create(DB, name, float(h)*1e-6, float(a), float(b))            
            
    setBondwireProfile(name, profile_type)
    AddWarningMessage('{} is set!'.format(name))
    return result
    
def isfloat(x):
    try:
        return (float(x) > 0)
    except:
        return False

def getPW():
    result = {}
    for i in oEditor.FindObjects('type', 'bondwire'):
        pw = oEditor.GetPropertyValue('BaseElementTab', i, 'PathWidth')
        if pw in ['0fm']:
           continue
        else:
            result[i] = pw
    return result
    
def changeBondwirePathWidth(bondwires, pathwidth = '0fm'):
    if len(bondwires) == 0:
        return None
    oEditor.ChangeProperty(
        [
            "NAME:AllTabs",
            [
                "NAME:BaseElementTab",
                [
                    "NAME:PropServers", 
                ] + bondwires,
                [
                    "NAME:ChangedProps",
                    [
                        "NAME:PathWidth",
                        "Value:="		, pathwidth
                    ]
                ]
            ]
        ])
        
def change(bondwire_name, direction, distance, point="Pt1"):
    if bondwire_name not in oEditor.FindObjects('Type', 'bondwire'):
        return
    pt0 = oEditor.GetPropertyValue("BaseElementTab", bondwire_name, 'pt0')
    pt1 = oEditor.GetPropertyValue("BaseElementTab", bondwire_name, 'pt1')
    x0, y0 = map(float, pt0.strip().split(','))
    x1, y1 = map(float, pt1.strip().split(','))
    length = math.sqrt((x1-x0)**2 + (y1-y0)**2)
    dx = distance*(x1-x0)/(length)
    dy = distance*(y1-y0)/(length)
    
    dvector = {  "Forward": (dx, dy),
                "Backward": (-dx, -dy),
                "Left":(-dy, dx),
                "Right":(dy, -dx),
                }
    du, dv = dvector[direction]
    if point == "Pt0":
        x, y = x0 + du, y0 + dv 
    else:
        x, y = x1 + du, y1 + dv

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
                        "NAME:{}".format(point),
                        "X:="			, "{}mm".format(x),
                        "Y:="			, "{}mm".format(y)
                    ]
                ]
            ]
        ])        

def reverse(bw_name):
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

def alignBondwireCenter(bondwire, point='Pt0'):
    try:
        x, y = oEditor.GetPropertyValue('BaseElementTab', bondwire, point).split(',')
        x, y = float(x), float(y)
        
        if point == 'Pt0':
            layer = oEditor.GetPropertyValue('BaseElementTab', bondwire, 'Start Layer')
        else:
            layer = oEditor.GetPropertyValue('BaseElementTab', bondwire, 'End Layer')
        
        
        objs = oEditor.FindObjectsByPoint(oEditor.Point().Set(x*1e-3, y*1e-3), layer)

        for i in objs:
            if oEditor.GetPropertyValue('BaseElementTab', i, 'Type') in ['Via', 'Pin']:
                u, v = oEditor.GetPropertyValue('BaseElementTab', i, 'Location').split(',')
                break
            else:
                pass
               
        oEditor.ChangeProperty(
            [
                "NAME:AllTabs",
                [
                    "NAME:BaseElementTab",
                    [
                        "NAME:PropServers", 
                        bondwire,
                    ],
                    [
                        "NAME:ChangedProps",
                        [
                            "NAME:{}".format(point),
                            "X:="			, "{}mm".format(u),
                            "Y:="			, "{}mm".format(v),
                        ]
                    ]
                ]
            ])
        AddWarningMessage('{} is aligned to {} center!'.format(bondwire, i))
    except:
        logging.exception('error')
#Separate Code-------------------------------------------------------
def ccw(A,B,C):
    Ax, Ay = A
    Bx, By = B
    Cx, Cy = C
    return (Cy-Ay) * (Bx-Ax) > (By-Ay) * (Cx-Ax)


def intersect(A,B,C,D):    
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)


def checkintersection(segments):
    for (A, B), (C, D) in combinations(segments, 2):
        if intersect(A, B, C, D):
            return True
    return False

def getPkgGrid(pin_name):
    layer = oEditor.GetPropertyValue('BaseElementTab', pin_name, 'Start Layer')
    x0, y0 = oEditor.GetPropertyValue('BaseElementTab', pin_name, 'Location').split(',')
    x0, y0 = float(x0), float(y0)

    grid = []    
    for i in range(-10, 11):
        for j in range(-10, 11):
            x = (x0 + 0.04 * i) * 1e-3
            y = (y0 + 0.04 * j) * 1e-3
            pt = oEditor.Point()
            pt.Set(x,y)
            if pin_name in oEditor.FindObjectsByPoint(pt, layer):
                grid.append((x, y))
    return grid
     


def getDieGrid(pin_name):
    layer = oEditor.GetPropertyValue('BaseElementTab', pin_name, 'Start Layer')
    grid = {}
    for i in oEditor.FindObjects('Type', 'bondwire'):
        p1 = oEditor.Point()
        x, y = oEditor.GetPropertyValue('BaseElementTab', i, 'Pt1').split(',')
        pt = p1.Set(float(x)*1e-3 ,float(y)*1e-3)
        obj = oEditor.FindObjectsByPoint(p1, layer)

        if pin_name in oEditor.FindObjectsByPoint(pt, layer):
            x, y = oEditor.GetPropertyValue('BaseElementTab', i, 'Pt0').split(',')
            x, y = float(x)*1e-3+random.uniform(0, 1)*1e-9 ,float(y)*1e-3+random.uniform(0, 1)*1e-9
            grid[(x, y)] = i
    return grid

def separate(pcb_pad):    
    pkg = getPkgGrid(pcb_pad)
    AddWarningMessage('Pkg Locations: {}'.format(len(pkg)))

    die = getDieGrid(pcb_pad)
    AddWarningMessage('die Locations: {}'.format(len(die)))

    pair = {}
    N = 0
    while(True):
        N+=1
        if N > 100000:
            AddWarningMessage('Failed')
            segments = []
            break
        segments = []
        random.shuffle(pkg)
        for (pt0, pt1) in zip(die.keys(), pkg):
            segments.append((pt0, pt1))
        if checkintersection(segments) == False:
            AddWarningMessage('Successful')
            break
        
    for pt0, pt1 in segments:
        pair[die[pt0]] = pt1
        
    AddWarningMessage(str(pair))
    try:
        for bw_name in pair:
            x, y = pair[bw_name]
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
                                "X:="			, str(x),
                                "Y:="			, str(y)
                            ]
                        ]
                    ]
                ])
    except:
        pass


#----------------------------------------------------------------------------
class MyForm(Forms.Form):
    def __init__(self):
        self.tabPage1 = Forms.TabPage()
        self.ok_bt = Forms.Button()
        self.label2 = Forms.Label()
        self.modelname_lb = Forms.Label()
        self.groupBox1 = Forms.GroupBox()
        self.label8 = Forms.Label()
        self.label9 = Forms.Label()
        self.label10 = Forms.Label()
        self.label7 = Forms.Label()
        self.label6 = Forms.Label()
        self.label5 = Forms.Label()
        self.apply_bt = Forms.Button()
        self.beta_tb = Forms.TextBox()
        self.alpha_tb = Forms.TextBox()
        self.h1_tb = Forms.TextBox()
        self.groupBox2 = Forms.GroupBox()
        self.create_bt = Forms.Button()
        self.name_tb = Forms.TextBox()
        self.delete_bt = Forms.Button()
        self.type_cb = Forms.ComboBox()
        self.model_lb = Forms.ListBox()
        self.switch_tab = Forms.TabControl()
        self.tabPage2 = Forms.TabPage()
        self.groupBox5 = Forms.GroupBox()
        self.label13 = Forms.Label()
        self.label12 = Forms.Label()
        self.label11 = Forms.Label()
        self.separate_bt = Forms.Button()
        self.align_bt = Forms.Button()
        self.reverse_bt = Forms.Button()
        self.groupBox4 = Forms.GroupBox()
        self.right_bt = Forms.Button()
        self.backward_bt = Forms.Button()
        self.left_bt = Forms.Button()
        self.forward_bt = Forms.Button()
        self.groupBox3 = Forms.GroupBox()
        self.unit_lb = Forms.Label()
        self.label3 = Forms.Label()
        self.step_tb = Forms.TextBox()
        self.pt1_rb = Forms.RadioButton()
        self.pt0_rb = Forms.RadioButton()
        self.tabPage1.SuspendLayout()
        self.groupBox1.SuspendLayout()
        self.groupBox2.SuspendLayout()
        self.switch_tab.SuspendLayout()
        self.tabPage2.SuspendLayout()
        self.groupBox5.SuspendLayout()
        self.groupBox4.SuspendLayout()
        self.groupBox3.SuspendLayout()
        self.SuspendLayout()
        # tabPage1
        self.tabPage1.BackColor = Drawing.Color.Transparent
        self.tabPage1.Controls.Add(self.ok_bt)
        self.tabPage1.Controls.Add(self.label2)
        self.tabPage1.Controls.Add(self.modelname_lb)
        self.tabPage1.Controls.Add(self.groupBox1)
        self.tabPage1.Controls.Add(self.groupBox2)
        self.tabPage1.Controls.Add(self.delete_bt)
        self.tabPage1.Controls.Add(self.type_cb)
        self.tabPage1.Controls.Add(self.model_lb)
        self.tabPage1.Font = Drawing.Font("Arial", 9.75, Drawing.FontStyle.Regular, Drawing.GraphicsUnit.Point)
        self.tabPage1.Location = Drawing.Point(4, 25)
        self.tabPage1.Name = "tabPage1"
        self.tabPage1.Padding = Forms.Padding(3)
        self.tabPage1.Size = Drawing.Size(417, 506)
        self.tabPage1.TabIndex = 0
        self.tabPage1.Text = "Profile Edit"
        # ok_bt
        self.ok_bt.Anchor = (((Forms.AnchorStyles.Bottom | Forms.AnchorStyles.Right)))
        self.ok_bt.Font = Drawing.Font("Arial", 12, Drawing.FontStyle.Regular, Drawing.GraphicsUnit.Point)
        self.ok_bt.Location = Drawing.Point(304, 458)
        self.ok_bt.Name = "ok_bt"
        self.ok_bt.Size = Drawing.Size(100, 40)
        self.ok_bt.TabIndex = 14
        self.ok_bt.Text = "Interact"
        self.ok_bt.UseVisualStyleBackColor = True
        self.ok_bt.Click += self.ok_bt_Click

        # label2
        self.label2.AutoSize = True
        self.label2.Font = Drawing.Font("Arial", 9.75, Drawing.FontStyle.Regular, Drawing.GraphicsUnit.Point)
        self.label2.Location = Drawing.Point(222, 8)
        self.label2.Name = "label2"
        self.label2.Size = Drawing.Size(47, 16)
        self.label2.TabIndex = 10
        self.label2.Text = "Profile:"
        # modelname_lb
        self.modelname_lb.AutoSize = True
        self.modelname_lb.Font = Drawing.Font("Arial", 9.75, Drawing.FontStyle.Regular, Drawing.GraphicsUnit.Point)
        self.modelname_lb.Location = Drawing.Point(12, 8)
        self.modelname_lb.Name = "modelname_lb"
        self.modelname_lb.Size = Drawing.Size(84, 16)
        self.modelname_lb.TabIndex = 7
        self.modelname_lb.Text = "Model Name:"
        # groupBox1
        self.groupBox1.Anchor = (((Forms.AnchorStyles.Top | Forms.AnchorStyles.Right)))
        self.groupBox1.Controls.Add(self.label8)
        self.groupBox1.Controls.Add(self.label9)
        self.groupBox1.Controls.Add(self.label10)
        self.groupBox1.Controls.Add(self.label7)
        self.groupBox1.Controls.Add(self.label6)
        self.groupBox1.Controls.Add(self.label5)
        self.groupBox1.Controls.Add(self.apply_bt)
        self.groupBox1.Controls.Add(self.beta_tb)
        self.groupBox1.Controls.Add(self.alpha_tb)
        self.groupBox1.Controls.Add(self.h1_tb)
        self.groupBox1.Font = Drawing.Font("Arial", 9.75, Drawing.FontStyle.Regular, Drawing.GraphicsUnit.Point)
        self.groupBox1.Location = Drawing.Point(222, 99)
        self.groupBox1.Name = "groupBox1"
        self.groupBox1.Size = Drawing.Size(182, 209)
        self.groupBox1.TabIndex = 12
        self.groupBox1.TabStop = False
        self.groupBox1.Text = "Dimension"
        # label8
        self.label8.AutoSize = True
        self.label8.Font = Drawing.Font("Arial", 9.75, Drawing.FontStyle.Regular, Drawing.GraphicsUnit.Point)
        self.label8.Location = Drawing.Point(133, 108)
        self.label8.Name = "label8"
        self.label8.Size = Drawing.Size(28, 16)
        self.label8.TabIndex = 20
        self.label8.Text = "deg"
        # label9
        self.label9.AutoSize = True
        self.label9.Font = Drawing.Font("Arial", 9.75, Drawing.FontStyle.Regular, Drawing.GraphicsUnit.Point)
        self.label9.Location = Drawing.Point(133, 72)
        self.label9.Name = "label9"
        self.label9.Size = Drawing.Size(28, 16)
        self.label9.TabIndex = 19
        self.label9.Text = "deg"
        # label10
        self.label10.AutoSize = True
        self.label10.Font = Drawing.Font("Arial", 9.75, Drawing.FontStyle.Regular, Drawing.GraphicsUnit.Point)
        self.label10.Location = Drawing.Point(133, 33)
        self.label10.Name = "label10"
        self.label10.Size = Drawing.Size(25, 16)
        self.label10.TabIndex = 18
        self.label10.Text = "um"
        # label7
        self.label7.AutoSize = True
        self.label7.Font = Drawing.Font("Arial", 9.75, Drawing.FontStyle.Regular, Drawing.GraphicsUnit.Point)
        self.label7.Location = Drawing.Point(13, 108)
        self.label7.Name = "label7"
        self.label7.Size = Drawing.Size(36, 16)
        self.label7.TabIndex = 17
        self.label7.Text = "beta:"
        # label6
        self.label6.AutoSize = True
        self.label6.Font = Drawing.Font("Arial", 9.75, Drawing.FontStyle.Regular, Drawing.GraphicsUnit.Point)
        self.label6.Location = Drawing.Point(7, 72)
        self.label6.Name = "label6"
        self.label6.Size = Drawing.Size(42, 16)
        self.label6.TabIndex = 16
        self.label6.Text = "alpha:"
        # label5
        self.label5.AutoSize = True
        self.label5.Font = Drawing.Font("Arial", 9.75, Drawing.FontStyle.Regular, Drawing.GraphicsUnit.Point)
        self.label5.Location = Drawing.Point(24, 33)
        self.label5.Name = "label5"
        self.label5.Size = Drawing.Size(25, 16)
        self.label5.TabIndex = 15
        self.label5.Text = "h1:"
        # apply_bt
        self.apply_bt.Anchor = (((Forms.AnchorStyles.Bottom | Forms.AnchorStyles.Right)))
        self.apply_bt.Font = Drawing.Font("Arial", 12, Drawing.FontStyle.Regular, Drawing.GraphicsUnit.Point)
        self.apply_bt.Location = Drawing.Point(40, 150)
        self.apply_bt.Name = "apply_bt"
        self.apply_bt.Size = Drawing.Size(100, 40)
        self.apply_bt.TabIndex = 15
        self.apply_bt.Text = "Apply"
        self.apply_bt.UseVisualStyleBackColor = True
        self.apply_bt.Click += self.apply_bt_Click

        # beta_tb
        self.beta_tb.Font = Drawing.Font("Arial", 9.75, Drawing.FontStyle.Regular, Drawing.GraphicsUnit.Point)
        self.beta_tb.Location = Drawing.Point(54, 108)
        self.beta_tb.Name = "beta_tb"
        self.beta_tb.Size = Drawing.Size(73, 22)
        self.beta_tb.TabIndex = 6
        self.beta_tb.TextChanged += self.beta_tb_TextChanged

        # alpha_tb
        self.alpha_tb.Font = Drawing.Font("Arial", 9.75, Drawing.FontStyle.Regular, Drawing.GraphicsUnit.Point)
        self.alpha_tb.Location = Drawing.Point(54, 69)
        self.alpha_tb.Name = "alpha_tb"
        self.alpha_tb.Size = Drawing.Size(73, 22)
        self.alpha_tb.TabIndex = 5
        self.alpha_tb.TextChanged += self.alpha_tb_TextChanged

        # h1_tb
        self.h1_tb.Font = Drawing.Font("Arial", 9.75, Drawing.FontStyle.Regular, Drawing.GraphicsUnit.Point)
        self.h1_tb.Location = Drawing.Point(54, 30)
        self.h1_tb.Name = "h1_tb"
        self.h1_tb.Size = Drawing.Size(73, 22)
        self.h1_tb.TabIndex = 4
        self.h1_tb.TextChanged += self.h1_tb_TextChanged

        # groupBox2
        self.groupBox2.Anchor = (((Forms.AnchorStyles.Bottom | Forms.AnchorStyles.Right)))
        self.groupBox2.Controls.Add(self.create_bt)
        self.groupBox2.Controls.Add(self.name_tb)
        self.groupBox2.Font = Drawing.Font("Arial", 9.75, Drawing.FontStyle.Regular, Drawing.GraphicsUnit.Point)
        self.groupBox2.Location = Drawing.Point(222, 314)
        self.groupBox2.Name = "groupBox2"
        self.groupBox2.Size = Drawing.Size(182, 133)
        self.groupBox2.TabIndex = 13
        self.groupBox2.TabStop = False
        self.groupBox2.Text = "New Profile"
        # create_bt
        self.create_bt.Anchor = (((Forms.AnchorStyles.Bottom | Forms.AnchorStyles.Right)))
        self.create_bt.Font = Drawing.Font("Arial", 12, Drawing.FontStyle.Regular, Drawing.GraphicsUnit.Point)
        self.create_bt.Location = Drawing.Point(40, 71)
        self.create_bt.Name = "create_bt"
        self.create_bt.Size = Drawing.Size(100, 40)
        self.create_bt.TabIndex = 16
        self.create_bt.Text = "Add"
        self.create_bt.UseVisualStyleBackColor = True
        self.create_bt.Click += self.create_bt_Click

        # name_tb
        self.name_tb.Font = Drawing.Font("Arial", 9.75, Drawing.FontStyle.Regular, Drawing.GraphicsUnit.Point)
        self.name_tb.Location = Drawing.Point(24, 31)
        self.name_tb.Name = "name_tb"
        self.name_tb.Size = Drawing.Size(134, 22)
        self.name_tb.TabIndex = 7
        self.name_tb.TextChanged += self.name_tb_TextChanged

        # delete_bt
        self.delete_bt.Anchor = (((Forms.AnchorStyles.Bottom | Forms.AnchorStyles.Left)))
        self.delete_bt.Font = Drawing.Font("Arial", 12, Drawing.FontStyle.Regular, Drawing.GraphicsUnit.Point)
        self.delete_bt.Location = Drawing.Point(104, 458)
        self.delete_bt.Name = "delete_bt"
        self.delete_bt.Size = Drawing.Size(100, 40)
        self.delete_bt.TabIndex = 8
        self.delete_bt.Text = "Delete"
        self.delete_bt.UseVisualStyleBackColor = True
        self.delete_bt.Click += self.delete_bt_Click

        # type_cb
        self.type_cb.Anchor = (((Forms.AnchorStyles.Top | Forms.AnchorStyles.Right)))
        self.type_cb.Font = Drawing.Font("Arial", 9.75, Drawing.FontStyle.Regular, Drawing.GraphicsUnit.Point)
        self.type_cb.FormattingEnabled = True
        self.type_cb.Location = Drawing.Point(222, 43)
        self.type_cb.Name = "type_cb"
        self.type_cb.Size = Drawing.Size(182, 24)
        self.type_cb.TabIndex = 11
        self.type_cb.Text = "None"
        self.type_cb.SelectedIndexChanged += self.type_cb_SelectedIndexChanged

        # model_lb
        self.model_lb.Anchor = ((((Forms.AnchorStyles.Top | Forms.AnchorStyles.Bottom)| Forms.AnchorStyles.Left)))
        self.model_lb.Font = Drawing.Font("Arial", 9.75, Drawing.FontStyle.Regular, Drawing.GraphicsUnit.Point)
        self.model_lb.FormattingEnabled = True
        self.model_lb.ItemHeight = 16
        self.model_lb.Location = Drawing.Point(12, 43)
        self.model_lb.Name = "model_lb"
        self.model_lb.ScrollAlwaysVisible = True
        self.model_lb.Size = Drawing.Size(192, 404)
        self.model_lb.TabIndex = 9
        self.model_lb.SelectedIndexChanged += self.model_lb_SelectedIndexChanged

        # switch_tab
        self.switch_tab.Controls.Add(self.tabPage1)
        self.switch_tab.Controls.Add(self.tabPage2)
        self.switch_tab.Dock = Forms.DockStyle.Fill
        self.switch_tab.Font = Drawing.Font("Arial", 9.75, Drawing.FontStyle.Regular, Drawing.GraphicsUnit.Point)
        self.switch_tab.Location = Drawing.Point(0, 0)
        self.switch_tab.Margin = Forms.Padding(5)
        self.switch_tab.Name = "switch_tab"
        self.switch_tab.SelectedIndex = 0
        self.switch_tab.Size = Drawing.Size(425, 535)
        self.switch_tab.TabIndex = 0
        # tabPage2
        self.tabPage2.BackColor = Drawing.Color.Transparent
        self.tabPage2.Controls.Add(self.groupBox5)
        self.tabPage2.Controls.Add(self.groupBox4)
        self.tabPage2.Controls.Add(self.groupBox3)
        self.tabPage2.Font = Drawing.Font("Arial", 9.75, Drawing.FontStyle.Regular, Drawing.GraphicsUnit.Point)
        self.tabPage2.Location = Drawing.Point(4, 25)
        self.tabPage2.Name = "tabPage2"
        self.tabPage2.Padding = Forms.Padding(3)
        self.tabPage2.Size = Drawing.Size(417, 506)
        self.tabPage2.TabIndex = 1
        self.tabPage2.Text = "Bondwire Move"
        # groupBox5
        self.groupBox5.Anchor = ((((Forms.AnchorStyles.Top | Forms.AnchorStyles.Left)| Forms.AnchorStyles.Right)))
        self.groupBox5.Controls.Add(self.label13)
        self.groupBox5.Controls.Add(self.label12)
        self.groupBox5.Controls.Add(self.label11)
        self.groupBox5.Controls.Add(self.separate_bt)
        self.groupBox5.Controls.Add(self.align_bt)
        self.groupBox5.Controls.Add(self.reverse_bt)
        self.groupBox5.Font = Drawing.Font("Arial", 9.75, Drawing.FontStyle.Regular, Drawing.GraphicsUnit.Point)
        self.groupBox5.Location = Drawing.Point(6, 314)
        self.groupBox5.Name = "groupBox5"
        self.groupBox5.Size = Drawing.Size(405, 182)
        self.groupBox5.TabIndex = 2
        self.groupBox5.TabStop = False
        self.groupBox5.Text = "Functions"
        # label13
        self.label13.AutoSize = True
        self.label13.Font = Drawing.Font("Arial", 9.75, Drawing.FontStyle.Regular, Drawing.GraphicsUnit.Point)
        self.label13.Location = Drawing.Point(141, 85)
        self.label13.Name = "label13"
        self.label13.Size = Drawing.Size(207, 16)
        self.label13.TabIndex = 5
        self.label13.Text = "\"Select Bondwires and Pt to Align\""
        # label12
        self.label12.AutoSize = True
        self.label12.Font = Drawing.Font("Arial", 9.75, Drawing.FontStyle.Regular, Drawing.GraphicsUnit.Point)
        self.label12.Location = Drawing.Point(141, 139)
        self.label12.Name = "label12"
        self.label12.Size = Drawing.Size(216, 16)
        self.label12.TabIndex = 4
        self.label12.Text = "\"Select Pad to Separate Bondwires\""
        # label11
        self.label11.AutoSize = True
        self.label11.Font = Drawing.Font("Arial", 9.75, Drawing.FontStyle.Regular, Drawing.GraphicsUnit.Point)
        self.label11.Location = Drawing.Point(141, 33)
        self.label11.Name = "label11"
        self.label11.Size = Drawing.Size(183, 16)
        self.label11.TabIndex = 3
        self.label11.Text = "\"Select Bondwires to Reverse\""
        # separate_bt
        self.separate_bt.Font = Drawing.Font("Arial", 9.75, Drawing.FontStyle.Regular, Drawing.GraphicsUnit.Point)
        self.separate_bt.Location = Drawing.Point(15, 128)
        self.separate_bt.Name = "separate_bt"
        self.separate_bt.Size = Drawing.Size(120, 40)
        self.separate_bt.TabIndex = 2
        self.separate_bt.Text = "Separate"
        self.separate_bt.UseVisualStyleBackColor = True
        self.separate_bt.Click += self.separate_bt_Click

        # align_bt
        self.align_bt.Font = Drawing.Font("Arial", 9.75, Drawing.FontStyle.Regular, Drawing.GraphicsUnit.Point)
        self.align_bt.Location = Drawing.Point(15, 74)
        self.align_bt.Name = "align_bt"
        self.align_bt.Size = Drawing.Size(120, 40)
        self.align_bt.TabIndex = 1
        self.align_bt.Text = "Aligh Center"
        self.align_bt.UseVisualStyleBackColor = True
        self.align_bt.Click += self.align_bt_Click

        # reverse_bt
        self.reverse_bt.Font = Drawing.Font("Arial", 9.75, Drawing.FontStyle.Regular, Drawing.GraphicsUnit.Point)
        self.reverse_bt.Location = Drawing.Point(15, 22)
        self.reverse_bt.Name = "reverse_bt"
        self.reverse_bt.Size = Drawing.Size(120, 40)
        self.reverse_bt.TabIndex = 0
        self.reverse_bt.Text = "Reverse"
        self.reverse_bt.UseVisualStyleBackColor = True
        self.reverse_bt.Click += self.reverse_bt_Click

        # groupBox4
        self.groupBox4.Anchor = ((((Forms.AnchorStyles.Top | Forms.AnchorStyles.Left)| Forms.AnchorStyles.Right)))
        self.groupBox4.Controls.Add(self.right_bt)
        self.groupBox4.Controls.Add(self.backward_bt)
        self.groupBox4.Controls.Add(self.left_bt)
        self.groupBox4.Controls.Add(self.forward_bt)
        self.groupBox4.Font = Drawing.Font("Arial", 9.75, Drawing.FontStyle.Regular, Drawing.GraphicsUnit.Point)
        self.groupBox4.Location = Drawing.Point(6, 97)
        self.groupBox4.Name = "groupBox4"
        self.groupBox4.Size = Drawing.Size(405, 211)
        self.groupBox4.TabIndex = 1
        self.groupBox4.TabStop = False
        self.groupBox4.Text = "Move"
        # right_bt
        self.right_bt.BackColor = Drawing.Color.Navy
        self.right_bt.Font = Drawing.Font("Arial", 12, Drawing.FontStyle.Regular, Drawing.GraphicsUnit.Point)
        self.right_bt.ForeColor = Drawing.SystemColors.ButtonHighlight
        self.right_bt.Location = Drawing.Point(262, 65)
        self.right_bt.Name = "right_bt"
        self.right_bt.Size = Drawing.Size(100, 80)
        self.right_bt.TabIndex = 3
        self.right_bt.Text = "Right"
        self.right_bt.UseVisualStyleBackColor = False
        self.right_bt.Click += self.right_bt_Click

        # backward_bt
        self.backward_bt.BackColor = Drawing.Color.Navy
        self.backward_bt.Font = Drawing.Font("Arial", 12, Drawing.FontStyle.Regular, Drawing.GraphicsUnit.Point)
        self.backward_bt.ForeColor = Drawing.SystemColors.ButtonHighlight
        self.backward_bt.Location = Drawing.Point(156, 117)
        self.backward_bt.Name = "backward_bt"
        self.backward_bt.Size = Drawing.Size(100, 80)
        self.backward_bt.TabIndex = 2
        self.backward_bt.Text = "Backward"
        self.backward_bt.UseVisualStyleBackColor = False
        self.backward_bt.Click += self.backward_bt_Click

        # left_bt
        self.left_bt.BackColor = Drawing.Color.Navy
        self.left_bt.Font = Drawing.Font("Arial", 12, Drawing.FontStyle.Regular, Drawing.GraphicsUnit.Point)
        self.left_bt.ForeColor = Drawing.SystemColors.ButtonHighlight
        self.left_bt.Location = Drawing.Point(50, 65)
        self.left_bt.Name = "left_bt"
        self.left_bt.Size = Drawing.Size(100, 80)
        self.left_bt.TabIndex = 1
        self.left_bt.Text = "Left"
        self.left_bt.UseVisualStyleBackColor = False
        self.left_bt.Click += self.left_bt_Click

        # forward_bt
        self.forward_bt.BackColor = Drawing.Color.Navy
        self.forward_bt.Font = Drawing.Font("Arial", 12, Drawing.FontStyle.Regular, Drawing.GraphicsUnit.Point)
        self.forward_bt.ForeColor = Drawing.SystemColors.ButtonHighlight
        self.forward_bt.Location = Drawing.Point(156, 21)
        self.forward_bt.Name = "forward_bt"
        self.forward_bt.Size = Drawing.Size(100, 80)
        self.forward_bt.TabIndex = 0
        self.forward_bt.Text = "Forward"
        self.forward_bt.UseVisualStyleBackColor = False
        self.forward_bt.Click += self.forward_bt_Click

        # groupBox3
        self.groupBox3.Anchor = ((((Forms.AnchorStyles.Top | Forms.AnchorStyles.Left)| Forms.AnchorStyles.Right)))
        self.groupBox3.Controls.Add(self.unit_lb)
        self.groupBox3.Controls.Add(self.label3)
        self.groupBox3.Controls.Add(self.step_tb)
        self.groupBox3.Controls.Add(self.pt1_rb)
        self.groupBox3.Controls.Add(self.pt0_rb)
        self.groupBox3.Font = Drawing.Font("Arial", 9.75, Drawing.FontStyle.Regular, Drawing.GraphicsUnit.Point)
        self.groupBox3.Location = Drawing.Point(6, 6)
        self.groupBox3.Name = "groupBox3"
        self.groupBox3.Size = Drawing.Size(405, 85)
        self.groupBox3.TabIndex = 0
        self.groupBox3.TabStop = False
        self.groupBox3.Text = "Point To Move"
        # unit_lb
        self.unit_lb.AutoSize = True
        self.unit_lb.Font = Drawing.Font("Arial", 9.75, Drawing.FontStyle.Regular, Drawing.GraphicsUnit.Point)
        self.unit_lb.Location = Drawing.Point(348, 40)
        self.unit_lb.Name = "unit_lb"
        self.unit_lb.Size = Drawing.Size(29, 16)
        self.unit_lb.TabIndex = 5
        self.unit_lb.Text = "mm"
        # label3
        self.label3.AutoSize = True
        self.label3.Font = Drawing.Font("Arial", 9.75, Drawing.FontStyle.Regular, Drawing.GraphicsUnit.Point)
        self.label3.Location = Drawing.Point(227, 40)
        self.label3.Name = "label3"
        self.label3.Size = Drawing.Size(36, 16)
        self.label3.TabIndex = 4
        self.label3.Text = "step:"
        # step_tb
        self.step_tb.Font = Drawing.Font("Arial", 9.75, Drawing.FontStyle.Regular, Drawing.GraphicsUnit.Point)
        self.step_tb.Location = Drawing.Point(269, 38)
        self.step_tb.Name = "step_tb"
        self.step_tb.Size = Drawing.Size(73, 22)
        self.step_tb.TabIndex = 3
        self.step_tb.Text = "0.01"
        self.step_tb.TextAlign = Forms.HorizontalAlignment.Center
        self.step_tb.TextChanged += self.step_tb_TextChanged

        # pt1_rb
        self.pt1_rb.AutoSize = True
        self.pt1_rb.Checked = True
        self.pt1_rb.Font = Drawing.Font("Arial", 9.75, Drawing.FontStyle.Regular, Drawing.GraphicsUnit.Point)
        self.pt1_rb.Location = Drawing.Point(70, 38)
        self.pt1_rb.Name = "pt1_rb"
        self.pt1_rb.Size = Drawing.Size(45, 20)
        self.pt1_rb.TabIndex = 2
        self.pt1_rb.TabStop = True
        self.pt1_rb.Text = "Pt1"
        self.pt1_rb.UseVisualStyleBackColor = True
        # pt0_rb
        self.pt0_rb.AutoSize = True
        self.pt0_rb.Font = Drawing.Font("Arial", 9.75, Drawing.FontStyle.Regular, Drawing.GraphicsUnit.Point)
        self.pt0_rb.Location = Drawing.Point(15, 38)
        self.pt0_rb.Name = "pt0_rb"
        self.pt0_rb.Size = Drawing.Size(45, 20)
        self.pt0_rb.TabIndex = 1
        self.pt0_rb.Text = "Pt0"
        self.pt0_rb.UseVisualStyleBackColor = True
        # Form1
        self.AutoScaleDimensions = Drawing.SizeF(7, 15)
        self.AutoScaleMode = Forms.AutoScaleMode.Font
        self.ClientSize = Drawing.Size(425, 535)
        self.Controls.Add(self.switch_tab)
        self.FormBorderStyle = Forms.FormBorderStyle.FixedSingle
        self.MaximizeBox = False
        self.MinimizeBox = False
        self.Name = "Form1"
        self.Text = "Bondwire Profile Editor"
        self.TopMost = True
        self.FormClosed += self.Form1_FormClosed

        self.Load += self.Form1_Load

        self.tabPage1.ResumeLayout(False)
        self.tabPage1.PerformLayout()
        self.groupBox1.ResumeLayout(False)
        self.groupBox1.PerformLayout()
        self.groupBox2.ResumeLayout(False)
        self.groupBox2.PerformLayout()
        self.switch_tab.ResumeLayout(False)
        self.tabPage2.ResumeLayout(False)
        self.groupBox5.ResumeLayout(False)
        self.groupBox5.PerformLayout()
        self.groupBox4.ResumeLayout(False)
        self.groupBox3.ResumeLayout(False)
        self.groupBox3.PerformLayout()
        self.ResumeLayout(False)

    def forward_bt_Click(self, sender, e):
        try:
            direction = sender.Text
            distance = float(self.step_tb.Text)
            bondwires = oEditor.GetSelections()
            point = 'Pt0' if self.pt0_rb.Checked else 'Pt1'
            
            for bondwire in bondwires:
                change(bondwire, direction, distance, point)
            oEditor.Select(bondwires)
        except:
            MessageBox.Show("Please Select Bondwires First!", 'Wrong Selection!') 
            
    def alpha_tb_TextChanged(self, sender, e):
        self.checkInputValue(sender)

    def create_bt_Click(self, sender, e):
        name = self.name_tb.Text
        profile_type = self.type_cb.SelectedIndex    
        h = self.h1_tb.Text
        a = self.alpha_tb.Text
        b = self.beta_tb.Text

        x = addProfile(name, profile_type, h, a, b)
        self.db[name] = x
        self.refreshListBox()
        self.name_tb.Text = ''

    def backward_bt_Click(self, sender, e):
        self.forward_bt_Click(sender, e)

    def left_bt_Click(self, sender, e):
        self.forward_bt_Click(sender, e)

    def align_bt_Click(self, sender, e):
        all_bondwires = oEditor.FindObjects('type', 'bondwire')
        bondwires = set(oEditor.GetSelections()).intersection(set(all_bondwires))
        
        point = 'Pt0' if self.pt0_rb.Checked else 'Pt1'
        for i in bondwires:
            alignBondwireCenter(i, point)
        oEditor.Select(list(bondwires))


    def step_tb_TextChanged(self, sender, e):
        pass

    def Form1_FormClosed(self, sender, e):
        all_bondwires = oEditor.FindObjects('type', 'bondwire')
        self.changePathWidth(list(all_bondwires))

    def ok_bt_Click(self, sender, e):
        self.ok_bt.Enabled = False 
        oDesktop.PauseScript("You can interact with AEDT now.") 

    def delete_bt_Click(self, sender, e):
        selected_profiles = [i for i in self.model_lb.SelectedItems]
        removeProfile(selected_profiles)
        self.refreshListBox()
        self.delete_bt.Enabled = False
        self.modelname_lb.Text = 'Model Name:'

    def name_tb_TextChanged(self, sender, e):
        self.checkCreateValid()

    def type_cb_SelectedIndexChanged(self, sender, e):
        try:
            bondwire_type = { 0: (False, False, False, False),
                              1: (True, False, False, self.checkApplyValid()),
                              2: (True, True, True, self.checkApplyValid()) }
 
            ( self.h1_tb.Enabled,
              self.alpha_tb.Enabled,
              self.beta_tb.Enabled,
              self.apply_bt.Enabled,) = bondwire_type[sender.SelectedIndex]
                
            self.checkCreateValid()
        except:
            pass

    def reverse_bt_Click(self, sender, e):
        all_bondwires = oEditor.FindObjects('type', 'bondwire')
        bondwires = set(oEditor.GetSelections()).intersection(set(all_bondwires))
        
        for i in bondwires:
            reverse(i)
        oEditor.Select(list(bondwires)) 

    def Form1_Load(self, sender, e):
        try:
            self.typemap = {-1: "None", 1: "JEDEC4", 2: "JEDEC5"}
            #self.x0 = self.model_lb.Items[0]
            self.delete_bt.Enabled = False
            self.create_bt.Enabled = False
            self.pw_info = {}
            self.refreshListBox()
            self.db = {}
            self.type_cb.Items.Add('None')              
            self.type_cb.Items.Add('JEDEC4')
            self.type_cb.Items.Add('JEDEC5')            
        except:
            logging.exception('error')

    def model_lb_SelectedIndexChanged(self, sender, e):
        try:
            selected_bondwires = []
            for i in range(len(self.model_lb.SelectedItems)):
                selected_bondwires += self.category[self.model_lb.SelectedItems[i]]
            N = len(selected_bondwires)
            self.modelname_lb.Text = 'Bondwires: #{}'.format(N)
            self.changePathWidth(selected_bondwires)
            oEditor.Select(selected_bondwires)
            
            self.delete_bt.Enabled = True if N == 0 else False
                    
            info = []
            for i in self.model_lb.SelectedItems:
                info.append(self.info[i])
                
                bw_type, h1, alpha, beta = zip(*info)
                if len(set(bw_type)) == 1:
                    self.type_cb.Text = self.typemap[bw_type[0]]
                else:
                    self.type_cb.Text = ''
                
                if len(set(h1)) == 1:
                    self.h1_tb.Text = h1[0]
                else:
                    self.h1_tb.Text = ''
                
                if len(set(alpha)) == 1:
                    self.alpha_tb.Text = alpha[0]
                else:
                    self.alpha_tb.Text = ''               

                if len(set(beta)) == 1:
                    self.beta_tb.Text = beta[0]
                else:
                    self.beta_tb.Text = '' 
        except:
            logging.exception('error')
            
    def beta_tb_TextChanged(self, sender, e):
        self.checkInputValue(sender)

    def right_bt_Click(self, sender, e):
        self.forward_bt_Click(sender, e)

    def separate_bt_Click(self, sender, e):
        try:
            sele = oEditor.GetSelections()
            for s in sele:
                separate(s)
            oEditor.Select(sele)
        except:
            MessageBox.Show("Please Select Package Pad!", 'Wrong Selection!')
            logging.exception('error')

    def apply_bt_Click(self, sender, e):
        try:
            profile_type = self.type_cb.SelectedIndex    
            h = self.h1_tb.Text
            a = self.alpha_tb.Text
            b = self.beta_tb.Text

            selected_profiles = [i.Text for i in self.model_lb.SelectedItems]
            
            for name in selected_profiles:
                try:
                    self.db[name].Delete()
                except:
                    pass
                x = editProfile(name, profile_type, h, a, b)
                self.db[name] = x
                
            self.refreshListBox()            
            
            for i in self.model_lb.Items:
                if i.Text in selected_profiles:
                    self.model_lb.SelectedItems.Add(i)
        except:
            logging.exception('error')

    def h1_tb_TextChanged(self, sender, e):
        self.checkInputValue(sender)

    def refreshListBox(self):
        self.modelname_lb.Text = 'Model Name:'
        self.category = getCategory()
        self.info = getProfileInfo()    
        self.model_lb.Items.Clear()
        
        for i in sorted(self.category):
            self.model_lb.Items.Add(i)
            
        self.delete_bt.Enabled = False

    def changePathWidth(self, selected_bondwires):
        x = getPW()
        for i in x:
            self.pw_info[i] = x[i]
            
        all_bondwires = oEditor.FindObjects('type', 'bondwire')
        result = {}
        for i in selected_bondwires:
            try:
                result[self.pw_info[i]] += [i]
            except:
                result[self.pw_info[i]] = [i]
        
        result['0fm'] = list(set(all_bondwires).difference(set(selected_bondwires)))
        
        for diameter in result:
            changeBondwirePathWidth(result[diameter], diameter)

    def checkApplyValid(self):
        condition = [isfloat(self.h1_tb.Text),
                     self.type_cb.SelectedIndex == 1,
                     len(self.model_lb.SelectedItems)]
        if all(condition):
            self.apply_bt.Enabled = True
            return True
        
        condition = [isfloat(self.h1_tb.Text), 
                     isfloat(self.alpha_tb.Text),
                     isfloat(self.beta_tb.Text),
                     self.type_cb.SelectedIndex == 2,
                     len(self.model_lb.SelectedItems)
                     ]
        if all(condition):
            self.apply_bt.Enabled = True
            return True
        else:
            self.apply_bt.Enabled = False
            return False
    
        
        
    def checkCreateValid(self):
        condition = [isfloat(self.h1_tb.Text),
                     self.type_cb.SelectedIndex == 1,
                     len(self.name_tb.Text) > 0,
                     self.name_tb.Text.lower() not in [i.lower() for i in self.category]
                     ]
        if all(condition):
            self.create_bt.Enabled = True
            return True
        
        condition = [isfloat(self.h1_tb.Text), 
                     isfloat(self.alpha_tb.Text),
                     isfloat(self.beta_tb.Text),
                     self.type_cb.SelectedIndex == 2,
                     len(self.name_tb.Text) > 0,
                     self.name_tb.Text.lower() not in [i.lower() for i in self.category]                     
                     ]
        if all(condition):
            self.create_bt.Enabled = True
            return True
        else:
            self.create_bt.Enabled = False
            return False    
       
    def checkInputValue(self, sender):
        if isfloat(sender.Text) and float(sender.Text) > 0:
            sender.BackColor = Color.White            
        else:
            sender.BackColor = Color.Red
            
        self.checkCreateValid()
        self.checkApplyValid()

if __name__ == '__main__':
    try:
        form = MyForm()
        form.ShowDialog()
        form = MyForm()
        form.Dispose()
        #form.Show()
        #oDesktop.PauseScript()
    except:
        logging.exception('ERROR!')
