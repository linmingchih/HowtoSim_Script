# coding=utf-8
import os, clr, re, sys, logging, time
os.chdir(os.path.dirname(__file__))
clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')

from System import Drawing, Array, ComponentModel, Diagnostics, IO
from System.Windows import Forms
import System.Object as object
import System.String as string
from System.Windows.Forms import DialogResult, OpenFileDialog ,SaveFileDialog, FolderBrowserDialog
from System.Windows.Forms import Clipboard, MessageBox

#------------------------------------------------------------------------------
# Initialize AEDT
#------------------------------------------------------------------------------
logging.basicConfig(filename='ExportLayoutQ3D.log', filemode='w', level=logging.DEBUG, format='%(message)s')
os.chdir(os.path.dirname(__file__))
t0 = time.time()

import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oDesktop.ClearMessages("", "", 2)
try:
    oProject = oDesktop.GetActiveProject()
    oDesign = oProject.GetActiveDesign()
except:
    MessageBox.Show("Please Open HFSS 3D Layout Design")
    
#------------------------------------------------------------------------------
# Quit if Design Type and Solution Setup not Right
#------------------------------------------------------------------------------
if oDesign.GetDesignType() != 'HFSS 3D Layout Design':
    MessageBox.Show('Not HFSS 3D Layout Design!', 'Error Message')
    sys.exit(0)

oModule = oDesign.GetModule("SolveSetups")
setups = oModule.GetSetups()
if not setups:
    MessageBox.Show('Please Add HFSS Solution Setup First!', 'Error Message')
    sys.exit()
    
oEditor = oDesign.GetActiveEditor()

isEnabled = oDesktop.GetAutoSaveEnabled()
if isEnabled:
    oDesktop.EnableAutoSave(False)
#------------------------------------------------------------------------------
# Define Functions
#------------------------------------------------------------------------------

def geBottomMetal():
    result = []
    for i in oEditor.GetStackupLayerNames():    
        info = oEditor.GetLayerInfo(i)  
        if 'Type: signal' in info:
            result.append(i)
    return result[-1]

def getLayerElevation():
    layer_elevation = {}
    bottom_metal = geBottomMetal()

    for i in oEditor.GetStackupLayerNames():    
        info = oEditor.GetLayerInfo(i)        
        lower_elevation = info[-1].split(':')[1].strip()
        thickness = info[-2].split(':')[1].strip()
        if i != bottom_metal:
            layer_elevation[i] = (lower_elevation + '+' + thickness, 'Up')
        else:
            layer_elevation[i] = (lower_elevation, 'Down')
            
    logging.exception(layer_elevation)  
    return layer_elevation

#------------------------------------------------------------------------------
#To Get Die Upper Elevation & BGA Lower Elevation
#------------------------------------------------------------------------------

def getComponentElevation():
    try:
        layer_elevation = getLayerElevation()
    
        component_elevation = {}
        for i in oEditor.FindObjects('Type', 'component'):
            info = oEditor.GetComponentInfo(i)
            layer = info[3].split('=')[1]
            elevation, group = layer_elevation[layer]
            
            if 'dt=1' in info[4] and ("sbsh='Cyl'" in info[4] or "sbsh='Sph'" in info[4]):
                m = re.search("sbh='(.*?)'", info[4])
                height = m.group(1)
            
            elif 'dt=2' in info[4]:
                m = re.search("dh='(.*?)'", info[4])
                height = m.group(1)
            
            elif 'dt=' not in info[4] and ("sbsh='Cyl'" in info[4] or "sbsh='Sph'" in info[4]):
                m = re.search("sbh='(.*?)'", info[4])
                height = m.group(1)
            
            else:
                height = '0mm'
            
            if group == 'Up':
                component_elevation[i] = '{}+{}'.format(elevation, height)
            else:
                component_elevation[i] = '{}-{}'.format(elevation, height)
    except:
            pass
    logging.exception(component_elevation)

    return component_elevation


