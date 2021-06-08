# coding=utf-8
import os, clr
os.chdir(os.path.dirname(__file__))
clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')

from System import Drawing, Array, ComponentModel, Diagnostics, IO
from System.Windows import Forms
import System.Object as object
import System.String as string
from System.Windows.Forms import MessageBox
#----------------------------------------------------------------------------
from collections import OrderedDict
import logging
logging.basicConfig(filename='./message.log', level=logging.DEBUG, filemode='w', format='%(message)s')
import re
import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oDesktop.ClearMessages("", "", 2)
oProject = oDesktop.GetActiveProject()
oDesign = oProject.GetActiveDesign()
oEditor = oDesign.GetActiveEditor()

lines = oEditor.FindObjects('type', 'line')


def getLayerLineInfo():
    data = OrderedDict()
    for layer in oEditor.GetStackupLayerNames():
        objs = oEditor.FindObjects('layer', layer)
        data[layer] = list(set(lines).intersection(set(objs)))

    result = OrderedDict()
    for layer in data:
        if not bool(data[layer]):
            continue
        result[layer] = {}
        for line in data[layer]:
            net = oEditor.GetPropertyValue('BaseElementTab', line, 'Net')
            line_width = oEditor.GetPropertyValue('BaseElementTab', line, 'LineWidth')
            try:
                result[layer][net] +=[(line, line_width)]
            except:
                result[layer][net] = [(line, line_width)]
    return result

def changeLineWidth(line, width):
    oEditor.ChangeProperty(
        [
            "NAME:AllTabs",
            [
                "NAME:BaseElementTab",
                [
                    "NAME:PropServers", 
                    line
                ],
                [
                    "NAME:ChangedProps",
                    [
                        "NAME:LineWidth",
                        "Value:="		, width
                    ]
                ]
            ]
        ])
