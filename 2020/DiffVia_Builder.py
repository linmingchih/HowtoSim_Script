import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.NewProject()
oProject.InsertDesign("HFSS", "ViaModel", "DrivenModal", "")
oDesign = oProject.GetActiveDesign()
oDesign.SetSolutionType("DrivenTerminal", False)
oEditor = oDesign.SetActiveEditor("3D Modeler")
oDesktop.ClearMessages('','',2)

unit='mil'

def setOverride():
    oDesign.SetDesignSettings(
        [
            "NAME:Design Settings Data",
            "Use Advanced DC Extrapolation:=", False,
            "Use Power S:="		, False,
            "Export After Simulation:=", False,
            "Allow Material Override:=", True,
            "Calculate Lossy Dielectrics:=", True,
            "Perform Minimal validation:=", False,
            "EnabledObjects:="	, [],
            "Port Validation Settings:=", "Standard"
        ], 
        [
            "NAME:Model Validation Settings",
            "EntityCheckLevel:="	, "Strict",
            "IgnoreUnclassifiedObjects:=", False,
            "SkipIntersectionChecks:=", False
        ])


def createDielectric(name, height, elevation, material='FR4_epoxy'):
    return oEditor.CreateBox(
        [
            "NAME:BoxParameters",
            "XPosition:="		, "{}{}".format(-offset, unit),
            "YPosition:="		, "{}{}".format(-width/2, unit),
            "ZPosition:="		, "{}{}".format(elevation, unit),
            "XSize:="		, "{}{}".format(offset+length, unit),
            "YSize:="		, "{}{}".format(width, unit),
            "ZSize:="		, "{}{}".format(height, unit)
        ], 
        [
            "NAME:Attributes",
            "Name:="		, "{}".format(name),
            "Flags:="		, "",
            "Color:="		, "(198 225 132)",
            "Transparency:="	, 0.9,
            "PartCoordinateSystem:=", "Global",
            "UDMId:="		, "",
            "MaterialValue:="	, "\"{}\"".format(material),
            "SurfaceMaterialValue:=", "\"\"",
            "SolveInside:="		, True,
            "IsMaterialEditable:="	, True,
            "UseMaterialAppearance:=", False,
            "IsLightweight:="	, False
        ])
        
def createMetal(name, height, elevation, material='copper', color="(255 0 132)"):
    return oEditor.CreateBox(
        [
            "NAME:BoxParameters",
            "XPosition:="		, "{}{}".format(-offset, unit),
            "YPosition:="		, "{}{}".format(-width/2, unit),
            "ZPosition:="		, "{}{}".format(elevation, unit),
            "XSize:="		, "{}{}".format(offset+length, unit),
            "YSize:="		, "{}{}".format(width, unit),
            "ZSize:="		, "{}{}".format(height, unit)
        ], 
        [
            "NAME:Attributes",
            "Name:="		, "{}".format(name),
            "Flags:="		, "",
            "Color:="		, color,
            "Transparency:="	, 0.8,
            "PartCoordinateSystem:=", "Global",
            "UDMId:="		, "",
            "MaterialValue:="	, "\"{}\"".format(material),
            "SurfaceMaterialValue:=", "\"\"",
            "SolveInside:="		, False,
            "IsMaterialEditable:="	, True,
            "UseMaterialAppearance:=", False,
            "IsLightweight:="	, False
        ])