#------------------------------------------------------------------------------
#To Get EDB Handle
#------------------------------------------------------------------------------
def getLayoutEDBHandle():
    clr.AddReference('Ansys.Ansoft.Edb')
    clr.AddReference('Ansys.Ansoft.SimSetupData')
    import Ansys.Ansoft.Edb as edb
    
    DB = edb.Database.Attach(int(oProject.GetEDBHandle()))
    cells = list(DB.TopCircuitCells)
    
    for i in cells:
        if i.GetName() == (oDesign.GetName() if ';' not in oDesign.GetName() else oDesign.GetName().split(';')[1]):
            layout = i.GetLayout()
            break
    return layout

#------------------------------------------------------------------------------
#To Get Pin Information
#------------------------------------------------------------------------------
def getPinInfo():
    layout = getLayoutEDBHandle()
    component_elevation = getComponentElevation()
    
    pin_info = []
    for i in layout.PadstackInstances:
        comp = i.GetComponent().GetName()
        if not comp:
            continue
        
        pin = i.GetName()
        net = i.GetNet().GetName()        
        #layer = i.GetLayerRange()[1].GetName()
        
        _, location, angle = i.GetPositionAndRotationValue()
        x, y = str(location).replace('(', '').replace(')', '').split(',')
        z = component_elevation[comp]
        location = (x, y, z)      
        
        pin_info.append((comp, pin, net, location))
    return pin_info


def getPinLocation():
    result = {}
    
    for comp, pin, _, location in getPinInfo():
        result[(comp, pin)] = location
    
    return result


#------------------------------------------------------------------------------
# To output data for ListView
#------------------------------------------------------------------------------
def getListViewInfo():
    pininfo = getPinInfo()
    
    listview_info = []
    for comp, pin, net, location in pininfo:
        if comp.upper() == 'BGA':
            listview_info.append(['Sink', comp, pin, net, ''])
        else:
            listview_info.append(['Source', comp, pin, net, ''])
    
    return listview_info

padInfo = getListViewInfo()

#------------------------------------------------------------------------------
# To update OK status in ListView
#------------------------------------------------------------------------------


def updatePadInfo():
    global padInfo
    result = []
    
    for i_type, i_comp, i_pin, i_net, i_status in padInfo:
        x = set(i_type)
        for j_type, j_comp, j_pin, j_net, j_status in padInfo:
            if i_net == j_net:
                x.add(j_type)
        if 'Source' in x and 'Sink' in x:
            status = 'Yes'
        else:
            status = ''
        result.append([i_type, i_comp, i_pin, i_net, status])
    
    padInfo = result

#------------------------------------------------------------------------------
# To output Model for Q3D
#------------------------------------------------------------------------------

def generateSourceSinkModel(listview_info):
    pinloc = getPinLocation()
    
    netgroup = {}
    for assignment, comp, pin, net, status in listview_info:
        if status == 'Float':
            continue
        loc = pinloc[(comp, pin)]
        try:
            netgroup[(net, comp, assignment)] += [(loc, pin)]
        except:
            netgroup[(net, comp, assignment)] = [(loc, pin)]
    
    return netgroup

def ExportQ3D(aedt_path):
    global oProject, oDesign, oEditor
    
    oModule = oDesign.GetModule("SolveSetups")
    oModule.ExportToQ3d(setups[0], aedt_path)
    oProject = oDesktop.OpenProject(aedt_path)
    oDesign = oProject.SetActiveDesign('Q3DDesign1')
    oEditor = oDesign.SetActiveEditor("3D Modeler")

#------------------------------------------------------------------------------
# Get Q3D nets & objects beloning to the net
#------------------------------------------------------------------------------

def getQ3DNets():
    oModule = oDesign.GetModule('BoundarySetup')
    x = oModule.GetExcitations()
    
    info = zip(x[0::2], x[1::2])
    signal_nets = [i for i, j in info if j=='SignalNet']

    result = {}
    for s in signal_nets:
        result[s] = []
        for i in oModule.GetExcitationAssignment(s):
            objname = oEditor.GetObjectNameByID(int(i))
            result[s].append(objname)
        
    return result

