relative_permittivity='4.11483+0.0281238*ln((2.53303e+22+Freq*Freq)/(4.95658e+09+Freq*Freq))'

bulk_conductivity='1e-12+3.12919e-12*Freq*(atan(Freq/70403)-atan(Freq/1.59155e+11))'

import ScriptEnv, random, string

def calculate(relative_permittivity,bulk_conductivity):
    from math import *
    ln=log
    F=[pow(10,i/10) for i in range(30, 130)]
    x=relative_permittivity
    y=bulk_conductivity

    Dk=eval('[{} for Freq in F]'.format(x))
    Cond=eval('[{} for Freq in F]'.format(y))

    td=[Cond_p/(2*pi*Freq)/(Dk_p*8.8542e-12) for Cond_p, Freq, Dk_p in zip(Cond,F,Dk)]

    with open("Dk_tanD.csv",'w') as f:
        f.write('Freq, Dk, TanD\n')
        for i,j,k in zip(F,Dk,td):
            f.write(str(i)+', ' + str(j)+', '+str(k)+'\n')
    
    generate_plot()    
    
    
def generate_plot():
    ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
    oDesktop.RestoreWindow()
    oProject = oDesktop.GetActiveProject()
    oDesign = oProject.GetActiveDesign()
    oModule = oDesign.GetModule("Solutions")
    
    name= ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(6)])
    
    oModule.ImportTable("Dk_tanD.csv", name, "Table", True, True, ["Freq", "Dk", "TanD"], [True, False, False])
    oModule = oDesign.GetModule("ReportSetup")
    oModule.CreateReport(name, "Modal Solution Data", "Rectangular Plot", name+" : Table", [], 
        [
            "Tb(Freq):="		, ["All"]
        ], 
        [
            "X Component:="		, "Tb(Freq)",
            "Y Component:="		, ["Tb(Dk)","Tb(TanD)"]
        ], [])
    oModule.ChangeProperty(
        [
            "NAME:AllTabs",
            [
                "NAME:Trace",
                [
                    "NAME:PropServers", 
                    name+":Tb(TanD)"
                ],
                [
                    "NAME:ChangedProps",
                    [
                        "NAME:Y Axis",
                        "Value:="		, "Y2"
                    ]
                ]
            ]
        ])
    oModule.ChangeProperty(
        [
            "NAME:AllTabs",
            [
                "NAME:Scaling",
                [
                    "NAME:PropServers", 
                    name+":AxisX"
                ],
                [
                    "NAME:ChangedProps",
                    [
                        "NAME:Axis Scaling",
                        "Value:="		, "Log"
                    ]
                ]
            ]
        ])

        
calculate(relative_permittivity,bulk_conductivity)             
