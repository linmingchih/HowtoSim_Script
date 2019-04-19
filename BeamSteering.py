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
    
    import wpf, time
    from System.Windows import Window, MessageBox
    os.chdir(os.path.dirname(__file__))
'''
exec(config)

import math, cmath
oProject = oDesktop.GetActiveProject()
oDesign = oProject.GetActiveDesign()  
oEditor = oDesign.SetActiveEditor("3D Modeler")

class excitation():
    def __init__(self):
        pass
    
    def setSolution(self, solution="Setup1:LastAdaptive", freq='70e9', variation=""):
        self.sources = self.getSourceNames()
        self.solution=solution
        self.freq=freq
        self.variation=variation
        
    def setWeighting(self, weighting):
        '''
        weighting => {'p1':(1,0), 'p2':(1,5), 'p3':(1,10), 'p4':(1,20)}
        '''
        for i in weighting:
            if i not in self.sources:
                raise Exception('Error: "Source {} does not exist!"'.format(i))
        oModule=oDesign.GetModule("Solutions")
        
        dic={i:(0,0) for i in oModule.GetAllSources()}
        for key in weighting:
            if key not in dic:
                raise Exception('Key "{}" does not exist in this project!'.format(key))
            else:
                dic[key] = weighting[key]
    
        def single_port(name, exc):
            mag, phase=exc
            return ["Name:=","{}:1".format(name),"Magnitude:=","{}W".format(mag),"Phase:=","{}deg".format(phase)]
        
        allport=[single_port(i, dic[i]) for i in dic]    
        oModule.EditSources([["IncludePortPostProcessing:=",False,"SpecifySystemPower:=",False]]+allport)

    def getSourceNames(self):
        oModule=oDesign.GetModule("Solutions")
        return oModule.GetAllSources()
    
    def exportFFDforEachSource(self, folder):
        oModule=oDesign.GetModule("RadField")
        oModule.InsertFarFieldSphereSetup(["NAME:ffd","UseCustomRadiationSurface:=",False,"ThetaStart:=","0deg","ThetaStop:=","180deg","ThetaStep:=","1deg","PhiStart:=","0deg","PhiStop:=","360deg","PhiStep:=","1deg","UseLocalCS:=",False])
        
        w={}
        for i in self.sources:
            for j in self.sources:
                w[j]=(0,0)
            w[i]=(1,0)
            self.setWeighting(w)
            ffdfile="{}/{}.ffd".format(folder, i)
            oModule.ExportRadiationFieldsToFile(["ExportFileName:=",ffdfile,"SetupName:=","ffd","IntrinsicVariationKey:=","Freq={}".format(self.freq),"DesignVariationKey:=",self.variation,"SolutionName:=",self.solution])
                    
        oModule.DeleteFarFieldSetup(["ffd"])

class ffd():
    def __init__(self, E=[]):
        self.E=E
        self.Ntheta=181
        self.Nphi=361
   
    def initialize(self, ffd_file):
        with open(ffd_file) as f:
            text=f.readlines()
    
        self.E=[]
        for i in text[4:]:
            self.E.append([float(j) for j in i.strip().split(' ')])
    
    def queryE(self, theta, phi):
        if 0<=theta<=180 and 0<=phi<=360:
            return self.E[theta*self.Nphi+phi]
        else:
            raise Exception('Error:"theta/phi not in range!"')

    def E2Gain(self, x):
        return (math.sqrt(sum([i*i for i in x])))  
        
    def __add__(self, other):
        newE=[]
        for i,j in zip(self.E, other.E):
            newE.append([i[n]+j[n] for n in range(4)])

        return ffd(newE)
    
    def _rotate(self, x, y, ang):
        a=math.sqrt(x*x+y*y)
        p=cmath.phase(complex(x,y))
        
        ang_r=math.radians(ang)
        return a*math.cos(p+ang_r), a*math.sin(p+ang_r)    
    
    def shiftPhase(self, phase):
        newE=[]
        for Et_re, Et_im, Ep_re, Ep_im in self.E:
            Et=list(self._rotate(Et_re, Et_im, phase))
            Ep=list(self._rotate(Ep_re, Ep_im, phase))
            newE.append(Et+Ep)
        self.E=newE
        return self
        
    def align(self, other, theta, phi):
        data=[]
        x1, x2, x3, x4=self.queryE(theta, phi)
        y1, y2, y3, y4=other.queryE(theta, phi)
        for i in range(0,360):
            z1, z2 = self._rotate(y1, y2, i)
            z3, z4= self._rotate(y3, y4, i)
            Et=self.E2Gain([z1+x1, z2+x2, z3+x3, z4+x4])
            data.append((Et, i))
        
        return max(data)[1]
        
    def computeCDF(self):
        pass

    def output(self):
        return self.E        
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
        
    def getVariations(self, Solution):
        oModule=self.oDesign.GetModule("Solutions")
        return oModule.GetAvailableVariations(Solution)

class MyWindow(Window):
    def __init__(self, oDesktop):
        wpf.LoadComponent(self, 'BeamSteering.xaml')
        self.temp=oDesktop.GetTempDirectory()
        self.sol=solutions()
        self.cb1.Items.Add('Far Fields')        
        self.cb1.SelectedIndex = 0

    def cb1_SelectionChanged(self, sender, e):
        self.cb2.Items.Clear()
        for i in self.sol.getAvailableSolution(self.cb1.SelectedItem):
            if 'AdaptivePass' not in i:
                self.cb2.Items.Add(i)       
        self.cb2.SelectedIndex = 0

    
    def cb2_SelectionChanged(self, sender, e):
        self.cb3.Items.Clear()

        for i in self.sol.getFrequency(self.cb2.SelectedItem):
            #f='{} GHz'.format(float(i)/1e9)
            self.cb3.Items.Add(i)
        self.cb3.SelectedIndex = 0
        try:
            for i in self.sol.getVariations(self.cb2.SelectedItem):
                self.cb4.Items.Add(i)
            self.cb4.SelectedIndex = 0
        except:
            pass
            
    def cb3_SelectionChanged(self, sender, e):
        pass
        
    def bt_Click(self, sender, e):
        try:
            self.info.Text=''
            
            self.exc=excitation()
            self.exc.setSolution(self.cb2.SelectedItem, self.cb3.SelectedItem, self.cb4.SelectedItem)
            self.exc.exportFFDforEachSource(self.temp)
            self.sources=self.exc.getSourceNames()
            MessageBox.Show("Far Field Export Completed!", "Export Status")
        except:
            MessageBox.Show("No Far Field to Export!", "Export Status")
            
    
    def info_MouseDoubleClick(self, sender, e):
        self.info.Text=str(self.sliderTheta.Value)
        pass
        
    def PreviewMouseLeftButtonUp(self, sender, e):
        self.info.Text='Computing...'

        try:
            self.info.Text='Computing...'
            flds=[(i, '{}/{}.ffd'.format(self.temp, i)) for i in self.sources]
            
            phased_exc={}
            theta, phi=int(self.sliderTheta.Value), int(self.sliderPhi.Value)
            x0=ffd()
            x0.initialize(flds[0][1])
            self.info.Text=''
            for i,j in flds:
                x=ffd()
                x.initialize(j)
                p=x0.align(x, theta, phi)
                self.info.Text+='{}:{}\n'.format(i,p)
                phased_exc[i]=(1,p)
        
            self.exc.setWeighting(phased_exc)
        except:
            self.info.Text='Please Export Far Field First!'

        
        
#Code End-------------------------------------        
MyWindow(oDesktop).ShowDialog()

