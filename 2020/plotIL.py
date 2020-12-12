
import os, sys, re, clr
import math, cmath
import collections

win64_dir = oDesktop.GetExeDir()
dll_dir = os.path.join(win64_dir, 'common/IronPython/DLLs')
python3_dir = os.path.join(win64_dir, 'commonfiles/CPython/3_7/winx64/Release/python')

sys.path.append(dll_dir)
sys.path.append(python3_dir)
clr.AddReference('IronPython.Wpf')

os.chdir(os.path.dirname(__file__))

clr.AddReference("System.Windows.Forms")

from System.Windows.Forms import DialogResult, OpenFileDialog
dialog = OpenFileDialog()
dialog.Filter = "text files (*.snp)|*.s*p"

if dialog.ShowDialog() == DialogResult.OK:
    with open('plotIL.bat', 'w') as f:
        f.writelines('"{}/python" ./plotIL3.py "{}"\n'.format(python3_dir, dialog.FileName))

    os.system('.\plotIL.bat')
else:
    pass




