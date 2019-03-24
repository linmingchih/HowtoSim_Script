oProject = oDesktop.GetActiveProject()
oDesign = oProject.GetActiveDesign()  
oEditor = oDesign.SetActiveEditor("3D Modeler")

import collections
class CatchView():
    def __init__(self, report_name, path):
        self.image_list=[]
        
        for v in self.initViews():
            oEditor.SetTopDownViewDirectionForActiveView(v)
            imahge_path='{}{}_{}.png'.format(path,report_name,v)
            self.saveImage(imahge_path)
            self.image_list.append((v,imahge_path))
        
        self.genhtml('{}{}.html'.format(path,report_name))
        
    def initViews(self):
        tostr=lambda *args: tuple(str(i) for i in args)
        
        views=collections.OrderedDict()
        views['top']=tostr(0,0,-1,-1,0,0)
        views['bottom']=tostr(0,0,-1,1,0,0)
        views['front']=tostr(1,0,0,0,1,0)
        views['back']=tostr(-1,0,0,0,1,0)
        views['left']=tostr(0,0,-1,0,1,0)
        views['right']=tostr(0,0,1,0,1,0)
        
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
               
    
    def genhtml(self, html_file):
        with open(html_file, 'w') as f:
            for i,j in self.image_list:
                f.writelines('<figcaption>view:{}</figcaption><img src="{}">'.format(i,j))
                
        import webbrowser, os
        webbrowser.open('file://' + os.path.realpath(html_file))  

CatchView('H_Field','d:/demo2/')    
     

        
      