def createVoid(radius, height, width, elevation):
    x=oEditor.CreateBox(
        [
            "NAME:BoxParameters",
            "XPosition:="		, "{}{}".format(-radius, unit),
            "YPosition:="		, "{}{}".format(-width/2, unit),
            "ZPosition:="		, "{}{}".format(elevation, unit),
            "XSize:="		, "{}{}".format(2*radius, unit),
            "YSize:="		, "{}{}".format(width, unit),
            "ZSize:="		, "{}{}".format(height, unit)
        ], 
        [
            "NAME:Attributes",
            "Name:="		, "Cylinder1",
            "Flags:="		, "NonModel#",
            "Color:="		, "(198 225 132)",
            "Transparency:="	, 0,
            "PartCoordinateSystem:=", "Global",
            "UDMId:="		, "",
            "MaterialValue:="	, "\"vacuum\"",
            "SurfaceMaterialValue:=", "\"\"",
            "SolveInside:="		, True,
            "IsMaterialEditable:="	, True,
            "UseMaterialAppearance:=", False,
            "IsLightweight:="	, False
        ])
        
    y=oEditor.CreateCylinder(
        [
            "NAME:CylinderParameters",
            "XCenter:="		, "{}{}".format(0, unit),
            "YCenter:="		, "{}{}".format(-width/2, unit),
            "ZCenter:="		, "{}{}".format(elevation, unit),
            "Radius:="		, "{}{}".format(radius, unit),
            "Height:="		, "{}{}".format(height, unit),
            "WhichAxis:="		, "Z",
            "NumSides:="		, "0"
        ], 
        [
            "NAME:Attributes",
            "Name:="		, "Cylinder1",
            "Flags:="		, "NonModel#",
            "Color:="		, "(198 225 132)",
            "Transparency:="	, 0,
            "PartCoordinateSystem:=", "Global",
            "UDMId:="		, "",
            "MaterialValue:="	, "\"vacuum\"",
            "SurfaceMaterialValue:=", "\"\"",
            "SolveInside:="		, True,
            "IsMaterialEditable:="	, True,
            "UseMaterialAppearance:=", False,
            "IsLightweight:="	, False
        ])
    z=oEditor.CreateCylinder(
        [
            "NAME:CylinderParameters",
            "XCenter:="		, "{}{}".format(0, unit),
            "YCenter:="		, "{}{}".format(width/2, unit),
            "ZCenter:="		, "{}{}".format(elevation, unit),
            "Radius:="		, "{}{}".format(radius, unit),
            "Height:="		, "{}{}".format(height, unit),
            "WhichAxis:="		, "Z",
            "NumSides:="		, "0"
        ], 
        [
            "NAME:Attributes",
            "Name:="		, "Cylinder1",
            "Flags:="		, "NonModel#",
            "Color:="		, "(198 225 132)",
            "Transparency:="	, 0,
            "PartCoordinateSystem:=", "Global",
            "UDMId:="		, "",
            "MaterialValue:="	, "\"vacuum\"",
            "SurfaceMaterialValue:=", "\"\"",
            "SolveInside:="		, True,
            "IsMaterialEditable:="	, True,
            "UseMaterialAppearance:=", False,
            "IsLightweight:="	, False
        ])
    # oEditor.Unite(
        # [
            # "NAME:Selections",
            # "Selections:="		, "{},{},{}".format(x,y,z)
        # ], 
        # [
            # "NAME:UniteParameters",
            # "KeepOriginals:="	, False
        # ])
    return [x, y, z]        

def createvia(radius, height, locx, locy, elevation, name="viaP", material='copper'):
    solveinside=True if material not in ['copper', 'pec'] else False
    
    x=oEditor.CreateCylinder(
        [
            "NAME:CylinderParameters",
            "XCenter:="		, "{}{}".format(locx, unit),
            "YCenter:="		, "{}{}".format(-locy, unit),
            "ZCenter:="		, "{}{}".format(elevation, unit),
            "Radius:="		, "{}{}".format(radius, unit),
            "Height:="		, "{}{}".format(height, unit),
            "WhichAxis:="		, "Z",
            "NumSides:="		, "0"
        ], 
        [
            "NAME:Attributes",
            "Name:="		, name,
            "Flags:="		, "",
            "Color:="		, "(255 28 64)",
            "Transparency:="	, 0,
            "PartCoordinateSystem:=", "Global",
            "UDMId:="		, "",
            "MaterialValue:="	, '\"{}\"'.format(material),
            "SurfaceMaterialValue:=", "\"\"",
            "SolveInside:="		, solveinside,
            "IsMaterialEditable:="	, True,
            "UseMaterialAppearance:=", False,
            "IsLightweight:="	, False
        ])
    return [x]
  
    
def createviaPair(radius, height, locx, locy, elevation, name='via', material='copper'):
    x = createvia(radius, height, locx, locy, elevation, name="{}P".format(name), material=material)
    y = createvia(radius, height, locx, -locy, elevation, name="{}N".format(name), material=material)
    return x+y
        
def subtract(A_list, B_list, KeepOriginals=False):
    oEditor.Subtract(
        [
            "NAME:Selections",
            "Blank Parts:="		, ','.join(A_list),
            "Tool Parts:="		, ','.join(B_list)
        ], 
        [
            "NAME:SubtractParameters",
            "KeepOriginals:="	, KeepOriginals
        ])

