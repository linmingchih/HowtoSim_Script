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
    
    def savePage(self, title):
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
        oEditor.ExportModelImageToFile(path, 600, 400, options)
               
    
    def genhtml(self):
        with open(self.html, 'w') as f:
            for k in self.pages:
                f.writelines('<H2>{}</H2>'.format(k))
                for i, j in self.pages[k]:
                    f.writelines('<img src="{}" bgcolor="#E6E6FA">'.format(j))
                
        import webbrowser, os
        webbrowser.open('file://' + os.path.realpath(self.html))  

cv=CatchView('d:/demo2', 'Testing2')
cv.savePage('E_Field')
#cv.savePage('H_Field')   
cv.genhtml()

        
      