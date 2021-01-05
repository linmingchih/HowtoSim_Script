from math import floor, ceil
from collections import defaultdict
import itertools
import time
import clr
clr.AddReference("System.Windows.Forms")
from System.Windows.Forms import MessageBox

t0 = time.time()
oDesktop.ClearMessages("", "", 2)
oProject = oDesktop.GetActiveProject()
oDesign = oProject.GetActiveDesign()
oEditor = oDesign.SetActiveEditor("3D Modeler")

unit = oEditor.GetModelUnits()
size = 0.1
n = 0

def float_range(xmin, xmax, step):
    result = []
    x = xmin
    while x <= xmax:
        result.append(x)
        x += step
        
    return result

def unite(cubes):
    data = ','.join(cubes)
    if len(cubes) > 1:
        oEditor.Unite(
            [
                "NAME:Selections",
                "Selections:="		, data
            ], 
            [
                "NAME:UniteParameters",
                "KeepOriginals:="	, False
            ])
    oEditor.PurgeHistory(
        [
            "NAME:Selections",
            "Selections:="		, cubes[0],
            "NewPartsModelFlag:="	, "Model"
        ])
    return cubes[0]

def changecolor(name, code):
    code = int(code)
    R= code % 256
    G = ((code - R) % (256**2)) / 256
    B = (code - R - 256*G) / 256**2
    
    oEditor.ChangeProperty(
        [
            "NAME:AllTabs",
            [
                "NAME:Geometry3DAttributeTab",
                [
                    "NAME:PropServers", 
                    name
                ],
                [
                    "NAME:ChangedProps",
                    [
                        "NAME:Color",
                        "R:="			, int(R),
                        "G:="			, int(G),
                        "B:="			, int(B)
                    ]
                ]
            ]
        ])

def continuous_count(x):
    result = []
    i0, loc0 = x[0]
    count = 1
    for i, loc in x[1:]:
        if i == i0:
            count += 1
        else:
            result.append((i0, loc0, count))
            i0, loc0 = i, loc
            count = 1
    result.append((i0, loc0, count))
    return result
    
def createcell(x, y, z, Nx, Ny, material):
    global n
    newname = oEditor.CreateBox(
        [
            "NAME:BoxParameters",
            "XPosition:="		, str(x-size/2) + unit,
            "YPosition:="		, str(y-size/2) + unit,
            "ZPosition:="		, str(z-size/2) + unit,
            "XSize:="		, str(size*Nx) + unit,
            "YSize:="		, str(size*Ny) + unit,
            "ZSize:="		, str(size) + unit
        ], 
        [
            "NAME:Attributes",
            "Name:="		, 'box{}'.format(n),
            "Flags:="		, "",
            "Color:="		, "(143 175 143)",
            "Transparency:="	, 0,
            "PartCoordinateSystem:=", "Global",
            "UDMId:="		, "",
            "MaterialValue:="	, material,
            "SurfaceMaterialValue:=", "\"\"",
            "SolveInside:="		, True,
            "ShellElement:="	, False,
            "ShellElementThickness:=", "0mm",
            "IsMaterialEditable:="	, True,
            "UseMaterialAppearance:=", False,
            "IsLightweight:="	, True
        ])
    n += 1    
    return newname


color = {}
material = {}
vertex_positions = []
 


#total = [oEditor.GetObjectName(i) for i in range(oEditor.GetNumObjects())]

#total = oEditor.GetSelections()
total = oEditor.GetSelections()
if len(total) == 0:
    MessageBox.Show("Please select objects to simplify!", 'Message Window')
    
for obj in total:
    try:
        material[obj] = oEditor.GetPropertyValue('Geometry3DAttributeTab', obj, 'Material')
        color[obj] = oEditor.GetPropertyValue('Geometry3DAttributeTab', obj, 'Color')
        
        for vid in oEditor.GetVertexIDsFromObject(obj):
            position = [float(i) for i in oEditor.GetVertexPosition(vid)]
            vertex_positions.append(position)
    except:
        AddWarningMessage('{} is ignored!'.format(obj))

vs = zip(*vertex_positions)
size_range = list(map(floor, map(min, vs))) + list(map(ceil, map(max, vs)))

#AddWarningMessage(str(material))
#AddWarningMessage(str(color))

xmin, ymin, zmin, xmax, ymax, zmax = map(int, size_range)

xrange = float_range(xmin, xmax, size)
yrange = float_range(ymin, ymax, size)
zrange = float_range(zmin, zmax, size)

data = defaultdict(list)

for k , j in itertools.product(zrange, yrange):
    queue = []
    for i in xrange:
        o = oEditor.GetBodyNamesByPosition(["NAME:Parameters", "XPosition:=", str(i)+unit,"YPosition:=", str(j)+unit, "ZPosition:=", str(k)+unit])
        if o:
            queue.append((o[0],i))
        else:
            queue.append(('dummy',i))
    
    for obj, loc, xlen in continuous_count(queue):
        if obj in total:
            data[obj] += [(loc, j, k, xlen)]
    
models = defaultdict(list)

for obj in data:
    if obj == '':
        continue
    i0, j0, k0, xlen0 = data[obj][0]
    ylen = 1

    for u in data[obj][1:]:
        
        i, j, k, xlen = u
        if (i, k, xlen) == (i0, k0, xlen0):
            ylen += 1
        else:
            models[obj] += [(i0, j0, k0, xlen0, ylen)]
            
            i0, j0, k0, xlen0 = i, j, k, xlen
            ylen = 1
    models[obj] += [(i0, j0, k0, xlen0, ylen)]
for obj in models:
    m = material[obj]
    if 'vacuum' in m:
        continue
    group = []
    for x, y, z, Nx, Ny in models[obj]:
        name = createcell(x, y, z, Nx, Ny, m)
        group.append(name)
        if len(group) == 10:      
            group =[unite(group)]
    x = unite(group)
    changecolor(x, color[obj])

    oEditor.ChangeProperty(
	[
		"NAME:AllTabs",
		[
			"NAME:Geometry3DAttributeTab",
			[
				"NAME:PropServers", 
				x
			],
			[
				"NAME:ChangedProps",
				[
					"NAME:Name",
					"Value:="		, 'copy_' + obj
				]
			]
		]
	])