def createPair(viawidth, line_width, line_spacing, height, elevation, material='copper'):
    dx=0 if perp else void_radius+line_width/2
    
    x=oEditor.CreatePolyline(
        [
            "NAME:PolylineParameters",
            "IsPolylineCovered:="	, True,
            "IsPolylineClosed:="	, False,
            [
                "NAME:PolylinePoints",
                [
                    "NAME:PLPoint",
                    "X:="			, "{}{}".format(0, unit),
                    "Y:="			, "{}{}".format(viawidth/2, unit),
                    "Z:="			, "{}{}".format(elevation+height/2, unit)
                ],
                [
                    "NAME:PLPoint",
                    "X:="			, "{}{}".format(dx, unit),
                    "Y:="			, "{}{}".format((line_width+line_spacing)/2, unit),
                    "Z:="			, "{}{}".format(elevation+height/2, unit)
                ],
                [
                    "NAME:PLPoint",
                    "X:="			, "{}{}".format(length, unit),
                    "Y:="			, "{}{}".format((line_width+line_spacing)/2, unit),
                    "Z:="			, "{}{}".format(elevation+height/2, unit)
                ]
            ],
            [
                "NAME:PolylineSegments",
                [
                    "NAME:PLSegment",
                    "SegmentType:="		, "Line",
                    "StartIndex:="		, 0,
                    "NoOfPoints:="		, 2
                ],
                [
                    "NAME:PLSegment",
                    "SegmentType:="		, "Line",
                    "StartIndex:="		, 1,
                    "NoOfPoints:="		, 2
                ]
            ],
            [
                "NAME:PolylineXSection",
                "XSectionType:="	, "Rectangle",
                "XSectionOrient:="	, "Auto",
                "XSectionWidth:="	, "{}{}".format(line_width, unit),
                "XSectionTopWidth:="	, "{}{}".format(line_width, unit),
                "XSectionHeight:="	, "{}{}".format(height, unit),
                "XSectionNumSegments:="	, "0",
                "XSectionBendType:="	, "Curved"
            ]
        ], 
        [
            "NAME:Attributes",
            "Name:="		, "pairP",
            "Flags:="		, "",
            "Color:="		, "(255 28 64)",
            "Transparency:="	, 0,
            "PartCoordinateSystem:=", "Global",
            "UDMId:="		, "",
            "MaterialValue:="	, "\"{}\"".format(material),
            "SurfaceMaterialValue:=", "\"\"",
            "SolveInside:="		, False,
            "IsMaterialEditable:="	, True,
            "UseMaterialAppearance:=", False,
            "IsLightweight:="	, False
        ])
        
    y=oEditor.CreatePolyline(
        [
            "NAME:PolylineParameters",
            "IsPolylineCovered:="	, True,
            "IsPolylineClosed:="	, False,
            [
                "NAME:PolylinePoints",
                [
                    "NAME:PLPoint",
                    "X:="			, "{}{}".format(0, unit),
                    "Y:="			, "{}{}".format(-viawidth/2, unit),
                    "Z:="			, "{}{}".format(elevation+height/2, unit)
                ],
                [
                    "NAME:PLPoint",
                    "X:="			, "{}{}".format(dx, unit),
                    "Y:="			, "{}{}".format(-(line_width+line_spacing)/2, unit),
                    "Z:="			, "{}{}".format(elevation+height/2, unit)
                ],
                [
                    "NAME:PLPoint",
                    "X:="			, "{}{}".format(length, unit),
                    "Y:="			, "{}{}".format(-(line_width+line_spacing)/2, unit),
                    "Z:="			, "{}{}".format(elevation+height/2, unit)
                ]
            ],
            [
                "NAME:PolylineSegments",
                [
                    "NAME:PLSegment",
                    "SegmentType:="		, "Line",
                    "StartIndex:="		, 0,
                    "NoOfPoints:="		, 2
                ],
                [
                    "NAME:PLSegment",
                    "SegmentType:="		, "Line",
                    "StartIndex:="		, 1,
                    "NoOfPoints:="		, 2
                ]
            ],
            [
                "NAME:PolylineXSection",
                "XSectionType:="	, "Rectangle",
                "XSectionOrient:="	, "Auto",
                "XSectionWidth:="	, "{}{}".format(line_width, unit),
                "XSectionTopWidth:="	, "{}{}".format(line_width, unit),
                "XSectionHeight:="	, "{}{}".format(height, unit),
                "XSectionNumSegments:="	, "0",
                "XSectionBendType:="	, "Curved"
            ]
        ], 
        [
            "NAME:Attributes",
            "Name:="		, "pairN",
            "Flags:="		, "",
            "Color:="		, "(255 28 64)",
            "Transparency:="	, 0,
            "PartCoordinateSystem:=", "Global",
            "UDMId:="		, "",
            "MaterialValue:="	, "\"{}\"".format(material),
            "SurfaceMaterialValue:=", "\"\"",
            "SolveInside:="		, False,
            "IsMaterialEditable:="	, True,
            "UseMaterialAppearance:=", False,
            "IsLightweight:="	, False
        ])
    return [x, y]
    
