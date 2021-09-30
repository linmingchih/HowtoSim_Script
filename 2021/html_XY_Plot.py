# coding=utf-8
import os, re, sys, clr, json, math, logging, webbrowser
os.chdir(os.path.dirname(__file__))
#logging.basicConfig(filename='gui.log', filemode='w', encoding='utf-8', level=logging.DEBUG)
clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')

from System import Drawing, Array, ComponentModel, Diagnostics, IO
from System.Windows import Forms
import System.Object as object
import System.String as string
from System.Windows.Forms import DialogResult, OpenFileDialog ,SaveFileDialog, FolderBrowserDialog
#----------------------------------------------------------------------------

template = r'''
<!DOCTYPE html>
<html>
  <head>
    <title>Embedding Vega-Lite</title>
    <script src="https://cdn.jsdelivr.net/npm/vega@5.20.2"></script>
    <script src="https://cdn.jsdelivr.net/npm/vega-lite@5.1.1"></script>
    <script src="https://cdn.jsdelivr.net/npm/vega-embed@6.18.2"></script>
  </head>
  <body>
    <div id="vis"></div>

    <script type="text/javascript">
      var yourVlSpec = {
  "params": [{
    "name": "grid",
    "select": "interval",
    "bind": "scales"
  }],
  "columns":4,
  "repeat": [$repeat$],

  "spec":
  { "layer":[
      {
        "width": 300,
        "heigh": 100,
        "mark": {"type":"line", "color":"red"},
        "encoding": {
          "x": {"field": "$x$", "type": "quantitative"},
          "y": {"field": {"repeat": "repeat"}, "type": "quantitative"},
        "tooltip": [
          {"field": "$x$", "type": "quantitative"},
          {"field": {"repeat": "repeat"}, "type": "quantitative"}
        ]
        }
      }  
    ]
  },

  "data": {
    "values": $value$  }  
}

      vegaEmbed('#vis', yourVlSpec);
    </script>
  </body>
</html>
'''
def run(csv_path):
    with open(csv_path) as f:
        text= f.readlines()

    output = []
    header = [i.replace('[', '').replace(']', '').replace('"','').strip() for i in text[0].split('","')]
    html_header = ','.join(['"{}"'.format(i) for i in header[1:]])
    for line in text[1:]:
        temp = []
        for x, y in zip(header, line.strip().split(',')):
            temp.append('"{}":{}'.format(x, y))
        output.append('{' + ','.join(temp) + '}')

    value = '[' + ','.join(output) + ']'

    html = template.replace('$repeat$', html_header).replace('$x$', header[0]).replace('$value$', value)
    html_path = csv_path.replace('csv', 'html')
    with open(html_path, 'w') as f:
        f.write(html)

    webbrowser.open(html_path)

try:
    image_path = './ANSYS.png'
    oDesktop.ClearMessages("", "", 2)
    AddWarningMessage('Welcome')    

    oProject = oDesktop.GetActiveProject()
    oDesign = oProject.GetActiveDesign()
    oModule = oDesign.GetModule("ReportSetup")
    reports = oModule.GetAllReportNames()

except:
    pass

#----------------------------------------------------------------------------
class MyForm(Forms.Form):
    def __init__(self):
        self.label1 = Forms.Label()
        self.comboBox1 = Forms.ComboBox()
        self.button1 = Forms.Button()
        self.SuspendLayout()
        # label1
        self.label1.AutoSize = True
        self.label1.Location = Drawing.Point(12, 9)
        self.label1.Name = "label1"
        self.label1.Size = Drawing.Size(84, 15)
        self.label1.TabIndex = 0
        self.label1.Text = "Report Name"
        # comboBox1
        self.comboBox1.FormattingEnabled = True
        self.comboBox1.Location = Drawing.Point(12, 27)
        self.comboBox1.Name = "comboBox1"
        self.comboBox1.Size = Drawing.Size(222, 23)
        self.comboBox1.TabIndex = 1
        # button1
        self.button1.Location = Drawing.Point(159, 56)
        self.button1.Name = "button1"
        self.button1.Size = Drawing.Size(75, 33)
        self.button1.TabIndex = 2
        self.button1.Text = "Generate"
        self.button1.UseVisualStyleBackColor = True
        self.button1.Click += self.button1_Click

        # Form1
        self.AutoScaleDimensions = Drawing.SizeF(7, 15)
        self.AutoScaleMode = Forms.AutoScaleMode.Font
        self.ClientSize = Drawing.Size(246, 103)
        self.Controls.Add(self.button1)
        self.Controls.Add(self.comboBox1)
        self.Controls.Add(self.label1)
        self.FormBorderStyle = Forms.FormBorderStyle.FixedSingle
        self.Name = "Form1"
        self.StartPosition = Forms.FormStartPosition.CenterScreen
        self.Text = "Open HTML Report"
        self.TopMost = True
        self.Load += self.Form1_Load

        self.ResumeLayout(False)
        self.PerformLayout()

    def Form1_Load(self, sender, e):
        self.table = {}
        for n, i in enumerate(reports):
            self.comboBox1.Items.Add(i)
            self.table[n] = i
        self.comboBox1.SelectedIndex = 0

    def button1_Click(self, sender, e):
        report_name = self.table[self.comboBox1.SelectedIndex]
        AddWarningMessage(str(report_name))
        
        oModule = oDesign.GetModule("ReportSetup")
        oModule.ExportToFile(report_name, report_name + '.csv', False)
        run(report_name + '.csv')

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
