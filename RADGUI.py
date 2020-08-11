import bpy, json
from bpy.props import StringProperty, IntProperty, FloatProperty, BoolProperty, PointerProperty
from bpy.types import Operator, PropertyGroup, Panel

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
#
#REVISION:
#   v1.0 * 2020 AUGUST 01
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
        print("Button "+str(self.__class__)+" Pressed!")

    def execute(self,context):
        self.CompiledExecute(context)
        return {'FINISHED'}

#==================================================#
#Panel Shell Class
#==================================================#
class PanelShell(Panel):
    arrContent = []

    #Footnote to be replaced with a generated function
    def CompiledDraw(self,context):
        pass

    #Occurs whenever the panel gets drawn
    def draw(self,context):
        #Content array holds priority over a compiled draw function
        if (self.arrContent != []):
            RAD_GUI_FACTORY.DrawJSONInterpreter(self,context,self.arrContent)
        else:
            self.CompiledDraw(context)                        

#==================================================#
#RAD GUI Factory
#==================================================#

class RAD_GUI_FACTORY():
    dictJSONContent = {}
    arrDynamicClasses = []
    arrManualClasses = []

    def DrawJSONInterpreter(source,context,dictInstructions = {}):
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
                    if "CLASS" not in dictIndex:
                        print("(OPERATOR) Required Attribute Missing: \"CLASS\"")
                        continue
                    elif str(dictIndex["CLASS"]).strip() == "":
                        print("(OPERATOR) Required Attribute - \"CLASS\" is blank")
                        continue
                    else:
                        dictAttributes["CLASS"] = str(dictIndex["CLASS"]).lower()

                    if "TEXT" in dictIndex:
                        if str(dictIndex["TEXT"]).strip() != "":
                            dictAttributes["TEXT"] = str(dictIndex["TEXT"]).strip()
                    if "TEXT_CTXT" in dictIndex:
                        if str(dictIndex["TEXT_CTXT"]).strip() != "":
                            dictAttributes["TEXT_CTXT"] = str().strip(dictIndex["TEXT_CTXT"])
                    if "TRANSLATE" in dictIndex:
                        dictAttributes["TRANSLATE"] = bool(dictIndex["TRANSLATE"])
                    if "ICON" in dictIndex:
                        if str(dictIndex["ICON"]).strip() != "":
                            dictAttributes["ICON"] = str(dictIndex["ICON"]).strip().upper()
                    if "EMBOSS" in dictIndex:
                        dictAttributes["EMBOSS"] = bool(dictIndex["EMBOSS"])
                    if "DEPRESS" in dictIndex:
                        dictAttributes["DEPRESS"] = bool(dictIndex["DEPRESS"])
                    if "ICON_VALUE" in dictIndex:
                        dictAttributes["ICON_VALUE"] = int(dictIndex["ICON_VALUE"])

                    objCurrentAction = objContext.operator(
                        dictAttributes["CLASS"],
                        text = dictAttributes["TEXT"],
                        text_ctxt = dictAttributes["TEXT_CTXT"],
                        translate = dictAttributes["TRANSLATE"],
                        icon = dictAttributes["ICON"],
                        emboss = dictAttributes["EMBOSS"],
                        depress = dictAttributes["DEPRESS"],
                        icon_value = dictAttributes["ICON_VALUE"]
                        )

                #We make a Label
                elif strCurrentType == "LABEL":

                    #Define Label Defaults
                    dictAttributes = {
                        "TEXT":"",
                        "TEXT_CTXT":"",
                        "TRANSLATE":True,
                        "ICON":"NONE",
                        "ICON_VALUE":0
                    }

                    #Required Attribute - Text
                    if "TEXT" not in dictIndex:
                        print("(LABEL) Required Attribute Missing: \"TEXT\"")
                        continue
                    elif str(dictIndex["TEXT"]).strip() == "":
                        print("(LABEL) Required Attribute - \"TEXT\" is blank")
                        continue
                    else:
                        dictAttributes["TEXT"] = str(dictIndex["TEXT"]).lower()

                    if "TEXT_CTXT" in dictIndex:
                        if str(dictIndex["TEXT_CTXT"]).strip() != "":
                            dictAttributes["TEXT_CTXT"] = str().strip(dictIndex["TEXT_CTXT"])
                    if "TRANSLATE" in dictIndex:
                        dictAttributes["TRANSLATE"] = bool(dictIndex["TRANSLATE"])
                    if "ICON" in dictIndex:
                        if str(dictIndex["ICON"]).strip() != "":
                            dictAttributes["ICON"] = str(dictIndex["ICON"]).strip().upper()
                    if "ICON_VALUE" in dictIndex:
                        dictAttributes["ICON_VALUE"] = int(dictIndex["ICON_VALUE"])

                    objContext.label(
                        text = dictAttributes["TEXT"],
                        text_ctxt = dictAttributes["TEXT_CTXT"],
                        translate = dictAttributes["TRANSLATE"],
                        icon = dictAttributes["ICON"],
                        icon_value = dictAttributes["ICON_VALUE"]
                        )

                #We make a property
                elif strCurrentType == "PROPERTY":
                    print ('TYPE: Property')

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
                    if "VARIABLE" not in dictIndex:
                        print("(PROPERTY) Required Attribute Missing: \"VARIABLE\"")
                        continue
                    elif str(dictIndex["VARIABLE"]).strip() == "" :
                        print("(PROPERTY) Required Attribute \"VARIABLE\" is Blank")
                        continue
                    else:
                        print ('(PROPERTY) Variable = \"'+str(dictIndex["VARIABLE"])+'\"')
                        #Get the scope, domain, and variable
                        dictAttributes["VARIABLE"] = str(dictIndex["VARIABLE"]).strip().split(".")
                        #We need to be sure at least a variable and domain were defined
                        if (len(dictAttributes["VARIABLE"]) != 2) and (len(dictAttributes["VARIABLE"]) != 3):
                            print("(PROPERTY) Required Attribute \"VARIABLE\" needs to be of format \'[SCOPE.]DOMAIN.VARIABLE\'")
                            continue
                        #Default Scope will be "SCENE"
                        elif len(dictAttributes["VARIABLE"]) == 2:
                            dictAttributes["VARIABLE"].insert(0,"SCENE")
                        #Just keep scope upper case
                        else:
                            dictAttributes["VARIABLE"][0] = str(dictAttributes["VARIABLE"][0]).upper()

                        #Given SCOPE.DOMAIN.VARIABLE , verify domain exists in scope
                        if (dictAttributes["VARIABLE"][0] == "SCENE"):
                            if (hasattr(bpy.types.Scene,dictAttributes["VARIABLE"][1]) == False):
                                print("(PROPERTY) The Domain \""+dictAttributes["VARIABLE"][1]+"\" in Required Attribute \"VARIABLE\" is not Present in the scene scope")
                                continue
                            else:
                                dictAttributes["DATA"] = getattr(context.scene,dictAttributes["VARIABLE"][1])

                        elif (dictAttributes["VARIABLE"][0] == "OBJECT"):
                            if (hasattr(bpy.types.Object,dictAttributes["VARIABLE"][1]) == False):
                                print("(PROPERTY) The Domain \""+dictAttributes["VARIABLE"][1]+"\" in Required Attribute \"VARIABLE\" is not Present in the object scope")
                                continue
                            else:
                                dictAttributes["DATA"] = getattr(context.object,dictAttributes["VARIABLE"][1])

                        else:
                            print("(PROPERTY) Required Attribute \"VARIABLE\" uses an unknown scope \""+dictAttributes["VARIABLE"][0]+"\"")
                            continue

                        #Fill out variables if defined
                        if "TEXT" in dictIndex:
                            if str(dictIndex["TEXT"]).strip() != "":
                                dictAttributes["TEXT"] = str(dictIndex["TEXT"]).strip()
                        if "TEXT_CTXT" in dictIndex:
                            if str(dictIndex["TEXT_CTXT"]).strip() != "":
                                dictAttributes["TEXT_CTXT"] = str().strip(dictIndex["TEXT_CTXT"])
                        if "TRANSLATE" in dictIndex:
                            dictAttributes["TRANSLATE"] = bool(dictIndex["TRANSLATE"])
                        if "ICON" in dictIndex:
                            if str(dictIndex["ICON"]).strip() != "":
                                dictAttributes["ICON"] = str(dictIndex["ICON"]).strip().upper()
                        if "EXPAND" in dictIndex:
                            dictAttributes["EXPAND"] = bool(dictIndex["EXPAND"])
                        if "SLIDER" in dictIndex:
                            dictAttributes["SLIDER"] = bool(dictIndex["SLIDER"])
                        if "TOGGLE" in dictIndex:
                            dictAttributes["TOGGLE"] = int(dictIndex["TOGGLE"])
                        if "ICON_ONLY" in dictIndex:
                            dictAttributes["ICON_ONLY"] = bool(dictIndex["ICON_ONLY"])
                        if "EVENT" in dictIndex:
                            dictAttributes["EVENT"] = bool(dictIndex["EVENT"])
                        if "FULL_EVENT" in dictIndex:
                            dictAttributes["FULL_EVENT"] = bool(dictIndex["FULL_EVENT"])
                        if "EMBOSS" in dictIndex:
                            dictAttributes["EMBOSS"] = bool(dictIndex["EMBOSS"])
                        if "INDEX" in dictIndex:
                            dictAttributes["INDEX"] = int(dictIndex["INDEX"])
                        if "ICON_VALUE" in dictIndex:
                            dictAttributes["ICON_VALUE"] = int(dictIndex["ICON_VALUE"])
                        if "INVERT_CHECKBOX" in dictIndex:
                            dictAttributes["INVERT_CHECKBOX"] = bool(dictIndex["INVERT_CHECKBOX"])

                        objContext.prop(
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
    def BuildProperties(cls,dictInput):
        clsResult = None
        dictAttributes = {}
        strClassName = "PROPERTIES_" + str(len(cls.arrDynamicClasses)) + "_DYNAMIC"
        strScope = ""
        strCurrentName = ""
        strCurrentType = ""
        dictParams = {}

        print("Building Properties-")
        print(str(dictInput))

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

            print("Index - value=\""+str(dictIndex)+"\" type=\""+str(type(dictIndex))+"\"")

            #We add only variables with a name and a type
            if("NAME" not in dictIndex) or ("TYPE" not in dictIndex):
                print("Left without Name or Type")
                continue
            #And no, it cant be empty
            elif (dictIndex["NAME"].strip() == "") or (dictIndex["TYPE"].strip() == ""):
                print("Left because Name or Type is empty")
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
                print("Adding a String")
                dictAttributes["__annotations__"][strCurrentName] = StringProperty(
                    name= dictParams["TEXT"],
                    description=dictParams["DESCRIPTION"],
                    default=dictParams["DEFAULT"],
                    maxlen=dictParams["LENGTH_MAX"]
                )

            elif (strCurrentType == "INTEGER"):
                print("Adding an Integer")
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
                print("Adding a Float")
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
                print("Adding a Boolean")
                dictAttributes["__annotations__"][strCurrentName] = BoolProperty(
                    name=dictParams["TEXT"],
                    description=dictParams["DESCRIPTION"],
                    default= dictParams["DEFAULT"]
                )

            print("Registering Properties Group with the following attributes:")
            print(str(dictAttributes))

            clsResult = type(strClassName,(PropertyGroupShell,),dictAttributes)

        return clsResult

    @classmethod
    def BuildOperator(cls,dictInput):
        clsResult = None
        dictAttributes = {}
        strClassName = "OPERATOR_OT_" + str(len(cls.arrDynamicClasses)) + "_DYNAMIC"

        print("Building Operator-")
        print(str(dictInput))

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
        clsResult = None
        dictAttributes = {}
        strClassName = "PANEL_PT_"+ str(len(cls.arrDynamicClasses)) + "_DYNAMIC"

        print("Building PANEL-")
        print(str(dictInput))

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

            #TO-DO:
            #Sanitize JSON Strings
            
            blnResult = True
        
        return blnResult

    @classmethod
    def register(cls,arrInputClassList = []):
        blnResult = False
        strCurrentType = ""
        clsBuiltObject = None

        print("JSON Dict-")
        print(str(cls.dictJSONContent))
        print("")
        print("Input Classes-")
        print(str(arrInputClassList))

        #We need some input, otherwise we leave
        if(cls.dictJSONContent == []) and (arrInputClassList == []):
            return blnResult

        cls.arrManualClasses = arrInputClassList

        #Generate classes defined in the JSON
        if (cls.dictJSONContent != []):
            for strIndex in cls.dictJSONContent:
                
                print("Reviewing JSON Index")
                print(strIndex)

                #Move onto the next item if it doesnt even have a type
                if "TYPE" not in cls.dictJSONContent[strIndex]:
                    continue

                clsBuiltObject = None

                #We do simple type checking to generate classes
                strCurrentType = str(cls.dictJSONContent[strIndex]["TYPE"]).upper()
                if (strCurrentType == "PANEL"):
                    print("Loading into Panel Builder")
                    clsBuiltObject = cls.BuildPanel(cls.dictJSONContent[strIndex])

                elif (strCurrentType == "PROPERTIES"):
                    print("Loading into Properties Builder")
                    clsBuiltObject = cls.BuildProperties(cls.dictJSONContent[strIndex])

                elif (strCurrentType == "OPERATOR"):
                    print("Loading into Operator Builder")
                    clsBuiltObject = cls.BuildOperator(cls.dictJSONContent[strIndex])

                if (clsBuiltObject != None):
                    cls.arrDynamicClasses.append(clsBuiltObject)
                else:
                    print("Failed to build object")
            
            print("Dynamic Classes-")
            print(str(cls.arrDynamicClasses))

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
    def unregister(cls):
        
        #UnRegister classes that were dynamically created
        if (cls.arrDynamicClasses != []):
            for clsDynamicIndex in cls.arrDynamicClasses:
                bpy.utils.unregister_class(clsDynamicIndex)

        #UnRegister the classes that were manually coded
        if (cls.arrManualClasses != []):
            for clsManualIndex in cls.arrManualClasses:
                bpy.utils.unregister_class(clsManualIndex)