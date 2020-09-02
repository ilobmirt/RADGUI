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
class RADGUI_PROPERTYGROUP_SHELL(PropertyGroup):
    Domain: str = ""
    Scope: str = "SCENE"

    @classmethod
    def register(cls) -> None:
        if (cls.Domain != ""):
            if (cls.Scope.upper() == "SCENE"):
                setattr(bpy.types.Scene,cls.Domain,PointerProperty(type=cls))
            elif (cls.Scope.upper() == "OBJECT"):
                setattr(bpy.types.Object,cls.Domain,PointerProperty(type=cls))

    @classmethod
    def unregister(cls) -> None:
        if (cls.Domain != ""):
            if (cls.Scope.upper() == "SCENE"):
                if hasattr(bpy.types.Scene,cls.Domain) == True:
                    delattr(bpy.types.Scene,cls.Domain)
            elif (cls.Scope.upper() == "OBJECT"):
                if hasattr(bpy.types.Object,cls.Domain) == True:
                    delattr(bpy.types.Object,cls.Domain)

#==================================================#
#Operator Shell Class
#==================================================#
class RADGUI_OPERATOR_SHELL(Operator):
    
    def CompiledExecute(self,Context) -> None:
        RADGUI_CONSOLE.WriteTags = {"OPERATOR":1}
        RADGUI_CONSOLE.Write("Button "+str(self.__class__)+" Pressed!")

    def execute(self,Context) -> Any:
        self.CompiledExecute(Context)
        return {'FINISHED'}

#==================================================#
#Panel Shell Class
#==================================================#
class RADGUI_PANEL_SHELL(Panel):
    Content: List[Dict[str, Any]] = []

    #Footnote to be replaced with a generated function
    def CompiledDraw(self,Context) -> None:
        pass

    #Occurs whenever the panel gets drawn
    def draw(self,Context) -> None:
        #Content array holds priority over a compiled draw function
        if (self.Content != []):
            RADGUI_ENGINE.Draw(self,Context,self.Content)
        else:
            self.CompiledDraw(Context)                        

#==================================================#
#RAD GUI Console
#==================================================#
class RADGUI_CONSOLE():
    OutputFilter: Dict[str,int] = {}
    WriteTags: Dict[str,int] = {}

    @classmethod
    def Write(cls,Input: str) -> None:

        CanWrite: bool = False
        WriteKey: str = ""
        WriteValue: int = 0

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
            print(Input)