def createMaterial(name, dk, tanD):

    oDefinitionManager = oProject.GetDefinitionManager()
    oDefinitionManager.AddMaterial(
        [
            "NAME:{}".format(name),
            "CoordinateSystemType:=", "Cartesian",
            "BulkOrSurfaceType:="	, 1,
            [
                "NAME:PhysicsTypes",
                "set:="			, ["Electromagnetic"]
            ],
            "permittivity:="	, "{}".format(dk),
            "dielectric_loss_tangent:=", "{}".format(tanD)
        ])

def addVariable(name, value):    
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
                        "NAME:{}".format(name),
                        "PropType:="		, "VariableProp",
                        "UserDef:="		, True,
                        "Value:="		, value
                    ]
                ]
            ]
        ])


def createPGvia(locx, locy, name='PGvia',type='GND'):
    outside_barrel=createvia(radius=via_radius, height=viatop, locx=locx, locy=locy,name=name, elevation=viabot, material='copper')
    inside_barrel=createvia(radius=via_radius-via_coating, height=pcb_thickness_minus_topmask, locx=locx, locy=locy, elevation=0, material='copper')
    
    padsTop=createvia(radius=via_pad_radius, height=elevation_dic[top_signal_layer][0], locx=locx, locy=locy, elevation=elevation_dic[top_signal_layer][1], name=name+'toppad', material='copper')
    padsBot=createvia(radius=via_pad_radius, height=elevation_dic[bot_signal_layer][0], locx=locx, locy=locy, elevation=elevation_dic[bot_signal_layer][1], name=name+'botpad', material='copper')
    
    subtract(outside_barrel + padsTop + padsBot + alllayers, inside_barrel)

    #Create voids of ground vias
    void_radius=void_radius_GNDvia if type=='GND' else void_radius_PWRvia
    gnd_via_antipad=createviaPair(radius=void_radius, height=pcb_thickness_minus_topmask, locx=locx, locy=locy, elevation=0, material='copper')
    if type=='GND':
        subtract(powerlayers, gnd_via_antipad)
        createvia(radius=ground_lead_radius, height=topmask_thickness, locx=locx, locy=locy, elevation=pcb_thickness_minus_topmask, material='pec')
    else:
        subtract(groundlayers, gnd_via_antipad)  

       
        
def createPGviaPair(locx, locy, name='PGvias', type='GND'):
    outside_barrel=createviaPair(radius=via_radius, height=viatop, locx=locx, locy=locy, elevation=viabot, name=name, material='copper')
    inside_barrel=createviaPair(radius=via_radius-via_coating, height=pcb_thickness_minus_topmask, locx=locx, locy=locy, elevation=0, material='copper')
    
    padsTop=createviaPair(radius=via_pad_radius, height=elevation_dic[top_signal_layer][0], locx=locx, locy=locy, elevation=elevation_dic[top_signal_layer][1], name=name+'top_pad', material='copper')
    padsBot=createviaPair(radius=via_pad_radius, height=elevation_dic[bot_signal_layer][0], locx=locx, locy=locy, elevation=elevation_dic[bot_signal_layer][1], name=name+'bot_pad', material='copper')
    
    subtract(outside_barrel + padsTop + padsBot+alllayers, inside_barrel)

    #Create voids of ground vias
    void_radius=void_radius_GNDvia if type=='GND' else void_radius_PWRvia
    gnd_via_antipad=createviaPair(radius=void_radius, height=pcb_thickness_minus_topmask, locx=locx, locy=locy, elevation=0, material='copper')
    if type=='GND':
        subtract(powerlayers, gnd_via_antipad)
        createviaPair(radius=ground_lead_radius, height=topmask_thickness, locx=locx, locy=locy, elevation=pcb_thickness_minus_topmask, material='pec')    
    else:
        subtract(groundlayers, gnd_via_antipad)
   
