text='''
'''

def getStackup(text):
    lines=[i.split('\t') for i in text.splitlines() if len(i.strip())>0]
    data=[]
    n=0
    for i in lines:
        name=i[0].strip() if i[0].strip() else 'UNNAMED_{:03d}'.format(n)
        n+=1
        thickness, Dk, Df=i[1], i[2], i[3]
        data.append((name,thickness, Dk, Df))
    return data

def _getDielectricMaterial(name, dk, df):
    return '''      <Material Name="{}">
        <Permittivity>
          <Double>{}</Double>
        </Permittivity>
        <DielectricLossTangent>
          <Double>{}</Double>
        </DielectricLossTangent>
      </Material>'''.format(name, dk, df)

def _getMetalMaterial(name='copper', conductivity=58000000):
    return '''      <Material Name="{}">
        <Permeability>
          <Double>0.999991</Double>
        </Permeability>
        <Conductivity>
          <Double>{}</Double>
        </Conductivity>
      </Material>'''.format(name, conductivity)
      
def Materials(data):
    x='''    <Materials>
{}
    </Materials>
    '''
    mlist=set()
        
    for i in data:
        if i[2]=='':
            mlist.add(_getMetalMaterial())
        else:
            mlist.add(_getDielectricMaterial(i[0], i[2], i[3]))
    mlist=list(mlist)
    mlist.sort()       
    return x.format('\n'.join(mlist))

def _getConductorLayer(fill, name, thickness):
    x='      <Layer Color="#fd777a" FillMaterial="{}" Material="copper" Name="{}" Thickness="{}" Type="conductor"/>'
    return x.format(fill, name, thickness)    

def _getDielectricLayer(material, name, thickness):
    x='      <Layer Color="#44614c" Material="{}" Name="{}" Thickness="{}" Type="dielectric"/>'
    return x.format(material, name, thickness)

def Layers(data):
    x='''    <Layers LengthUnit="mil">
{}
    </Layers>'''
    layerlist=[]        

    for i in range(len(data)):
        name, thickness = data[i][0:2]
        if data[i][2]=='':
            fill=data[i-1][0]
            layerlist.append(_getConductorLayer(fill, name, thickness))
        else:
            layerlist.append(_getDielectricLayer(name, name, thickness))
    return x.format('\n'.join(layerlist))
            
def xml(data):
    x='''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<c:Control xmlns:c="http://www.ansys.com/control" schemaVersion="1.0">

  <Stackup schemaVersion="1.0">
{}
{}
  </Stackup>
</c:Control>'''
  
    m=Materials(data)
    l=Layers(data)
    with open('stackup.xml', 'w') as f:
        f.write(x.format(m, l))
    return(x.format(m, l))

def ImportXML(text):
    data=getStackup(text)
    xml(data)
    oProject = oDesktop.GetActiveProject()
    oDesign = oProject.GetActiveDesign()
    oEditor = oDesign.SetActiveEditor("Layout")
    oEditor.ImportStackupXML("stackup.xml")
    oDesktop.ClearMessages("","",2)
    AddWarningMessage('Import Stackup Successfully!')

ImportXML(text)

