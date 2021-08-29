"""================================================================================================
This module and the classes within represent the Blender Python PropertyGroup used in a standard
project.

CLASSES:
    PropertyGroupShellMeta
    PropertyGroupShell
================================================================================================"""
from typing import List,Dict,Any # pylint: disable=unused-import
import bpy
from Console import Console
from property_collection import PropertyCollection
from reference.property import RefProperty

#==================================================#
#Property Group Shell Meta Class
#==================================================#
class PropertyGroupShellMeta(type):
    """
    A metaclass to allow for getters and setters to work on a class level rather than an instance level

    ATTRIBUTES:
    -----------
        value : Dict[str,Any]
            Represents the Class as a Dictionary

        scope : str
            Represents the scope this PropertyGroup affects.
    """
    #Represents the class as a Dictionary
    @property
    def value(cls) -> Dict[str,Any]:
        """
        GETTER: Represent the class as a dictionary

        PARAMETERS:
        -----------

            cls
                This is a reference to the class itself

        RETURNS:
        --------
            result : Dict[str,Any]
                This is the value of the class as a Dictionary object
        """
        output_tags: Dict[str,int] = {
            "PropertyGroupShell":1,
            "get_value":1
        }
        Console.Set_Tags(cls.namespace,output_tags)
        Console.Write(cls.namespace,"Getting dictionary value of {} propertygroup".format(cls.scope))
        output_tags["PropertyGroupShell"] = 2
        output_tags["get_value"] = 2
        Console.Set_Tags(cls.namespace,output_tags)
        result: Dict[str,Any] = {}

        for property_index in cls.__annotations__:
            result[property_index] = cls.get_property(property_index)

        Console.Write(cls.namespace,"SUCCESS: Dictionary value of {} propertygroup = {}".format(cls.scope,result))
        return result

    #Setting this value will set all the properties in the property group based on an input Dict
    @value.setter
    def value(cls, input_attributes: Dict[str,Any]) -> None:
        """
        SETTER:

        PARAMETERS:
        -----------

            cls
                Represents the class itself

            input_attributes : Dict[str, Any]
                This dictionary object holds the attributes to assign to the class

        RETURNS:
        --------

            None
        """
        output_tags: Dict[str,int] = {
            "PropertyGroupShell":1,
            "set_value":1
        }
        Console.Set_Tags(cls.namespace,output_tags)
        Console.Write(cls.namespace,"Setting Object Based on Dictionary Value {}".format(input_attributes))
        output_tags["PropertyGroupShell"] = 2
        output_tags["set_value"] = 2
        Console.Set_Tags(cls.namespace,output_tags)

        #We remove the properties that no longer exist, otherwise we update them
        for property_index in cls.__annotations__:
            if property_index not in input_attributes:
                Console.Write(cls.namespace,"Removing Property {}".format(property_index))
                cls.remove_property(property_index)

            else:
                Console.Write(cls.namespace,"Updating Property {}".format(property_index))
                cls.set_property(property_index,input_attributes[property_index])

        #Now we add the properties that don't yet exist
        for property_index in input_attributes:
            if property_index not in cls.__annotations__:
                Console.Write(cls.namespace,"Adding Property {}".format(property_index))
                cls.add_property(property_index,input_attributes[property_index])

    @property
    def scope(cls) -> str:
        """
        GETTER: Get the scope in which our PropertyGroup is connected to

        PARAMETERS:
        -----------

            cls
                References the class itself

        RETURNS:
        --------

            cls._scope : str
                Contains the value of the scope
        """
        return cls._scope

    @scope.setter
    def scope(cls, input_value: str) -> None:
        """
        SETTER: Set the scope from a given string. If it's a legal scope value,
        the class will remove its reference from its previous scope and re-reference
        itself to the new scope

        PARAMETERS:
        -----------

            cls
                References the class itself

        RETURNS:
        --------

            None
        """
        system_scopes: Dict[str,Any] = RefProperty.get_scopes()
        filtered_value: str = input_value.strip().upper()

        #We dont continue further if the given value is not an appropriate scope
        if filtered_value not in system_scopes:
            return

        #We don't continue further because there's already a PropertyGroup at our destination scope
        if hasattr(system_scopes[filtered_value],cls.namespace) is True:
            return

        #If we got here, it's safe to switch PropertyGroup scopes
        cls.unregister()
        cls._scope = filtered_value
        cls.register()

#==================================================#
#Property Group Shell Class
#==================================================#
class PropertyGroupShell(bpy.types.PropertyGroup, PropertyCollection, metaclass=PropertyGroupShellMeta):
    """
    Represents the PropertyGroup class used in a Blender Project

    ATTRIBUTES:
    -----------
        scope : str
            Represents the area where all properties in the property group
            are tied to.

    METHODS:
    --------
        register : None
        unregister : None
    """
    _scope: str = ""

    @classmethod
    def register(cls) -> None:
        """
        Adds a class pointer to the appropriate scope. Called when either the PropertyGroup is
        registerd to Blender or when the PropertyGroup is changing scopes

        PARAMETERS:
        -----------

            cls
                References the class itself

        RETURNS:
        --------

            None
        """
        output_tags: Dict[str,int] = {
            "PropertyGroupShell":1,
            "register":1
        }
        Console.Set_Tags(cls.namespace,output_tags)
        Console.Write(cls.namespace,"Registering {} propertygroup in Namespace {}".format(cls._scope,cls.namespace))
        output_tags["PropertyGroupShell"] = 2
        output_tags["register"] = 2
        Console.Set_Tags(cls.namespace,output_tags)

        system_scopes: Dict[str,Any] = RefProperty.get_scopes()

        if (cls.namespace != "") and (cls._scope in system_scopes):
            setattr(system_scopes[cls._scope],cls.namespace,bpy.props.PointerProperty(type=cls))
            Console.Write(cls.namespace, "SUCCESS: propertygroup has been registered")
        else:
            Console.Write(cls.namespace, "FAILURE: propertygroup needs a proper scope and a namespace")

    @classmethod
    def unregister(cls) -> None:
        """
        Removes the class pointer from the current scope. Called when either the PropertyGroup is
        getting unregistered from Blender or when the PropertyGroup is changing scopes

        PARAMETERS:
        -----------

            cls
                References the class itself

        RETURNS:
        --------

            None
        """
        output_tags: Dict[str,int] = {
            "PropertyGroupShell":1,
            "unregister":1
        }
        Console.Set_Tags(cls.namespace,output_tags)
        Console.Write(cls.namespace,"Unregistering {} propertygroup from Namespace {}".format(cls._scope,cls.namespace))
        output_tags["PropertyGroupShell"] = 2
        output_tags["unregister"] = 2
        Console.Set_Tags(cls.namespace,output_tags)

        system_scopes: Dict[str,Any] = RefProperty.get_scopes()

        if (cls.namespace != "") and (cls._scope in system_scopes):
            if hasattr(system_scopes[cls._scope],cls.namespace) is True:
                delattr(system_scopes[cls._scope],cls.namespace)
                Console.Write(cls.namespace, "SUCCESS: propertygroup has been unregistered")
            else:
                Console.Write(cls.namespace, "FAILURE: propertygroup was already unregistered")
        else:
            Console.Write(cls.namespace, "FAILURE: propertygroup needs a proper scope and a namespace")
