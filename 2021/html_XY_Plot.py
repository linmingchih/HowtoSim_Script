# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 07:55:10 2021

@author: mlin
"""
import os
import sys
import clr
import webbrowser
clr.AddReference("System.Windows.Forms")

from System.Windows.Forms import DialogResult, OpenFileDialog
dialog = OpenFileDialog()
dialog.Multiselect = False
dialog.Title = "html plot"
dialog.Filter = "csv files (*.csv)|*.csv"

if dialog.ShowDialog() == DialogResult.OK:
    csv_path = dialog.FileName

else:
    pass



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
    