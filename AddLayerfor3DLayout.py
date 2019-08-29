
import ScriptEnv

import xml.etree.ElementTree as ET
ET.register_namespace("c", 'http://www.ansys.com/control') 
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.GetActiveProject()
oDesign = oProject.GetActiveDesign()
oEditor = oDesign.SetActiveEditor("Layout")
oEditor.ExportStackupXML("C:\\stackup.xml")
tree = ET.ElementTree(file="C:\\stackup.xml")
root = tree.getroot()


newlayer='Layer Color="#868feb" FillMaterial="FR4_epoxy" Material="copper" Name="bbb" Thickness="0" Type="conductor"'
for elem in tree.iter(tag='Layers'):
    x=ET.Element(newlayer)  
    x.tail='\n'+' '*6
    elem.insert(0,x)

tree.write('C:\\stackup2.xml', xml_declaration=True, method="xml", encoding="UTF-8")
    
oEditor.ImportStackupXML("C:\\stackup2.xml")