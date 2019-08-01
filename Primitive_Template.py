##############################################################
#                           Imports
##############################################################
import sys 

class parameters():
    def __init__(self):
        self.primitiveParamDefs=[]
    
    def addReal(self, name, value, comment=''):
        x=UDPPrimitiveParameterDefinition2( name, 
                                            comment, 
                                            UnitType.LengthUnit, 
                                            ParamPropType.Value, 
                                            ParamPropFlag.MustBeReal,
                                            UDPParam(ParamDataType.Double, value))
        self.primitiveParamDefs.append(x)
        
    def addInt(self, name, value, comment=''):
        x=UDPPrimitiveParameterDefinition2( name, 
                                            comment, 
                                            UnitType.NoUnit, 
                                            ParamPropType.Number, 
                                            ParamPropFlag.MustBeInt,
                                            UDPParam(ParamDataType.Int, value))
        self.primitiveParamDefs.append(x)  

    def output(self):
        return self.primitiveParamDefs, int(len(self.primitiveParamDefs))

##############################################################
#                           Constants
##############################################################       

para=parameters()
para.addReal("Xpos", '0.0')
para.addReal("Ypos", '0.0')
para.addReal("Dist", '5.0')
para.addInt("Turns", '2')
para.addReal("Width", '2.0')
para.addReal("Thickness", '1.0')    
primitiveParamDefs, numParams=para.output()
  
primitiveInfo = UDPPrimitiveTypeInfo(
	name = "Box",
	purpose = "Create a Box in XY plane",
	company = "Ansys",
	date = "12-5-2012",
    version = "2.0")

lengthUnits = "mm"

registeredFaceNames = []
registeredEdgeNames = []
registeredVertexNames = []


##############################################################
#                       Class Implementation
##############################################################
class UDPExtension(IUDPExtension):

  def __init__(self):
    m_StartPt = UDPPosition(0,0,0)
    m_EndPt = UDPPosition(0,0,0)

#----------------------------------------------
# Interface implementations
#-----------------------------------------------

  def CreatePrimitive2(self, funcLib, paramValues):
    x0=paramValues[0].Data
    y0=paramValues[1].Data    
    box=funcLib.CreateBox(UDPPosition(x0,y0,0),[1,2,3])
    return box

  def GetPrimitiveTypeInfo(self):
    return primitiveInfo

  def GetLengthParameterUnits(self):
    return lengthUnits

  def GetPrimitiveParametersDefinition2(self):
    return primitiveParamDefs
    
  def GetRegisteredFaceNames(self):
    return registeredFaceNames

  def GetRegisteredEdgeNames(self):
    return registeredEdgeNames

  def GetRegisteredVertexNames(self):
    return registeredVertexNames
  
  def AreParameterValuesValid2(self, error, udpParams):
    return True

