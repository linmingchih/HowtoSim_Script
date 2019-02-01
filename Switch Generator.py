import clr
import os

# Verify these are needed.
clr.AddReference('System')
clr.AddReference('System.Drawing')
clr.AddReference("System.Windows.Forms")

#  Windows Forms Elements
from System.Drawing import Point, Icon, Color
from System.Windows import Forms
from System.Windows.Forms import Application, Form, TextBox, Label, MessageBox
from System.Windows.Forms import DialogResult, GroupBox, FormBorderStyle
from System.Windows.Forms import ComboBox, Button, DialogResult, FormStartPosition 
from System.Drawing import Size, Color, SolidBrush, Rectangle

class SelectFromList(Form):

    """
    form = SelectFromList(floor_types.keys())
    form.show()
    if form.DialogResult == DialogResult.OK:
        chosen_type_name = form.selected
    """

    def __init__(self):

        #  Window Settings
        self.Text = 'Switch Generator'

        self.Width = 200
        self.Height = 220   
        self.MinimizeBox = False
        self.MaximizeBox = False
        self.BackgroundColor = Color.Red
        self.FormBorderStyle = FormBorderStyle.FixedSingle
        self.ShowIcon = False
        

        self.label1 = Label()
        self.label1.Text='Input number:'
        self.label1.Location= Point(10,0)
        
        self.tb=TextBox()
        self.tb.Text="8"
        self.tb.Location = Point(10,25)        
        self.tb.Width=160

        self.label2 = Label()
        self.label2.Text='file name:'
        self.label2.Location= Point(10,60)
        
        self.filepath=TextBox()       
        self.filepath.Text="c:/switch.cir"
        self.filepath.Location = Point(10,85)        
        self.filepath.Width=160
        
        button = Button()
        button.Text = 'Generate'
        button.Location = Point(10,120)
        button.Width = 100
        button.Height = 30
        button.Click += self.button_click

        self.Controls.Add(self.label1)
        self.Controls.Add(self.tb)
        self.Controls.Add(self.label2)        
        self.Controls.Add(self.filepath)        
        self.Controls.Add(button)

    def button_click(self, sender, event):
        number=int(self.tb.Text)
        file=self.filepath.Text

        netlist='.subckt switch in '+ ' '.join(['o'+str(i+1) for i in range(number)]) +' on=1 Zt=50\n'
        for i in range(number):
            if i==0:
                netlist+='.if(on=={})\n'.format(i+1)
            else:
                netlist+='.elseif(on=={})\n'.format(i+1)
                
            for j in range(number):
                if i==j:
                    netlist+='r{0} o{0} in 0\n'.format(j+1)
                else:
                    netlist+='r{0} o{0} 0 Zt\n'.format(j+1)

        netlist+='.else\n'
        netlist+='\n'.join(['r{0} o{0} 0 Zt'.format(i+1) for i in range(number)])
        netlist+='\n.endif\n.ends'

        with open(file, 'w') as f:
            f.writelines(netlist)
            MessageBox.Show(self.filepath.Text + " is generated!")

    def show(self):
        """ Show Dialog """
        self.StartPosition = FormStartPosition.CenterParent;
        self.ShowDialog()
        
form1 = SelectFromList()
form1.show()