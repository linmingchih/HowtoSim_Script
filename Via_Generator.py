_view='''[
"NAME:options",
"MajorSize:="		, "10mm",
"MinorSize:="		, "1mm",
"MajorColor:="		, 16772075,
"MinorColor:="		, 16774645,
"ShowGrid:="		, True,
"PageExtent:="		, [-0.1,-0.1,0.1,0.1],
"background color:="	, 16777215,
"DefaultToSketchMode:="	, False,
"fillMode:="		, False,
"DocVisibilityFlag:="	, 962,
"FastViewTransforms:="	, True,
"PixelSnapTolerance:="	, 20,
"SnapAcrossHierarchy:="	, True,
"SnapTargetVertex_on:="	, True,
"SnapTargetEdgeCenter_on:=", True,
"SnapTargetObjCenter_on:=", True,
"SnapTargetEdge_on:="	, False,
"SnapTargetElecConnection_on:=", True,
"SnapTargetIntersection_on:=", False,
"SnapTargetGrid_on:="	, True,
"SnapSourceVertex_on:="	, True,
"SnapSourceEdgeCenter_on:=", True,
"SnapSourceObjCenter_on:=", True,
"SnapSourceEdge_on:="	, False,
"SnapSourceElecConnection_on:=", True,
"ConstrainToGrid:="	, False,
"DirectionConstraint:="	, 0,
"defaultholesize:="	, "25mil",
"show connection points:=", False,
"draw rats:="		, False,
"display vertex labels:=", False,
"ColorByNet:="		, True,
"display package graphics:=", False,
"rectangle description:=", 0,
"snaptoport:="		, True,
"autoplacecomp:="	, False,
"AutoScale:="		, True,
"measure display digits:=", 3,
"display measure units:=", False,
"SuppressPads:="	, True,
"AntiPadsAlwaysOn:="	, False,
"primary selection color:=", 255,
"secondary selection color:=", 3289780,
"preview selection:="	, False,
"anglesnap:="		, "5deg",
"AllowDragOnFirstClick:=", False,
"PinConnectivityPopup:=", False,
"OptionUseNamingConvention_PadPort:=", False,
"OptionNamingConvention_PadPort:=", "$REFDES_$PINNAME_$NETNAME",
"OptionUseNamingConvention_EdgePort:=", False,
"OptionNamingConvention_EdgePort:=", "$NETNAME",
"OptionUseNamingConvention_PointPort:=", False,
"OptionNamingConvention_PointPort:=", "$POSTERM_LAYER_$NEGTERM_LAYER",
"OptionUseNamingConvention_PinGroup:=", False,
"OptionNamingConvention_PinGroup:=", "$REFDES_GROUP_$NETNAME",
"useFixedDrawingResolution:=", False,
"DrawingResolution:="	, "0.002mm",
"Tol:="			, [1E-08,1E-08,1E-12],
"CN:="			, "EMDesign1"
]'''

_xml='''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<c:Control xmlns:c="http://www.ansys.com/control" schemaVersion="1.0">

  <Stackup schemaVersion="1.0">
    <Materials>
      <Material Name="FR4_epoxy">
        <Permittivity>
          <Double>4.4</Double>
        </Permittivity>
        <DielectricLossTangent>
          <Double>0.02</Double>
        </DielectricLossTangent>
      </Material>
      <Material Name="copper">
        <Permeability>
          <Double>0.999991</Double>
        </Permeability>
        <Conductivity>
          <Double>58000000</Double>
        </Conductivity>
      </Material>
    </Materials>
    <Layers LengthUnit="mil">
{0}
    </Layers>
  </Stackup>

</c:Control>'''

_create_via='''[
        "NAME:Contents",
        "name:="		, "{NAME}",
        "ReferencedPadstack:="	, "PlanarEMVia",
        "vposition:="		, [			"x:="			, "{X}",			"y:="			, "{Y}"],
        "vrotation:="		, ["0deg"],
        "overrides hole:="	, False,
        "hole diameter:="	, ["$D_Drill"],
        "Pin:="			, False,
        "highest_layer:="	, "layer1",
        "lowest_layer:="	, "layer{N}"
    ]'''