def readStackup(x):
    global stackup, stack_bottomup, elevation_dic
    stackup=[]
    for i in x.splitlines():
        j=i.strip()
        if len(j)==0:
            continue
        else:
            stype, name, thickness, material = j.split(',')
            assert stype in ['signal','power','ground','dielectric'], "{} type is not supported".format(stype)
            stackup.append((stype.strip(), name.strip(), float(thickness), material.strip()))

    stack_bottomup=stackup[::-1]
    elevation_dic={}
    elevation=0
    for _, name, height, material in stack_bottomup:
        elevation_dic[name]=(height, elevation)
        elevation+=height
        
    global metallayers, powerlayers, groundlayers, signallayers, alllayers, signal_metal_layers

    powerlayers=[i[1] for i in stack_bottomup if i[0]=='power']
    groundlayers=[i[1] for i in stack_bottomup if i[0]=='ground']
    metallayers=[i[1] for i in stack_bottomup if i[0]=='ground' or i[0]=='power']
    signal_metal_layers=[i[1] for i in stack_bottomup if i[0]=='ground' or i[0]=='power' or i[0]=='signal']

    signallayers=[i[1] for i in stack_bottomup if i[0]=='signal']
    alllayers=[i[1] for i in stack_bottomup]
    topmostlayer=alllayers[-1]
    

    
    global pcb_thickness, pcb_thickness_minus_topmask, topmask_thickness
    pcb_thickness_minus_topmask=elevation_dic[topmostlayer][1]
    topmask_thickness=elevation_dic[topmostlayer][0]
    pcb_thickness=pcb_thickness_minus_topmask+topmask_thickness

    global top_signal_layer, bot_signal_layer, viatop, viabot, H1, L1
    top_signal_layer=signallayers[-1]
    H1=elevation_dic[metallayers[-1]][1]-elevation_dic[metallayers[-2]][1] #gap betwee metal1 and metal2, used for caox feed
    L1=elevation_dic[metallayers[-1]][0] #thickness of metal1, used for coax feed
    bot_signal_layer=signallayers[0]
    viatop=elevation_dic[top_signal_layer][1]
    viabot=elevation_dic[bot_signal_layer][1]

  

def createWavePort():
    global layer_above_outlayer, layer_below_outlayer
    layer_above_outlayer= signal_metal_layers[signal_metal_layers.index(outlayer)-1]
    layer_below_outlayer= signal_metal_layers[signal_metal_layers.index(outlayer)+1]
    
    low=elevation_dic[layer_above_outlayer][1]
    high=elevation_dic[layer_below_outlayer][1]+elevation_dic[layer_below_outlayer][0]
    width_port=3*(2*line_width+line_spacing)
    oEditor.CreateRectangle(
        [
            "NAME:RectangleParameters",
            "IsCovered:="		, True,
            "XStart:="		, "{}{}".format(length, unit),
            "YStart:="		, "{}{}".format(-width_port/2, unit),
            "ZStart:="		, "{}{}".format(low, unit),
            "Width:="		, "{}{}".format(width_port, unit),
            "Height:="		, "{}{}".format(high-low, unit),
            "WhichAxis:="		, "X"
        ], 
        [
            "NAME:Attributes",
            "Name:="		, "OutPort",
            "Flags:="		, "",
            "Color:="		, "(255 0 255)",
            "Transparency:="	, 0.5,
            "PartCoordinateSystem:=", "Global",
            "UDMId:="		, "",
            "MaterialValue:="	, "\"vacuum\"",
            "SurfaceMaterialValue:=", "\"\"",
            "SolveInside:="		, True,
            "IsMaterialEditable:="	, True,
            "UseMaterialAppearance:=", False,
            "IsLightweight:="	, False
        ])    
    face_number=oEditor.GetFaceIDs("OutPort")[0]
    oModule = oDesign.GetModule("BoundarySetup")
    oModule.AutoIdentifyPorts(
	[
		"NAME:Faces", 
		face_number
	], True, 
	[
		"NAME:ReferenceConductors", 
		layer_above_outlayer, 
		layer_below_outlayer
	], "1", True)
    
    oDesign.ChangeProperty(
        [
            "NAME:AllTabs",
            [
                "NAME:HfssTab",
                [
                    "NAME:PropServers", 
                    "BoundarySetup:1"
                ],
                
                [
                
                    "NAME:ChangedProps",
                    [
                        "NAME:Deembed",
                        "Value:="		, True
                    ],               
                    [
                        "NAME:Deembed Dist",
                        "Value:="		, "{}{}".format(length-void_radius_Signal, unit)
                    ]

                ]
            ]
        ])   

