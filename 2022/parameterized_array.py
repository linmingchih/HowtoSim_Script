from pyaedt import Hfss

hfss = Hfss(specified_version='2022.1')

hfss['Nx'] = '4'
hfss['wx'] = '1mm'
hfss['wy'] = '10mm'
u=1

models = []
for i in range(100):
    x = hfss.modeler.create_rectangle(2, 
                                      [f'if(Nx>{i}, {u}*wx, wx)','0mm','0mm'], 
                                      [f'if(Nx>{i}, {i+1}*wx, wx)', 'wy'],
                                      name='rect')
    x.color = (255,0,0)
    u+=i+2
    models.append(x)

hfss.modeler.unite(models)
hfss.release_desktop(False, False)
