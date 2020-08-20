import bpy, json
from bpy.props import StringProperty, IntProperty, FloatProperty, BoolProperty, PointerProperty
from bpy.types import Operator, PropertyGroup, Panel
from typing import List, Dict, Any

#==================================================#
#RAD GUI
#==================================================#
#GOAL:
#   Provide any Blender3d project the capacity to follow RAD principals
#   where it concerns the graphical user interface and project variables
#   that make use of the project. This service will be provided as a
#   library.
#
#COPYRIGHT:
#   Creative Commons Zero v1.0 Universal
#   https://creativecommons.org/publicdomain/zero/1.0/
#
#DEVELOPED BY:
#[Name] * [Contact]
#   Ilobmirt * ilobmirt@gmail.com
#==================================================#


#==================================================#
#Property Shell Class
#==================================================#
class PropertyGroupShell(PropertyGroup):
    strPropertyDomain = ""
    strPropertyScope = "SCENE"

    @classmethod
    def register(cls):
        if (cls.strPropertyDomain != ""):
            if (cls.strPropertyScope.upper() == "SCENE"):
                setattr(bpy.types.Scene,cls.strPropertyDomain,PointerProperty(type=cls))
            elif (cls.strPropertyScope.upper() == "OBJECT"):
                setattr(bpy.types.Object,cls.strPropertyDomain,PointerProperty(type=cls))

    @classmethod
    def unregister(cls):
        if (cls.strPropertyDomain != ""):
            if (cls.strPropertyScope.upper() == "SCENE"):
                if hasattr(bpy.types.Scene,cls.strPropertyDomain) == True:
                    delattr(bpy.types.Scene,cls.strPropertyDomain)
            elif (cls.strPropertyScope.upper() == "OBJECT"):
                if hasattr(bpy.types.Object,cls.strPropertyDomain) == True:
                    delattr(bpy.types.Object,cls.strPropertyDomain)

#==================================================#
#Operator Shell Class
#==================================================#
class OperatorShell(Operator):
    
    def CompiledExecute(self,context):
        RADGUI_CONSOLE.WriteTags = {"OPERATOR":1}
        RADGUI_CONSOLE.Write("Button "+str(self.__class__)+" Pressed!")

    def execute(self,context):
        self.CompiledExecute(context)
        return {'FINISHED'}

#==================================================#
#Panel Shell Class
#==================================================#
class PanelShell(Panel):
    arrContent: List[Dict[str, Any]] = []

    #Footnote to be replaced with a generated function
    def CompiledDraw(self,context):
        pass

    #Occurs whenever the panel gets drawn
    def draw(self,context):
        #Content array holds priority over a compiled draw function
        if (self.arrContent != []):
            RADGUI_ENGINE.Draw(self,context,self.arrContent)
        else:
            self.CompiledDraw(context)                        

#==================================================#
#RAD GUI Console
#==================================================#

class RADGUI_CONSOLE():
    OutputFilter: Dict[str,int] = {}
    WriteTags: Dict[str,int] = {}

    @classmethod
    def Write(cls,input: str) -> None:

        CanWrite: bool = False
        Index: str = ""

        #Determine if message is to be written in screen
        #No filter or Tags = All Permitted
        if(cls.OutputFilter != {}) and (cls.WriteTags != {}):
            for WriteKey, WriteValue in cls.WriteTags.items():
                if (WriteKey in cls.OutputFilter):
                    if (WriteValue <= cls.OutputFilter[WriteKey]):
                        CanWrite = True
                        break
        else:
            CanWrite = True
        
        if(CanWrite == True):
            print(input)