def createTopPEC():
    oEditor.CreateRectangle(
        [
            "NAME:RectangleParameters",
            "IsCovered:="		, True,
            "XStart:="		, "{}{}".format(-offset,unit),
            "YStart:="		, "{}{}".format(-width/2,unit),
            "ZStart:="		, "{}{}".format(pcb_thickness,unit),
            "Width:="		, "{}{}".format(offset+length,unit),
            "Height:="		, "{}{}".format(width,unit),
            "WhichAxis:="		, "Z"
        ], 
        [
            "NAME:Attributes",
            "Name:="		, "topPEC",
            "Flags:="		, "",
            "Color:="		, "(255 255 0)",
            "Transparency:="	, 0.5,
            "PartCoordinateSystem:=", "Global",
            "UDMId:="		, "",
            "MaterialValue:="	, "\"vacuum\"",
            "SurfaceMaterialValue:=", "\"\"",
            "SolveInside:="		, True,
            "IsMaterialEditable:="	, True,
            "UseMaterialAppearance:=", False,
            "IsLightweight:="	, False
        ])
        
    void=createviaPair(Coaxdie, CoaxouterLength, 0, via_width/2, pcb_thickness_minus_topmask, name='PEC_void', material='copper')    
    subtract(["topPEC"], void)    
        
    oModule = oDesign.GetModule("BoundarySetup")
    oModule.AssignPerfectE(
        [
            "NAME:PerfE1",
            "Objects:="		, ["topPEC"],
            "InfGroundPlane:="	, False
        ])

def createCoax():
    global CoaxcenterLength, CoaxouterLength, Coaxouter, Coaxcenter, Coaxdie
    CoaxcenterLength= H1*0.6+(L1/0.2)*0.4
    CoaxouterLength = H1*0.6-(L1/0.2)*0.4   
    Coaxouter=via_pad_radius
    Coaxcenter=via_radius-via_coating
    Coaxdie=Coaxouter*0.9  

    outer=createviaPair(Coaxouter, CoaxouterLength, 0, via_width/2, pcb_thickness, name='coax_outer', material='pec')
    void=createviaPair(Coaxdie, CoaxouterLength, 0, via_width/2, pcb_thickness, name='coax_void', material='vacuum')
    subtract(outer, void)
    createMaterial('0.716873_0.001', 0.716873, 0.001)
    createviaPair(Coaxdie, CoaxouterLength, 0, via_width/2, pcb_thickness, name='coax_dk', material='0.716873_0.001')
    createviaPair(Coaxcenter, CoaxcenterLength, 0, via_width/2, pcb_thickness+CoaxouterLength-CoaxcenterLength, name='coax_inner', material='pec')

    
    
def createCoaxWavePort(Y, name, id, reference):
    oEditor = oDesign.SetActiveEditor("3D Modeler")
    oEditor.CreateCircle(
        [
            "NAME:CircleParameters",
            "IsCovered:="		, True,
            "XCenter:="		, "0mm",
            "YCenter:="		, "{}{}".format(Y, unit),
            "ZCenter:="		, "{}{}".format(pcb_thickness+CoaxouterLength, unit),
            "Radius:="		, "{}{}".format(Coaxouter, unit),
            "WhichAxis:="		, "Z",
            "NumSegments:="		, "0"
        ], 
        [
            "NAME:Attributes",
            "Name:="		, name,
            "Flags:="		, "",
            "Color:="		, "(122 122 0)",
            "Transparency:="	, 0,
            "PartCoordinateSystem:=", "Global",
            "UDMId:="		, "",
            "MaterialValue:="	, "\"vacuum\"",
            "SurfaceMaterialValue:=", "\"\"",
            "SolveInside:="		, True,
            "IsMaterialEditable:="	, True,
            "UseMaterialAppearance:=", False,
            "IsLightweight:="	, False
        ])
    face_number=oEditor.GetFaceIDs(name)[0]

    oModule = oDesign.GetModule("BoundarySetup")
    oModule.AutoIdentifyPorts(
	[
		"NAME:Faces", 
		int(face_number)
	], True, 
	[
		"NAME:ReferenceConductors", 
		"{}".format(reference)
	], "{}".format(id), True)

        
def createAirBox():
    oEditor.CreateRegion(
        [
            "NAME:RegionParameters",
            "+XPaddingType:="	, "Absolute Offset",
            "+XPadding:="		, "0mm",
            "-XPaddingType:="	, "Absolute Offset",
            "-XPadding:="		, "0mm",
            "+YPaddingType:="	, "Absolute Offset",
            "+YPadding:="		, "0mm",
            "-YPaddingType:="	, "Absolute Offset",
            "-YPadding:="		, "0mm",
            "+ZPaddingType:="	, "Absolute Offset",
            "+ZPadding:="		, "0mm",
            "-ZPaddingType:="	, "Absolute Offset",
            "-ZPadding:="		, "1mm"
        ], 
        [
            "NAME:Attributes",
            "Name:="		, "Region",
            "Flags:="		, "Wireframe#",
            "Color:="		, "(198 225 132)",
            "Transparency:="	, 0,
            "PartCoordinateSystem:=", "Global",
            "UDMId:="		, "",
            "MaterialValue:="	, "\"air\"",
            "SurfaceMaterialValue:=", "\"\"",
            "SolveInside:="		, True,
            "IsMaterialEditable:="	, True,
            "UseMaterialAppearance:=", False,
            "IsLightweight:="	, False
        ])

