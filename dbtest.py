# -*- coding: utf-8 -*-

import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oDesktop.ClearMessages("","",2)
import clr
clr.AddReference('Ansys.Ansoft.Edb')
import Ansys.Ansoft.Edb as edb
#------------------------------------------------------

db = edb.Database.Open('d:/demo/Project3.aedb',False)
try:
    cell = list(db.TopCircuitCells)
    layout = cell[0].GetLayout()
    AddWarningMessage(cell[0].GetName())


    for i in layout.PadstackInstances:
        i.SetLayerRange('top','bot')
        n+=1

    
except:
    AddErrorMessage('Excrption!!')
finally:
    db.Save()
    db.Close()

'''取得net名稱
db = edb.Database.Open('d:/demo/Project3.aedb',False)
try:
    cell = list(db.TopCircuitCells)
    layout = cell[0].GetLayout()
    for net in layout.Nets:
        AddWarningMessage(net.GetName())
    
except:
    AddErrorMessage('Excrption!!')
finally:
    db.Close()
'''

'''取得aedb cell名稱
db = edb.Database.Open('d:/demo/Project3.aedb',False)
try:
    cell = list(db.TopCircuitCells)
    for i in cell:
        AddWarningMessage(i.GetName())
    
except:
    AddErrorMessage('Excrption!!')
finally:
    db.Close()
'''
