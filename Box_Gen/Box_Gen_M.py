def buildBlock(x,y,z,oDesktop):

    oProject = oDesktop.GetActiveProject()
    oDesign = oProject.GetActiveDesign()
    oEditor = oDesign.SetActiveEditor("3D Modeler")
    oEditor.CreateBox(
        [
            "NAME:BoxParameters",
            "XPosition:="		, "0mm",
            "YPosition:="		, "0mm",
            "ZPosition:="		, "0mm",
            "XSize:="		, x,
            "YSize:="		, y,
            "ZSize:="		, z
        ], 
        [
            "NAME:Attributes",
            "Name:="		, "Box1",
            "Flags:="		, "",
            "Color:="		, "(143 175 143)",
            "Transparency:="	, 0,
            "PartCoordinateSystem:=", "Global",
            "UDMId:="		, "",
            "MaterialValue:="	, "\"vacuum\"",
            "SurfaceMaterialValue:=", "\"\"",
            "SolveInside:="		, True,
            "IsMaterialEditable:="	, True,
            "UseMaterialAppearance:=", False,
            "IsLightweight:="	, False
        ])
    oEditor.FitAll()