def AddSolutionSetup():
    oModule = oDesign.GetModule("AnalysisSetup")
    oModule.InsertSetup("HfssDriven", 
        [
            "NAME:Setup1",
            "AdaptMultipleFreqs:="	, False,
            "Frequency:="		, "25GHz",
            "MaxDeltaS:="		, 0.02,
            "PortsOnly:="		, False,
            "UseMatrixConv:="	, False,
            "MaximumPasses:="	, 20,
            "MinimumPasses:="	, 1,
            "MinimumConvergedPasses:=", 1,
            "PercentRefinement:="	, 20,
            "IsEnabled:="		, True,
            [
                "NAME:MeshLink",
                "ImportMesh:="		, False
            ],
            "BasisOrder:="		, 1,
            "DoLambdaRefine:="	, True,
            "DoMaterialLambda:="	, True,
            "SetLambdaTarget:="	, False,
            "Target:="		, 0.3333,
            "UseMaxTetIncrease:="	, False,
            "PortAccuracy:="	, 1e-05,
            "UseABCOnPort:="	, False,
            "SetPortMinMaxTri:="	, False,
            "UseDomains:="		, False,
            "UseIterativeSolver:="	, False,
            "SaveRadFieldsOnly:="	, False,
            "SaveAnyFields:="	, True,
            "IESolverType:="	, "Auto",
            "LambdaTargetForIESolver:=", 0.15,
            "UseDefaultLambdaTgtForIESolver:=", True
        ])
    oModule.InsertFrequencySweep("Setup1", 
        [
            "NAME:Sweep",
            "IsEnabled:="		, True,
            "RangeType:="		, "LinearCount",
            "RangeStart:="		, "0.001Hz",
            "RangeEnd:="		, "50GHz",
            "RangeCount:="		, 5001,
            "Type:="		, "Interpolating",
            "SaveFields:="		, False,
            "SaveRadFields:="	, False,
            "InterpTolerance:="	, 0.5,
            "InterpMaxSolns:="	, 250,
            "InterpMinSolns:="	, 0,
            "InterpMinSubranges:="	, 1,
            "ExtrapToDC:="		, False,
            "InterpUseS:="		, True,
            "InterpUsePortImped:="	, False,
            "InterpUsePropConst:="	, True,
            "UseDerivativeConvergence:=", False,
            "InterpDerivTolerance:=", 0.2,
            "UseFullBasis:="	, True,
            "EnforcePassivity:="	, True,
            "PassivityErrorTolerance:=", 0.0001
        ])


        
def main():
    setOverride()
    elevation=0
    for n, (type, name, height, material) in enumerate(stack_bottomup):
        if type=='signal':
            oEditor.FitAll()
            material=stack_bottomup[n+1][3]
            createDielectric(name, height, elevation, material)
        elif type=='dielectric':
            createDielectric(name, height, elevation, material)
        elif type=='ground':
            x=createMetal(name, height, elevation, material, "(128 128 255)")
        elif type=='power':
            x=createMetal(name, height, elevation, material) 
        else:
            pass
        elevation+=height

    #Create Void
    void=createVoid(radius=void_radius_Signal, height=pcb_thickness_minus_topmask, width=via_width, elevation=0)
    subtract(metallayers, void)

    #CreatePair
    pair=createPair(viawidth=via_width, line_width=line_width, line_spacing=line_spacing, height=elevation_dic[outlayer][0], elevation=elevation_dic[outlayer][1])

    #Create vias and pads
    outer_barrel=createviaPair(radius=via_radius, height=viatop, locx=0, locy=via_width/2, elevation=viabot, material='copper')
    inner_barrel=createviaPair(radius=via_radius-via_coating, height=pcb_thickness_minus_topmask, locx=0, locy=via_width/2, elevation=0, material='copper')

    padsTop=createviaPair(radius=via_pad_radius, height=elevation_dic[top_signal_layer][0], locx=0, locy=via_width/2, elevation=elevation_dic[top_signal_layer][1], material='copper')
    padsBot=createviaPair(radius=via_pad_radius, height=elevation_dic[outlayer][0], locx=0, locy=via_width/2, elevation=elevation_dic[outlayer][1], material='copper')
    subtract( outer_barrel+padsTop+padsBot+alllayers, inner_barrel, True)
    subtract(pair, inner_barrel)

    #Backdrill
    objects=alllayers+['viaP','viaN', 'pairP', 'pairN']

    drill=createviaPair(radius=backdrill_radius, height=elevation_dic[outlayer][1]-stub_length, locx=0, locy=via_width/2, elevation=0, material='copper')
    subtract(objects, drill)
    
    #Create Port
    createWavePort()    
    createCoax()
    createTopPEC()
    createCoaxWavePort(-via_width/2, name='coaxportP', id=2, reference="coax_outerP")
    createCoaxWavePort(via_width/2, name='coaxportN', id=3, reference="coax_outerN")
    oModule = oDesign.GetModule("BoundarySetup")
