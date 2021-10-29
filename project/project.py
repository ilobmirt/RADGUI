"""================================================================================================
This module is designed to create and manage a single RADGUI project

CLASSES:
    Project
================================================================================================"""
import uuid
import json
from typing import List, Dict, Any # pylint: disable=unused-import
import bpy
from event_manager import EventManager
from radgui_console import Console
from radgui_system import System
from reference.property import RefProperty
from .property_group_shell import PropertyGroupShell # pylint: disable=unused-import
from .operator_shell import OperatorShell # pylint: disable=unused-import
from .panel_shell import PanelShell # pylint: disable=unused-import

#==================================================#
#RADGUI Project
#==================================================#

class Project():
    """
    This class is used as an instance to create and manage a single RADGUI project

    ATTRIBUTES:
    -----------

    __project_id: uuid.UUID
        Private Value. Unique id given to the project upon creation.

    header: Dict[str, Any]
        Getter:
        Setter:

    console: Dict[str, Any]
        Getter:
        Setter:

    events: Dict[str, Any]
        Getter: Pulls event information from the event manager of all events
        registered with the project. This is represented in a dictionary
        Setter: Configures the events associated with the project from a dictionary.

    property_groups: Dict[str, Any]
        Dictionary collection of all property groups associated with the project.
        These objects are indexed by the scope of the properties

    operators: Dict[str, Any]
        Dictionary collection of all operators associated with the project.
        These objects are indexed by their name in the project

    panels: Dict[str, Any]
        Dictionary collection of all panels associated with the project.
        These objects are indexed by their name in the project

    id: uuid.UUID
        Getter: Read only value for the project's unique id

    value: Dict[str, Any]
        Getter: Represents the project as a Dictionary object
        Setter: Configures the project from a Dictionary obect

    METHODS:
    --------

    """

    __project_id:uuid.UUID = None
    property_groups:Dict[str,Any] = {}
    operators:Dict[str,Any] = {}
    panels:Dict[str,Any] = {}

    def __init__(self, **input_args) -> None:
        """
        Initializes a fresh instance of a RADGUI project.
        The project can then take in data from a JSON file or a given dictionary
        If neither of those is given, will be a blank project

        PARAMETERS:
        -----------

            self:
                Representing the instance of the class itself

            **input_args:
                a variable list of arguments passed to it.
                The list that this program will look at is the following...

                * id -
                    This is the unique id given to the project

                * filename -
                    This project will be populated by the information given in a JSON file

                * json -
                    This project will be populated by the information given in a Dictionary

        RETURNS:
        --------

            None

        """

        input_id:uuid.UUID = None
        if "id" in input_args:
            input_id = input_args["id"]

        input_filename:str = ""
        if "filename" in input_args:
            input_filename = input_args["filename"]

        input_json:Dict[str,Any] = {}
        if "json"  not in input_args:
            input_json = input_args["json"]

        self.__project_id = input_id

        input_dict:Dict[str,Any] = {}
        if input_filename is not "":
            #read file into JSON
            try:
                with open(input_filename,"r") as radgui_file:
                    input_dict = json.load(radgui_file)
            except:
                pass

        elif input_json is not {}:
            input_dict = input_json

        self.value = input_dict

    def __del__(self):
        """
        Instance uninitialization method. Cleanup and unregister everything
        this class is connected to.

        PARAMETERS:
        -----------
            self:
                Refrences the instance of the class itself

        RETURNS:
        --------

            None
        """
        #remove panels
        remove_list: List[any] = self.panels.keys()
        for panel_index in remove_list:
            self.remove_panel(panel_index)

        #remove operators
        remove_list = self.operators.keys()
        for operator_index in remove_list:
            self.remove_operator(operator_index)

        #remove property groups
        remove_list = self.property_groups.keys()
        for property_group_index in remove_list:
            self.remove_property_group(property_group_index)

        EventManager.unregister_project(self.__project_id)
        Console.remove_project_id(self.__project_id)
        System.remove_project_id(self.__project_id)
        return

    @property
    def id(self) -> uuid.UUID: # pylint: disable=C0103
        """
        GETTER: Obtain the project's unique id

        PARAMETERS:
        -----------

            self:
                References the instance of the project class itslef

        RETURNS:
        --------

            self.__project_id:
                the unique read-only project id set upon the class' creation
        """
        return self.__project_id

    @property
    def header(self) -> Dict[str,Any]:
        """
        """
        result: Dict[str,Any] = {
            "CONSOLE":self.console
        }
        return result

    @header.setter
    def header(self,input_value:Dict[str,Any]) -> None:
        """
        """
        return

    @property
    def console(self) -> Dict[str, Any]:
        """
        """
        result: Dict[str,Any] = {
            "OUTPUT":Console.get_medium(self.__project_id),
            "FILTER":Console.get_filter(self.__project_id)
        }
        return result

    @console.setter
    def console(self,input_value:Dict[str,Any]) -> None:
        """
        """
        return

    @property
    def events(self) -> Dict[str,List[Dict[str,Any]]]:
        """
        Gets the status of registered events from the Event Manager

        PARAMETERS:
        -----------

            self:
                References the instance of the project class itself

        RETURNS:
        --------

            result: Dict[str,List[Dict[str,Any]]]
                This dictionary holds the value of registered events as it would in a JSON file
        """
        result: Dict[str,List[Dict[str,Any]]] = {}
        result = EventManager.get_project_value(self.__project_id)
        return result

    @events.setter
    def events(self,input_attributes:Dict[str,List[Dict[str,Any]]]) -> None:
        """
        Configures the events registered with the Event Manager from a given Dictionary

        PARAMETERS:
        -----------

            self:
                References the instance of the project class itself

            input_attributes: Dict[str, Any]
                The dictionary to configure project related events from

        RETURNS:
        --------

            None
        """
        EventManager.set_project_value(self.__project_id,input_attributes)
        return

    @property
    def value(self) -> Dict[str,Any]:
        """
        GETTER: Represent the RADGUI Project as a Dictionary Object

        PARAMETERS:
        -----------

            self:
                References the current instance of the Project class

        RETURNS:
        --------

            result : Dict[str,Any]
                This dictionary represents the project and its properties
        """
        result:Dict[str,Any] = {
            "TYPE":"RADGUI_PROJECT",
            "BODY":{}
        }

        return result

    @value.setter
    def value(self,input_attributes:Dict[str,Any]) -> None:
        """
        SETTER: Configures the RADGUI Project object from a Dictionary object

        PARAMETERS:
        -----------

            self:
                References the current instance of the Project class

            input_attributes : Dict[str, Any]
                Dictionary object holding the attributes to assign to the Project object

        RETURNS:
        --------

            None
        """

    #Create a property group
    def create_property_group(self, **input_args) -> bool:
        """
        Generate a property group class from the property group shell

        PARAMETERS:
        -----------
            self:
                References the Project instance itself.

            **input_args:
                a variable list of arguments passed to it.
                The list that this program will look at is the following...

                scope: str
                    MANDATORY. The scope that this property group will exist
                    in. Must not already exist in the project.

                value: Dict[str,Dict[str,Any]]
                    The starting value of the property group. This dictionary
                    holds the variables of the property group and their
                    properties.

        RETURNS:
        --------
            result: bool
                The state of the creation of a property group. True if successful.

        """
        result:bool = False

        Console.set_filter(self.__project_id,{"project":1,"create_property_group":1})
        Console.write(self.__project_id,f"Creating property group for project - \"{self.__project_id.hex}\"")
        Console.set_filter(self.__project_id,{"project":2,"create_property_group":2})

        #We need the scope of the property group
        if "scope" not in input_args:
            Console.write(self.__project_id,"FAILURE: Scope was not provided to create property group")
            return result

        input_scope:str = input_args["scope"]
        input_scope = input_scope.strip().upper()

        #The scope can't already exist
        if input_scope in self.property_groups:
            Console.write(self.__project_id,f"FAILURE: Property group already exists in scope - \"{input_scope}\"")
            return result

        #The scope must be a valid scope
        if input_scope not in RefProperty.get_scopes().keys():
            Console.write(self.__project_id,f"FAILURE: Given scope \"{input_scope}\" is not a valid scope type.")
            return result

        #Assign it an initial value if given a value
        input_value:Dict[str,Dict[str,Any]] = {}
        if "value" in input_args:
            input_value = input_args["value"]

        #Create the class for the scope, then register it
        autogen_classname:str=f"PROPERTYGROUP_{input_scope}_IN_{self.__project_id.hex.upper()}"
        autogen_attributes:Dict[str,Any] = {
            "scope":input_scope,
            "__project_id":self.__project_id
        }
        autogen_class = type(autogen_classname,(PropertyGroupShell,),autogen_attributes)
        self.property_groups.update({input_scope:autogen_class})

        if input_value is not {}:
            self.property_groups[input_scope].value = input_value

        bpy.utils.register_class(self.property_groups[input_scope])

        result = True
        Console.write(self.__project_id,f"SUCCESS: Created Class \"{autogen_classname}\" for scope \"{input_scope}\"")

        return result

    #Remove an existing property group
    def remove_property_group(self,input_scope:str) -> bool:
        """
        Removes an already existing property group

        PARAMETERS:
        -----------
            self:
                References the Project instance itself.

            input_scope: str
                This is the scope we will remove.

        RETURNS:
        --------
            result: bool
                The state of the removal of the property group. True if successful.

        """
        result:bool = False
        input_scope = input_scope.strip().upper()

        Console.set_filter(self.__project_id,{"project":1,"remove_property_group":1})
        Console.write(self.__project_id,f"Removing property group for scope \"{input_scope}\"")
        Console.set_filter(self.__project_id,{"project":2,"remove_property_group":2})

        if input_scope not in self.property_groups:
            Console.write(self.__project_id,f"FAILURE: Given scope \"{input_scope}\" not associated in project \"{self.__project_id.hex.upper()}\"")
            return result

        #Unregister the class
        bpy.utils.unregister_class(self.property_groups[input_scope])
        self.property_groups.pop(input_scope)

        result = True
        Console.write(self.__project_id,f"SUCCESS: Removed Property Group for scope \"{input_scope}\"")

        return result

    #Add an operator
    def create_operator(self,**input_args) -> bool:
        """
        Creates a custom operator holding custom properties and content

        PARAMETERS:
        -----------
            self:
                References the Project instance itself.

            **input_args:
                a variable list of arguments passed to it.
                The list that this program will look at is the following...

                name: str
                    Mandatory. The name of the operator in the project

                value: Dict[str,Any]
                    This is the starting value of the operator

        RETURNS:
        --------
            result: bool
                The state of the creation of the operator. True if successful.

        """

    #Remove an operator
    def remove_operator(self,input_name: str) -> bool:
        """

        PARAMETERS:
        -----------

        RETURNS:
        --------
            result: bool
                The state of the removal of the operator. True if successful.

        """
        result:bool = False
        input_name = input_name.strip()

        Console.set_filter(self.__project_id,{"project":1,"remove_operator":1})
        Console.write(self.__project_id,f"Removing operator \"{input_name}\"")
        Console.set_filter(self.__project_id,{"project":2,"remove_operator":2})

        if input_name not in self.operators:
            Console.write(self.__project_id,f"FAILURE: The operator \"{input_name}\" does not exist in project \"{self.__project_id.hex.upper()}\"")
            return result

        bpy.utils.unregister_class(self.operators[input_name])
        self.operators.pop(input_name)

        result = True
        Console.write(self.__project_id,f"SUCCESS: Removed operator \"{input_name}\"")

        return result

    #Add a panel
    def create_panel(self,**input_args) -> bool:
        """

        PARAMETERS:
        -----------
            self:
                References the Project instance itself.

            **input_args:
                a variable list of arguments passed to it.
                The list that this program will look at is the following...

        RETURNS:
        --------
            result: bool
                The state of the creation of a panel. True if successful.

        """
        result:bool = False
        return result

    #Remove a panel
    def remove_panel(self,input_name: str) -> bool:
        """
        Removes the named panel from the project and Blender

        PARAMETERS:
        -----------
            self:
                References the instance of the class itself

            input_name:str
                The name of the panel to remove

        RETURNS:
        --------
            result: bool
                The state of the removal of the panel. True if successful.

        """
        result:bool = False
        input_name = input_name.strip()

        Console.set_filter(self.__project_id,{"project":1,"remove_panel":1})
        Console.write(self.__project_id,f"Removing panel \"{input_name}\"")
        Console.set_filter(self.__project_id,{"project":2,"remove_panel":2})

        if input_name not in self.panels:
            Console.write(self.__project_id,f"FAILURE: The panel \"{input_name}\" does not exist in project \"{self.__project_id.hex.upper()}\"")
            return result

        bpy.utils.unregister_class(self.panels[input_name])
        self.panels.pop(input_name)

        result = True
        Console.write(self.__project_id,f"SUCCESS: Removed panel \"{input_name}\"")

        return result
