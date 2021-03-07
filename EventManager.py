from sys import modules as sysModules
from typing import List, Dict, Any
from . import Console

#==================================================#
#RAD GUI Event Manager
#==================================================#
class EventManager():
    RegisteredEvents: Dict[str, Dict[str, Any]] = {}
    IsStrict: bool = False

    @classmethod
    def AddEvent(cls,MethodID: str,InputEvents: List[Dict[str,Any]]) -> None:
        
        Console.WriteTags = {"RADGUI_EVENT_MANAGER":1}
        Console.Write("(RADGUI_EVENT_MANAGER) Adding event for module {}".format(MethodID))
        Console.WriteTags = {"RADGUI_EVENT_MANAGER":2}

        #Method name and at least one event should be provided
        if ((MethodID.strip() == "") or (len(InputEvents) == 0)):
            Console.Write("(RADGUI_EVENT_MANAGER) Empty arguments provided to event registration")
            return

        #Consider it better to work on a local copy of the index, and add/modify the registered events without issue
        SandboxIndex: Dict[str, Dict[str, Any]] = {}

        #Add the method in if it did not exist
        if (MethodID in cls.RegisteredEvents):
            
            #Fill out sandbox
            SandboxIndex = {
                MethodID : cls.RegisteredEvents[MethodID]
            }
            
        else:

            SandboxIndex = {
                MethodID : {
                    "TARGETS":[],
                    "EVENTS":[]
                }
            }

            TargetModuleName:str = ""
            TargetClassName: str = ""
            TargetMethodName: str = ""
            LoadedModules: List[str] = []
            ConsideredModules: List[str] = []
            ModuleIndex: str = ""
            ModuleContents: List[str] = []
            ConsideredClass: Any = None
            ClassContents: List[str] = []
            ConsideredMethod: Any = None
            ConsideredMethods: List[Any] = []

            #We do our best to get the right module, class, & method
            TargetModuleName: str = ".".join(MethodID.split(".")[:-2])
            TargetClassName: str = MethodID.split(".")[-2]
            TargetMethodName: str = MethodID.split(".")[-1]

            #Does the defined module even exist in loaded modules?
            LoadedModules = LoadedModules = sysModules.keys()
            ConsideredModules = list(filter(lambda x: TargetModuleName in x, LoadedModules))

            #We can only continue if we see any modules
            if (len(ConsideredModules) == 0):
                Console.Write("(RADGUI_EVENT_MANAGER) No modules like \"{}\" found in the system".format(TargetModuleName))

            #Strict Mode requires that only the exact module to exist
            elif (cls.IsStrict == True):
                if (TargetModuleName in ConsideredModules):
                    ConsideredModules = [TargetModuleName]

                else:
                    Console.Write("(RADGUI_EVENT_MANAGER) Strict Mode found no modules exactly like \"{}\"".format(TargetModuleName))
                    return

            Console.Write("(RADGUI_EVENT_MANAGER) Found {} Possible Module(s) - {}".format(len(ConsideredModules),ConsideredModules))

            #Find all the classes that match the class name in all modules
            for ModuleIndex in ConsideredModules:
                #List all the classes in the Module
                ModuleContents = dir(sysModules[ModuleIndex])

                #Move onto the next Index if the class cant be found
                if (TargetClassName not in ModuleContents):
                    continue

                #We do have the class in the module? Lets try and check it out
                try:
                    ConsideredClass = getattr(sysModules[ModuleIndex],TargetClassName)
                    ClassContents = dir(ConsideredClass)
                except:
                    Console.Write("(RADGUI_EVENT_MANAGER) Had issue getting contents of Class \"{}\" in Module \"{}\"".format(TargetClassName,ModuleIndex))
                    continue

                #Move onto the next Index if the method cant be found
                if (TargetMethodName not in ClassContents):
                    continue

                #Verify type is a method
                try:
                    ConsideredMethod = getattr(ConsideredClass,TargetMethodName)
                    if ConsideredMethod.__class__.__name__ != 'method':
                        Console.Write("(RADGUI_EVENT_MANAGER) {}.{}.{} is actually not a method but a \"{}\"".format(ModuleIndex,TargetClassName,TargetMethodName,ConsideredMethod.__class__.__name__))
                        continue
                    else:
                        ConsideredMethods.append(ConsideredMethod)
                        Console.Write("(RADGUI_EVENT_MANAGER) {}.{}.{} added to considered methods".format(ModuleIndex,TargetClassName,TargetMethodName))
                except:
                    Console.Write("(RADGUI_EVENT_MANAGER) Had issue getting properties of method \"{}\" in Class \"{}\"".format(TargetMethodName,TargetClassName))
                    continue

            #We're left with all the functions that might be the one described
            #Do we have anything?
            if (len(ConsideredMethods) == 0):
                Console.Write("(RADGUI_EVENT_MANAGER) No Methods found")
                return
            elif ((cls.IsStrict == True) and (len(ConsideredMethods) > 1)):
                Console.Write("(RADGUI_EVENT_MANAGER) Somehow, more than one method was found in {} that matched search criteria.".format(TargetClassName))
                Console.Write("(RADGUI_EVENT_MANAGER) Strict mode only allows for one method to be associated in a reference")
                return

            #Push Methods to the Sandbox
            SandboxIndex[MethodID]["TARGETS"] = ConsideredMethods
            Console.Write("(RADGUI_EVENT_MANAGER) Considered Methods Added to Sandbox")

        #Optimize Event list that would call method
        IsSubset: bool = False
        IsSuperset:bool = False
        IsMatch: bool = False
        ToAdd: bool = False
        InputEventIndex: Dict[str,Any] = {}
        CalculatedEventIndex: Dict[str,Any] = {}

        #If it has no events yet, just optimize the list provided
        if (len(SandboxIndex[MethodID]["EVENTS"]) == 0):
            SandboxIndex[MethodID]["EVENTS"] = InputEvents

        #Loop through each item to add in InputEvents
        for InputEventIndex in InputEvents:

            Console.Write("-- For [{}] in [{}]".format(str(InputEventIndex),str(InputEvents)))
            IsSubset = False
            IsSuperset = False
            IsMatch = False
            ToAdd = False               

            for CalculatedEventIndex in list(SandboxIndex[MethodID]["EVENTS"]):
                
                Console.Write("-->-- For [{}] in [{}]".format(str(CalculatedEventIndex),str(SandboxIndex[MethodID]["EVENTS"])))
                IsSubset = set(InputEventIndex.items()).issubset(set(CalculatedEventIndex.items()))
                IsSuperset = set(InputEventIndex.items()).issuperset(set(CalculatedEventIndex.items()))
                IsMatch = (InputEventIndex == CalculatedEventIndex)

                #Dont Wanna duplicate data
                if (IsMatch == True):
                    Console.Write("-->-- Matches")
                    ToAdd = False
                    break

                #Dont want to add more narrow Event Criteria when looser criteria already exists
                if (IsSuperset==True):
                    Console.Write("-->-- Is Superset")
                    ToAdd = False
                    break

                #Remove more narrow Event Criteria
                if (IsSubset == True):
                    Console.Write("-->-- Is Subset")
                    Console.Write("-- Removing [{}]".format(CalculatedEventIndex))
                    SandboxIndex[MethodID]["EVENTS"].remove(CalculatedEventIndex)

                #If you got here, it might be up for consideration
                ToAdd = True
            
            if (ToAdd == True):
                Console.Write("-- Adding [{}]".format(InputEventIndex))
                SandboxIndex[MethodID]["EVENTS"].append(InputEventIndex)

        #Move the Sandbox back to the Registered Events
        cls.RegisteredEvents[MethodID] = SandboxIndex[MethodID]
        Console.Write("(RADGUI_EVENT_MANAGER) REGISTERED EVENTS = \n {}".format(str(cls.RegisteredEvents)))
        
    @classmethod
    def RemoveEvent(cls,MethodID: str,InputEvents: List[Dict[str,Any]] = []) -> None:
        Console.WriteTags = {"RADGUI_EVENT_MANAGER":1}
        Console.Write("(RADGUI_EVENT_MANAGER) Removing event associations associated with method \"{}\"".format(MethodID))
        Console.WriteTags = {"RADGUI_EVENT_MANAGER":2}

        #Continue if Method is named
        if (MethodID.strip() == ""):
            Console.Write("(RADGUI_EVENT_MANAGER) No method named to remove")
            return

        #Continue if Method exists
        if (MethodID not in cls.RegisteredEvents):
            Console.Write("(RADGUI_EVENT_MANAGER) \"{}\" is already not registered".format(MethodID))
            return

        #Without defining any special events in particular, just remove the whole thing
        if (len(InputEvents) == 0):
            del cls.RegisteredEvents[MethodID]
            return

        #We must remove all events in MethodID that match InputEvents
        InputEventIndex: Dict[str,Any] = {}
        CalculatedEventIndex: Dict[str,Any] = {}

        for InputEventIndex in InputEvents:
            for CalculatedEventIndex in list(cls.RegisteredEvents[MethodID]["EVENTS"]):
                if (InputEventIndex == CalculatedEventIndex):
                    cls.RegisteredEvents[MethodID]["EVENTS"].remove(CalculatedEventIndex)
                    break

    @classmethod
    def HandleEvent(cls,InputEvent: Dict[str, Any]) -> None:
        Console.WriteTags = {"RADGUI_EVENT_MANAGER":1}
        Console.Write("(RADGUI_EVENT_MANAGER) Event Raised \n {}".format(str(InputEvent)))
        Console.WriteTags = {"RADGUI_EVENT_MANAGER":2}

        #Move through each Key which holds a reference to the class and function
        CurrentRegisteredIndex: str = ""
        CurrentEventsIndex: Dict[str, Any] = {}
        MethodIndex: Any = None
        IsSubset:bool = False

        for CurrentRegisteredIndex in list(cls.RegisteredEvents):
            
            IsSubset = False
                        
            for CurrentEventsIndex in list(cls.RegisteredEvents[CurrentRegisteredIndex]["EVENTS"]):
                
                IsSubset = set(CurrentEventsIndex.items()).issubset(set(InputEvent.items()))
                Console.Write("-- REGISTERED EVENT [{}] - IS SUBSET [{}]".format(CurrentRegisteredIndex,IsSubset))

                if (IsSubset == True):
                    
                    for MethodIndex in cls.RegisteredEvents[CurrentRegisteredIndex]["TARGETS"]:
                        try:
                            MethodIndex(InputEvent)
                        except:
                            Console.Write("~~ Failed to Execute Method")
                            continue