#    try:
#        oModule.DeleteBoundaries(["coax_outerN_T1"])
#        oModule.DeleteBoundaries(["coax_outerP_T1"])
#    except:
#        pass
        
    createAirBox()
    try:
        AddSolutionSetup()
    except:
        pass
#Set Parameters Here---------------------------------------------------------------


#define materials used in stackup

createMaterial('3.14_0.0017', 3.14, 0.0017)
createMaterial('3.22_0.0018', 3.22, 0.0018)
createMaterial('3.10_0.0017', 3.10, 0.0017)

#define stackup
x='''
dielectric, top_mask, 1, SolderMask
signal, top, 1.7, copper
dielectric, in1, 3.2, 3.14_0.0017
ground, G2, 1.3, copper
dielectric, in2, 5.5, 3.22_0.0018
signal, S3, 0.6, copper
dielectric, in3, 5.8, 3.14_0.0017
ground, G4, 1.3, copper
dielectric, in4, 3.5, 3.14_0.0017
power, P5, 2.6, copper
dielectric, in5, 10.2, 3.10_0.0017
power, P6, 2.6, copper
dielectric, in6, 3.5, 3.14_0.0017
ground, G7, 1.3, copper
dielectric, in7, 5.8, 3.14_0.0017
signal, S8, 0.6, copper
dielectric, in8, 5.5, 3.22_0.0018
ground, G9, 1.3, copper
dielectric, in9, 5.8, 3.14_0.0017
signal, S10, 0.6, copper
dielectric, in10, 5.5, 3.22_0.0018
ground, G11, 1.3, copper
dielectric, in11, 5.8, 3.14_0.0017
signal, S12, 0.6, copper
dielectric, in12, 5.5, 3.22_0.0018
ground, G13, 1.3, copper
dielectric, in13, 6, 3.14_0.0017
ground, G14, 1.3, copper
dielectric, in14, 5.5, 3.22_0.0018
signal, S15, 0.6, copper
dielectric, in15, 5.8, 3.14_0.0017
ground, G16, 1.3, copper
dielectric, in16, 5.5, 3.22_0.0018
signal, S17, 0.6, copper
dielectric, in17, 5.8, 3.14_0.0017
ground, G18, 1.3, copper
dielectric, in18, 5.5, 3.22_0.0018
signal, S19, 0.6, copper
dielectric, in19, 5.8, 3.14_0.0017
ground, G20, 1.3, copper
dielectric, in20, 3.5, 3.14_0.0017
power, P21, 2.6, copper
dielectric, in21, 10.2, 3.10_0.0017
power, P22, 2.6, copper
dielectric, in22, 3.5, 3.14_0.0017
ground, G23, 1.3, copper
dielectric, in23, 5.8, 3.14_0.0017
signal, S24, 0.6, copper
dielectric, in24, 5.5, 3.22_0.0018
ground, G25, 1.3, copper
dielectric, in25, 3.2, 3.14_0.0017
signal, bottom, 1.7, copper
dielectric, bottom_mask, 1, SolderMask
'''
stackup=readStackup(x)

#define PCB size
offset=100
length=200
width=200

#define signal vias
void_radius_Signal=16
void_radius_GNDvia=13
void_radius_PWRvia=13

via_width=40
via_radius=5
via_coating=1
via_pad_radius=9

ground_via_width=120
ground_lead_radius=5

#define transmission lines
perp=True
inlayer='Top'
outlayer='S12'
line_width=5.8
line_spacing=8

#create backdrill
backdrill_radius=7
stub_length=12

main()

#create ground/power vias
createPGviaPair(-30,40, name='Gvia1', type='GND')
createPGviaPair(30,40, name='Pvia1', type='PWR')
createPGvia(-40,0, name='Pvia2', type='PWR')