#==================================================#
#RAD GUI Engine
#==================================================#
class RADGUI_ENGINE():
    @classmethod
    def Draw(cls,Source,ContextEnvironment,Instructions: List[Dict[str, Any]] = []) -> None:

        #Console Filter
        RADGUI_CONSOLE.WriteTags = {"RADGUI_ENGINE":1}

        #Layout Related Variables
        Layout: Any = Source.layout
        Row: Any = None
        Column: Any = None
        #Instruction Context
        LastContext: str = "LAYOUT"
        CurrentContext: str = ""
        ContextObject: Any = None
        CurrentAction: Any = None
        CurrentType: str = ""
        CurrentInstruction: Dict[str, Any] = {}

        #We go from the start of the array to the end of the array
        for CurrentInstruction in Instructions:

            #Build for the defaults of the instruction type, then fill with defined fields
            Attributes: Dict[str, Any] = {}

            #Define the context of the object
            #If no context is provided, the last context will be used
            if "CONTEXT" not in CurrentInstruction:
                CurrentContext = LastContext.upper()
            #Otherwise, where are we going to render the object?
            else:
                CurrentContext = str(CurrentInstruction["CONTEXT"]).upper()

            #Wish this was a switch statement
            #Use this IF/ELIF tree to keep track of context
            if CurrentContext == "LAYOUT":
                ContextObject = Layout
                LastContext = "LAYOUT"

            elif CurrentContext == "ROW":
                #If no row has been saved yet, base one off of layout
                if Row == None:
                    ContextObject = Layout.row()
                #Okay, the row object does exist
                else:
                    ContextObject = Row
                LastContext = "ROW"

            elif CurrentContext == "COLUMN":
                #If no column has been saved yet, base one off of layout
                if Column == None:
                    ContextObject = Layout.column()
                #Okay, the row object does exist
                else:
                    ContextObject = Column
                LastContext = "COLUMN"

            #With the context defined, what the hell are we doing?
            if "TYPE" in CurrentInstruction:
                #What type is it?
                CurrentType = str(CurrentInstruction["TYPE"]).upper()

                #We make a Row or Column
                if (CurrentType == "ROW") or (CurrentType == "COLUMN"):

                    #Define ROW & COLUMN Defaults
                    Attributes = {
                        "ALIGN":False,
                        "SAVE":False
                    }

                    if "ALIGN" in CurrentInstruction:
                         Attributes["ALIGN"] = CurrentInstruction["ALIGN"]
                    if "SAVE" in CurrentInstruction:
                         Attributes["SAVE"] = CurrentInstruction["SAVE"]

                    #Make the Row Object
                    if CurrentType == "ROW":
                        CurrentAction = ContextObject.row(align=Attributes["ALIGN"])
                        #Do we save the object in a reference?
                        if Attributes["SAVE"] == True:
                            Row = CurrentAction

                    elif CurrentType == "COLUMN":
                        CurrentAction = ContextObject.column(align=Attributes["ALIGN"])
                        #Do we save the object in a reference?
                        if Attributes["SAVE"] == True:
                            Column = CurrentAction

                #We make an Operator
                elif CurrentType == "OPERATOR":
                    
                    cls.WriteOperator(ContextObject,CurrentInstruction)

                #We make a Label
                elif CurrentType == "LABEL":

                    cls.WriteLabel(ContextObject,CurrentInstruction)

                #We make a property
                elif CurrentType == "PROPERTY":
                    
                    cls.WriteProperty(ContextObject,ContextEnvironment,CurrentInstruction)

    @classmethod
    def WriteOperator(cls,Context,Command: Dict[str, Any] = {}) -> None:
        
        #Console Filter
        RADGUI_CONSOLE.WriteTags = {"RADGUI_ENGINE":2}

        #Define Operator Defaults
        Attributes: Dict[str, Any] = {
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
        if "CLASS" not in Command:
            RADGUI_CONSOLE.Write("(OPERATOR) Required Attribute Missing: \"CLASS\"")
            return
        elif str(Command["CLASS"]).strip() == "":
            RADGUI_CONSOLE.Write("(OPERATOR) Required Attribute - \"CLASS\" is blank")
            return
        else:
            Attributes["CLASS"] = str(Command["CLASS"]).lower()

        if "TEXT" in Command:
            if str(Command["TEXT"]).strip() != "":
                Attributes["TEXT"] = str(Command["TEXT"]).strip()
        if "TEXT_CTXT" in Command:
            if str(Command["TEXT_CTXT"]).strip() != "":
                Attributes["TEXT_CTXT"] = str().strip(Command["TEXT_CTXT"])
        if "TRANSLATE" in Command:
            Attributes["TRANSLATE"] = bool(Command["TRANSLATE"])
        if "ICON" in Command:
            if str(Command["ICON"]).strip() != "":
                Attributes["ICON"] = str(Command["ICON"]).strip().upper()
        if "EMBOSS" in Command:
            Attributes["EMBOSS"] = bool(Command["EMBOSS"])
        if "DEPRESS" in Command:
            Attributes["DEPRESS"] = bool(Command["DEPRESS"])
        if "ICON_VALUE" in Command:
            Attributes["ICON_VALUE"] = int(Command["ICON_VALUE"])

        CurrentAction: Any = Context.operator(
            Attributes["CLASS"],
            text = Attributes["TEXT"],
            text_ctxt = Attributes["TEXT_CTXT"],
            translate = Attributes["TRANSLATE"],
            icon = Attributes["ICON"],
            emboss = Attributes["EMBOSS"],
            depress = Attributes["DEPRESS"],
            icon_value = Attributes["ICON_VALUE"]
            )

    @classmethod
    def WriteProperty(cls,ContextObject,ContextEnvironment,Command: Dict[str, Any] = {}) -> None:
        
        #Console Filter
        RADGUI_CONSOLE.WriteTags = {"RADGUI_ENGINE":2}

        #Define Property Defaults
        Attributes: Dict[str, Any] = {
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
        if "VARIABLE" not in Command:
            RADGUI_CONSOLE.Write("(PROPERTY) Required Attribute Missing: \"VARIABLE\"")
            return
        elif str(Command["VARIABLE"]).strip() == "" :
            RADGUI_CONSOLE.Write("(PROPERTY) Required Attribute \"VARIABLE\" is Blank")
            return
        else:
            RADGUI_CONSOLE.Write('(PROPERTY) Variable = \"'+str(Command["VARIABLE"])+'\"')
            #Get the scope, domain, and variable
            Attributes["VARIABLE"] = str(Command["VARIABLE"]).strip().split(".")
            #We need to be sure at least a variable and domain were defined
            if (len(Attributes["VARIABLE"]) != 2) and (len(Attributes["VARIABLE"]) != 3):
                RADGUI_CONSOLE.Write("(PROPERTY) Required Attribute \"VARIABLE\" needs to be of format \'[SCOPE.]DOMAIN.VARIABLE\'")
                return
            #Default Scope will be "SCENE"
            elif len(Attributes["VARIABLE"]) == 2:
                Attributes["VARIABLE"].insert(0,"SCENE")
            #Just keep scope upper case
            else:
                Attributes["VARIABLE"][0] = str(Attributes["VARIABLE"][0]).upper()

            #Given SCOPE.DOMAIN.VARIABLE , verify domain exists in scope
            if (Attributes["VARIABLE"][0] == "SCENE"):
                if (hasattr(bpy.types.Scene,Attributes["VARIABLE"][1]) == False):
                    RADGUI_CONSOLE.Write("(PROPERTY) The Domain \""+Attributes["VARIABLE"][1]+"\" in Required Attribute \"VARIABLE\" is not Present in the scene scope")
                    return
                else:
                    Attributes["DATA"] = getattr(ContextEnvironment.scene,Attributes["VARIABLE"][1])

            elif (Attributes["VARIABLE"][0] == "OBJECT"):
                if (hasattr(bpy.types.Object,Attributes["VARIABLE"][1]) == False):
                    RADGUI_CONSOLE.Write("(PROPERTY) The Domain \""+Attributes["VARIABLE"][1]+"\" in Required Attribute \"VARIABLE\" is not Present in the object scope")
                    return
                else:
                    Attributes["DATA"] = getattr(ContextEnvironment.object,Attributes["VARIABLE"][1])

            else:
                RADGUI_CONSOLE.Write("(PROPERTY) Required Attribute \"VARIABLE\" uses an unknown scope \""+Attributes["VARIABLE"][0]+"\"")
                return

            #Fill out variables if defined
            if "TEXT" in Command:
                if str(Command["TEXT"]).strip() != "":
                    Attributes["TEXT"] = str(Command["TEXT"]).strip()
            if "TEXT_CTXT" in Command:
                if str(Command["TEXT_CTXT"]).strip() != "":
                    Attributes["TEXT_CTXT"] = str().strip(Command["TEXT_CTXT"])
            if "TRANSLATE" in Command:
                Attributes["TRANSLATE"] = bool(Command["TRANSLATE"])
            if "ICON" in Command:
                if str(Command["ICON"]).strip() != "":
                    Attributes["ICON"] = str(Command["ICON"]).strip().upper()
            if "EXPAND" in Command:
                Attributes["EXPAND"] = bool(Command["EXPAND"])
            if "SLIDER" in Command:
                Attributes["SLIDER"] = bool(Command["SLIDER"])
            if "TOGGLE" in Command:
                Attributes["TOGGLE"] = int(Command["TOGGLE"])
            if "ICON_ONLY" in Command:
                Attributes["ICON_ONLY"] = bool(Command["ICON_ONLY"])
            if "EVENT" in Command:
                Attributes["EVENT"] = bool(Command["EVENT"])
            if "FULL_EVENT" in Command:
                Attributes["FULL_EVENT"] = bool(Command["FULL_EVENT"])
            if "EMBOSS" in Command:
                Attributes["EMBOSS"] = bool(Command["EMBOSS"])
            if "INDEX" in Command:
                Attributes["INDEX"] = int(Command["INDEX"])
            if "ICON_VALUE" in Command:
                Attributes["ICON_VALUE"] = int(Command["ICON_VALUE"])
            if "INVERT_CHECKBOX" in Command:
                Attributes["INVERT_CHECKBOX"] = bool(Command["INVERT_CHECKBOX"])

            ContextObject.prop(
                Attributes["DATA"],
                Attributes["VARIABLE"][2],
                text = Attributes["TEXT"],
                text_ctxt = Attributes["TEXT_CTXT"],
                translate = Attributes["TRANSLATE"],
                icon = Attributes["ICON"],
                expand = Attributes["EXPAND"],
                slider = Attributes["SLIDER"],
                toggle = Attributes["TOGGLE"],
                icon_only = Attributes["ICON_ONLY"],
                event = Attributes["EVENT"],
                full_event = Attributes["FULL_EVENT"],
                emboss = Attributes["EMBOSS"],
                index = Attributes["INDEX"],
                icon_value = Attributes["ICON_VALUE"],
                invert_checkbox = Attributes["INVERT_CHECKBOX"]
            )

    @classmethod
    def WriteLabel(cls,Context,Command: Dict[str, Any] = {}) -> None:

        #Console Filter
        RADGUI_CONSOLE.WriteTags = {"RADGUI_ENGINE":2}

        #Define Label Defaults
        Attributes: Dict[str,Any] = {
            "TEXT":"",
            "TEXT_CTXT":"",
            "TRANSLATE":True,
            "ICON":"NONE",
            "ICON_VALUE":0
        }

        #Required Attribute - Text
        if "TEXT" not in Command:
            RADGUI_CONSOLE.Write("(LABEL) Required Attribute Missing: \"TEXT\"")
            return
        elif str(Command["TEXT"]).strip() == "":
            RADGUI_CONSOLE.Write("(LABEL) Required Attribute - \"TEXT\" is blank")
            return
        else:
            Attributes["TEXT"] = str(Command["TEXT"]).lower()

        if "TEXT_CTXT" in Command:
            if str(Command["TEXT_CTXT"]).strip() != "":
                Attributes["TEXT_CTXT"] = str().strip(Command["TEXT_CTXT"])
        if "TRANSLATE" in Command:
            Attributes["TRANSLATE"] = bool(Command["TRANSLATE"])
        if "ICON" in Command:
            if str(Command["ICON"]).strip() != "":
                Attributes["ICON"] = str(Command["ICON"]).strip().upper()
        if "ICON_VALUE" in Command:
            Attributes["ICON_VALUE"] = int(Command["ICON_VALUE"])

        Context.label(
            text = Attributes["TEXT"],
            text_ctxt = Attributes["TEXT_CTXT"],
            translate = Attributes["TRANSLATE"],
            icon = Attributes["ICON"],
            icon_value = Attributes["ICON_VALUE"]
            )

#==================================================#
#RAD GUI Factory
#==================================================#

class RADGUI_FACTORY():
    JSONContent: Dict[str,Any] = {}
    DynamicClasses: List[Any] = []
    ManualClasses: List[Any] = []

    @classmethod
    def BuildProperties(cls,Input: Dict[str,Any]) -> Any:

        RADGUI_CONSOLE.WriteTags = {"RADGUI_FACTORY":2}

        Result: Any = None
        Attributes: Dict[str, Any] = {}
        ClassName: str = "PROPERTIES_" + str(len(cls.DynamicClasses)) + "_DYNAMIC"
        Scope: str = ""
        CurrentName: str = ""
        CurrentType: str = ""
        Params: Dict[str,Any] = {}
        ContentIndex: Dict[str, Any] = {}
        ParamsIndex: str = ""

        RADGUI_CONSOLE.Write("Building Properties-")
        RADGUI_CONSOLE.Write(str(Input))

        #To-Do: Build Class Attributes
        #If it doesnt have a type, domain, and content it's not a property group
        if ("TYPE" not in Input) or ("DOMAIN" not in Input) or ("CONTENT" not in Input):
            return Result
        #If it does, and then it says it's not a property group, its not a property group
        if (str(Input["TYPE"]).upper() != "PROPERTIES"):
            return Result
        #Property groups need a domain and no, it cant be empty
        if (str(Input["DOMAIN"]).strip() == ""):
            return Result
        #Property Group also needs content and no, it can't be empty
        if (len(Input["CONTENT"]) == 0):
            return Result

        #We got here, so we must be doing something right

        #Properties are defined through annotations rather than declarations
        Attributes["__annotations__"] = {}

        #Domain - Where these properties can be found
        Attributes["Domain"] = Input["DOMAIN"]

        #SCOPE - OBJECT / (SCENE)
        if ("SCOPE" in Input):
            Scope = str(Input["SCOPE"]).upper()
            if(Scope == "OBJECT") or (Scope == "SCENE"):
                Attributes["Scope"] = Scope

        #Loop through each property
        for ContentIndex in Input["CONTENT"]:

            RADGUI_CONSOLE.Write("Index - value=\""+str(ContentIndex)+"\" type=\""+str(type(ContentIndex))+"\"")

            #We add only variables with a name and a type
            if("NAME" not in ContentIndex) or ("TYPE" not in ContentIndex):
                RADGUI_CONSOLE.Write("Left without Name or Type")
                continue
            #And no, it cant be empty
            elif (ContentIndex["NAME"].strip() == "") or (ContentIndex["TYPE"].strip() == ""):
                RADGUI_CONSOLE.Write("Left because Name or Type is empty")
                continue

            CurrentName = ContentIndex["NAME"]
            CurrentType = ContentIndex["TYPE"].upper()
            Params.clear()

            #Set Parameter Defaults
            if (CurrentType == "STRING"):
                Params = {
                    "DEFAULT":"",
                    "LENGTH_MAX":0,
                    "DESCRIPTION":"",
                    "TEXT":""
                }

            elif (CurrentType == "INTEGER"):
                Params = {
                    "DEFAULT":0,
                    "HARD_MIN":-2147483648,
                    "HARD_MAX":2147483647,
                    "SOFT_MIN":-2147483648,
                    "SOFT_MAX":2147483647,
                    "STEP":1,
                    "DESCRIPTION":"",
                    "TEXT":""
                }

            elif (CurrentType == "FLOAT"):
                Params = {
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

            elif (CurrentType == "BOOL") or (CurrentType == "BOOLEAN"):
                Params = {
                    "DEFAULT":False,
                    "DESCRIPTION":"",
                    "TEXT":""
                }
            
            else:
                continue

            #Override Params Dictionary
            for ParamsIndex in Params:
                if (ParamsIndex in ContentIndex):
                    Params[ParamsIndex] = ContentIndex[ParamsIndex]

            #Annotate the current property based on the type again
            if (CurrentType == "STRING"):
                RADGUI_CONSOLE.Write("Adding a String")
                Attributes["__annotations__"][CurrentName] = StringProperty(
                    name= Params["TEXT"],
                    description=Params["DESCRIPTION"],
                    default=Params["DEFAULT"],
                    maxlen=Params["LENGTH_MAX"]
                )

            elif (CurrentType == "INTEGER"):
                RADGUI_CONSOLE.Write("Adding an Integer")
                Attributes["__annotations__"][CurrentName] = IntProperty(
                    name= Params["TEXT"],
                    description=Params["DESCRIPTION"],
                    default=Params["DEFAULT"],
                    min=Params["SOFT_MIN"],
                    max=Params["HARD_MAX"],
                    soft_min=Params["SOFT_MIN"],
                    soft_max=Params["SOFT_MAX"],
                    step= Params["STEP"]
                )
                
            elif (CurrentType == "FLOAT"):
                RADGUI_CONSOLE.Write("Adding a Float")
                Attributes["__annotations__"][CurrentName] = FloatProperty(
                    name=Params["TEXT"],
                    description=Params["DESCRIPTION"],
                    default=Params["DEFAULT"],
                    min=Params["HARD_MIN"],
                    max=Params["HARD_MAX"],
                    soft_min=Params["SOFT_MIN"],
                    soft_max=Params["SOFT_MAX"],
                    step=Params["STEP"],
                    precision=Params["PRECISION"]
                )
                
            elif (CurrentType == "BOOL") or (CurrentType == "BOOLEAN"):
                RADGUI_CONSOLE.Write("Adding a Boolean")
                Attributes["__annotations__"][CurrentName] = BoolProperty(
                    name=Params["TEXT"],
                    description=Params["DESCRIPTION"],
                    default= Params["DEFAULT"]
                )

            RADGUI_CONSOLE.Write("Registering Properties Group with the following attributes:")
            RADGUI_CONSOLE.Write(str(Attributes))

            Result = type(ClassName,(RADGUI_PROPERTYGROUP_SHELL,),Attributes)

        return Result

    @classmethod
    def BuildOperator(cls,Input: Dict[str,Any]) -> Any:

        RADGUI_CONSOLE.WriteTags = {"RADGUI_FACTORY":2}

        Result: Any = None
        Attributes: Dict[str,Any] = {}
        ClassName: str = "OPERATOR_OT_" + str(len(cls.DynamicClasses)) + "_DYNAMIC"

        RADGUI_CONSOLE.Write("Building Operator-")
        RADGUI_CONSOLE.Write(str(Input))

        #To-Do: Build Class Attributes
        #If it doesnt have a type, text, class, and domain, it's not an operator
        if ("TYPE" not in Input) or ("TEXT" not in Input) or ("CLASS" not in Input) or ("DOMAIN" not in Input):
            return Result
        #If it does, and then it says it's not an operator, its not an operator
        if (str(Input["TYPE"]).upper() != "OPERATOR"):
            return Result
        #Text, Domain ,and Class need to have a non-zero length
        if (str(Input["TEXT"]).strip() == "") or (str(Input["DOMAIN"]).strip() == "") or (str(Input["CLASS"]).strip() == ""):
            return Result

        #With a domain and class given, describe it to blender
        Attributes["bl_idname"] = str(Input["DOMAIN"]).lower() + "." + str(Input["CLASS"]).lower()
        #Describe Button Label to Blender
        Attributes["bl_label"] = Input["TEXT"]

        Result = type(ClassName,(RADGUI_OPERATOR_SHELL,),Attributes)
        return Result

    @classmethod
    def BuildPanel(cls,Input: Dict[str,Any]) -> Any:

        RADGUI_CONSOLE.WriteTags = {"RADGUI_FACTORY":2}

        Result: Any = None
        Attributes: Dict[str,Any] = {}
        ClassName: str = "PANEL_PT_"+ str(len(cls.DynamicClasses)) + "_DYNAMIC"

        RADGUI_CONSOLE.Write("Building PANEL-")
        RADGUI_CONSOLE.Write(str(Input))

        #To-Do: Build Class Attributes
        #If it doesnt have a Type, Space, Region, and Content, it's not a panel
        if ("TYPE" not in Input) or ("SPACE" not in Input) or ("REGION" not in Input) or ("CONTENT" not in Input):
            return Result
        #If it does, and then it says it's not a panel, its not a panel
        if (str(Input["TYPE"]).upper() != "PANEL"):
            return Result
        #Domain and Class need to have a non-zero length
        if (str(Input["SPACE"]).strip() == "") or (str(Input["REGION"]).strip() == ""):
            return Result
        #Property Group also needs content and no, it can't be empty
        if (Input["CONTENT"] == {}):
            return Result

        #Now that we're here, lets build the panel attributes
        Attributes["bl_space_type"] = Input["SPACE"]
        Attributes["bl_region_type"] = Input["REGION"]
        Attributes["Content"] = Input["CONTENT"]

        #Does it have a label? If not, a blank quote will do
        if ("LABEL" in Input):
            Attributes["bl_label"] = Input["LABEL"]
        else:
            Attributes["bl_label"] = ""

        Result = type(ClassName,(RADGUI_PANEL_SHELL,),Attributes)
        return Result

    @classmethod
    def LoadJSON(cls,Input: str = "") -> bool:

        Result: bool = False

        #We have a filename as an input read and build classes
        if(Input.strip() != ""):
            #Try loading the file and leave if it fails
            try:            
                #Load the JSON File into memory as a dict array
                with open(Input,"r") as fileInput:
                    cls.JSONContent = json.load(fileInput)

                Result = True

            except:
                pass
            
        return Result

    @classmethod
    def Register(cls,InputClasses: List[Any] = []) -> bool:

        RADGUI_CONSOLE.WriteTags = {"RADGUI_FACTORY":1}

        Result: bool = False
        CurrentType: str = ""
        BuiltObject: Any = None
        ContentIndex: str = ""
        ManualIndex: Any = None
        DynamicIndex: Any = None

        RADGUI_CONSOLE.Write("JSON Dict-")
        RADGUI_CONSOLE.Write(str(cls.JSONContent))
        RADGUI_CONSOLE.Write("")
        RADGUI_CONSOLE.Write("Input Classes-")
        RADGUI_CONSOLE.Write(str(InputClasses))

        #We need some input, otherwise we leave
        if(cls.JSONContent == []) and (InputClasses == []):
            return Result

        cls.ManualClasses = InputClasses

        if (cls.JSONContent != []):
            for ContentIndex in cls.JSONContent:
                
                RADGUI_CONSOLE.Write("Reviewing JSON Index")
                RADGUI_CONSOLE.Write(ContentIndex)

                #Move onto the next item if it doesnt even have a type
                if "TYPE" not in cls.JSONContent[ContentIndex]:
                    continue

                BuiltObject = None
                CurrentType = str(cls.JSONContent[ContentIndex]["TYPE"]).upper()

                if (CurrentType == "CONFIG") or (CurrentType == "CONFIGURATION") or (CurrentType == "SETTINGS"):
                    RADGUI_CONSOLE.Write("(RADGUI_FACTORY.REGISTER) Setting Configuration")
                    #Console config
                    if("CONSOLE_FILTER" in cls.JSONContent[ContentIndex]):
                        RADGUI_CONSOLE.OutputFilter = cls.JSONContent[ContentIndex]["CONSOLE_FILTER"]

                elif (CurrentType == "PANEL"):
                    RADGUI_CONSOLE.Write("(RADGUI_FACTORY.REGISTER) Loading into Panel Builder")
                    BuiltObject = cls.BuildPanel(cls.JSONContent[ContentIndex])

                elif (CurrentType == "PROPERTIES"):
                    RADGUI_CONSOLE.Write("(RADGUI_FACTORY.REGISTER) Loading into Properties Builder")
                    BuiltObject = cls.BuildProperties(cls.JSONContent[ContentIndex])

                elif (CurrentType == "OPERATOR"):
                    RADGUI_CONSOLE.Write("(RADGUI_FACTORY.REGISTER) Loading into Operator Builder")
                    BuiltObject = cls.BuildOperator(cls.JSONContent[ContentIndex])

                else:
                    RADGUI_CONSOLE.Write("(RADGUI_FACTORY.REGISTER) Failed to understand type - \"" + CurrentType + "\"")

                if (BuiltObject != None):
                    cls.DynamicClasses.append(BuiltObject)
            
            RADGUI_CONSOLE.Write("Dynamic Classes-")
            RADGUI_CONSOLE.Write(str(cls.DynamicClasses))

        #Register the classes that were manually coded
        if (cls.ManualClasses != []):
            for ManualIndex in cls.ManualClasses:
                bpy.utils.register_class(ManualIndex)
        
        #Register classes that were dynamically created
        if (cls.DynamicClasses != []):
            for DynamicIndex in cls.DynamicClasses:
                bpy.utils.register_class(DynamicIndex)
        
        #We got here in one piece, congrats
        Result = True
        return Result

    @classmethod
    def Unregister(cls) -> bool:
        
        RADGUI_CONSOLE.WriteTags = {"RADGUI_FACTORY":1}
        Result: bool = False
        ManualIndex: Any = None
        DynamicIndex: Any = None

        try:
            #UnRegister classes that were dynamically created
            if (cls.DynamicClasses != []):
                for DynamicIndex in cls.DynamicClasses:
                    bpy.utils.unregister_class(DynamicIndex)

            #UnRegister the classes that were manually coded
            if (cls.ManualClasses != []):
                for ManualIndex in cls.ManualClasses:
                    bpy.utils.unregister_class(ManualIndex)

            Result = True

        except expression as identifier:
            RADGUI_CONSOLE.Write("(RADGUI_FACTORY.UNREGISTER) Failed to unregister classes")

        return Result