#------------------------------------------------------------------------------
# Assign Source/Sink
#------------------------------------------------------------------------------
    
def AssignSource(name, faceIDs, net):
    oModule = oDesign.GetModule("BoundarySetup")
    oModule.AssignSource(
	[
		"NAME:{}".format(name),
		"Faces:="		, faceIDs,
		"ParentBndID:="		, "VSS_RING",
		"TerminalType:="	, "ConstantVoltage",
		"Net:="			, net
	])

def AssignSink(name, faceIDs, net):
    oModule = oDesign.GetModule("BoundarySetup")
    oModule.AssignSink(
	[
		"NAME:{}".format(name),
		"Faces:="		, faceIDs,
		"ParentBndID:="		, "VSS_RING",
		"TerminalType:="	, "ConstantVoltage",
		"Net:="			, net
	])

#------------------------------------------------------------------------------
# Get the face at the location from the objects of the net
#------------------------------------------------------------------------------
def getFaceID(net, location):
    x, y, z = location
    q3dnet = getQ3DNets()
    possible_objs = oEditor.GetBodyNamesByPosition(["NAME:Parameters",
                                                    "XPosition:=", x,
                                                    "YPosition:=", y,
                                                    "ZPosition:=", z])
    
    objs = set(possible_objs).intersection(set(q3dnet[net]))
    for obj in objs:
        face = oEditor.GetFaceByPosition(["NAME:FaceParameters",
                                          "BodyName:=", obj,
                                          "XPosition:=", x,
                                          "YPosition:=", y,
                                          "ZPosition:=", z])
        if face:
            return face
        return None

#------------------------------------------------------------------------------
# Get the faces of the net
#------------------------------------------------------------------------------

def getSourceSinkFaces(model):
    result = {}
    for net, comp, assignment in model:
        result[(net, comp, assignment)] = []
        for location, pin in model[(net, comp, assignment)]:
            faceID = getFaceID(net, location)
            result[(net, comp, assignment)].append((faceID, pin))
    
    return result

#------------------------------------------------------------------------------
# Do Source/Sink Setting
#------------------------------------------------------------------------------

rule = 'net_comp_pin'
def reOrder3(*args):
    if rule == 'net_comp_pin':
        return (args[0], args[1], args[2])
    elif rule == 'net_pin_comp':
        return (args[0], args[2], args[1])
    elif rule == 'comp_pin_net':
        return (args[1], args[2], args[0])    
    elif rule == 'comp_net_pin':
        return (args[1], args[0], args[2])    
    elif rule == 'pin_net_comp':
        return (args[2], args[0], args[1])
    elif rule == 'pin_comp_net':
        return (args[2], args[1], args[0])

def reOrder2(*args):
    if rule in ['net_comp_pin', 'net_pin_comp', 'pin_net_comp']:
        return (args[0], args[1])
    else:
        return (args[1], args[0])


def setSourceSink(source_sink_faces, source_merge = 'False', sink_merge = 'True'):
    for net, comp, assignment in source_sink_faces:
        facepins = source_sink_faces[(net, comp, assignment)]
        faces , pins = zip(*facepins)         
        
        if assignment == 'Source':
            if source_merge and len(faces) > 1:
                name = '{}_{}'.format(*reOrder2(net, comp))
                AssignSource(name, faces, net)
            else:
                for face, pin in facepins:
                    name = '{}_{}_{}'.format(*reOrder3(net, comp, pin))
                    AssignSource(name, [face], net)             

        elif assignment == 'Sink':
            if sink_merge and len(faces) > 1:
                name = '{}_{}'.format(*reOrder2(net, comp))           
                AssignSink(name, faces, net)
            else:
                name = '{}_{}_{}'.format(*reOrder3(net, comp, pins[0]))
                AssignSink(name, [faces[0]], net)
                for face, pin in facepins[1:]:
                    name = '{}_{}_{}'.format(*reOrder3(net, comp, pin))
                    AssignSource(name, [face], net)  