_change_via='''[
        "NAME:AllTabs",
        [
            "NAME:BaseElementTab",
            [
                "NAME:PropServers", 
                "{NAME}"
            ],
            [
                "NAME:ChangedProps",
                [
                    "NAME:Net",
                    "Value:="		, "{NET}"
                ],
                [
                    "NAME:Padstack Usage",
                    "Start Layer:="		, "layer1",
                    "Stop Layer:="		, "layer{N}",
                    "SolderBallLayer:="	, "",
                    [
                        "NAME:LayerMap",
                        "LayoutToDef:="		, [{REF}]
                    ],
                    "ApplyDefChanges:="	, 1,
                    [
                        "NAME:PadstackDef",
                        "nam:="			, "PlanarEMVia",
                        "lib:="			, "",
                        "mat:="			, "",
                        "plt:="			, "100",
                        [
                            "NAME:pds",
                            [
                                "NAME:lgm",
                                "lay:="			, "layer1",
                                "id:="			, 1,
                                "pad:="			, [									"shp:="			, "Cir",									"Szs:="			, ["$D_pad"],									"X:="			, "0mm",									"Y:="			, "0mm",									"R:="			, "0deg"],
                                "ant:="			, [									"shp:="			, "Cir",									"Szs:="			, ["$D_antipad"],									"X:="			, "0mm",									"Y:="			, "0mm",									"R:="			, "0deg"],
                                "thm:="			, [									"shp:="			, "No",									"Szs:="			, [],									"X:="			, "0mm",									"Y:="			, "0mm",									"R:="			, "0deg"],
                                "X:="			, "0",
                                "Y:="			, "0",
                                "dir:="			, "No"
                            ]
                        ],
                        "hle:="			, [							"shp:="			, "Cir",							"Szs:="			, ["$D_Drill"],							"X:="			, "0mm",							"Y:="			, "0mm",							"R:="			, "0deg"],
                        "hRg:="			, "UTL",
                        "sbsh:="		, "None",
                        "sbpl:="		, "abv",
                        "sbr:="			, "0mm",
                        "sb2:="			, "0mm",
                        "sbn:="			, ""
                    ],
                    [
                        "NAME:BackDrill",
                        "BackdrillTop:="	, "",
                        "BackdrillTopDiameter:=", "0",
                        "BackdrillBot:="	, "",
                        "BackdrillBotDiameter:=", "0"
                    ]
                ]
            ]
        ]
    ]'''

_rect='''[
    "NAME:Contents",
    "rectGeometry:="	, [			"Name:="		, "rect_{}",			"LayerName:="		, "layer"+str(i+1),			"lw:="			, "0",			"Ax:="			, "-10mm",			"Ay:="			, "5mm",			"Bx:="			, "10mm",			"By:="			, "-5mm",			"cr:="			, "0mm",			"ang:="			, "0deg"]
]'''

_rect_property='''[
    "NAME:AllTabs",
    [
        "NAME:BaseElementTab",
        [
            "NAME:PropServers", 
            "rect_{}"
        ],
        [
            "NAME:ChangedProps",
            [
                "NAME:Net",
                "Value:="		, "GND"
            ]
        ]
    ]
]'''
    
_layer='''<Layer Color="#d63b07" FillMaterial="FR4_epoxy" Material="copper" Name="layer{0}" Thickness="1" Type="conductor"/>'''

_diele='''<Layer Color="#264a33" Material="FR4_epoxy" Name="Dielectric{0}" Thickness="10" Type="dielectric"/>'''

_var='''[
    "NAME:AllTabs",
    [
        "NAME:ProjectVariableTab",
        [
            "NAME:PropServers", 
            "ProjectVariables"
        ],
        [
            "NAME:NewProps",
            [
                "NAME:{K}",
                "PropType:="		, "VariableProp",
                "UserDef:="		, True,
                "Value:="		, "{V}"
            ]
        ]
    ]
]'''

_line='''[
    "NAME:Contents",
    "lineGeometry:="	, [			"Name:="		, "{NAME}",			"LayerName:="		, "{LAYER}",			"lw:="			, "{LW}",			"endstyle:="		, 0,			"StartCap:="		, 0,			"n:="			, 3,			"U:="			, "mm",			"x:="			, {X1},			"y:="			, {Y1},			"x:="			, {X2},			"y:="			, {Y2},			"x:="			, {X3},			"y:="			, {Y3}]
]'''




