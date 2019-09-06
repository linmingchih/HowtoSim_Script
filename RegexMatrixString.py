import re, clr
clr.AddReference('System.Windows.Forms')
from System.Windows.Forms import Clipboard

import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.GetActiveProject()
oDesign = oProject.GetActiveDesign()

oModule = oDesign.GetModule("BoundarySetup")
ports=oModule.GetExcitations()[::2]

x=[(i,j) for i in ports for j in ports]
oDesktop.ClearMessages("", "", 2)
AddWarningMessage(str(x))

def TypeA():
    '''return dB(S(pad1,pad1));dB(S(pad2,pad2)),...'''
    match=[]
    for i, j in x:
        try:
            Ni=int(re.search('pad(\d+)', i).group(1))
            Nj=int(re.search('pad(\d+)', j).group(1))
            if Ni==Nj:
                match.append((i,j))
        except:
            pass
            
    result=';'.join(['dB(S({},{}))'.format(i,j) for i,j in match])
    
    try:
        AddWarningMessage(result)
        Clipboard.SetText(result)
    except:
        AddWarningMessage('Failed!')

TypeA()