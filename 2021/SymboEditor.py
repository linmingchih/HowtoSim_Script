# coding=utf-8
spacing = 5

import os, re, sys, clr, json, math, logging
os.chdir(os.path.dirname(__file__))
logging.basicConfig(filename='gui.log', filemode='w', encoding='utf-8', level=logging.DEBUG)
clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')

from System import Drawing, Array, ComponentModel, Diagnostics, IO
from System.Windows import Forms
import System.Object as object
import System.String as string
from System.Windows.Forms import DialogResult, OpenFileDialog ,SaveFileDialog, FolderBrowserDialog
#----------------------------------------------------------------------------
oProject = oDesktop.GetActiveProject()
oDefinitionEditor = None
pin_table = {}

def getSymbolNames():
    oDefinitionManager = oProject.GetDefinitionManager()
    oSymbolManager = oDefinitionManager.GetManager("Symbol")

    return oSymbolManager.GetNames()
    
def getPinNames():
    result = {}
    i=0
    while True:
        i+=1
        prop = oDefinitionEditor.GetProperties('BaseElementTab', 'SchObj@{}'.format(i))
        if not prop:
            break
        if 'PinName' in prop:
            pin_name = oDefinitionEditor.GetPropertyValue('BaseElementTab', 'SchObj@{}'.format(i), 'PinName')
            pin_id = oDefinitionEditor.GetPropertyValue('BaseElementTab', 'SchObj@{}'.format(i), 'SchematicID')
            result[pin_name] = pin_id
    return result
    


def movePin(pin_name, x1, y1):
    pid = pin_table[pin_name]        
    scale = 0.00254
    location = oDefinitionEditor.GetPropertyValue('BaseElementTab', 'SchObj@{}'.format(pid), 'HotSpot')
    x0, y0 = location.split(',')
    dx = scale * (x1-float(x0)/scale)
    dy = scale * (y1-float(y0)/scale)
    
    oDefinitionEditor.Move(
        [
            "NAME:Selections",
            "Selections:="		, ["SchObj@{}".format(pid)]
        ], 
        [
            "NAME:FlipParameters",
            "xdelta:="		, dx,
            "ydelta:="		, dy
        ])

    oDefinitionEditor.ChangeProperty(
        [
            "NAME:AllTabs",
            [
                "NAME:BaseElementTab",
                [
                    "NAME:PropServers", 
                    "SchObj@{}".format(pid)
                ],
                [
                    "NAME:ChangedProps",
                    [
                        "NAME:Length",
                        "Value:="		, "0mil"
                    ]
                ]
            ]
        ])

def moveRect(obj_id, x1, y1, height=0):   
    scale = 0.00254
    location = oDefinitionEditor.GetPropertyValue('BaseElementTab', 'SchObj@{}'.format(obj_id), 'Center')
    x0, y0 = location.split(',')
    x0 = float(x0.replace('mil', ''))*2.54e-5
    y0 = float(y0.replace('mil', ''))*2.54e-5
    dx = scale * (x1-float(x0)/scale)
    dy = scale * (y1-float(y0)/scale)
    
    oDefinitionEditor.Move(
        [
            "NAME:Selections",
            "Selections:="		, ["SchObj@{}".format(obj_id)]
        ], 
        [
            "NAME:FlipParameters",
            "xdelta:="		, dx,
            "ydelta:="		, dy
        ])
    
    if height:
        oDefinitionEditor.ChangeProperty(
            [
                "NAME:AllTabs",
                [
                    "NAME:BaseElementTab",
                    [
                        "NAME:PropServers", 
                        "SchObj@{}".format(obj_id)
                    ],
                    [
                        "NAME:ChangedProps",
                        [
                            "NAME:Height",
                            "Value:="		, "{}mil".format(height*100)
                        ]
                    ]
                ]
            ])    