class via_wizard():    
    def __init__(self, n, inlayer, outlayer):

        self.n=n
        self.inlayer=inlayer
        self.outlayer=outlayer
        
        import ScriptEnv        
        ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
        oDesktop.RestoreWindow()
        self.oProject = oDesktop.NewProject()
        self.oProject.InsertDesign("HFSS 3D Layout Design", "EMDesign1", "", "")        
        self.oDesign = self.oProject.SetActiveDesign("EMDesign1")
        self.oEditor = self.oDesign.SetActiveEditor("Layout")
        self.oEditor.ChangeOptions(eval(_view))
   
    def genVariable(self):
        for key in self.var_dic:
            x=eval(_var.format(K=key, V=self.var_dic[key]))
            self.oProject.ChangeProperty(x)
    
    def genStackup(self):
        s=[]
        for i in range(self.n-1):
            s.append(' '*6+_layer.format(i+1))
            s.append(' '*6+_diele.format(i+1))
        s.append(' '*6+_layer.format(self.n))
        with open ("stackup.xml",'w') as f:
            f.write(_xml.format('\n'.join(s)))  
        
        self.oEditor.ImportStackupXML("stackup.xml")
    
    def genGND(self):
        planes=[i for i in range(self.n) if i not in [self.inlayer-1, self.outlayer-1]]
        for i in planes:
            x=eval(_rect.format(i+1))
            self.oEditor.CreateRectangle(x)
            x=eval(_rect_property.format(i+1))
            self.oEditor.ChangeProperty(x)
    
    def genVia(self, x, y, name, net):
        x=eval(_create_via.format(X=x, Y=y, N=self.n, NAME=name))
        self.oEditor.CreateVia(x)
        
        ref=','.join(['"layer{0}:=","layer1"'.format(i+1) for i in range(self.n)])
        x=eval(_change_via.format(N=self.n, NAME=name, REF=ref, NET=net))
        self.oEditor.ChangeProperty(x)   
    
    def genInOut(self):
        oEditor=self.oEditor
        oEditor.CreateLine(
            [
                "NAME:Contents",
                "lineGeometry:="	, [			"Name:="		, "in_p",			"LayerName:="		, "layer"+str(self.inlayer),			"lw:="			, "$in_lw",			"endstyle:="		, 0,			"StartCap:="		, 0,			"n:="			, 3,			"U:="			, "mm",			"x:="			, "-$dist/2",			"y:="			, 0,			"x:="			, "-$in_dist/2",			"y:="			, "-abs($dist-$in_dist)/2",			"x:="			, "-$in_dist/2",			"y:="			, -5]
            ])
        oEditor.ChangeProperty(
            [
                "NAME:AllTabs",
                [
                    "NAME:BaseElementTab",
                    [
                        "NAME:PropServers", 
                        "in_p"
                    ],
                    [
                        "NAME:ChangedProps",
                        [
                            "NAME:Net",
                            "Value:="		, "sig_p"
                        ]
                    ]
                ]
            ])
            
        #-----------------------------
        oEditor.CreateLine(
            [
                "NAME:Contents",
                "lineGeometry:="	, [			"Name:="		, "in_n",			"LayerName:="		, "layer"+str(self.inlayer),			"lw:="			, "$in_lw",			"endstyle:="		, 0,			"StartCap:="		, 0,			"n:="			, 3,			"U:="			, "mm",			"x:="			, "$dist/2",			"y:="			, 0,			"x:="			, "$in_dist/2",			"y:="			, "-abs($dist-$in_dist)/2",			"x:="			, "$in_dist/2",			"y:="			, -5]
            ])
        oEditor.ChangeProperty(
            [
                "NAME:AllTabs",
                [
                    "NAME:BaseElementTab",
                    [
                        "NAME:PropServers", 
                        "in_n"
                    ],
                    [
                        "NAME:ChangedProps",
                        [
                            "NAME:Net",
                            "Value:="		, "sig_n"
                        ]
                    ]
                ]
            ])
        #--------------------------------

        oEditor.CreateLine(
            [
                "NAME:Contents",
                "lineGeometry:="	, [			"Name:="		, "out_p",			"LayerName:="		, "layer"+str(self.outlayer),			"lw:="			, "$out_lw",			"endstyle:="		, 0,			"StartCap:="		, 0,			"n:="			, 3,			"U:="			, "mm",			"x:="			, "-$dist/2",			"y:="			, 0,			"x:="			, "-$out_dist/2",			"y:="			, "abs($dist-$out_dist)/2",			"x:="			, "-$out_dist/2",			"y:="			, 5]
            ])
        oEditor.ChangeProperty(
            [
                "NAME:AllTabs",
                [
                    "NAME:BaseElementTab",
                    [
                        "NAME:PropServers", 
                        "out_p"
                    ],
                    [
                        "NAME:ChangedProps",
                        [
                            "NAME:Net",
                            "Value:="		, "sig_p"
                        ]
                    ]
                ]
            ])

        #-------------------------------
        oEditor.CreateLine(
            [
                "NAME:Contents",
                "lineGeometry:="	, [			"Name:="		, "out_n",			"LayerName:="		, "layer"+str(self.outlayer),			"lw:="			, "$out_lw",			"endstyle:="		, 0,			"StartCap:="		, 0,			"n:="			, 3,			"U:="			, "mm",			"x:="			, "$dist/2",			"y:="			, 0,			"x:="			, "$out_dist/2",			"y:="			, "abs($dist-$out_dist)/2",			"x:="			, "$out_dist/2",			"y:="			, 5]
            ])
        oEditor.ChangeProperty(
            [
                "NAME:AllTabs",
                [
                    "NAME:BaseElementTab",
                    [
                        "NAME:PropServers", 
                        "out_n"
                    ],
                    [
                        "NAME:ChangedProps",
                        [
                            "NAME:Net",
                            "Value:="		, "sig_n"
                        ]
                    ]
                ]
            ])
    
    
    
    def show(self):
        self.var_dic={  '$D_drill'  :'1mm', 
                        '$D_pad'    :'2mm', 
                        '$D_antipad':'3mm', 
                        '$dist'     :'4mm',
                        '$via_gap'  :'5mm',
                        '$in_lw'    :'1mm',
                        '$in_dist'  :'2mm',                      
                        '$out_lw'   :'1mm',
                        '$out_dist' :'2mm',
                        }    
        self.genVariable()
        self.genStackup()
        self.genGND()
        self.genVia(x='-$dist/2',y='0mm', name='via_n', net='sig_p')
        self.genVia(x='$dist/2',y='0mm', name='via_p', net='sig_n')   
        self.genVia(x='-$dist/2-$via_gap',y='0mm', name='gn', net='GND')
        self.genVia(x='$dist/2+$via_gap',y='0mm', name='gp', net='GND')
        self.genInOut()
        self.oEditor.ZoomToFit()

