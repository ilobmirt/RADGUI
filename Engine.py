from bpy.types import Scene as bpyScene, Object as bpyObject
from typing import List, Dict, Any
from . import Console

#==================================================#
#RAD GUI Engine
#==================================================#
class Engine():
    @classmethod
    def Draw(cls,Source,ContextEnvironment,Instructions: List[Dict[str, Any]] = []) -> None:

        #Console Filter
        Console.WriteTags = {"RADGUI_ENGINE":1}

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
        Console.WriteTags = {"RADGUI_ENGINE":2}

        #Define Operator Defaults
        Attributes: Dict[str, Any] = {
            "CLASS":"",
            "TEXT":"",
            "TEXT_CTXT":"",
            "TRANSLATE":True,
            "ICON":"NONE",
            "EMBOSS":True,
            "DEPRESS":False,
            "ICON_VALUE":0,
            "EVENT_ID":""
        }

        #Required Attribute - Class Name
        if "CLASS" not in Command:
            Console.Write("(OPERATOR) Required Attribute Missing: \"CLASS\"")
            return
        elif str(Command["CLASS"]).strip() == "":
            Console.Write("(OPERATOR) Required Attribute - \"CLASS\" is blank")
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
        if "EVENT_ID" in Command:
            if str(Command["EVENT_ID"]).strip() != "":
                Attributes["EVENT_ID"] = str(Command["EVENT_ID"]).strip()

        CurrentAction = Context.operator(
            Attributes["CLASS"],
            text = Attributes["TEXT"],
            text_ctxt = Attributes["TEXT_CTXT"],
            translate = Attributes["TRANSLATE"],
            icon = Attributes["ICON"],
            emboss = Attributes["EMBOSS"],
            depress = Attributes["DEPRESS"],
            icon_value = Attributes["ICON_VALUE"]
            )

        if (Attributes["EVENT_ID"] != ""):
            CurrentAction.EventID = Attributes["EVENT_ID"]

    @classmethod
    def WriteProperty(cls,ContextObject,ContextEnvironment,Command: Dict[str, Any] = {}) -> None:
        
        #Console Filter
        Console.WriteTags = {"RADGUI_ENGINE":2}

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
            Console.Write("(PROPERTY) Required Attribute Missing: \"VARIABLE\"")
            return
        elif str(Command["VARIABLE"]).strip() == "" :
            Console.Write("(PROPERTY) Required Attribute \"VARIABLE\" is Blank")
            return
        else:
            Console.Write('(PROPERTY) Variable = \"'+str(Command["VARIABLE"])+'\"')
            #Get the scope, domain, and variable
            Attributes["VARIABLE"] = str(Command["VARIABLE"]).strip().split(".")
            #We need to be sure at least a variable and domain were defined
            if (len(Attributes["VARIABLE"]) != 2) and (len(Attributes["VARIABLE"]) != 3):
                Console.Write("(PROPERTY) Required Attribute \"VARIABLE\" needs to be of format \'[SCOPE.]DOMAIN.VARIABLE\'")
                return
            #Default Scope will be "SCENE"
            elif len(Attributes["VARIABLE"]) == 2:
                Attributes["VARIABLE"].insert(0,"SCENE")
            #Just keep scope upper case
            else:
                Attributes["VARIABLE"][0] = str(Attributes["VARIABLE"][0]).upper()

            #Given SCOPE.DOMAIN.VARIABLE , verify domain exists in scope
            if (Attributes["VARIABLE"][0] == "SCENE"):
                if (hasattr(bpyScene,Attributes["VARIABLE"][1]) == False):
                    Console.Write("(PROPERTY) The Domain \""+Attributes["VARIABLE"][1]+"\" in Required Attribute \"VARIABLE\" is not Present in the scene scope")
                    return
                else:
                    Attributes["DATA"] = getattr(ContextEnvironment.scene,Attributes["VARIABLE"][1])

            elif (Attributes["VARIABLE"][0] == "OBJECT"):
                if (hasattr(bpyObject,Attributes["VARIABLE"][1]) == False):
                    Console.Write("(PROPERTY) The Domain \""+Attributes["VARIABLE"][1]+"\" in Required Attribute \"VARIABLE\" is not Present in the object scope")
                    return
                else:
                    Attributes["DATA"] = getattr(ContextEnvironment.object,Attributes["VARIABLE"][1])

            else:
                Console.Write("(PROPERTY) Required Attribute \"VARIABLE\" uses an unknown scope \""+Attributes["VARIABLE"][0]+"\"")
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
        Console.WriteTags = {"RADGUI_ENGINE":2}

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
            Console.Write("(LABEL) Required Attribute Missing: \"TEXT\"")
            return
        elif str(Command["TEXT"]).strip() == "":
            Console.Write("(LABEL) Required Attribute - \"TEXT\" is blank")
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