def removeSheet():
    oEditor.Delete(
        [
            "NAME:Selections",
            "Selections:="		, ','.join(oEditor.GetObjectsInGroup('Sheets'))
        ])

#------------------------------------------------------------------------------
# Main Window
#------------------------------------------------------------------------------

class MyForm(Forms.Form):
    def __init__(self):
        self.components = ComponentModel.Container()
        #resources = ComponentModel.ComponentResourceManager(typeof(Form1))
        #listViewItem1 = Forms.ListViewItem(Array[string](["Source","U1","A1","DQ0","True"]), -1, Drawing.Color.OrangeRed, Drawing.Color.Empty, None)
        self.toolStrip1 = Forms.ToolStrip()
        self.toolStripButton1 = Forms.ToolStripButton()
        self.toolStripButton2 = Forms.ToolStripButton()
        self.toolStripButton3 = Forms.ToolStripButton()
        self.toolStripSeparator1 = Forms.ToolStripSeparator()
        self.toolStripLabel1 = Forms.ToolStripLabel()
        self.toolStripComboBox1 = Forms.ToolStripComboBox()        
        
        self.listView1 = Forms.ListView()
        self.columnHeader1 = ((Forms.ColumnHeader()))
        self.columnHeader2 = ((Forms.ColumnHeader()))
        self.columnHeader3 = ((Forms.ColumnHeader()))
        self.columnHeader4 = ((Forms.ColumnHeader()))
        self.columnHeader5 = ((Forms.ColumnHeader()))
        self.button1 = Forms.Button()
        self.toolStripLabel1 = Forms.ToolStripLabel()
        self.checkBox1 = Forms.CheckBox()
        self.checkBox2 = Forms.CheckBox()
        self.toolTip1 = Forms.ToolTip(self.components)
        self.contextMenuStrip1 = Forms.ContextMenuStrip(self.components)
        self.sourceToolStripMenuItem = Forms.ToolStripMenuItem()
        self.sinkToolStripMenuItem = Forms.ToolStripMenuItem()
        self.floatToolStripMenuItem = Forms.ToolStripMenuItem()
        self.toolStrip1.SuspendLayout()
        self.contextMenuStrip1.SuspendLayout()
        self.SuspendLayout()
        # toolStrip1
        self.toolStrip1.ImageScalingSize = Drawing.Size(20, 20)
        self.toolStrip1.Items.Add(self.toolStripButton1)
        self.toolStrip1.Items.Add(self.toolStripButton2)
        self.toolStrip1.Items.Add(self.toolStripButton3)
        self.toolStrip1.Items.Add(self.toolStripSeparator1)
        self.toolStrip1.Items.Add(self.toolStripLabel1)
        self.toolStrip1.Items.Add(self.toolStripComboBox1)
        #self.toolStrip1.SelectedIndex = 0
        self.toolStrip1.Location = Drawing.Point(10, 10)
        self.toolStrip1.Name = "toolStrip1"
        self.toolStrip1.Size = Drawing.Size(815, 26)
        self.toolStrip1.TabIndex = 0
        self.toolStrip1.Text = "toolStrip1"
        # toolStripButton1
        self.toolStripButton1.DisplayStyle = Forms.ToolStripItemDisplayStyle.Text
        self.toolStripButton1.ForeColor = Drawing.Color.OrangeRed

        self.toolStripButton1.ImageTransparentColor = Drawing.Color.Magenta
        self.toolStripButton1.Name = "toolStripButton1"
        self.toolStripButton1.Size = Drawing.Size(61, 23)
        self.toolStripButton1.Text = "Source"
        self.toolStripButton1.Click += self.toolStripButton1_Click
        # toolStripButton2
        self.toolStripButton2.DisplayStyle = Forms.ToolStripItemDisplayStyle.Text
        self.toolStripButton2.ForeColor = Drawing.Color.SeaGreen

        self.toolStripButton2.ImageTransparentColor = Drawing.Color.Magenta
        self.toolStripButton2.Name = "toolStripButton2"
        self.toolStripButton2.Size = Drawing.Size(43, 23)
        self.toolStripButton2.Text = "Sink"
        self.toolStripButton2.Click += self.toolStripButton2_Click
        # toolStripButton3
        self.toolStripButton3.DisplayStyle = Forms.ToolStripItemDisplayStyle.Text
        self.toolStripButton3.ForeColor = Drawing.Color.DodgerBlue

        self.toolStripButton3.ImageTransparentColor = Drawing.Color.Magenta
        self.toolStripButton3.Name = "toolStripButton3"
        self.toolStripButton3.Size = Drawing.Size(47, 23)
        self.toolStripButton3.Text = "Float"
        self.toolStripButton3.Click += self.toolStripButton3_Click
        # toolStripSeparator1
        self.toolStripSeparator1.Name = "toolStripSeparator1"
        self.toolStripSeparator1.Size = Drawing.Size(6, 26)

        # toolStripLabel1
        self.toolStripLabel1.Name = "toolStripLabel1"
        self.toolStripLabel1.Size = Drawing.Size(104, 24)
        self.toolStripLabel1.Text = "Naming Rule:"
        # toolStripComboBox1
        self.toolStripComboBox1.Items.Add("net_comp_pin")
        self.toolStripComboBox1.Items.Add("net_pin_comp")
        self.toolStripComboBox1.Items.Add("comp_pin_net")
        self.toolStripComboBox1.Items.Add("comp_net_pin")
        self.toolStripComboBox1.Items.Add("pin_net_comp")
        self.toolStripComboBox1.Items.Add("pin_comp_net")
        self.toolStripComboBox1.SelectedIndex = 0
        self.toolStripComboBox1.Name = "toolStripComboBox1"
        self.toolStripComboBox1.Size = Drawing.Size(200, 27)        
        
        
        # listView1
        self.listView1.Anchor = (((((Forms.AnchorStyles.Top | Forms.AnchorStyles.Bottom)| Forms.AnchorStyles.Left)| Forms.AnchorStyles.Right)))
        self.listView1.BorderStyle = Forms.BorderStyle.FixedSingle
        self.listView1.Columns.Add(self.columnHeader1)
        self.listView1.Columns.Add(self.columnHeader2)
        self.listView1.Columns.Add(self.columnHeader3)
        self.listView1.Columns.Add(self.columnHeader4)
        self.listView1.Columns.Add(self.columnHeader5)
        #self.listView1.Columns.SelectedIndex = 0
        self.listView1.ContextMenuStrip = self.contextMenuStrip1
        self.listView1.FullRowSelect = True
        self.listView1.GridLines = True
        self.listView1.HideSelection = False
        #self.listView1.Items.Add(listViewItem1)
        #self.listView1.SelectedIndex = 0
        self.listView1.Location = Drawing.Point(10, 41)
        self.listView1.Name = "listView1"
        self.listView1.Size = Drawing.Size(815, 453)
        self.listView1.TabIndex = 1
        self.listView1.UseCompatibleStateImageBehavior = False
        self.listView1.View = Forms.View.Details
        self.listView1.ColumnClick += self.listView1_ColumnClick
        self.listView1.ItemSelectionChanged += self.listView1_ItemSelectionChanged
        # columnHeader1
        self.columnHeader1.Text = "Type"
        self.columnHeader1.Width = 126
        # columnHeader2
        self.columnHeader2.Text = "Component"
        self.columnHeader2.Width = 154
        # columnHeader3
        self.columnHeader3.Text = "Pin"
        self.columnHeader3.Width = 83
        # columnHeader4
        self.columnHeader4.Text = "Net"
        self.columnHeader4.Width = 286
        # columnHeader5
        self.columnHeader5.Text = "Both Source/Sink "
        self.columnHeader5.Width = 127
        # button1
        self.button1.Anchor = (((Forms.AnchorStyles.Bottom | Forms.AnchorStyles.Right)))
        self.button1.BackColor = Drawing.Color.DodgerBlue
        self.button1.Font = Drawing.Font("Microsoft Sans Serif", 12, Drawing.FontStyle.Bold, Drawing.GraphicsUnit.Point)
        self.button1.ForeColor = Drawing.SystemColors.ButtonHighlight
        self.button1.Location = Drawing.Point(715, 500)
        self.button1.Name = "button1"
        self.button1.Size = Drawing.Size(110, 41)
        self.button1.TabIndex = 2
        self.button1.Text = "Export"
        self.button1.UseVisualStyleBackColor = False
        self.button1.Click += self.button1_Click_1
        # toolStripLabel1
        self.toolStripLabel1.Name = "toolStripLabel1"
        self.toolStripLabel1.Size = Drawing.Size(0, 23)
        # checkBox1
        self.checkBox1.Anchor = (((Forms.AnchorStyles.Bottom | Forms.AnchorStyles.Left)))
        self.checkBox1.AutoSize = True
        self.checkBox1.Font = Drawing.Font("Microsoft Sans Serif", 10.2, Drawing.FontStyle.Regular, Drawing.GraphicsUnit.Point)
        self.checkBox1.Location = Drawing.Point(13, 511)
        self.checkBox1.Name = "checkBox1"
        self.checkBox1.Size = Drawing.Size(136, 24)
        self.checkBox1.TabIndex = 3
        self.checkBox1.Text = "Merge Source"
        self.checkBox1.UseVisualStyleBackColor = True
        # checkBox2
        self.checkBox2.Anchor = (((Forms.AnchorStyles.Bottom | Forms.AnchorStyles.Left)))
        self.checkBox2.AutoSize = True
        self.checkBox2.Checked = True
        self.checkBox2.CheckState = Forms.CheckState.Checked
        self.checkBox2.Font = Drawing.Font("Microsoft Sans Serif", 10.2, Drawing.FontStyle.Regular, Drawing.GraphicsUnit.Point)
        self.checkBox2.Location = Drawing.Point(155, 511)
        self.checkBox2.Name = "checkBox2"
        self.checkBox2.Size = Drawing.Size(115, 24)
        self.checkBox2.TabIndex = 4
        self.checkBox2.Text = "Merge Sink"
        self.checkBox2.UseVisualStyleBackColor = True
        # contextMenuStrip1
        self.contextMenuStrip1.ImageScalingSize = Drawing.Size(20, 20)
        self.contextMenuStrip1.Items.Add(self.sourceToolStripMenuItem)
        self.contextMenuStrip1.Items.Add(self.sinkToolStripMenuItem)
        self.contextMenuStrip1.Items.Add(self.floatToolStripMenuItem)
        #self.contextMenuStrip1.SelectedIndex = 0
        self.contextMenuStrip1.Name = "contextMenuStrip1"
        self.contextMenuStrip1.Size = Drawing.Size(127, 76)
        # sourceToolStripMenuItem
        self.sourceToolStripMenuItem.Name = "sourceToolStripMenuItem"
        self.sourceToolStripMenuItem.Size = Drawing.Size(126, 24)
        self.sourceToolStripMenuItem.Text = "Source"
        self.sourceToolStripMenuItem.Click += self.sourceToolStripMenuItem_Click
        # sinkToolStripMenuItem
        self.sinkToolStripMenuItem.Name = "sinkToolStripMenuItem"
        self.sinkToolStripMenuItem.Size = Drawing.Size(126, 24)
        self.sinkToolStripMenuItem.Text = "Sink"
        self.sinkToolStripMenuItem.Click += self.sinkToolStripMenuItem_Click
        # floatToolStripMenuItem
        self.floatToolStripMenuItem.Name = "floatToolStripMenuItem"
        self.floatToolStripMenuItem.Size = Drawing.Size(126, 24)
        self.floatToolStripMenuItem.Text = "Float"
        self.floatToolStripMenuItem.Click += self.floatToolStripMenuItem_Click
        # Form1
        self.AutoScaleDimensions = Drawing.SizeF(8, 16)
        self.AutoScaleMode = Forms.AutoScaleMode.Font
        self.BackColor = Drawing.Color.Azure
        self.ClientSize = Drawing.Size(835, 554)
        self.Controls.Add(self.checkBox2)
        self.Controls.Add(self.checkBox1)
        self.Controls.Add(self.button1)
        self.Controls.Add(self.listView1)
        self.Controls.Add(self.toolStrip1)
        self.Name = "Form1"
        self.Padding = Forms.Padding(10)
        self.Text = "Q3D Terminal Assignment"
        self.Load += self.Form1_Load
        self.toolStrip1.ResumeLayout(False)
        self.toolStrip1.PerformLayout()
        self.contextMenuStrip1.ResumeLayout(False)
        self.ResumeLayout(False)
        self.PerformLayout()


    def Form1_Load(self, sender, e):
        self.sortIndex = 0
        self.ascending = True
        self.reFresh()
        global padInfo
    
    def reFresh(self):
        self.listView1.Items.Clear()
        updatePadInfo()
        
        padInfo.sort(key=lambda tup: tup[self.sortIndex], reverse = self.ascending)
         
        for terminal, comp, pin, net, status in padInfo:
            if terminal == 'Source':
                color = Drawing.Color.OrangeRed
            elif terminal == 'Sink':
                color = Drawing.Color.SeaGreen
            else:
                color = Drawing.Color.DodgerBlue
                
            listViewItem1 = Forms.ListViewItem(Array[string]([terminal, comp, pin, net, status]), -1, color, Drawing.Color.Empty, None)
            self.listView1.Items.Add(listViewItem1)

    def toolStripButton1_Click(self, sender, e):
        if not self.listView1.SelectedIndices:
            return
        for i in self.listView1.SelectedIndices:
            padInfo[i][0] = 'Source'
        self.reFresh()

    def toolStripButton2_Click(self, sender, e):
        if not self.listView1.SelectedIndices:
            return
        for i in self.listView1.SelectedIndices:
            padInfo[i][0] = 'Sink'
        self.reFresh()
        
    def toolStripButton3_Click(self, sender, e):
        if not self.listView1.SelectedIndices:
            return    
        for i in self.listView1.SelectedIndices:
            padInfo[i][0] = 'Float'
        self.reFresh()
        
    def listView1_ColumnClick(self, sender, e):
        self.sortIndex = e.Column
        self.ascending = not self.ascending
        self.reFresh()

    def listView1_ItemSelectionChanged(self, sender, e):
        if len(sender.SelectedItems) > 0:
            self.contextMenuStrip1.Enabled = True
        else:
            self.contextMenuStrip1.Enabled = False

    def sourceToolStripMenuItem_Click(self, sender, e):
        self.toolStripButton1_Click(sender, e)

    def sinkToolStripMenuItem_Click(self, sender, e):
        self.toolStripButton2_Click(sender, e)

    def floatToolStripMenuItem_Click(self, sender, e):
        self.toolStripButton3_Click(sender, e)
        
    def button1_Click_1(self, sender, e):
        dialog = SaveFileDialog()
        dialog.Filter = "aedt files (*.aedt)|*.aedt"
        
        if dialog.ShowDialog() == DialogResult.OK:
            for i in self.Controls:
                i.Enabled = False
            
            model = generateSourceSinkModel(padInfo)   
            ExportQ3D(dialog.FileName)
            source_sink_faces = getSourceSinkFaces(model)
            
            isSourceMerge = self.checkBox1.Checked
            isSinkMerge = self.checkBox2.Checked
            try:
                global rule
                rule = self.toolStripComboBox1.Text
                setSourceSink(source_sink_faces, isSourceMerge, isSinkMerge)
                removeSheet()
            except:
                logging.exception(source_sink_faces)
                MessageBox.Show("Failed!", 'Error')
                raise
            
            MessageBox.Show("Completed!", 'Information')
            self.Close()
        else:
            pass
            

if __name__ == '__main__':
    form = MyForm()
    form.ShowDialog()
    form = MyForm()
    form.Dispose()
    oDesktop.EnableAutoSave(isEnabled)
    AddWarningMessage('Time: {}secs'.format(time.time()-t0))