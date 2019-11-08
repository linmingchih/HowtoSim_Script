
import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.GetActiveProject()
oDesign = oProject.GetActiveDesign()
oEditor = oDesign.SetActiveEditor("SchematicEditor")

def cutpaste(port, x, y, angle):
    oEditor.Cut(
	[
		"NAME:Selections",
		"Selections:="		, [port]
	])
    oEditor.Paste(
        [
            "NAME:Attributes",
            "Page:="		, 1,
            "X:="			, x,
            "Y:="			, y,
            "Angle:="		, angle,
            "Flip:="		, False
        ])
        
def addres(x,y,angle):
    oEditor.CreateComponent(
        [
            "NAME:ComponentProps",
            "Name:="		, "Nexxim Circuit Elements\\Resistors:RES_",
            "Id:="			, "6"
        ], 
        [
            "NAME:Attributes",
            "Page:="		, 1,
            "X:="			, x,
            "Y:="			, y,
            "Angle:="		, angle,
            "Flip:="		, False
        ])

scale=2.54e-5
x=[i for i in oEditor.GetSelections() if i.startswith('IPort')]
AddWarningMessage(str(x))
for port in x:
    a=oEditor.GetPropertyValue("BaseElementTab", port, "Component Angle")
    angle=a[:-1]

    loc=oEditor.GetPropertyValue("BaseElementTab", port, "Component Location")
    x,y=[i.strip()[:-3] for i in loc.split(',')]
    x,y=int(x), int(y)
    if angle=='0':
        AddWarningMessage(port)        
        cutpaste(port, x*scale, (y+500)*scale,0)
        addres(x*scale, (y+200)*scale,90)
    if angle=='180':
        AddWarningMessage(port)        
        cutpaste(port, x*scale, (y-500)*scale,0)
        addres(x*scale, (y-200)*scale,90)    
    if angle=='90':
        AddWarningMessage(port)        
        cutpaste(port, (x-500)*scale, y*scale,0)
        addres((x-200)*scale, y*scale,0)     
    if angle=='270':
        AddWarningMessage(port)        
        cutpaste(port, (x+500)*scale, y*scale,0)
        addres((x+200)*scale, y*scale,0)
    else:
        pass
        
