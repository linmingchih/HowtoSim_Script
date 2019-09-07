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
#AddWarningMessage(str(x))

def TypeA():
    match=[]
    for i, j in x:
        try:
            if i==j:
                match.append((i,j))
        except:
            pass
    if not match:
        AddWarningMessage('No match, Please check condition!')
        return None
    else:
        AddWarningMessage('{} matches!'.format(len(match)))
        [AddWarningMessage(str(i)) for i in match]
        result=';'.join(['dB(S({},{}))'.format(i,j) for i,j in match])
        Clipboard.SetText(result)

def TypeB():
    match=[]
    for i, j in x:
        try:
            mi=re.search('_(\d+)_.*S(\d+)', i)
            mj=re.search('_(\d+)_.*S(\d+)', j)
            if mi.group(1)!=mj.group(1) and mi.group(2)==mj.group(2):
                match.append((i,j))
        except:
            pass
    if not match:
        AddWarningMessage('No match, Please check condition!')
        return None
    else:
        AddWarningMessage('{} matches!'.format(len(match)))
        [AddWarningMessage(str(i)) for i in match]
        result=';'.join(['dB(S({},{}))'.format(i,j) for i,j in match])
        Clipboard.SetText(result)
        
def TypeC():
    match=[]
    for i, j in x:
        try:
            mi=re.search('_(\d+)_.*S(\d+)', i)
            mj=re.search('_(\d+)_.*S(\d+)', j)
            if mi.group(1)==mj.group(1) and (mi.group(2),mj.group(2)) in [('3','4'),('7','8'),('9','10'),('14','15')]:
                match.append((i,j))
        except:
            pass
    if not match:
        AddWarningMessage('No match, Please check condition!')
        return None
    else:
        AddWarningMessage('{} matches!'.format(len(match)))
        [AddWarningMessage(str(i)) for i in match]
        result=';'.join(['dB(S({},{}))'.format(i,j) for i,j in match])
        Clipboard.SetText(result)

def TypeD():
    match=[]
    for i, j in x:
        try:
            mi=re.search('_(\d+)_.*S(\d+)', i)
            mj=re.search('_(\d+)_.*S(\d+)', j)
            if mi.group(1)==mj.group(1) and (mi.group(2),mj.group(2)) in [('3','4'),('7','8'),('9','10'),('14','15')]:
                match.append((i,j))
        except:
            pass
    if not match:
        AddWarningMessage('No match, Please check condition!')
        return None
    else:
        AddWarningMessage('{} matches!'.format(len(match)))
        [AddWarningMessage(str(i)) for i in match]
        result=';'.join(['mag(Z({},{}))'.format(i,j) for i,j in match])
        Clipboard.SetText(result)
TypeD()