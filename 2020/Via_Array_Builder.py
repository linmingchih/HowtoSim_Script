import ScriptEnv, time
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.NewProject()
oProject.InsertDesign("HFSS", "ViaModel", "DrivenModal", "")
oDesign = oProject.GetActiveDesign()
oDesign.SetSolutionType("DrivenTerminal", False)
oEditor = oDesign.SetActiveEditor("3D Modeler")
oDesktop.ClearMessages('','',2)

unit='mil'
portid=1
pec_void_list=[]
startT=time.time()

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

def createVoid(radius, height, width, elevation, wkcs="Global"):
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
            "PartCoordinateSystem:=", wkcs,
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
            "PartCoordinateSystem:=", wkcs,
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
            "PartCoordinateSystem:=", wkcs,
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

def createvia(radius, height, locx, locy, elevation, name="viaP", material='copper', wkcs="Global", color="(255 28 64)"):
    solveinside=True if material not in ['copper', 'pec'] else False
    
    x=oEditor.CreateCylinder(
        [
            "NAME:CylinderParameters",
            "XCenter:="		, "{}{}".format(locx, unit),
            "YCenter:="		, "{}{}".format(locy, unit),
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
            "Color:="		, color,
            "Transparency:="	, 0,
            "PartCoordinateSystem:=", wkcs,
            "UDMId:="		, "",
            "MaterialValue:="	, '\"{}\"'.format(material),
            "SurfaceMaterialValue:=", "\"\"",
            "SolveInside:="		, solveinside,
            "IsMaterialEditable:="	, True,
            "UseMaterialAppearance:=", False,
            "IsLightweight:="	, False
        ])
    return [x]
  
    
def createviaPair(radius, height, locx, locy, elevation, name='via', material='copper', wkcs='Global', color="(255 255 0)"):
    x = createvia(radius, height, locx, locy, elevation, name="{}P".format(name), material=material, color=color)
    y = createvia(radius, height, locx, -locy, elevation, name="{}N".format(name), material=material, color=color)
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

def createPair(viawidth, line_width, line_spacing, height, elevation, length=1, material='copper', wkcs="Global"):
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
            "PartCoordinateSystem:=", wkcs,
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
            "PartCoordinateSystem:=", wkcs,
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
    color="(255 255 0)" if type=='GND' else "(0 128 0)"
    outside_barrel=createvia(radius=via_radius, height=viatop, locx=locx, locy=locy,name=name, elevation=viabot, material='copper', color=color)
    inside_barrel=createvia(radius=via_radius-via_coating, height=pcb_thickness_minus_topmask, locx=locx, locy=locy, elevation=0, material='copper', color=color)
    
    padsTop=createvia(radius=via_pad_radius, height=elevation_dic[top_signal_layer][0], locx=locx, locy=locy, elevation=elevation_dic[top_signal_layer][1], name=name+'toppad', material='copper', color=color)
    padsBot=createvia(radius=via_pad_radius, height=elevation_dic[bot_signal_layer][0], locx=locx, locy=locy, elevation=elevation_dic[bot_signal_layer][1], name=name+'botpad', material='copper', color=color)
    
    subtract(outside_barrel + padsTop + padsBot + alllayers, inside_barrel)

    #Create voids of ground vias
    void_radius=void_radius_GNDvia if type=='GND' else void_radius_PWRvia
    gnd_via_antipad=createvia(radius=void_radius, height=pcb_thickness_minus_topmask, locx=locx, locy=locy, elevation=0, material='copper', color=color)
    if type=='GND':
        subtract(powerlayers, gnd_via_antipad)
        createvia(radius=ground_lead_radius, height=topmask_thickness, locx=locx, locy=locy, elevation=pcb_thickness_minus_topmask, material='pec', color=color)
    else:
        subtract(groundlayers, gnd_via_antipad)  

       
        
def createPGviaPair(locx, locy, name='PGvias', type='GND'):
    color="(255 255 0)" if type=='GND' else "(0 128 0)"
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
        createviaPair(radius=ground_lead_radius, height=topmask_thickness, locx=locx, locy=locy, elevation=pcb_thickness_minus_topmask, material='pec', color="(0 0 0)")    
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

def purgeAllLayers():
    for i in metallayers:
        oEditor.PurgeHistory(
            [
                "NAME:Selections",
                "Selections:="		, i,
                "NewPartsModelFlag:="	, "Model"
            ])  