import clr
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')

from System.Drawing import Point
from System.Windows.Forms import Application, Button, Form, Label, TextBox

class SimpleTextBoxForm(Form):
    def __init__(self):
        self.Text = "Via Generator"

        self.Width = 300
        self.Height = 200

        self.label1 = Label()
        self.label1.Text = "Number of Layers:"
        self.label1.Location = Point(50, 25)
        self.label1.Height = 25
        self.label1.Width = 120

        self.textbox1 = TextBox()
        self.textbox1.Text = "8"
        self.textbox1.Location = Point(200, 25)
        self.textbox1.Width = 50

        self.label2 = Label()
        self.label2.Text = "Input Layer:"
        self.label2.Location = Point(50, 50)
        self.label2.Height = 25
        self.label2.Width = 120

        self.textbox2 = TextBox()
        self.textbox2.Text = "1"
        self.textbox2.Location = Point(200, 50)
        self.textbox2.Width = 50        
        
        self.label3 = Label()
        self.label3.Text = "Output Layer:"
        self.label3.Location = Point(50, 75)
        self.label3.Height = 25
        self.label3.Width = 120

        self.textbox3 = TextBox()
        self.textbox3.Text = "8"
        self.textbox3.Location = Point(200, 75)
        self.textbox3.Width = 50   
        
        self.button1 = Button()
        self.button1.Text = 'Generate'
        self.button1.Location = Point(25, 125)
        self.button1.Click += self.update


        self.AcceptButton = self.button1


        self.Controls.Add(self.label1)
        self.Controls.Add(self.label2)
        self.Controls.Add(self.label3)        
        self.Controls.Add(self.textbox1)
        self.Controls.Add(self.textbox2)
        self.Controls.Add(self.textbox3)        
        self.Controls.Add(self.button1)


    def update(self, sender, event):
        vw=via_wizard(int(self.textbox1.Text), int(self.textbox2.Text), int(self.textbox3.Text))
        vw.show()


form = SimpleTextBoxForm()
Application.Run(form)        

