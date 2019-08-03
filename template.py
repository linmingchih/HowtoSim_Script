config='''import os, sys, re, clr
try:
    dll_dir='C:/Program Files/AnsysEM/AnsysEM19.3/Win64/common/IronPython/DLLs'
    if not os.path.isdir(dll_dir):
        raise Exception 
except:
    m=re.search('(.*Win64)', __file__)
    dll_dir=m.group(1)+'/common/IronPython/DLLs'
finally:
    sys.path.append(dll_dir)
    clr.AddReference('IronPython.Wpf')  
    
    import wpf
    from System.Windows import Window
    from System.Windows.Controls import ListBoxItem
    os.chdir(os.path.dirname(__file__))
'''
exec(config)
#Functions---------------------------------------------------------------------|



    
#GUI---------------------------------------------------------------------------|
class MyWindow(Window):
    def __init__(self):
        wpf.LoadComponent(self, 'template.xaml')
        

#Code End----------------------------------------------------------------------|       
MyWindow().ShowDialog()