#==================================================#
#RAD GUI Engine
#==================================================#
class RADGUI_ENGINE():
    @classmethod
    def Draw(cls,source,context,dictInstructions: List[Dict[str, Any]] = []) -> None:

        #Console Filter
        RADGUI_CONSOLE.WriteTags = {"RADGUI_ENGINE":1}

        #Layout Related Variables
        layout = source.layout
        row = None
        column = None
        #Instruction Context
        strLastContext = "LAYOUT"
        strCurrentContext = ""
        objContext = None
        objCurrentAction = None
        strCurrentType = ""

        #We go from the start of the array to the end of the array
        for dictIndex in dictInstructions:

            #Build for the defaults of the instruction type, then fill with defined fields
            dictAttributes = {}

            #Define the context of the object
            #If no context is provided, the last context will be used
            if "CONTEXT" not in dictIndex:
                strCurrentContext = strLastContext.upper()
            #Otherwise, where are we going to render the object?
            else:
                strCurrentContext = str(dictIndex["CONTEXT"]).upper()

            #Wish this was a switch statement
            #Use this IF/ELIF tree to keep track of context
            if strCurrentContext == "LAYOUT":
                objContext = layout
                strLastContext = "LAYOUT"

            elif strCurrentContext == "ROW":
                #If no row has been saved yet, base one off of layout
                if row == None:
                    objContext = layout.row()
                #Okay, the row object does exist
                else:
                    objContext = row
                strLastContext = "ROW"

            elif strCurrentContext == "COLUMN":
                #If no column has been saved yet, base one off of layout
                if column == None:
                    objContext = layout.column()
                #Okay, the row object does exist
                else:
                    objContext = column
                strLastContext = "COLUMN"

            #With the context defined, what the hell are we doing?
            if "TYPE" in dictIndex:
                #What type is it?
                strCurrentType = str(dictIndex["TYPE"]).upper()

                #We make a Row or Column
                if (strCurrentType == "ROW") or (strCurrentType == "COLUMN"):

                    #Define ROW & COLUMN Defaults
                    dictAttributes = {
                        "ALIGN":False,
                        "SAVE":False
                    }

                    if "ALIGN" in dictIndex:
                         dictAttributes["ALIGN"] = dictIndex["ALIGN"]
                    if "SAVE" in dictIndex:
                         dictAttributes["SAVE"] = dictIndex["SAVE"]

                    #Make the Row Object
                    if strCurrentType == "ROW":
                        objCurrentAction = objContext.row(align=dictAttributes["ALIGN"])
                        #Do we save the object in a reference?
                        if dictAttributes["SAVE"] == True:
                            row = objCurrentAction

                    elif strCurrentType == "COLUMN":
                        objCurrentAction = objContext.column(align=dictAttributes["ALIGN"])
                        #Do we save the object in a reference?
                        if dictAttributes["SAVE"] == True:
                            column = objCurrentAction

                #We make an Operator
                elif strCurrentType == "OPERATOR":
                    
                    cls.WriteOperator(objContext,dictIndex)

                #We make a Label
                elif strCurrentType == "LABEL":

                    cls.WriteLabel(objContext,dictIndex)

                #We make a property
                elif strCurrentType == "PROPERTY":
                    
                    cls.WriteProperty(objContext,context,dictIndex)

    @classmethod
    def WriteOperator(cls,context,command: Dict[str, Any] = {}) -> None:
        
        #Console Filter
        RADGUI_CONSOLE.WriteTags = {"RADGUI_ENGINE":2}

        #Define Operator Defaults
        dictAttributes = {
            "CLASS":"",
            "TEXT":"",
            "TEXT_CTXT":"",
            "TRANSLATE":True,
            "ICON":"NONE",
            "EMBOSS":True,
            "DEPRESS":False,
            "ICON_VALUE":0
        }

        #Required Attribute - Class Name
        if "CLASS" not in command:
            RADGUI_CONSOLE.Write("(OPERATOR) Required Attribute Missing: \"CLASS\"")
            return
        elif str(command["CLASS"]).strip() == "":
            RADGUI_CONSOLE.Write("(OPERATOR) Required Attribute - \"CLASS\" is blank")
            return
        else:
            dictAttributes["CLASS"] = str(command["CLASS"]).lower()

        if "TEXT" in command:
            if str(command["TEXT"]).strip() != "":
                dictAttributes["TEXT"] = str(command["TEXT"]).strip()
        if "TEXT_CTXT" in command:
            if str(command["TEXT_CTXT"]).strip() != "":
                dictAttributes["TEXT_CTXT"] = str().strip(command["TEXT_CTXT"])
        if "TRANSLATE" in command:
            dictAttributes["TRANSLATE"] = bool(command["TRANSLATE"])
        if "ICON" in command:
            if str(command["ICON"]).strip() != "":
                dictAttributes["ICON"] = str(command["ICON"]).strip().upper()
        if "EMBOSS" in command:
            dictAttributes["EMBOSS"] = bool(command["EMBOSS"])
        if "DEPRESS" in command:
            dictAttributes["DEPRESS"] = bool(command["DEPRESS"])
        if "ICON_VALUE" in command:
            dictAttributes["ICON_VALUE"] = int(command["ICON_VALUE"])

        objCurrentAction = context.operator(
            dictAttributes["CLASS"],
            text = dictAttributes["TEXT"],
            text_ctxt = dictAttributes["TEXT_CTXT"],
            translate = dictAttributes["TRANSLATE"],
            icon = dictAttributes["ICON"],
            emboss = dictAttributes["EMBOSS"],
            depress = dictAttributes["DEPRESS"],
            icon_value = dictAttributes["ICON_VALUE"]
            )

    @classmethod
    def WriteProperty(cls,ContextObject,ContextEnvironment,command: Dict[str, Any] = {}) -> None:
        
        #Console Filter
        RADGUI_CONSOLE.WriteTags = {"RADGUI_ENGINE":2}

        #Define Property Defaults
        dictAttributes = {
            "VARIABLE":[],
            "DATA":None,
            "TEXT":"",
            "TEXT_CTXT":"",
            "TRANSLATE":True,
            "ICON":"NONE",
            "EXPAND":False,
            "SLIDER":False,
            "TOGGLE":-1,
            "ICON_ONLY":False,
            "EVENT":False,
            "FULL_EVENT":False,
            "EMBOSS":True,
            "INDEX":-1,
            "ICON_VALUE":0,
            "INVERT_CHECKBOX":False
        }

        #Required Attribute - Variable
        if "VARIABLE" not in command:
            RADGUI_CONSOLE.Write("(PROPERTY) Required Attribute Missing: \"VARIABLE\"")
            return
        elif str(command["VARIABLE"]).strip() == "" :
            RADGUI_CONSOLE.Write("(PROPERTY) Required Attribute \"VARIABLE\" is Blank")
            return
        else:
            RADGUI_CONSOLE.Write('(PROPERTY) Variable = \"'+str(command["VARIABLE"])+'\"')
            #Get the scope, domain, and variable
            dictAttributes["VARIABLE"] = str(command["VARIABLE"]).strip().split(".")
            #We need to be sure at least a variable and domain were defined
            if (len(dictAttributes["VARIABLE"]) != 2) and (len(dictAttributes["VARIABLE"]) != 3):
                RADGUI_CONSOLE.Write("(PROPERTY) Required Attribute \"VARIABLE\" needs to be of format \'[SCOPE.]DOMAIN.VARIABLE\'")
                return
            #Default Scope will be "SCENE"
            elif len(dictAttributes["VARIABLE"]) == 2:
                dictAttributes["VARIABLE"].insert(0,"SCENE")
            #Just keep scope upper case
            else:
                dictAttributes["VARIABLE"][0] = str(dictAttributes["VARIABLE"][0]).upper()

            #Given SCOPE.DOMAIN.VARIABLE , verify domain exists in scope
            if (dictAttributes["VARIABLE"][0] == "SCENE"):
                if (hasattr(bpy.types.Scene,dictAttributes["VARIABLE"][1]) == False):
                    RADGUI_CONSOLE.Write("(PROPERTY) The Domain \""+dictAttributes["VARIABLE"][1]+"\" in Required Attribute \"VARIABLE\" is not Present in the scene scope")
                    return
                else:
                    dictAttributes["DATA"] = getattr(ContextEnvironment.scene,dictAttributes["VARIABLE"][1])

            elif (dictAttributes["VARIABLE"][0] == "OBJECT"):
                if (hasattr(bpy.types.Object,dictAttributes["VARIABLE"][1]) == False):
                    RADGUI_CONSOLE.Write("(PROPERTY) The Domain \""+dictAttributes["VARIABLE"][1]+"\" in Required Attribute \"VARIABLE\" is not Present in the object scope")
                    return
                else:
                    dictAttributes["DATA"] = getattr(ContextEnvironment.object,dictAttributes["VARIABLE"][1])

            else:
                RADGUI_CONSOLE.Write("(PROPERTY) Required Attribute \"VARIABLE\" uses an unknown scope \""+dictAttributes["VARIABLE"][0]+"\"")
                return

            #Fill out variables if defined
            if "TEXT" in command:
                if str(command["TEXT"]).strip() != "":
                    dictAttributes["TEXT"] = str(command["TEXT"]).strip()
            if "TEXT_CTXT" in command:
                if str(command["TEXT_CTXT"]).strip() != "":
                    dictAttributes["TEXT_CTXT"] = str().strip(command["TEXT_CTXT"])
            if "TRANSLATE" in command:
                dictAttributes["TRANSLATE"] = bool(command["TRANSLATE"])
            if "ICON" in command:
                if str(command["ICON"]).strip() != "":
                    dictAttributes["ICON"] = str(command["ICON"]).strip().upper()
            if "EXPAND" in command:
                dictAttributes["EXPAND"] = bool(command["EXPAND"])
            if "SLIDER" in command:
                dictAttributes["SLIDER"] = bool(command["SLIDER"])
            if "TOGGLE" in command:
                dictAttributes["TOGGLE"] = int(command["TOGGLE"])
            if "ICON_ONLY" in command:
                dictAttributes["ICON_ONLY"] = bool(command["ICON_ONLY"])
            if "EVENT" in command:
                dictAttributes["EVENT"] = bool(command["EVENT"])
            if "FULL_EVENT" in command:
                dictAttributes["FULL_EVENT"] = bool(command["FULL_EVENT"])
            if "EMBOSS" in command:
                dictAttributes["EMBOSS"] = bool(command["EMBOSS"])
            if "INDEX" in command:
                dictAttributes["INDEX"] = int(command["INDEX"])
            if "ICON_VALUE" in command:
                dictAttributes["ICON_VALUE"] = int(command["ICON_VALUE"])
            if "INVERT_CHECKBOX" in command:
                dictAttributes["INVERT_CHECKBOX"] = bool(command["INVERT_CHECKBOX"])

            ContextObject.prop(
                dictAttributes["DATA"],
                dictAttributes["VARIABLE"][2],
                text = dictAttributes["TEXT"],
                text_ctxt = dictAttributes["TEXT_CTXT"],
                translate = dictAttributes["TRANSLATE"],
                icon = dictAttributes["ICON"],
                expand = dictAttributes["EXPAND"],
                slider = dictAttributes["SLIDER"],
                toggle = dictAttributes["TOGGLE"],
                icon_only = dictAttributes["ICON_ONLY"],
                event = dictAttributes["EVENT"],
                full_event = dictAttributes["FULL_EVENT"],
                emboss = dictAttributes["EMBOSS"],
                index = dictAttributes["INDEX"],
                icon_value = dictAttributes["ICON_VALUE"],
                invert_checkbox = dictAttributes["INVERT_CHECKBOX"]
            )

    @classmethod
    def WriteLabel(cls,context,command: Dict[str, Any] = {}) -> None:

        #Console Filter
        RADGUI_CONSOLE.WriteTags = {"RADGUI_ENGINE":2}

        #Define Label Defaults
        dictAttributes = {
            "TEXT":"",
            "TEXT_CTXT":"",
            "TRANSLATE":True,
            "ICON":"NONE",
            "ICON_VALUE":0
        }

        #Required Attribute - Text
        if "TEXT" not in command:
            RADGUI_CONSOLE.Write("(LABEL) Required Attribute Missing: \"TEXT\"")
            return
        elif str(command["TEXT"]).strip() == "":
            RADGUI_CONSOLE.Write("(LABEL) Required Attribute - \"TEXT\" is blank")
            return
        else:
            dictAttributes["TEXT"] = str(command["TEXT"]).lower()

        if "TEXT_CTXT" in command:
            if str(command["TEXT_CTXT"]).strip() != "":
                dictAttributes["TEXT_CTXT"] = str().strip(command["TEXT_CTXT"])
        if "TRANSLATE" in command:
            dictAttributes["TRANSLATE"] = bool(command["TRANSLATE"])
        if "ICON" in command:
            if str(command["ICON"]).strip() != "":
                dictAttributes["ICON"] = str(command["ICON"]).strip().upper()
        if "ICON_VALUE" in command:
            dictAttributes["ICON_VALUE"] = int(command["ICON_VALUE"])

        context.label(
            text = dictAttributes["TEXT"],
            text_ctxt = dictAttributes["TEXT_CTXT"],
            translate = dictAttributes["TRANSLATE"],
            icon = dictAttributes["ICON"],
            icon_value = dictAttributes["ICON_VALUE"]
            )

