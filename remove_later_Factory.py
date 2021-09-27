import bpy, json
from bpy.props import StringProperty, IntProperty, FloatProperty, BoolProperty
from typing import List, Dict, Any
from . import Console, EventManager, PropertyGroupShell, OperatorShell, PanelShell

#==================================================#
#RAD GUI Factory
#==================================================#

class Factory():
    JSONContent: Dict[str,Any] = {}
    DynamicClasses: List[Any] = []
    ManualClasses: List[Any] = []

    @classmethod
    def BuildProperties(cls,Input: Dict[str,Any]) -> Any:

        Console.WriteTags = {"RADGUI_FACTORY":2}

        Result: Any = None
        Attributes: Dict[str, Any] = {}
        ClassName: str = "PROPERTIES_" + str(len(cls.DynamicClasses)) + "_DYNAMIC"
        Scope: str = ""
        CurrentName: str = ""
        CurrentType: str = ""
        Params: Dict[str,Any] = {}
        ContentIndex: Dict[str, Any] = {}
        ParamsIndex: str = ""

        Console.Write("Building Properties-")
        Console.Write(str(Input))

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

            Console.Write("Index - value=\""+str(ContentIndex)+"\" type=\""+str(type(ContentIndex))+"\"")

            #We add only variables with a name and a type
            if("NAME" not in ContentIndex) or ("TYPE" not in ContentIndex):
                Console.Write("Left without Name or Type")
                continue
            #And no, it cant be empty
            elif (ContentIndex["NAME"].strip() == "") or (ContentIndex["TYPE"].strip() == ""):
                Console.Write("Left because Name or Type is empty")
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
                Console.Write("Adding a String")
                Attributes["__annotations__"][CurrentName] = StringProperty(
                    name= Params["TEXT"],
                    description=Params["DESCRIPTION"],
                    default=Params["DEFAULT"],
                    maxlen=Params["LENGTH_MAX"],
                    update=eval("lambda Part1,Part2: PropertyGroupShell.PropertyUpdate(Part1,Part2,'"+CurrentName+"')")
                )

            elif (CurrentType == "INTEGER"):
                Console.Write("Adding an Integer")
                Attributes["__annotations__"][CurrentName] = IntProperty(
                    name= Params["TEXT"],
                    description=Params["DESCRIPTION"],
                    default=Params["DEFAULT"],
                    min=Params["SOFT_MIN"],
                    max=Params["HARD_MAX"],
                    soft_min=Params["SOFT_MIN"],
                    soft_max=Params["SOFT_MAX"],
                    step= Params["STEP"],
                    update=eval("lambda Part1,Part2: PropertyGroupShell.PropertyUpdate(Part1,Part2,'"+CurrentName+"')")
                )
                
            elif (CurrentType == "FLOAT"):
                Console.Write("Adding a Float")
                Attributes["__annotations__"][CurrentName] = FloatProperty(
                    name=Params["TEXT"],
                    description=Params["DESCRIPTION"],
                    default=Params["DEFAULT"],
                    min=Params["HARD_MIN"],
                    max=Params["HARD_MAX"],
                    soft_min=Params["SOFT_MIN"],
                    soft_max=Params["SOFT_MAX"],
                    step=Params["STEP"],
                    precision=Params["PRECISION"],
                    update=eval("lambda Part1,Part2: PropertyGroupShell.PropertyUpdate(Part1,Part2,'"+CurrentName+"')")
                )
                
            elif (CurrentType == "BOOL") or (CurrentType == "BOOLEAN"):
                Console.Write("Adding a Boolean")
                Attributes["__annotations__"][CurrentName] = BoolProperty(
                    name=Params["TEXT"],
                    description=Params["DESCRIPTION"],
                    default= Params["DEFAULT"],
                    update=eval("lambda Part1,Part2: PropertyGroupShell.PropertyUpdate(Part1,Part2,'"+CurrentName+"')")
                )

            Console.Write("Registering Properties Group with the following attributes:")
            Console.Write(str(Attributes))

            Result = type(ClassName,(PropertyGroupShell,),Attributes)

        return Result

    @classmethod
    def BuildOperator(cls,Input: Dict[str,Any]) -> Any:

        Console.WriteTags = {"RADGUI_FACTORY":2}

        Result: Any = None
        Attributes: Dict[str,Any] = {}
        ClassName: str = "OPERATOR_OT_" + str(len(cls.DynamicClasses)) + "_DYNAMIC"

        Console.Write("Building Operator-")
        Console.Write(str(Input))

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

        #Set Annotation for Event System
        Attributes["__annotations__"] = {}
        Attributes["__annotations__"]["EventID"] = StringProperty(name= "Event_ID")

        Result = type(ClassName,(OperatorShell,),Attributes)
        return Result

    @classmethod
    def BuildPanel(cls,Input: Dict[str,Any]) -> Any:

        Console.WriteTags = {"RADGUI_FACTORY":2}

        Result: Any = None
        Attributes: Dict[str,Any] = {}
        ClassName: str = "PANEL_PT_"+ str(len(cls.DynamicClasses)) + "_DYNAMIC"

        Console.Write("Building PANEL-")
        Console.Write(str(Input))

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

        Result = type(ClassName,(PanelShell,),Attributes)
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

        Console.WriteTags = {"RADGUI_FACTORY":1}

        Result: bool = False
        CurrentType: str = ""
        BuiltObject: Any = None
        ContentIndex: str = ""
        ManualIndex: Any = None
        DynamicIndex: Any = None

        Console.Write("JSON Dict-")
        Console.Write(str(cls.JSONContent))
        Console.Write("")
        Console.Write("Input Classes-")
        Console.Write(str(InputClasses))

        #We need some input, otherwise we leave
        if(cls.JSONContent == []) and (InputClasses == []):
            return Result

        cls.ManualClasses = InputClasses

        if (cls.JSONContent != []):
            for ContentIndex in cls.JSONContent:
                
                Console.Write("Reviewing JSON Index")
                Console.Write(ContentIndex)

                #Move onto the next item if it doesnt even have a type
                if "TYPE" not in cls.JSONContent[ContentIndex]:
                    continue

                BuiltObject = None
                CurrentType = str(cls.JSONContent[ContentIndex]["TYPE"]).upper()

                if (CurrentType == "CONFIG") or (CurrentType == "CONFIGURATION") or (CurrentType == "SETTINGS"):
                    Console.Write("(RADGUI_FACTORY.REGISTER) Setting Configuration")
                    #Console config
                    if("CONSOLE_FILTER" in cls.JSONContent[ContentIndex]):
                        Console.Write("- Console Filter")
                        Console.OutputFilter = cls.JSONContent[ContentIndex]["CONSOLE_FILTER"]
                    #Event Registration
                    if ("EVENTS" in cls.JSONContent[ContentIndex]):
                        Console.Write("- Event Registration")
                        
                        #Set Strict Mode
                        if "STRICT" in cls.JSONContent[ContentIndex]["EVENTS"]:
                            EventManager.IsStrict = bool(cls.JSONContent[ContentIndex]["EVENTS"]["STRICT"])
                        
                        #Register Events
                        if "ASSOCIATIONS" in cls.JSONContent[ContentIndex]["EVENTS"]:

                            MethodIndex: str = ""

                            for MethodIndex in cls.JSONContent[ContentIndex]["EVENTS"]["ASSOCIATIONS"]:
                                EventManager.AddEvent(MethodIndex,cls.JSONContent[ContentIndex]["EVENTS"]["ASSOCIATIONS"][MethodIndex])

                        #EventManager.RegisteredEvents = cls.JSONContent[ContentIndex]["EVENTS"]

                elif (CurrentType == "PANEL"):
                    Console.Write("(RADGUI_FACTORY.REGISTER) Loading into Panel Builder")
                    BuiltObject = cls.BuildPanel(cls.JSONContent[ContentIndex])

                elif (CurrentType == "PROPERTIES"):
                    Console.Write("(RADGUI_FACTORY.REGISTER) Loading into Properties Builder")
                    BuiltObject = cls.BuildProperties(cls.JSONContent[ContentIndex])

                elif (CurrentType == "OPERATOR"):
                    Console.Write("(RADGUI_FACTORY.REGISTER) Loading into Operator Builder")
                    BuiltObject = cls.BuildOperator(cls.JSONContent[ContentIndex])

                else:
                    Console.Write("(RADGUI_FACTORY.REGISTER) Failed to understand type - \"" + CurrentType + "\"")

                if (BuiltObject != None):
                    cls.DynamicClasses.append(BuiltObject)
            
            Console.Write("Dynamic Classes-")
            Console.Write(str(cls.DynamicClasses))

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
        
        Console.WriteTags = {"RADGUI_FACTORY":1}
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

        except:
            Console.Write("(RADGUI_FACTORY.UNREGISTER) Failed to unregister classes")

        return Result