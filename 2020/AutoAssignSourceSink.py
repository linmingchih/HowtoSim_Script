oProject = oDesktop.GetActiveProject()
oDesign = oProject.GetActiveDesign()
oEditor = oDesign.SetActiveEditor('3D Modeler')
oModule = oDesign.GetModule('BoundarySetup')
oDesktop.ClearMessages("","",2)
def getinfo():
    x = oModule.GetExcitations()
    info = zip(x[0::2], x[1::2])

    signal_nets = [i for i, j in info if j=='SignalNet']
    sources = [i for i, j in info if j=='Source']
    sinks = [i for i, j in info if j=='Sink']
    if not signal_nets:
        AddErrorMessage("There is no SignalNet!")
    else:
        return signal_nets, sources, sinks

signal_nets, sources, sinks = getinfo()
result = {}
for s in signal_nets:
    result[s] = []
    for i in oModule.GetExcitationAssignment(s):
        objname = oEditor.GetObjectNameByID(int(i))
        result[s] += oEditor.GetFaceIDs(objname)

for i in oEditor.GetSelections():
    if i[0:4] == 'Face':
        faceid = i[4:]
        NotinSignalNet = True
        for net in result:
            if faceid in result[net]:
                NotinSignalNet = False
                break
        if NotinSignalNet:
            AddWarningMessage("{} is not on SignalNet".format(i))
            continue

        for i in range(1,10000):
            name = '{}-0'.format(net)
            if name not in sinks:
                break
                
            name = '{}-{}'.format(net,i)
            if name not in sources:
                break
        
        if '0' in name:
            oModule.AssignSink(
                [
                    "NAME:{}".format(name),
                    "Faces:="		, [int(faceid)],
                    "ParentBndID:="		, net,
                    "Net:="			, net
                ])
            signal_nets, sources, sinks = getinfo()    
        else:
            oModule.AssignSource(
                [
                    "NAME:{}".format(name),
                    "Faces:="		, [int(faceid)],
                    "ParentBndID:="		, net,
                    "Net:="			, net
                ])       
            signal_nets, sources, sinks = getinfo()
    else:
        pass