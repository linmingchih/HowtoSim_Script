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

#Code Start-----------------------------------
class solutions():
    def __init__(self):
        oProject = oDesktop.GetActiveProject()
        self.oDesign = oProject.GetActiveDesign()
        
    def getReportType(self):
        oModule=self.oDesign.GetModule("ReportSetup")
        return oModule.GetAvailableReportTypes()

    def getAvailableSolution(self, ReportType):
        oModule=self.oDesign.GetModule("ReportSetup")
        return oModule.GetAvailableSolutions(ReportType)
    
    def getFrequency(self, Solution):
        oModule=self.oDesign.GetModule("Solutions")
        return oModule.GetSolveRangeInfo(Solution)

class MyWindow(Window):
    def __init__(self, oDesktop):
        wpf.LoadComponent(self, 'ShowSolution.xaml')
        
        self.sol=solutions()
        self.cb1.ItemsSource=self.sol.getReportType()        
        self.cb1.SelectedIndex = 0

    def cb1_SelectionChanged(self, sender, e):
        self.cb2.Items.Clear()
        for i in self.sol.getAvailableSolution(self.cb1.SelectedItem):
            if 'AdaptivePass' not in i:
                self.cb2.Items.Add(i)       
        self.cb2.SelectedIndex = 0

    
    def cb2_SelectionChanged(self, sender, e):
        self.cb3.Items.Clear()
        try:
            for i in self.sol.getFrequency(self.cb2.SelectedItem):
                f='{} GHz'.format(float(i)/1e9)
                self.cb3.Items.Add(f)
            self.cb3.SelectedIndex = 0
        except:
            pass
            
            

    def cb3_SelectionChanged(self, sender, e):
        pass

     

#Code End-------------------------------------        
MyWindow(oDesktop).ShowDialog()