def editSymbol(data):
    y0_left = 0
    for group in data['left']:
        for pin_name in group:
            movePin(pin_name, -3, y0_left)
            y0_left -= 1
        y0_left -= spacing

    y0_right = 0
    for group in data['right']:
        for pin_name in group:
            movePin(pin_name, 5, y0_right)
            y0_right -= 1
        y0_right -= spacing
        
    for pin_name in data['undefined']:
        movePin(pin_name, 5, y0_right)
        y0_right -= 1

    y0 = min(y0_left, y0_right)

    moveRect("1", 1, y0/2, abs(y0)+4)        
    moveRect("2", -0.5, 0)

#----------------------------------------------------------------------------
class MyForm(Forms.Form):
    def __init__(self):
        treeNode1 = Forms.TreeNode("Left")
        treeNode2 = Forms.TreeNode("Right")
        self.listBox1 = Forms.ListBox()
        self.textBox1 = Forms.TextBox()
        self.button_left = Forms.Button()
        self.treeView1 = Forms.TreeView()
        self.label2 = Forms.Label()
        self.button_clear = Forms.Button()
        self.button_right = Forms.Button()
        self.button_ungroup = Forms.Button()
        self.button_symbol = Forms.Button()
        self.label1 = Forms.Label()
        self.comboBox1 = Forms.ComboBox()
        self.SuspendLayout()
        # listBox1
        self.listBox1.FormattingEnabled = True
        self.listBox1.ItemHeight = 19
        self.listBox1.Location = Drawing.Point(12, 98)
        self.listBox1.Name = "listBox1"
        self.listBox1.SelectionMode = Forms.SelectionMode.MultiExtended
        self.listBox1.Size = Drawing.Size(295, 403)
        self.listBox1.TabIndex = 0
        self.listBox1.SelectedIndexChanged += self.listBox1_SelectedIndexChanged

        # textBox1
        self.textBox1.Location = Drawing.Point(85, 57)
        self.textBox1.Name = "textBox1"
        self.textBox1.Size = Drawing.Size(586, 27)
        self.textBox1.TabIndex = 3
        self.textBox1.TextChanged += self.textBox1_TextChanged

        # button_left
        self.button_left.Anchor = (((Forms.AnchorStyles.Bottom | Forms.AnchorStyles.Right)))
        self.button_left.Font = Drawing.Font("Microsoft JhengHei UI", 10.2, Drawing.FontStyle.Regular, Drawing.GraphicsUnit.Point)
        self.button_left.Location = Drawing.Point(315, 186)
        self.button_left.Name = "button_left"
        self.button_left.Size = Drawing.Size(139, 64)
        self.button_left.TabIndex = 6
        self.button_left.Text = "Group Left"
        self.button_left.UseVisualStyleBackColor = True
        self.button_left.Click += self.button_left_Click

        # treeView1
        self.treeView1.AllowDrop = True
        self.treeView1.Anchor = (((Forms.AnchorStyles.Top | Forms.AnchorStyles.Right)))
        self.treeView1.Cursor = Forms.Cursors.Default
        self.treeView1.Location = Drawing.Point(460, 98)
        self.treeView1.Name = "treeView1"
        treeNode1.Name = "Left"
        treeNode1.Text = "Left"
        treeNode2.Name = "Right"
        treeNode2.Text = "Right"
        self.treeView1.Nodes.Add(treeNode1)
        self.treeView1.Nodes.Add(treeNode2)
        #self.treeView1.Nodes.SelectedIndex = 0
        self.treeView1.Size = Drawing.Size(336, 405)
        self.treeView1.TabIndex = 7
        self.treeView1.AfterSelect += self.treeView1_AfterSelect

        # label2
        self.label2.AutoSize = True
        self.label2.Font = Drawing.Font("Microsoft JhengHei UI", 10.2, Drawing.FontStyle.Regular, Drawing.GraphicsUnit.Point)
        self.label2.Location = Drawing.Point(12, 62)
        self.label2.Name = "label2"
        self.label2.Size = Drawing.Size(53, 22)
        self.label2.TabIndex = 9
        self.label2.Text = "Filter:"
        # button_clear
        self.button_clear.Font = Drawing.Font("Microsoft JhengHei UI", 10.2, Drawing.FontStyle.Regular, Drawing.GraphicsUnit.Point)
        self.button_clear.Location = Drawing.Point(692, 55)
        self.button_clear.Name = "button_clear"
        self.button_clear.Size = Drawing.Size(104, 37)
        self.button_clear.TabIndex = 10
        self.button_clear.Text = "Clear"
        self.button_clear.UseVisualStyleBackColor = True
        self.button_clear.Click += self.button_clear_Click

        # button_right
        self.button_right.Anchor = (((Forms.AnchorStyles.Bottom | Forms.AnchorStyles.Right)))
        self.button_right.Font = Drawing.Font("Microsoft JhengHei UI", 10.2, Drawing.FontStyle.Regular, Drawing.GraphicsUnit.Point)
        self.button_right.Location = Drawing.Point(315, 256)
        self.button_right.Name = "button_right"
        self.button_right.Size = Drawing.Size(139, 64)
        self.button_right.TabIndex = 11
        self.button_right.Text = "Group Right"
        self.button_right.UseVisualStyleBackColor = True
        self.button_right.Click += self.button_right_Click

        # button_ungroup
        self.button_ungroup.Anchor = (((Forms.AnchorStyles.Bottom | Forms.AnchorStyles.Right)))
        self.button_ungroup.Font = Drawing.Font("Microsoft JhengHei UI", 10.2, Drawing.FontStyle.Regular, Drawing.GraphicsUnit.Point)
        self.button_ungroup.Location = Drawing.Point(315, 439)
        self.button_ungroup.Name = "button_ungroup"
        self.button_ungroup.Size = Drawing.Size(139, 64)
        self.button_ungroup.TabIndex = 12
        self.button_ungroup.Text = "Ungroup"
        self.button_ungroup.UseVisualStyleBackColor = True
        self.button_ungroup.Click += self.button_ungroup_Click

        # button_symbol
        self.button_symbol.Anchor = (((Forms.AnchorStyles.Bottom | Forms.AnchorStyles.Right)))
        self.button_symbol.Font = Drawing.Font("Microsoft JhengHei UI", 12, Drawing.FontStyle.Regular, Drawing.GraphicsUnit.Point)
        self.button_symbol.Location = Drawing.Point(592, 514)
        self.button_symbol.Name = "button_symbol"
        self.button_symbol.Size = Drawing.Size(204, 46)
        self.button_symbol.TabIndex = 13
        self.button_symbol.Text = "Generate Symbol"
        self.button_symbol.UseVisualStyleBackColor = True
        self.button_symbol.Click += self.button_symbol_Click

        # label1
        self.label1.AutoSize = True
        self.label1.Font = Drawing.Font("Microsoft JhengHei UI", 10.2, Drawing.FontStyle.Regular, Drawing.GraphicsUnit.Point)
        self.label1.Location = Drawing.Point(12, 20)
        self.label1.Name = "label1"
        self.label1.Size = Drawing.Size(75, 22)
        self.label1.TabIndex = 14
        self.label1.Text = "Symbol:"
        # comboBox1
        self.comboBox1.FormattingEnabled = True
        self.comboBox1.Location = Drawing.Point(85, 15)
        self.comboBox1.Name = "comboBox1"
        self.comboBox1.Size = Drawing.Size(586, 27)
        self.comboBox1.TabIndex = 15
        self.comboBox1.SelectedIndexChanged += self.comboBox1_SelectedIndexChanged_1

        # Form1
        self.AutoScaleDimensions = Drawing.SizeF(9, 19)
        self.AutoScaleMode = Forms.AutoScaleMode.Font
        self.ClientSize = Drawing.Size(811, 572)
        self.Controls.Add(self.comboBox1)
        self.Controls.Add(self.label1)
        self.Controls.Add(self.button_symbol)
        self.Controls.Add(self.button_ungroup)
        self.Controls.Add(self.button_right)
        self.Controls.Add(self.button_clear)
        self.Controls.Add(self.label2)
        self.Controls.Add(self.treeView1)
        self.Controls.Add(self.button_left)
        self.Controls.Add(self.textBox1)
        self.Controls.Add(self.listBox1)
        self.FormBorderStyle = Forms.FormBorderStyle.FixedSingle
        self.MaximizeBox = False
        self.MinimizeBox = False
        self.Name = "Form1"
        self.StartPosition = Forms.FormStartPosition.CenterScreen
        self.Text = "Symbol Editor"
        self.TopMost = True
        self.FormClosing += self.Form1_FormClosing

        self.Load += self.Form1_Load

        self.ResumeLayout(False)
        self.PerformLayout()

    def textBox1_TextChanged(self, sender, e):
        self.refresh_list_view()

    def treeView1_AfterSelect(self, sender, e):
        pass

    def button_left_Click(self, sender, e):
        if len(self.listBox1.SelectedItems) == 0:
            return        
        self.treeView1.Nodes[0].Nodes.Add(str(self.left_group_id))
        for i in self.listBox1.SelectedItems:
            self.treeView1.Nodes[0].Nodes[self.left_group_id].Nodes.Add(i)
            self.pins.remove(i)
        self.left_group_id += 1
        self.treeView1.ExpandAll()
        self.refresh_list_view()

    def button_right_Click(self, sender, e):
        if len(self.listBox1.SelectedItems) == 0:
            return
        self.treeView1.Nodes[1].Nodes.Add(str(self.right_group_id))
        for i in self.listBox1.SelectedItems:
            self.treeView1.Nodes[1].Nodes[self.right_group_id].Nodes.Add(i)
            self.pins.remove(i)
        self.right_group_id += 1
        self.treeView1.ExpandAll()
        self.refresh_list_view()

    def comboBox1_SelectedIndexChanged_1(self, sender, e):
        global pin_table
        global oDefinitionEditor
        if oDefinitionEditor:
            oDefinitionEditor.CloseEditor()
            
        oDefinitionEditor = oProject.SetActiveDefinitionEditor("SymbolEditor", sender.Text)
        oDefinitionEditor.ZoomToFit()
        pin_table = getPinNames()
        self.button_ungroup_Click(sender, e)

    def button_symbol_Click(self, sender, e):
        result = {'left':[], 'right':[]}
        for node in self.treeView1.Nodes[0].Nodes:
            result['left'].append([i.Text for i in node.Nodes])
        for node in self.treeView1.Nodes[1].Nodes:
            result['right'].append([i.Text for i in node.Nodes])
            #result[str(('right', node.Text))] = [i.Text for i in node.Nodes]        
        result['undefined'] = self.pins
        
        editSymbol(result)
        oDefinitionEditor.ZoomToFit()
        oDefinitionEditor.Save()

    def Form1_FormClosing(self, sender, e):
        if oDefinitionEditor:
            oDefinitionEditor.CloseEditor()

    def Form1_Load(self, sender, e):
        for i in getSymbolNames():
            self.comboBox1.Items.Add(i)
            
        self.button_ungroup_Click(sender, e)

    def listBox1_SelectedIndexChanged(self, sender, e):
        pass

    def refresh_list_view(self):    
        self.listBox1.Items.Clear()
        pattern = self.textBox1.Text.strip()
        if pattern:
            try:
                toshowlist = [i for i in self.pins if re.search(pattern, i)]
            except:
                toshowlist = []
        else:
            toshowlist = self.pins
            
        for i in toshowlist:
            self.listBox1.Items.Add(i)

    def button_ungroup_Click(self, sender, e):
        self.left_group_id = 0
        self.right_group_id = 0            
        self.pins = sorted(pin_table.keys())
        self.refresh_list_view()
        self.treeView1.Nodes[0].Nodes.Clear()
        self.treeView1.Nodes[1].Nodes.Clear()

    def button_clear_Click(self, sender, e):
        self.textBox1.Text = ''

if __name__ == '__main__':
    try:
        form = MyForm()
        form.ShowDialog()
        form = MyForm()
        form.Dispose()
        #form.Show()
        #oDesktop.PauseScript()
    except:
        logging.exception('ERROR!')
