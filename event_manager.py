"""================================================================================================
This module is designed to connect events that occur within blender and pass on event data to
programmer defined functions. Usually, ones that they write themselves.

CLASSES:
    EventManager
================================================================================================"""
import uuid
from sys import modules as sysModules
from typing import List, Dict, Any
from radgui_console import Console

#==================================================#
#RAD GUI Event Manager
#==================================================#
class EventManager():
    """
    This class is to...
    * Store references to handler methods that get called by events
    * Define the kind of events that will call the handler methods

    ATTRIBUTES:
    -----------

        __registered_events: Dict[uuid.UUID,Dict[str,List[Dict[str,Any]]]]
            Collection of event associations.
            [Project ID] --> [Handler Method Name] --> [Event List]
            uuid.UUID    --> str                   --> List[Dict[str,Any]]

        __registered_handlers: Dict[str, List[Any]]
            Collection of methods to call
            Handler Method Name --> Method List

        __is_strict: Dict[str,bool]
            Collection of strictness definitions by project id

    METHODS:
    --------

        property_update: None
        add_event: bool
        remove_event: bool
        handle_event: None
        add_handler: bool
        remove_handler: bool
    """
    __registered_events: Dict[uuid.UUID,Dict[str,List[Dict[str,Any]]]] = {}
    __registered_handlers: Dict[str, List[Any]] = {}
    __is_strict: Dict[str,bool] = {}

    @staticmethod
    def property_update(event_class: Any, context: Any, project_id: uuid.UUID, property_name: str) -> None:
        """
        Static method to be called by blender's property objects.
        Passes event information of the property value change to the event handler

        PARAMETERS:
        -----------

            event_class: Any
                class object that holds the property

            context: Any
                Context in which this event fired

            project_id: uuid.UUID
                Unique Project Id this event relates to

            property_name: str
                Name of the property that fired the event

        RETURNS:
        --------

            None
        """

        generated_event : Dict[str, Any] = {
                "EVENT_ID":property_name,
                "EVENT_CLASS":event_class,
                "CONTEXT":context,
                "OBJECT_TYPE":"VARIABLE",
                "EVENT_TYPE":"VARIABLE_CHANGED",
                "VALUE":getattr(event_class,property_name)
            }

        EventManager.handle_event(project_id,generated_event)

    @classmethod
    def add_event(cls, input_project_id: uuid.UUID, input_method_id: str, input_events: List[ Dict[ str,Any ] ]) -> bool:
        """
        Adds a list of events (each event per Dictionary) that would call a handler method.
        Returns True if the event list was successfully updated with the new List. False if
        we were unable to update the events List with new data.

        PARAMETERS:
        -----------

            cls:
                Represents the class itself.

            input_project_id: uuid.UUID
                Unique id of the project working with the event system

            input_method_id: str
                String representing the handler method to call when the input events happen
                in the format "MODULE.CLASS.METHOD"

            input_events: List[ Dict[ str,Any ] ]
                List containing all the events that would call the input method.


        RETURNS:
        --------

            result: bool
                Represents if the event has been updated or not.
        """
        result:bool = False
        input_method_id = input_method_id.strip()

        Console.set_write_tags(input_project_id,{"RADGUI_EVENT_MANAGER":1})
        Console.write(input_project_id,f"(RADGUI_EVENT_MANAGER) Adding event for module \"{input_method_id}\"")
        Console.set_write_tags(input_project_id,{"RADGUI_EVENT_MANAGER":2})

        #Method name and at least one event should be provided
        if (input_method_id == "") or (len(input_events) == 0):
            Console.write(input_project_id,"(RADGUI_EVENT_MANAGER) Empty arguments provided to event registration")
            return result

        #Consider it better to work on a local copy of the index, and add/modify the registered events without issue
        sandbox_event: List[Dict[str,Any]] = []

        #Add the method in if it did not exist
        if input_method_id in cls.__registered_events[input_project_id]:

            #Fill out sandbox
            sandbox_event = cls.__registered_events[input_project_id][input_method_id]

        #At this point, we try and make sure that the handler exists or try adding it
        does_have_handler: bool = False
        if input_method_id not in cls.__registered_handlers:
            does_have_handler = cls.add_handler(input_project_id,input_method_id)
        else:
            does_have_handler = True

        #Do we have a handle on our events?
        if does_have_handler is False:
            Console.write(input_project_id,"(RADGUI_EVENT_MANAGER) Unable to get a handler function for such an event")
            return result

        #Optimize Event list that would call method
        is_subset: bool = False
        is_superset:bool = False
        is_match: bool = False
        to_add: bool = False
        index_event: Dict[str,Any] = {}
        index_calculated_event: Dict[str,Any] = {}

        #If it has no events yet, just optimize the list provided
        if len(sandbox_event) == 0:
            sandbox_event = input_events

        #Loop through each item to add in InputEvents
        for index_event in input_events:

            Console.write(input_project_id,f"-- For [{str(index_event)}] in [{str(input_events)}]")
            is_subset = False
            is_superset = False
            is_match = False
            to_add = False

            for index_calculated_event in list(sandbox_event):

                Console.write(input_project_id,f"-->-- For [{str(index_calculated_event)}] in [{str(sandbox_event)}]")
                is_subset = set(index_event.items()).issubset(set(index_calculated_event.items()))
                is_superset = set(index_event.items()).issuperset(set(index_calculated_event.items()))
                is_match = (index_event == index_calculated_event)

                #Dont Wanna duplicate data
                if is_match is True:
                    Console.write(input_project_id,"-->-- Matches")
                    to_add = False
                    break

                #Dont want to add more narrow Event Criteria when looser criteria already exists
                if is_superset is True:
                    Console.write(input_project_id,"-->-- Is Superset")
                    to_add = False
                    break

                #Remove more narrow Event Criteria
                if is_subset is True:
                    Console.write(input_project_id,"-->-- Is Subset")
                    Console.write(input_project_id,f"-- Removing [{str(index_calculated_event)}]")
                    sandbox_event[input_method_id].remove(index_calculated_event)

                #If you got here, it might be up for consideration
                to_add = True

            if to_add is True:
                Console.write(input_project_id,f"-- Adding [{str(index_event)}]")
                sandbox_event[input_method_id].append(index_event)

        #Move the Sandbox back to the Registered Events
        cls.__registered_events[input_project_id][input_method_id] = sandbox_event
        Console.write(input_project_id,f"(RADGUI_EVENT_MANAGER) REGISTERED EVENTS = \n {str(cls.__registered_events)}")
        result = True

        return result

    @classmethod
    def remove_event(cls, input_project_id: uuid.UUID, input_method_id: str, input_events: List[ Dict[ str,Any ] ]) -> bool:
        """
        Removes a list of events that are currently tied to a handler method.
        A blank input event list would remove all events from a project and its ties to a handler method.
        Returns true if the events were removed successfully. False if there was a failure to remove the events.

        PARAMETERS:
        -----------

            cls:
                Represents the class itself.

            input_project_id: uuid.UUID
                Unique id representing the project working with the event system

            input_method_id: str
                String representing the handler method to remove the events list from
                in the format "MODULE.CLASS.METHOD"

            input_events: List[ Dict[ str,Any ] ]
                List of events to remove from the handler method within the given project id.
                A blank list will remove all events from the handler method within the given
                project id.

        RETURNS:
        --------

            result: bool
                Boolean representing the success of the removal
        """
        result:bool = False
        is_content_removed:bool = False
        input_method_id = input_method_id.strip()

        Console.set_write_tags(input_project_id,{"RADGUI_EVENT_MANAGER":1})
        Console.write(input_project_id,f"(RADGUI_EVENT_MANAGER) Removing event associations associated with method \"{input_method_id}\"")
        Console.set_write_tags(input_project_id,{"RADGUI_EVENT_MANAGER":2})

        #Continue if Method is named
        if input_method_id == "":
            Console.write(input_project_id,"(RADGUI_EVENT_MANAGER) No method named to remove")
            return result

        #Continue if Method exists
        if input_method_id not in cls.__registered_events[input_project_id]:
            Console.write(input_project_id,f"(RADGUI_EVENT_MANAGER) method\"{input_method_id}\" is already not registered in the project")
            return result

        #Without defining any special events in particular, just remove the whole thing
        if len(input_events) == 0:
            del cls.__registered_events[input_project_id][input_method_id]
            is_content_removed = True
        else:
            #We must remove all events in MethodID that match InputEvents
            index_event: Dict[str,Any] = {}
            index_calculated_event: Dict[str,Any] = {}

            for index_event in input_events:
                for index_calculated_event in list(cls.__registered_events[input_project_id][input_method_id]):
                    if index_event == index_calculated_event:
                        cls.__registered_events[input_project_id][input_method_id].remove(index_calculated_event)
                        is_content_removed = True
                        break

        #If no longer needed, we remove the handler method
        if is_content_removed is True:
            index_project: Dict[str,Any] = {}
            does_handler_exist: bool = False

            for index_project in cls.__registered_events:
                if input_method_id in index_project:
                    does_handler_exist = True
                    break

            if does_handler_exist is False:
                cls.remove_handler(input_method_id)

        Console.write(input_project_id,"(RADGUI_EVENT_MANAGER) Successfully removed event")
        result = True

        return result

    @classmethod
    def handle_event(cls, input_project_id: uuid.UUID, input_event: Dict[ str,Any ]) -> None:
        """
        Take an event based dictionary and determine which handler method to call if need be.

        PARAMETERS:
        -----------

            cls:
                Represents the class itself.

            input_project_id: uuid.UUID
                Uniqu id that represents the project working with the event system

            input_event: Dict[ str,Any ]
                Dictionary representing the event that happened.

        RETURNS:
        --------

            None
        """
        Console.set_write_tags(input_project_id,{"RADGUI_EVENT_MANAGER":1})
        Console.write(input_project_id,f"(RADGUI_EVENT_MANAGER) Event Raised \n {str(input_event)}")
        Console.set_write_tags(input_project_id,{"RADGUI_EVENT_MANAGER":2})

        #Move through each Key which holds a reference to the class and function
        index_handler: str = ""
        index_event: Dict[str, Any] = {}
        index_method: Any = None
        is_subset:bool = False

        for index_handler in list(cls.__registered_events[input_project_id]):

            is_subset = False

            for index_event in list(cls.__registered_events[input_project_id][index_handler]):

                is_subset = set(index_event.items()).issubset(set(input_event.items()))
                Console.write(input_project_id,f"-- REGISTERED EVENT [{index_handler}] - IS SUBSET [{is_subset}]")

                if is_subset is True:

                    for index_method in cls.__registered_handlers[index_handler]:
                        try:
                            index_method(input_event)
                        except:
                            Console.write(input_project_id,"~~ Failed to Execute Method")
                            continue

    @classmethod
    def add_handler(cls, input_project_id: uuid.UUID, input_handler_name: str) -> bool:
        """
        Registers a method to call for events. Returns True when the method reference has been added
        to the event manager. Returns False if the method failed to be added to the event manager

        PARAMETERS:
        -----------

            cls:
                Represents the class itself.

            input_project_id: uuid.UUID
                Unique id that represents the project working with the event system

            input_handler_name: str
                Name of the handler method to add in the format "MODULE.CLASS.METHOD"

        RETURNS:
        --------

            result: bool
                Returns if the handler method reference was able to be added to the event manager

        """

        result:bool = False
        input_handler_name = input_handler_name.strip()

        Console.set_write_tags(input_project_id,{"RADGUI_EVENT_MANAGER":1})
        Console.write(input_project_id, f"(RADGUI_EVENT_MANAGER) Adding handler method {input_handler_name}")
        Console.set_write_tags(input_project_id,{"RADGUI_EVENT_MANAGER":2})

        if input_project_id not in cls.__is_strict:
            is_strict = False
        else:
            is_strict = cls.__is_strict[input_project_id]

        if input_handler_name == "":
            Console.write(input_project_id, "(RADGUI_EVENT_MANAGER) nothing given to add for handler")
            return result

        input_handler_split=input_handler_name.split('.')
        if len(input_handler_split) < 3:
            Console.write(input_project_id, "(RADGUI_EVENT_MANAGER) Handler needs a Module name, a class name, and a method name")
            return result

        #We do our best to get the right module, class, & method
        module_name:str = ".".join(input_handler_split[:-2])
        class_name:str = input_handler_split[-2]
        method_name:str = input_handler_split[-1]

        #Does the defined module even exist in loaded modules?
        loaded_modules: List[str] = sysModules.keys()
        considered_modules: List[str] = list(filter(lambda x: module_name in x, loaded_modules))

        #We can only continue if we see any modules
        if len(considered_modules) == 0:
            Console.write(input_project_id, f"(RADGUI_EVENT_MANAGER) No modules like \"{module_name}\" found in the system")
            return result

        #Or if in strict mode, we must get the module ID exact
        elif is_strict is True:
            if module_name in considered_modules:
                considered_modules = [module_name]
            else:
                Console.write(input_project_id, f"(RADGUI_EVENT_MANAGER) Strict Mode found no modules exactly like \"{module_name}\"")
                return result

        Console.write(input_project_id, f"(RADGUI_EVENT_MANAGER) Found {len(considered_modules)} Possible Module(s) - {considered_modules}")

        index_module: str = ""
        module_contents: List[str] = []
        considered_class: Any = None
        class_contents: List[str] = []
        unverified_method: Any = None
        considered_methods: List[Any] = []

        #Find all the classes that match the class name in all modules
        for index_module in considered_modules:
            #List all the classes in the Module
            module_contents = dir(sysModules[index_module])

            #Move onto the next Index if the class cant be found
            if class_name not in module_contents:
                continue

            #We do have the class in the module? Lets try and check it out
            try:
                considered_class = getattr(sysModules[index_module],class_name)
                class_contents = dir(considered_class)
            except:
                Console.write(input_project_id, f"(RADGUI_EVENT_MANAGER) Had issue getting contents of Class \"{class_name}\" in Module \"{index_module}\"")
                continue

            #Move onto the next Index if the method cant be found
            if method_name not in class_contents:
                continue

            #Verify type is a method
            try:
                unverified_method = getattr(considered_class,method_name)
                if unverified_method.__class__.__name__ != 'method':
                    Console.write(input_project_id, f"(RADGUI_EVENT_MANAGER) {index_module}.{class_name}.{method_name} is actually not a method but a \"{unverified_method.__class__.__name__}\"")
                    continue
                considered_methods.append(unverified_method)
                Console.write(input_project_id, f"(RADGUI_EVENT_MANAGER) {index_module}.{class_name}.{method_name} added to considered methods")

            except:
                Console.write(input_project_id, f"(RADGUI_EVENT_MANAGER) Had issue getting properties of method \"{method_name}\" in Class \"{class_name}\"")
                continue

        #We're left with all the functions that might be the one described
        #Do we have anything?
        if len(considered_methods) == 0:
            Console.write(input_project_id, "(RADGUI_EVENT_MANAGER) No Methods found")
            return result
        elif (is_strict is True) and (len(considered_methods) > 1):
            Console.write(input_project_id, f"(RADGUI_EVENT_MANAGER) Somehow, more than one method was found in {class_name} that matched search criteria.")
            Console.write(input_project_id, "(RADGUI_EVENT_MANAGER) Strict mode only allows for one method to be associated in a reference")
            return result

        #Add methods to list of class handler methods
        cls.__registered_handlers[input_handler_name.strip()] = considered_methods
        Console.write(input_project_id, f"(RADGUI_EVENT_MANAGER) Handler method(s) \"{input_handler_name}\" added to list of registered handlers")
        result = True

        return result

    @classmethod
    def remove_handler(cls,input_handler_name: str = "") -> bool:
        """
        Removes a handler method from the event manager. Returns True if the handler method was removed.
        Returns False if the handler method wasn't removed.

        PARAMETERS:
        -----------

            cls:
                Represents the class itself.

            input_handler_name: str
                The name of the handler method to remove

        RETURNS:
        --------

            result: bool
                Returns if the handler method reference was able to be removed from the event manager
        """
        result:bool = False
        input_handler_name = input_handler_name.strip()

        Console.set_write_tags(None,{"RADGUI_EVENT_MANAGER":1})
        Console.write(None, f"(RADGUI_EVENT_MANAGER) Removing handler method {input_handler_name}")
        Console.set_write_tags(None,{"RADGUI_EVENT_MANAGER":2})

        if input_handler_name == "":
            Console.write(None, "(RADGUI_EVENT_MANAGER) No handler method given")
            return result

        if input_handler_name not in cls.__registered_handlers:
            Console.write(None, f"(RADGUI_EVENT_MANAGER) Handler method(s) \"{input_handler_name}\" already does not exist in list of registered handlers")
            return result

        cls.__registered_handlers.popitem(input_handler_name)
        Console.write(None, f"(RADGUI_EVENT_MANAGER) Handler method(s) \"{input_handler_name}\" removed from list of registered handlers")
        result = True

        return result

    @classmethod
    def set_strictness(cls, input_project_id: uuid.UUID, strictness_value: bool) -> None:
        """
        Set the strictness for a project when it comes to adding method refrences

        PARAMETERS:
        -----------

            cls:
                Represents the class itself.

            input_project_id: uuid.UUID
                Unique id that represents the project working with the event system

            strictness_value: bool
                Represents the strictness of the handler method matching. True = Exact mathcing.

        RETURNS:
        --------

            NONE
        """
        cls.__is_strict[input_project_id]=strictness_value

    @classmethod
    def get_strictness(cls, input_project_id: uuid.UUID) -> bool:
        """
        Gets the strictness of a project when it comes to adding method refrences

        PARAMETERS:
        -----------

            cls:
                Represents the class itself.

            input_project_id: uuid.UUID
                Unique id that represents the project working with the event system

        RETURNS:
        --------

            result: bool
                The value of strictness associated with the project
        """
        result: bool = False

        if input_project_id in cls.__is_strict:
            result = cls.__is_strict[input_project_id]

        return result