def createWavePort(wkcs="Global", length=1):
    global layer_above_outlayer, layer_below_outlayer, portid
    layer_above_outlayer= signal_metal_layers[signal_metal_layers.index(outlayer)-1]
    layer_below_outlayer= signal_metal_layers[signal_metal_layers.index(outlayer)+1]
    
    low=elevation_dic[layer_above_outlayer][1]
    high=elevation_dic[layer_below_outlayer][1]+elevation_dic[layer_below_outlayer][0]
    width_port=4*(2*line_width+line_spacing)
    rect=oEditor.CreateRectangle(
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
            "PartCoordinateSystem:=", wkcs,
            "UDMId:="		, "",
            "MaterialValue:="	, "\"vacuum\"",
            "SurfaceMaterialValue:=", "\"\"",
            "SolveInside:="		, True,
            "IsMaterialEditable:="	, True,
            "UseMaterialAppearance:=", False,
            "IsLightweight:="	, False
        ])    
    face_number=oEditor.GetFaceIDs(rect)[0]
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
	], str(portid), True)

    
    oDesign.ChangeProperty(
        [
            "NAME:AllTabs",
            [
                "NAME:HfssTab",
                [
                    "NAME:PropServers", 
                    "BoundarySetup:{}".format(portid)
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
    portid+=1
    
def createTopPEC():
    oEditor.SetWCS(
        [
            "NAME:SetWCS Parameter",
            "Working Coordinate System:=", "Global",
            "RegionDepCSOk:="	, False
        ])
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
        
    subtract(["topPEC"], pec_void_list)    
        
    oModule = oDesign.GetModule("BoundarySetup")
    oModule.AssignPerfectE(
        [
            "NAME:PerfE1",
            "Objects:="		, ["topPEC"],
            "InfGroundPlane:="	, False
        ])

def createCoax(wkcs="Global"):
    global CoaxcenterLength, CoaxouterLength, Coaxouter, Coaxcenter, Coaxdie, pec_void_list
    CoaxcenterLength= H1*0.6+(L1/0.2)*0.4
    CoaxouterLength = H1*0.6-(L1/0.2)*0.4   
    Coaxouter=via_pad_radius
    Coaxcenter=via_radius-via_coating
    Coaxdie=Coaxouter*0.9  

    outer=createviaPair(Coaxouter, CoaxouterLength, 0, via_width/2, pcb_thickness, name='coax_outer', material='pec', wkcs=wkcs, color="(242 106 228)")
    void=createviaPair(Coaxdie, CoaxouterLength, 0, via_width/2, pcb_thickness, name='coax_void', material='vacuum', wkcs=wkcs)
    subtract(outer, void)
    createMaterial('0.716873_0.001', 0.716873, 0.001)
    createviaPair(Coaxdie, CoaxouterLength, 0, via_width/2, pcb_thickness, name='coax_dk', material='0.716873_0.001', wkcs=wkcs, color="(255 255 255)")
    createviaPair(Coaxcenter, CoaxcenterLength, 0, via_width/2, pcb_thickness+CoaxouterLength-CoaxcenterLength, name='coax_inner', material='pec', wkcs=wkcs, color="(0 0 0)")
      
    pec_void_list+=createviaPair(Coaxdie, CoaxouterLength, 0, via_width/2, pcb_thickness_minus_topmask, name='PEC_void', material='copper')    
    return outer
    
def createCoaxWavePort(Y, name, id, reference, wkcs='Global'):
    oEditor = oDesign.SetActiveEditor("3D Modeler")
    newname=oEditor.CreateCircle(
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
            "PartCoordinateSystem:=", wkcs,
            "UDMId:="		, "",
            "MaterialValue:="	, "\"vacuum\"",
            "SurfaceMaterialValue:=", "\"\"",
            "SolveInside:="		, True,
            "IsMaterialEditable:="	, True,
            "UseMaterialAppearance:=", False,
            "IsLightweight:="	, False
        ])
    face_number=oEditor.GetFaceIDs(newname)[0]

    oModule = oDesign.GetModule("BoundarySetup")
    oModule.AutoIdentifyPorts(
	[
		"NAME:Faces", 
		int(face_number)
	], True, 
	[
		"NAME:ReferenceConductors", 
		"{}".format(reference)
	], str(portid), True)
    global portid
    portid+=1

        
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


        
def creatDK():
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
    
def createSetup():
    createTopPEC()    
    createAirBox()
    try:
        AddSolutionSetup()
    except:
        pass
    totalT=time.time()-startT
    AddWarningMessage("Build Time: {}secs".format(totalT))    
        
def createSignalVia(x0, y0):

    wkcs=createCS(x0, y0)
    #Create Void
    void=createVoid(radius=void_radius_Signal, height=pcb_thickness_minus_topmask, width=via_width, elevation=0, wkcs=wkcs)
    subtract(metallayers, void)

    #CreatePair
    pair=createPair(viawidth=via_width, line_width=line_width, line_spacing=line_spacing, height=elevation_dic[outlayer][0], elevation=elevation_dic[outlayer][1], length=length-x0, wkcs=wkcs)

    #Create vias and pads
    outer_barrel=createviaPair(radius=via_radius, height=viatop, locx=0, locy=via_width/2, elevation=viabot, material='copper', wkcs=wkcs, color="(255 0 0)")
    inner_barrel=createviaPair(radius=via_radius-via_coating, height=pcb_thickness_minus_topmask, locx=0, locy=via_width/2, elevation=0, material='copper', wkcs=wkcs, color="(255 0 0)")

    padsTop=createviaPair(radius=via_pad_radius, height=elevation_dic[top_signal_layer][0], locx=0, locy=via_width/2, elevation=elevation_dic[top_signal_layer][1], material='copper', wkcs=wkcs, color="(255, 0, 0)")
    padsBot=createviaPair(radius=via_pad_radius, height=elevation_dic[outlayer][0], locx=0, locy=via_width/2, elevation=elevation_dic[outlayer][1], material='copper', wkcs=wkcs, color="(255, 0, 0)")
    subtract( outer_barrel+padsTop+padsBot+alllayers, inner_barrel, True)
    subtract(pair, inner_barrel)

    #Backdrill
    #objects=alllayers+['viaP','viaN', 'pairP', 'pairN']
    objects=alllayers+pair+outer_barrel
    drill=createviaPair(radius=backdrill_radius, height=elevation_dic[outlayer][1]-stub_length, locx=0, locy=via_width/2, elevation=0, material='copper', wkcs=wkcs)
    subtract(objects, drill)
    
    #Create Port
    createWavePort(wkcs=wkcs, length=length-x0)    
    refP, refN=createCoax(wkcs=wkcs)

    createCoaxWavePort(-via_width/2, name='coaxportP', id=2, reference=refP, wkcs=wkcs)
    createCoaxWavePort(via_width/2, name='coaxportN', id=3, reference=refN, wkcs=wkcs)
    oModule = oDesign.GetModule("BoundarySetup")
#    try:
#        oModule.DeleteBoundaries(["coax_outerN_T1"])
#        oModule.DeleteBoundaries(["coax_outerP_T1"])
#    except:
#        pass
def setGlobalCS():
    oEditor.SetWCS(
        [
            "NAME:SetWCS Parameter",
            "Working Coordinate System:=", "Global",
            "RegionDepCSOk:="	, False
        ])
       
def createCS(x, y):
    oEditor.SetWCS(
        [
            "NAME:SetWCS Parameter",
            "Working Coordinate System:=", "Global",
            "RegionDepCSOk:="	, False
        ])
    oEditor.CreateRelativeCS(
        [
            "NAME:RelativeCSParameters",
            "Mode:="		, "Axis/Position",
            "OriginX:="		, "{}{}".format(x, unit),
            "OriginY:="		, "{}{}".format(y, unit),
            "OriginZ:="		, "0mm",
            "XAxisXvec:="		, "1mm",
            "XAxisYvec:="		, "0mm",
            "XAxisZvec:="		, "0mm",
            "YAxisXvec:="		, "0mm",
            "YAxisYvec:="		, "1mm",
            "YAxisZvec:="		, "0mm"
        ], 
        [
            "NAME:Attributes",
            "Name:="		, "Relative_{}_{}".format(x,y)
        ])
    return "Relative_{}_{}".format(x,y)

    
#Set Parameters Here---------------------------------------------------------------

#Define dielectric: type, name, thickness, material
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

#define material
createMaterial('3.14_0.0017', 3.14, 0.0017)
createMaterial('3.22_0.0018', 3.22, 0.0018)
createMaterial('3.10_0.0017', 3.10, 0.0017)

#define PCB size
offset=200
length=200
width=600

#define via gepmetry
void_radius_Signal=16
void_radius_GNDvia=13
void_radius_PWRvia=13

via_width=40
via_radius=5
via_coating=1
via_pad_radius=9

ground_via_width=120
ground_lead_radius=5

perp=True
inlayer='Top'

line_width=5.8
line_spacing=8

backdrill_radius=7
stub_length=12


creatDK()

outlayer='S3'
line_width=5.8
line_spacing=8
createSignalVia(0, -120)
createSignalVia(0, +120)
createSignalVia(0, 0)

outlayer='S8'
line_width=6
line_spacing=10
createSignalVia(-80, -120)
createSignalVia(-80, 120)
createSignalVia(-80, 0)

outlayer='S17'
line_width=5
line_spacing=7
createSignalVia(80, -120)
createSignalVia(80, 120)
createSignalVia(80, 0)

setGlobalCS()

createPGvia(-120,-220, name='Gvia1', type='GND')
createPGvia(-80,-220, name='Gvia2', type='GND')
createPGvia(-40,-220, name='Gvia3', type='GND')
createPGvia(0,-220, name='Gvia4', type='GND')
createPGvia(40,-220, name='Gvia5', type='GND')
createPGvia(80,-220, name='Gvia6', type='GND')
createPGvia(120,-220, name='Gvia7', type='GND')

createPGvia(-120,-180, name='Gvia8', type='GND')
createPGvia(-80,-180, name='Pvia1', type='PWR')
createPGvia(-40,-180, name='Gvia9', type='GND')
createPGvia(0,-180, name='Pvia2', type='PWR')
createPGvia(40,-180, name='Gvia10', type='GND')
createPGvia(80,-180, name='Pvia3', type='PWR')
createPGvia(120,-180, name='Gvia11', type='GND')

createPGvia(-120,-140, name='Gvia12', type='GND')
createPGvia(-40,-140, name='Gvia13', type='GND')
createPGvia(40,-140, name='Gvia14', type='GND')
createPGvia(120,-140, name='Gvia15', type='GND')

createPGvia(-120,-100, name='Gvia16', type='GND')
createPGvia(-40,-100, name='Gvia17', type='GND')
createPGvia(40,-100, name='Gvia18', type='GND')
createPGvia(120,-100, name='Gvia19', type='GND')

createPGvia(-120,-60, name='Gvia20', type='GND')
createPGvia(-80,-60, name='Pvia4', type='PWR')
createPGvia(-40,-60, name='Gvia21', type='GND')
createPGvia(0,-60, name='Pvia5', type='PWR')
createPGvia(40,-60, name='Gvia22', type='GND')
createPGvia(80,-60, name='Pvia6', type='PWR')
createPGvia(120,-60, name='Gvia23', type='GND')

createPGvia(-120,-20, name='Gvia24', type='GND')
createPGvia(-40,-20, name='Gvia25', type='GND')
createPGvia(40,-20, name='Gvia26', type='GND')
createPGvia(120,-20, name='Gvia27', type='GND')

createPGvia(-120,20, name='Gvia28', type='GND')
createPGvia(-40,20, name='Gvia29', type='GND')
createPGvia(40,20, name='Gvia30', type='GND')
createPGvia(120,20, name='Gvia31', type='GND')

createPGvia(-120,60, name='Gvia32', type='GND')
createPGvia(-80,60, name='Pvia7', type='PWR')
createPGvia(-40,60, name='Gvia33', type='GND')
createPGvia(0,60, name='Pvia8', type='PWR')
createPGvia(40,60, name='Gvia34', type='GND')
createPGvia(80,60, name='Pvia9', type='PWR')
createPGvia(120,60, name='Gvia35', type='GND')

createPGvia(-120,100, name='Gvia36', type='GND')
createPGvia(-40,100, name='Gvia37', type='GND')
createPGvia(40,100, name='Gvia38', type='GND')
createPGvia(120,100, name='Gvia39', type='GND')

createPGvia(-120,140, name='Gvia40', type='GND')
createPGvia(-40,140, name='Gvia41', type='GND')
createPGvia(40,140, name='Gvia42', type='GND')
createPGvia(120,140, name='Gvia43', type='GND')

createPGvia(-120,180, name='Gvia44', type='GND')
createPGvia(-80,180, name='Pvia10', type='PWR')
createPGvia(-40,180, name='Gvia45', type='GND')
createPGvia(0,180, name='Pvia11', type='PWR')
createPGvia(40,180, name='Gvia46', type='GND')
createPGvia(80,180, name='Pvia12', type='PWR')
createPGvia(120,180, name='Gvia47', type='GND')

createPGvia(-120,220, name='Gvia48', type='GND')
createPGvia(-80,220, name='Gvia49', type='GND')
createPGvia(-40,220, name='Gvia50', type='GND')
createPGvia(0,220, name='Gvia51', type='GND')
createPGvia(40,220, name='Gvia52', type='GND')
createPGvia(80,220, name='Gvia53', type='GND')
createPGvia(120,220, name='Gvia54', type='GND')

#Create Solution Setup
createSetup()
