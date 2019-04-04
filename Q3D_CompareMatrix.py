# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 10:25:14 2019

@author: mlin
"""
import re, collections
import webbrowser, os
import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()  

class genPlot():
    def __init__(self, report_name, directory):
        self.directory=directory
        oProject = oDesktop.NewProject()
        self.project_name=oProject.GetName()
        design_name=report_name
        self.report_name=report_name
        
        oProject.InsertDesign("Q3D Extractor", design_name, "", "")
        self.oDesign = oProject.SetActiveDesign(design_name)
        oModule = self.oDesign.GetModule("AnalysisSetup")
        oModule.InsertSetup("Matrix",["NAME:Setup1","AdaptiveFreq:=","1GHz","SaveFields:=",False,"Enabled:=",True,["NAME:Cap","MaxPass:=",10,"MinPass:=",1,"MinConvPass:=",1,"PerError:=",1,"PerRefine:=",30,"AutoIncreaseSolutionOrder:=",False,"SolutionOrder:=","High"]])
    
    def insertPlot(self, plot_name, label_Y='Value'):
        oModule=self.oDesign.GetModule("ReportSetup")
        oModule.CreateReport(plot_name,"Matrix","Rectangular Plot","Setup1:LastAdaptive",["Context:=","Original"],["Freq:=",["All"]],["X Component:=","Freq","Y Component:=",["Freq"]],[])
        oModule.DeleteTraces([plot_name+":=",["Freq"]])
        oModule.ChangeProperty(["NAME:AllTabs",["NAME:Axis",["NAME:PropServers",plot_name+":AxisY1"],["NAME:ChangedProps",["NAME:Name","Value:=",label_Y]]]])
        oModule.ChangeProperty(["NAME:AllTabs",["NAME:General",["NAME:PropServers",plot_name+":General"],["NAME:ChangedProps",["NAME:Plot Area Color","R:=",20,"G:=",20,"B:=",20]]]])
        oModule.ChangeProperty(["NAME:AllTabs",["NAME:Grid",["NAME:PropServers",plot_name+":Grid"],["NAME:ChangedProps",["NAME:Show minor X grid","Value:=",False],["NAME:Show minor Y grid","Value:=",False]]]])
        oModule.ChangeProperty(["NAME:AllTabs",["NAME:Legend",["NAME:PropServers",plot_name+":Legend"],["NAME:ChangedProps",["NAME:Show Trace Name","Value:=",False],["NAME:Show Solution Name","Value:=",False],["NAME:Show Variation Key","Value:=",False]]]])

        self.plot_name=plot_name
    
    def addData(self, csv_file):
        oModule=self.oDesign.GetModule("ReportSetup")
        oModule.ImportIntoReport(self.plot_name, csv_file)
        
    def exportImage(self):
        oModule=self.oDesign.GetModule("ReportSetup")
        oModule.CreateReport('dummy',"Matrix","Rectangular Plot","Setup1:LastAdaptive",["Context:=","Original"],["Freq:=",["All"]],["X Component:=","Freq","Y Component:=",["Freq"]],[])
        try:
            os.mkdir(self.directory+'/'+self.report_name)
        except:
            pass
        png_name='{}/{}/{}.png'.format(self.directory, self.report_name, self.plot_name)
        oModule=self.oDesign.GetModule("ReportSetup")

        oModule.ExportImageToFile(self.plot_name, png_name, 640, 480)
        oModule.DeleteReports(['dummy'])
        oModule.DeleteReports([self.plot_name])
        
        return png_name
    
    def exit(self):
        oDesktop.DeleteProject(self.project_name)
        del(self)

class matrix():
    def __init__(self, file):
        self.name=os.path.basename(file).split('.')[0]
        self.dir=os.path.dirname(file)
        with open(file) as f:
            text=f.readlines()
        
        header=re.findall(r'\"(.+?)\"', text[0])
        
        data=[]
        for i in text[1:]:
            data.append([float(j) for j in i.split(',')])
        
        data=list(map(list, zip(*data)))   
        
        self.result=collections.OrderedDict()
        
        for i in range(len(header)):
            self.result[header[i]]=data[i]
        
    def getKeys(self):
        return self.result.keys()
    
    def saveCSV(self, key):
        csv_name='{}/{}_{}.csv'.format(self.dir, self.name, key.replace(':',''))
        content=['"Freq [GHz]" , "{}_{}"\n'.format(self.name, key)]
        for n, i in enumerate(self.result['Freq [GHz]']):
            content.append('{} , {}\n'.format(i, self.result[key][n]))
        with open(csv_name, 'w') as f:
            f.writelines(content)
            
        return csv_name

     
    
class report():
    def __init__(self, report_name='ANSYS', directory='d:/demo'):
        self.directory=directory
        self.gp=genPlot(report_name, directory)
    
    def genHTML(self, f1, f2, html_file):
        mx1=matrix(f1)
        mx2=matrix(f2)
        gallery=[]

        for k in mx1.getKeys():
            if k=='Freq [GHz]': continue
            try:
                csv1=mx1.saveCSV(k)
                csv2=mx2.saveCSV(k)
            except:
                continue      
            self.gp.insertPlot(k.replace(':','_'))
            self.gp.addData(csv1)
            self.gp.addData(csv2)
            gallery.append(self.gp.exportImage())
            os.remove(csv1)
            os.remove(csv2)
        self.gp.exit()
        html_path=self.directory+'/'+html_file
        with open(html_path, 'w') as f:            
            for k in gallery:
                f.writelines('<img src="{}">\n'.format(k))
                    
        webbrowser.open('file://' + os.path.realpath(html_path))          

rp=report('case2', 'd:/demo2')     
f1='d:/demo/db1.csv' 
f2='d:/demo/db2.csv'    
rp.genHTML(f1, f2, 'ANSYS.html')







