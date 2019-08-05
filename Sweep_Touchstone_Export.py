import ScriptEnv

class solutions():
    def __init__(self):
        oProject = oDesktop.GetActiveProject()
        self.oDesign = oProject.GetActiveDesign()
        
    def getReportType(self):
        oModule=self.oDesign.GetModule("ReportSetup")
        return oModule.GetAvailableReportTypes()

    def getAvailableSolution(self, ReportType):
        oModule=self.oDesign.GetModule("ReportSetup")
        return oModule.GetAvailableSolutions(ReportType)
    
    def getFrequency(self, Solution):
        oModule=self.oDesign.GetModule("Solutions")
        return oModule.GetSolveRangeInfo(Solution)
        
    def getVariations(self, Solution):
        oModule=self.oDesign.GetModule("Solutions")
        return oModule.GetAvailableVariations(Solution)

oProject = oDesktop.GetActiveProject()
oDesign = oProject.GetActiveDesign()
oModule = oDesign.GetModule("Solutions")

sol=solutions()
for i in sol.getReportType():
    for j in sol.getAvailableSolution(i):
        if 'Sweep' not in j:
            continue
        for k in sol.getVariations(j):
            try:
                snpfile="{}{}.s{}p".format(oProject.GetPath(),k,oModule.GetEditSourcesCount())
                oModule.ExportNetworkData(k, [j], 3, snpfile, ["All"], True, 50, "S", -1, 0, 15, True, False, False)
                AddWarningMessage("Export: {}".format(snpfile))
            except:
                pass