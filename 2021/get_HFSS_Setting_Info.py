# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 13:10:32 2021

@author: mlin
"""
import os
import System
import webbrowser
from datetime import datetime

os.chdir(os.path.dirname(__file__))
css = '''
<style type="text/css">
<!--
 .tab { margin-left: 40px; }
-->
</style>
'''

class html():
    def __init__(self, file_path):        
        self.file_path = file_path
        self.data = []
    
    def __enter__(self):
        self.data = ['<!DOCTYPE html>', '<html>', '<body>']
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.data += ['</body>', '</html>']
        with open(self.file_path, 'w') as f:
            f.write(css)
            f.write('\n'.join(self.data))
        
        webbrowser.open(self.file_path)

    def H1(self, x):
        self.data += ['<h1>{}</h1>'.format(x)]
        
    def H2(self, x):
        self.data += ['<h2>[{}]</h2>'.format(x)]

    def H3(self, x):
        self.data += ['<h3>[{}]</h3>'.format(x)]
        
    def p(self, x):
        self.data += ['<p>{}</p>'.format(x)]
    
    def strong(self, x):
         self.data += ['<strong>{}</strong>'.format(x)]
         
    def ul(self, x):
        self.data += ['<ul>'] + ['<li>{}</li>'.format(i) for i in x] + ['</ul>']
    
    def ol(self, x):
        self.data += ['<ol>'] + ['<li>{}</li>'.format(i) for i in x] + ['</ol>']
        
    def link(self, text, url):
        self.data += ['<a href="{}">{}</a>'.format(url, text)]
    
    def image(self, path, width=400):
        self.data += ['<img src={} width="{}">'.format(path, width)]
        
    def hr(self):
        self.data += ['<hr>']

    def summary(self, title, content):
        self.data += ['<details>', 
                      '<summary>{}</summary>'.format(title), 
                      '<p>{}</p>'.format(content),
                      '</details>']
        
with html('d:/demo/test.html') as h:
    h.H1('HFSS Setting Report')
    date = datetime.today().strftime('%Y-%m-%d')
    time = datetime.now().strftime("%H:%M:%S")

    h.p('Report Data: ' + date + ' / ' + time)
    
    h.H3('Platform')
    cpu_cores = 'CPU Cores: {}'.format(System.Environment.ProcessorCount)   
    version = 'AEDT Version: {}'.format(oDesktop.GetVersion())
    build_time = 'Built Time: {}'.format(oDesktop.GetBuildDateTimeString())
    ppeEnabled = 'PPE Enabled: {}'.format(oDesktop.GetPPELicensingEnabled())
    syslib = 'SysLib Path: {}'.format(oDesktop.GetSysLibDirectory())
    h.ul([cpu_cores, version, build_time, ppeEnabled, syslib])
    
    
    h.H3('Project & Design')
    oProject = oDesktop.GetActiveProject()
    oDesign = oProject.GetActiveDesign()
    oProject.GetPath()
    solution_type = 'Solution Type: {}'.format(oDesign.GetSolutionType())
    project_name = 'Project Name: {}{}'.format(oProject.GetPath(), oProject.GetName() + '.aedt')
    design_name = 'Design Name: {}'.format(oDesign.GetName())
    h.ul([project_name, design_name, solution_type])
    
    oEditor = oDesign.SetActiveEditor("3D Modeler")
    oDefinitionManager = oProject.GetDefinitionManager()

    h.H3('Message Manager')   
    messages = oDesktop.GetMessages(oProject.GetName(), oDesign.GetName(), 0)
    h.p('\n'.join(messages))

    h.H3('Boundary Condition')
    oModule	 = oDesign.GetModule('BoundarySetup')
    boundaries = oModule.GetBoundaries()
    for i in boundaries[::2]:
        h.strong(i)
        properties = oDesign.GetProperties('HfssTab', 'BoundarySetup:{}'.format(i))
        values = [oDesign.GetPropertyValue('HfssTab', 'BoundarySetup:{}'.format(i), j) for j in properties]
        data = ['{}: <mark>{}</mark>'.format(m, n) for m, n in zip(properties, values)]
        h.ul(data)
        
    h.H3('Excitations')
    excitations = oModule.GetExcitations()
    ports = []
    for i in excitations[::2]:
        i = i.split(':')[0]
        h.strong('(Terminal) '+ i)
        properties = oDesign.GetProperties('HfssTab', 'BoundarySetup:{}'.format(i))
        values = [oDesign.GetPropertyValue('HfssTab', 'BoundarySetup:{}'.format(i), j) for j in properties]
        if properties[-1] == 'Port Name':
            if values[-1] not in ports:
                ports.append(values[-1])
        
        data = ['{}: <mark>{}</mark>'.format(m, n) for m, n in zip(properties, values)]
        h.ul(data)
    
    for i in ports:
        h.strong('(Port) ' + i)
        properties = oDesign.GetProperties('HfssTab', 'BoundarySetup:{}'.format(i))
        values = [oDesign.GetPropertyValue('HfssTab', 'BoundarySetup:{}'.format(i), j) for j in properties]
        
        data = ['{}: <mark>{}</mark>'.format(m, n) for m, n in zip(properties, values)]
        h.ul(data)    
    
    
    
    h.H3('Differential Pairs')
    for num, i in enumerate(oModule.GetDiffPairs()):
        h.strong(num)
        properties = i[0::2]
        values = i[1::2]
        data = ['{}: <mark>{}</mark>'.format(m, n) for m, n in zip(properties, values)]
        h.ul(data)
    
    h.H3('Mesh Settings')
    oModule	 = oDesign.GetModule('MeshSetup')
    
    mesh_operations = []
    for i in ['Length Based',
              'Skin Depth Based',
              'ApplyCurvlinear Based',
              'Model Resolution Based',
              'Surface Approximation Based',
              'Surface Priority Based',
              'Mesh Region']:
        
        mesh_operations += oModule.GetOperationNames(i)
    for i in mesh_operations:
        h.strong(i)
        properties = oDesign.GetProperties('MeshSetupTab', 'MeshSetup:{}'.format(i))
        values = [oDesign.GetPropertyValue('MeshSetupTab', 'MeshSetup:{}'.format(i), j) for j in properties]
        data = ['{}: <mark>{}</mark>'.format(m, n) for m, n in zip(properties, values)]
        h.ul(data)
                   
    h.H3('Simulation Setups')
    oModule = oDesign.GetModule('AnalysisSetup')
    setups = oModule.GetSetups()
    for i in setups:
        h.strong(i)
        properties = oDesign.GetProperties('HfssTab', 'AnalysisSetup:{}'.format(i))
        values = [oDesign.GetPropertyValue('HfssTab', 'AnalysisSetup:{}'.format(i), k) for k in properties]
        data = ['{}: <mark>{}</mark>'.format(m, n) for m, n in zip(properties, values)]
        h.ul(data)
    

        oModule = oDesign.GetModule('AnalysisSetup')
        sweeps = oModule.GetSweeps(i)
        for j in sweeps:
            h.strong('{}:{}'.format(i, j))
            properties = oDesign.GetProperties('HfssTab', 'AnalysisSetup:{}:{}'.format(i, j))
            values = [oDesign.GetPropertyValue('HfssTab', 'AnalysisSetup:{}:{}'.format(i, j), k) for k in properties]
            data = ['{}: <mark>{}</mark>'.format(m, n) for m, n in zip(properties, values)]
            h.ul(data)
    
    h.H3('Materials')    
    materials = oDefinitionManager.GetProjectMaterialNames()
    oMaterialManager = oDefinitionManager.GetManager("Material")
    for i in materials:
        objs = oEditor.GetObjectsByMaterial(i)
        h.strong(i + ': {} objs'.format(len(objs)))
        materialData = oMaterialManager.GetData(i)
        h.p(str(materialData))
    

        
    