#==================================================#
#RAD GUI Factory
#==================================================#

class RADGUI_FACTORY():
    dictJSONContent = {}
    arrDynamicClasses = []
    arrManualClasses = []

    @classmethod
    def BuildProperties(cls,dictInput):

        RADGUI_CONSOLE.WriteTags = {"RADGUI_FACTORY":2}

        clsResult = None
        dictAttributes = {}
        strClassName = "PROPERTIES_" + str(len(cls.arrDynamicClasses)) + "_DYNAMIC"
        strScope = ""
        strCurrentName = ""
        strCurrentType = ""
        dictParams = {}

        RADGUI_CONSOLE.Write("Building Properties-")
        RADGUI_CONSOLE.Write(str(dictInput))

        #To-Do: Build Class Attributes
        #If it doesnt have a type, domain, and content it's not a property group
        if ("TYPE" not in dictInput) or ("DOMAIN" not in dictInput) or ("CONTENT" not in dictInput):
            return clsResult
        #If it does, and then it says it's not a property group, its not a property group
        if (str(dictInput["TYPE"]).upper() != "PROPERTIES"):
            return clsResult
        #Property groups need a domain and no, it cant be empty
        if (str(dictInput["DOMAIN"]).strip() == ""):
            return clsResult
        #Property Group also needs content and no, it can't be empty
        if (len(dictInput["CONTENT"]) == 0):
            return clsResult

        #We got here, so we must be doing something right

        #Properties are defined through annotations rather than declarations
        dictAttributes["__annotations__"] = {}

        #Domain - Where these properties can be found
        dictAttributes["strPropertyDomain"] = dictInput["DOMAIN"]

        #SCOPE - OBJECT / (SCENE)
        if ("SCOPE" in dictInput):
            strScope = str(dictInput["SCOPE"]).upper()
            if(strScope == "OBJECT") or (strScope == "SCENE"):
                dictAttributes["strPropertyScope"] = strScope

        #Loop through each property
        for dictIndex in dictInput["CONTENT"]:

            RADGUI_CONSOLE.Write("Index - value=\""+str(dictIndex)+"\" type=\""+str(type(dictIndex))+"\"")

            #We add only variables with a name and a type
            if("NAME" not in dictIndex) or ("TYPE" not in dictIndex):
                RADGUI_CONSOLE.Write("Left without Name or Type")
                continue
            #And no, it cant be empty
            elif (dictIndex["NAME"].strip() == "") or (dictIndex["TYPE"].strip() == ""):
                RADGUI_CONSOLE.Write("Left because Name or Type is empty")
                continue

            strCurrentName = dictIndex["NAME"]
            strCurrentType = dictIndex["TYPE"].upper()
            dictParams.clear()

            #Set Parameter Defaults
            if (strCurrentType == "STRING"):
                dictParams = {
                    "DEFAULT":"",
                    "LENGTH_MAX":0,
                    "DESCRIPTION":"",
                    "TEXT":""
                }

            elif (strCurrentType == "INTEGER"):
                dictParams = {
                    "DEFAULT":0,
                    "HARD_MIN":-2147483648,
                    "HARD_MAX":2147483647,
                    "SOFT_MIN":-2147483648,
                    "SOFT_MAX":2147483647,
                    "STEP":1,
                    "DESCRIPTION":"",
                    "TEXT":""
                }

            elif (strCurrentType == "FLOAT"):
                dictParams = {
                    "DEFAULT":0.0,
                    "HARD_MIN":-3.402823e38,
                    "HARD_MAX":3.402823e38,
                    "SOFT_MIN":-3.402823e38,
                    "SOFT_MAX":3.402823e38,
                    "STEP":3,
                    "PRECISION":2,
                    "DESCRIPTION":"",
                    "TEXT":""
                }

            elif (strCurrentType == "BOOL") or (strCurrentType == "BOOLEAN"):
                dictParams = {
                    "DEFAULT":False,
                    "DESCRIPTION":"",
                    "TEXT":""
                }
            
            else:
                continue

            #Override DictParams
            for strParamsIndex in dictParams:
                if (strParamsIndex in dictIndex):
                    dictParams[strParamsIndex] = dictIndex[strParamsIndex]

            #Annotate the current property based on the type again
            if (strCurrentType == "STRING"):
                RADGUI_CONSOLE.Write("Adding a String")
                dictAttributes["__annotations__"][strCurrentName] = StringProperty(
                    name= dictParams["TEXT"],
                    description=dictParams["DESCRIPTION"],
                    default=dictParams["DEFAULT"],
                    maxlen=dictParams["LENGTH_MAX"]
                )

            elif (strCurrentType == "INTEGER"):
                RADGUI_CONSOLE.Write("Adding an Integer")
                dictAttributes["__annotations__"][strCurrentName] = IntProperty(
                    name= dictParams["TEXT"],
                    description=dictParams["DESCRIPTION"],
                    default=dictParams["DEFAULT"],
                    min=dictParams["SOFT_MIN"],
                    max=dictParams["HARD_MAX"],
                    soft_min=dictParams["SOFT_MIN"],
                    soft_max=dictParams["SOFT_MAX"],
                    step= dictParams["STEP"]
                )
                
            elif (strCurrentType == "FLOAT"):
                RADGUI_CONSOLE.Write("Adding a Float")
                dictAttributes["__annotations__"][strCurrentName] = FloatProperty(
                    name=dictParams["TEXT"],
                    description=dictParams["DESCRIPTION"],
                    default=dictParams["DEFAULT"],
                    min=dictParams["HARD_MIN"],
                    max=dictParams["HARD_MAX"],
                    soft_min=dictParams["SOFT_MIN"],
                    soft_max=dictParams["SOFT_MAX"],
                    step=dictParams["STEP"],
                    precision=dictParams["PRECISION"]
                )
                
            elif (strCurrentType == "BOOL") or (strCurrentType == "BOOLEAN"):
                RADGUI_CONSOLE.Write("Adding a Boolean")
                dictAttributes["__annotations__"][strCurrentName] = BoolProperty(
                    name=dictParams["TEXT"],
                    description=dictParams["DESCRIPTION"],
                    default= dictParams["DEFAULT"]
                )

            RADGUI_CONSOLE.Write("Registering Properties Group with the following attributes:")
            RADGUI_CONSOLE.Write(str(dictAttributes))

            clsResult = type(strClassName,(PropertyGroupShell,),dictAttributes)

        return clsResult

    @classmethod
    def BuildOperator(cls,dictInput):

        RADGUI_CONSOLE.WriteTags = {"RADGUI_FACTORY":2}

        clsResult = None
        dictAttributes = {}
        strClassName = "OPERATOR_OT_" + str(len(cls.arrDynamicClasses)) + "_DYNAMIC"

        RADGUI_CONSOLE.Write("Building Operator-")
        RADGUI_CONSOLE.Write(str(dictInput))

        #To-Do: Build Class Attributes
        #If it doesnt have a type, text, class, and domain, it's not an operator
        if ("TYPE" not in dictInput) or ("TEXT" not in dictInput) or ("CLASS" not in dictInput) or ("DOMAIN" not in dictInput):
            return clsResult
        #If it does, and then it says it's not an operator, its not an operator
        if (str(dictInput["TYPE"]).upper() != "OPERATOR"):
            return clsResult
        #Text, Domain ,and Class need to have a non-zero length
        if (str(dictInput["TEXT"]).strip() == "") or (str(dictInput["DOMAIN"]).strip() == "") or (str(dictInput["CLASS"]).strip() == ""):
            return clsResult

        #With a domain and class given, describe it to blender
        dictAttributes["bl_idname"] = str(dictInput["DOMAIN"]).lower() + "." + str(dictInput["CLASS"]).lower()
        #Describe Button Label to Blender
        dictAttributes["bl_label"] = dictInput["TEXT"]

        clsResult = type(strClassName,(OperatorShell,),dictAttributes)
        return clsResult

    @classmethod
    def BuildPanel(cls,dictInput):

        RADGUI_CONSOLE.WriteTags = {"RADGUI_FACTORY":2}

        clsResult = None
        dictAttributes = {}
        strClassName = "PANEL_PT_"+ str(len(cls.arrDynamicClasses)) + "_DYNAMIC"

        RADGUI_CONSOLE.Write("Building PANEL-")
        RADGUI_CONSOLE.Write(str(dictInput))

        #To-Do: Build Class Attributes
        #If it doesnt have a Type, Space, Region, and Content, it's not a panel
        if ("TYPE" not in dictInput) or ("SPACE" not in dictInput) or ("REGION" not in dictInput) or ("CONTENT" not in dictInput):
            return clsResult
        #If it does, and then it says it's not a panel, its not a panel
        if (str(dictInput["TYPE"]).upper() != "PANEL"):
            return clsResult
        #Domain and Class need to have a non-zero length
        if (str(dictInput["SPACE"]).strip() == "") or (str(dictInput["REGION"]).strip() == ""):
            return clsResult
        #Property Group also needs content and no, it can't be empty
        if (len(dictInput["CONTENT"]) == 0):
            return clsResult

        #Now that we're here, lets build the panel attributes
        dictAttributes["bl_space_type"] = dictInput["SPACE"]
        dictAttributes["bl_region_type"] = dictInput["REGION"]
        dictAttributes["arrContent"] = dictInput["CONTENT"]

        #Does it have a label? If not, a blank quote will do
        if ("LABEL" in dictInput):
            dictAttributes["bl_label"] = dictInput["LABEL"]
        else:
            dictAttributes["bl_label"] = ""

        clsResult = type(strClassName,(PanelShell,),dictAttributes)
        return clsResult

    @classmethod
    def LoadJSON(cls,strInputJSONFile = ""):

        blnResult = False

        #We have a filename as an input read and build classes
        if(strInputJSONFile != ""):
            #Try loading the file and leave if it fails
            try:            
                #Load the JSON File into memory as a dict array
                with open(strInputJSONFile,"r") as fileInput:
                    cls.dictJSONContent = json.load(fileInput)
            except:
                return blnResult
            
            blnResult = True
        
        return blnResult

    @classmethod
    def Register(cls,arrInputClassList = []) -> bool:

        RADGUI_CONSOLE.WriteTags = {"RADGUI_FACTORY":1}

        blnResult = False
        strCurrentType = ""
        clsBuiltObject = None

        RADGUI_CONSOLE.Write("JSON Dict-")
        RADGUI_CONSOLE.Write(str(cls.dictJSONContent))
        RADGUI_CONSOLE.Write("")
        RADGUI_CONSOLE.Write("Input Classes-")
        RADGUI_CONSOLE.Write(str(arrInputClassList))

        #We need some input, otherwise we leave
        if(cls.dictJSONContent == []) and (arrInputClassList == []):
            return blnResult

        cls.arrManualClasses = arrInputClassList

        if (cls.dictJSONContent != []):
            for strIndex in cls.dictJSONContent:
                
                RADGUI_CONSOLE.Write("Reviewing JSON Index")
                RADGUI_CONSOLE.Write(strIndex)

                #Move onto the next item if it doesnt even have a type
                if "TYPE" not in cls.dictJSONContent[strIndex]:
                    continue

                clsBuiltObject = None
                strCurrentType = str(cls.dictJSONContent[strIndex]["TYPE"]).upper()

                if (strCurrentType == "CONFIG") or (strCurrentType == "CONFIGURATION") or (strCurrentType == "SETTINGS"):
                    RADGUI_CONSOLE.Write("(RADGUI_FACTORY.REGISTER) Setting Configuration")
                    #Console config
                    if("CONSOLE_FILTER" in cls.dictJSONContent[strIndex]):
                        RADGUI_CONSOLE.OutputFilter = cls.dictJSONContent[strIndex]["CONSOLE_FILTER"]

                elif (strCurrentType == "PANEL"):
                    RADGUI_CONSOLE.Write("(RADGUI_FACTORY.REGISTER) Loading into Panel Builder")
                    clsBuiltObject = cls.BuildPanel(cls.dictJSONContent[strIndex])

                elif (strCurrentType == "PROPERTIES"):
                    RADGUI_CONSOLE.Write("(RADGUI_FACTORY.REGISTER) Loading into Properties Builder")
                    clsBuiltObject = cls.BuildProperties(cls.dictJSONContent[strIndex])

                elif (strCurrentType == "OPERATOR"):
                    RADGUI_CONSOLE.Write("(RADGUI_FACTORY.REGISTER) Loading into Operator Builder")
                    clsBuiltObject = cls.BuildOperator(cls.dictJSONContent[strIndex])

                else:
                    RADGUI_CONSOLE.Write("(RADGUI_FACTORY.REGISTER) Failed to understand type - \"" + strCurrentType + "\"")

                if (clsBuiltObject != None):
                    cls.arrDynamicClasses.append(clsBuiltObject)
            
            RADGUI_CONSOLE.Write("Dynamic Classes-")
            RADGUI_CONSOLE.Write(str(cls.arrDynamicClasses))

        #Register the classes that were manually coded
        if (cls.arrManualClasses != []):
            for clsManualIndex in cls.arrManualClasses:
                bpy.utils.register_class(clsManualIndex)
        
        #Register classes that were dynamically created
        if (cls.arrDynamicClasses != []):
            for clsDynamicIndex in cls.arrDynamicClasses:
                bpy.utils.register_class(clsDynamicIndex)
        
        #We got here in one piece, congrats
        blnResult = True
        return blnResult

    @classmethod
    def Unregister(cls):
        
        #UnRegister classes that were dynamically created
        if (cls.arrDynamicClasses != []):
            for clsDynamicIndex in cls.arrDynamicClasses:
                bpy.utils.unregister_class(clsDynamicIndex)

        #UnRegister the classes that were manually coded
        if (cls.arrManualClasses != []):
            for clsManualIndex in cls.arrManualClasses:
                bpy.utils.unregister_class(clsManualIndex)