config='''import os, sys, re, clr
try:
    dll_dir='C:/Program Files/AnsysEM/AnsysEM19.3/Win64/common/IronPython/DLLs'
    if not os.path.isdir(dll_dir):
        raise Exception 
except:
    m=re.search('(.*Win64)', __file__)
    dll_dir=m.group(1)+'/common/IronPython/DLLs'
finally:
    sys.path.append(dll_dir)
    clr.AddReference('IronPython.Wpf')  
    
    import wpf
    from System.Windows import Window
    os.chdir(os.path.dirname(__file__))
'''
exec(config)

class Matrix():
    def __init__(self, directory='c:/'):
        oProject = oDesktop.GetActiveProject()
        self.oDesign = oProject.GetActiveDesign()
        self.directory=directory      
        self.name=self.oDesign.GetName()
    
    def createReport(self,  solution='Setup1:Sweep1', context='Original'):
        name='{}_{}'.format(self.name, context)
        self.filename='{}{}.csv'.format(self.directory, name)

        #sources=['netA:Source4','netB:Source5','netGnd:Source6','netGnd:Source7','netGnd:Source8']        
        #nets=['netA', 'netB', 'netGnd']
        
        oModule=self.oDesign.GetModule("Solutions")
        sources=oModule.GetNetworkDataSolutionDefinition(solution)
        nets= set([i.split(':')[0] for i in sources])

        _C=['C({},{})'.format(j,i) for i in nets for j in nets]
        _G=['G({},{})'.format(j,i) for i in nets for j in nets]
        _DCL=['DCL({},{})'.format(j,i) for i in sources for j in sources]
        _DCR=['DCR({},{})'.format(j,i) for i in sources for j in sources]
        _ACL=['ACL({},{})'.format(j,i) for i in sources for j in sources]
        _ACR=['ACR({},{})'.format(j,i) for i in sources for j in sources]
        
        data=_C+_G+_DCL+_DCR+_ACL+_ACR
        oModule = self.oDesign.GetModule("ReportSetup")
        oModule.CreateReport(name,"Matrix","Data Table", solution, ["Context:=", context],["Freq:=",["All"]],["X Component:=","Freq","Y Component:=", data],[])
        oModule.ExportToFile(name, self.filename)
        oModule.DeleteReports([name])
    
    
    def fixReport(self):
        with open(self.filename) as f:
            text=f.readlines()
            
        header=re.findall(r'\"(.+?)\"', text[0])
        data=text[1].strip().split(',')
        
        with open(self.filename,'w') as f:
            f.writelines(','.join(['"'+i+'"' for i,j in zip(header, data) if len(j)>0])+'\n')
            for i in text[1:]:
                f.writelines(','.join([j for j in i.strip().split(',') if len(j)>0])+'\n')
        
        os.system('notepad.exe {}'.format(self.filename))
        
#Code Start-----------------------------------
class MyWindow(Window):
    def __init__(self, oDesktop):
        wpf.LoadComponent(self, 'Matrix_Export.xaml')
        
    def Button_Click(self, sender, e):
        m=Matrix(self.tb1.Text)
        m.createReport(self.tb2.Text, self.tb3.Text)
        m.fixReport()     
        

#Code End-------------------------------------        
MyWindow(oDesktop).ShowDialog()

