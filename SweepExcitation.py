oProject = oDesktop.GetActiveProject()
oDesign = oProject.GetActiveDesign()  
oEditor = oDesign.SetActiveEditor("3D Modeler")

import collections, os
class CatchView():
    def __init__(self, path, report_name):
        self.path=path
        self.pages=collections.OrderedDict()        
        self.v=self.initViews()
        self.dir='{}/{}'.format(path,report_name)
        try:
            os.mkdir(self.dir)
        except:
            pass
        self.html='{}/{}.html'.format(path, report_name)
    
    def saveSection(self, title):
        self.pages[title]=[]
        for v in self.v:
            oEditor.SetTopDownViewDirectionForActiveView(v)
            image_path='{}/{}_{}.png'.format(self.dir, title, v)
            self.saveImage(image_path)
            self.pages[title].append((v,image_path))
                
    def initViews(self):
        tostr=lambda *args: tuple(str(i) for i in args)
        
        views=collections.OrderedDict()

        views['front']=tostr(0,0,-1,0,1,0)
        views['back']=tostr(0,0,-1,0,-1,0)
        views['top']=tostr(1,0,0,0,1,0)
        views['bottom']=tostr(-1,0,0,0,1,0)
        views['left']=tostr(0,0,-1,-1,0,0)
        views['right']=tostr(0,0,-1,1,0,0)      
        
        exsistingCS=oEditor.GetRelativeCoordinateSystems()
        
        for k in views:
            if k not in exsistingCS: self.createCS(k, views[k])
        
        return views.keys()
        
    def createCS(self, name, u):
        oEditor.SetWCS(["NAME:Set WCSParameter","Working Coordinate System:=","Global","RegionDepCSOk:=",False])
        
        cs=oEditor.CreateRelativeCS(["NAME:RelativeCSParameters","Mode:=","Axis/Position","OriginX:=","0mm","OriginY:=","0mm","OriginZ:=","0mm","XAxisXvec:=",u[0],"XAxisYvec:=",u[1],"XAxisZvec:=",u[2],"YAxisXvec:=",u[3],"YAxisYvec:=",u[4],"YAxisZvec:=",u[5]],["NAME:Attributes","Name:=",name])    
        
    def saveImage(self, path):
        oEditor.FitAll()
        options=['NAME:SaveImageParams','ShowAxis:=','Default','ShowGrid:=','Default','ShowRuler:=','Default']
        oEditor.ExportModelImageToFile(path, 300,240, options)
               
    
    def genhtml(self):
        with open(self.html, 'w') as f:
            f.writelines('<style>H2{background: blue;color: #fff;padding: 5px 5px;}</style>\n')
            
            for k in self.pages:
                f.writelines('<H2>{}</H2>\n'.format(k))
                for i, j in self.pages[k]:
                    f.writelines('<img src="{}">\n'.format(j))
                
        import webbrowser, os
        webbrowser.open('file://' + os.path.realpath(self.html))  

        
class excitation():
    def __init__(self, weighting):
        '''
        weighting( {'p1':(1,0), 'p2':(1,5), 'p3':(1,10), 'p4':(1,20)}
        '''
        self.oModule=oDesign.GetModule("Solutions")
        
        self.dic={i:(0,0) for i in self.oModule.GetAllSources()}
        for key in weighting:
            if key not in self.dic:
                raise Exception('Key "{}" does not exist in this project!'.format(key))
            else:
                self.dic[key] = weighting[key]
        
    def set(self):
        def single_port(name, exc):
            mag, phase=exc
            return ["Name:=","{}:1".format(name),"Magnitude:=","{}W".format(mag),"Phase:=","{}deg".format(phase)]
        
        allport=[single_port(i, self.dic[i]) for i in self.dic]    
        self.oModule.EditSources([["IncludePortPostProcessing:=",False,"SpecifySystemPower:=",False]]+allport)


modes=collections.OrderedDict()
modes['mode0 0 deg']={'p1':(1,0),'p2':(1,0),'p3':(1,0),'p4':(1,0)}        
modes['mode1 20deg']={'p1':(1,0),'p2':(1,20),'p3':(1,40),'p4':(1,60)}
modes['mode2 40deg']={'p1':(1,0),'p2':(1,40),'p3':(1,80),'p4':(1,120)}
modes['mode3 60deg']={'p1':(1,0),'p2':(1,60),'p3':(1,120),'p4':(1,180)}
modes['mode4 80deg']={'p1':(1,0),'p2':(1,80),'p3':(1,160),'p4':(1,240)}        

cv=CatchView('d:/demo2', 'FarField')
for m in modes:
    exc=excitation(modes[m])
    exc.set()
    cv.saveSection(m)
cv.genhtml()

        
      