#----------------------------------------------------------------------------
class MyForm(Forms.Form):
    def __init__(self):
        self.label1 = Forms.Label()
        self.label2 = Forms.Label()
        self.listBox_selection = Forms.ListBox()
        self.comboBox_layer = Forms.ComboBox()
        self.textBox_net = Forms.TextBox()
        self.label3 = Forms.Label()
        self.textBox_linewidth = Forms.TextBox()
        self.button_change = Forms.Button()
        self.label4 = Forms.Label()
        self.SuspendLayout()
        # label1
        self.label1.AutoSize = True
        self.label1.Location = Drawing.Point(13, 10)
        self.label1.Name = "label1"
        self.label1.Size = Drawing.Size(50, 19)
        self.label1.TabIndex = 0
        self.label1.Text = "Layer:"
        # label2
        self.label2.AutoSize = True
        self.label2.Location = Drawing.Point(13, 72)
        self.label2.Name = "label2"
        self.label2.Size = Drawing.Size(103, 19)
        self.label2.TabIndex = 1
        self.label2.Text = "Net Keyword:"
        self.label2.Click += self.label2_Click

        # listBox_selection
        self.listBox_selection.FormattingEnabled = True
        self.listBox_selection.ItemHeight = 19
        self.listBox_selection.Location = Drawing.Point(174, 32)
        self.listBox_selection.Name = "listBox_selection"
        self.listBox_selection.SelectionMode = Forms.SelectionMode.MultiExtended
        self.listBox_selection.Size = Drawing.Size(225, 308)
        self.listBox_selection.TabIndex = 2
        self.listBox_selection.SelectedIndexChanged += self.listBox_selection_SelectedIndexChanged

        # comboBox_layer
        self.comboBox_layer.FormattingEnabled = True
        self.comboBox_layer.Location = Drawing.Point(13, 32)
        self.comboBox_layer.Name = "comboBox_layer"
        self.comboBox_layer.Size = Drawing.Size(151, 27)
        self.comboBox_layer.TabIndex = 3
        self.comboBox_layer.SelectedIndexChanged += self.comboBox_layer_SelectedIndexChanged

        # textBox_net
        self.textBox_net.Location = Drawing.Point(13, 94)
        self.textBox_net.Name = "textBox_net"
        self.textBox_net.Size = Drawing.Size(151, 27)
        self.textBox_net.TabIndex = 4
        self.textBox_net.Text = ".*"
        self.textBox_net.TextChanged += self.textBox_net_TextChanged

        # label3
        self.label3.AutoSize = True
        self.label3.Location = Drawing.Point(13, 207)
        self.label3.Name = "label3"
        self.label3.Size = Drawing.Size(88, 19)
        self.label3.TabIndex = 5
        self.label3.Text = "Line Width:"
        # textBox_linewidth
        self.textBox_linewidth.Location = Drawing.Point(13, 229)
        self.textBox_linewidth.Name = "textBox_linewidth"
        self.textBox_linewidth.Size = Drawing.Size(151, 27)
        self.textBox_linewidth.TabIndex = 6
        # button_change
        self.button_change.Font = Drawing.Font("Microsoft JhengHei UI", 12, Drawing.FontStyle.Bold, Drawing.GraphicsUnit.Point)
        self.button_change.Location = Drawing.Point(13, 278)
        self.button_change.Name = "button_change"
        self.button_change.Size = Drawing.Size(151, 62)
        self.button_change.TabIndex = 7
        self.button_change.Text = "CHANGE"
        self.button_change.UseVisualStyleBackColor = True
        self.button_change.Click += self.button_change_Click

        # label4
        self.label4.AutoSize = True
        self.label4.Location = Drawing.Point(174, 10)
        self.label4.Name = "label4"
        self.label4.Size = Drawing.Size(104, 19)
        self.label4.TabIndex = 8
        self.label4.Text = "Net Selection:"
        # Form1
        self.AutoScaleDimensions = Drawing.SizeF(9, 19)
        self.AutoScaleMode = Forms.AutoScaleMode.Font
        self.ClientSize = Drawing.Size(412, 353)
        self.Controls.Add(self.label4)
        self.Controls.Add(self.button_change)
        self.Controls.Add(self.textBox_linewidth)
        self.Controls.Add(self.label3)
        self.Controls.Add(self.textBox_net)
        self.Controls.Add(self.comboBox_layer)
        self.Controls.Add(self.listBox_selection)
        self.Controls.Add(self.label2)
        self.Controls.Add(self.label1)
        self.FormBorderStyle = Forms.FormBorderStyle.FixedSingle
        self.MaximizeBox = False
        self.MinimizeBox = False
        self.MinimumSize = Drawing.Size(400, 400)
        self.Name = "Form1"
        self.Padding = Forms.Padding(10)
        self.SizeGripStyle = Forms.SizeGripStyle.Show
        self.StartPosition = Forms.FormStartPosition.CenterScreen
        self.Text = "Line Width Editor"
        self.TopMost = True
        self.Load += self.Form1_Load

        self.ResumeLayout(False)
        self.PerformLayout()
    
    def refreshListBox(self):
        self.listBox_selection.Items.Clear()
        for net in self.info[self.comboBox_layer.Text]:
            if re.search(self.textBox_net.Text, net):
                width = self.info[self.comboBox_layer.Text][net][0][1]
                self.listBox_selection.Items.Add('{} - {}'.format(net, width))    
    
    def textBox_net_TextChanged(self, sender, e):
        self.refreshListBox()

    def label2_Click(self, sender, e):
        pass

    def listBox_selection_SelectedIndexChanged(self, sender, e):
        pass

    def comboBox_layer_SelectedIndexChanged(self, sender, e):
        self.refreshListBox()

    def button_change_Click(self, sender, e):
        try:
            new_width = self.textBox_linewidth.Text
            
            for net_width in self.listBox_selection.SelectedItems:
                net = net_width.split()[0]
                
                for n, (line, width) in enumerate(self.info[self.comboBox_layer.Text][net]):
                    changeLineWidth(line, new_width)
                    self.info[self.comboBox_layer.Text][net][n] = (line, new_width)
            
            self.refreshListBox()
        except:
            logging.exception('Error')
            MessageBox.Show('Invalid Input!')
            self.refreshListBox()

    def Form1_Load(self, sender, e):
        self.info = getLayerLineInfo()
        for layer in self.info:
            self.comboBox_layer.Items.Add(layer)
            self.comboBox_layer.SelectedIndex = 0

if __name__ == '__main__':
    form = MyForm()
    form.ShowDialog()
    form = MyForm()
    form.Dispose()
    AddWarningMessage('Good Bye!')
    #form.Show()
    #oDesktop.PauseScript()
