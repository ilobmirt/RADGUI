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
    def events(self) -> Dict[str,Any]:
        """
        Gets the status of registered events from the Event Manager

        PARAMETERS:
        -----------

            self:
                References the instance of the project class itself

        RETURNS:
        --------

            result: Dict[str, Any]
                This dictionary holds the value of registered events as it would in a JSON file
        """
        result: Dict[str,Any] = {}
        #result = EventManager.
        return result

    @events.setter
    def events(self,input_attributes:Dict[str,Any]) -> None:
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

    #Add a property group
    def create_property_group(self,**input_args) -> bool:
        """
        Creates a property group object within the project.
        This is indexed by the scope that property group functions in.

        PARAMETERS:
        -----------

            self:
                References the current instance of the Project class

            **input_args:
                A variable list of arguments passed to this function
                The list that this program will look at is the following...

                * scope -
                    The scope in which the property group will function in.

                * attributes -
                    If provided, the new property group will be configured by this dictionary

        RETURNS:
        --------

            result:bool
                Returns if the project was able to successfully create a new project scope

        """
        result:bool = False

        input_scope:str = ""
        if "scope" in input_args:
            input_scope = input_args["scope"]
            input_scope = input_scope.strip().upper()

        input_attributes:Dict[str,Any] = {}
        if "attributes" in input_args:
            input_attributes = input_args["attributes"]

        #We can't add to an existing property group
        if input_scope in self.property_groups:
            return result

        #We can't proceed if scope isnt legal
        if input_scope not in RefProperty.get_scopes():
            return result

        result = True
        return result

    #Remove a property group
    def remove_property_group(self,input_scope: str) -> None:
        """..."""
        #Cleanup input for property group scope
        input_scope = input_scope.strip().upper()

        #Only bother with the appropriate scope
        if input_scope.upper() in self.property_groups:
            bpy.utils.unregister_class(self.property_groups[input_scope.upper()])
            self.property_groups.pop(input_scope.upper())

    #Add an operator
    def create_operator(self,**input_args) -> bool:
        """

        PARAMETERS:
        -----------

        RETURNS:
        --------

        """

    #Remove an operator
    def remove_operator(self,input_name: str) -> bool:
        """

        PARAMETERS:
        -----------

        RETURNS:
        --------

        """
        if input_name in self.operators:
            bpy.utils.unregister_class(self.operators[input_name])
            self.operators.pop(input_name)

    #Add a panel
    def create_panel(self,**input_args) -> bool:
        """

        PARAMETERS:
        -----------

        RETURNS:
        --------

        """
        result:bool = False
        return result

    #Remove a panel
    def remove_panel(self,input_name: str) -> bool:
        """

        PARAMETERS:
        -----------

        RETURNS:
        --------

        """
        if input_name in self.panels:
            bpy.utils.unregister_class(self.panels[input_name])
            self.panels.pop(input_name)
