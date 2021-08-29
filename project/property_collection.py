"""================================================================================================
This module represents functionality that will be applied to child classes of both PropertyGroup
and Operator. The ability to add and remove properties to the class.

CLASSES:
    PropertyCollection

================================================================================================"""
from typing import List, Dict, Any
import bpy
from EventManager import EventManager # pylint: disable=unused-import
from Console import Console
from reference.property import RefProperty

class PropertyCollection():
    """
    This class holds a collection of properties and has the ability to add and remove property obejcts

    ATTRIBUTES:
    -----------
        __annotations__ : Dict[str,Any]
            Holds all of the properties in the class

        namespace: str
            Represents the project's unique identifier

    METHODS:
    --------
        add_property
        remove_property
        get_property
        set_property
        get_event_handling
        set_event_handling
        add_bool_property
        add_boolvector_property
        add_enumerator_property
        add_float_property
        add_floatvector_property
        add_int_property
        add_intvector_property
        add_string_property
    """
    __annotations__: Dict[str,Any] = {}
    namespace: str = ""


    #Add a property to the group
    @classmethod
    def add_property(cls,input_name: str,input_attributes: Dict[str,Any]) -> None:
        """
        Adds a property to the class given the name and its attributes

        PARAMETERS:
        -----------

        cls
            references the class itself because this function affects the class

        input_name : str
            This is the name of the property we are adding to the class.

        input_attributes : Dict[str,Any]
            This dictionary contains the attributes that the property will initialize with.

        RETURNS:
        --------

        None
        """
        output_tags: Dict[str,int] = {
            "PropertyCollection":1,
            "add_property":1
        }
        Console.Set_Tags(cls.namespace,output_tags)
        Console.Write(cls.namespace,"Adding property \"{}\" to {}".format(input_name,type(cls).__name__))
        output_tags["PropertyCollection"] = 2
        output_tags["add_property"] = 2
        Console.Set_Tags(cls.namespace,output_tags)
        #Property must have a type
        if "TYPE" not in input_attributes:
            Console.Write(cls.namespace,"ERROR: No Type Defined. Aborting Method")
            return

        #We got here, lets start adding the parameters for the property
        current_type = input_attributes["TYPE"].upper()

        #Set Parameter Defaults
        if current_type in ["BOOL","BOOLEAN","BLN"]:
            Console.Write(cls.namespace,"Adding a boolean property")
            cls.add_bool_property(input_name,input_attributes)

        elif current_type in ["BOOLVECTOR"]:
            Console.Write(cls.namespace,"Adding a boolean vector property")
            cls.add_boolvector_property(input_name,input_attributes)

        elif current_type in ["ENUM","ENUMERATOR"]:
            Console.Write(cls.namespace,"Adding an enumerator property")
            cls.add_enumerator_property(input_name,input_attributes)

        elif current_type in ["FLT","FLOAT"]:
            Console.Write(cls.namespace,"Adding a float property")
            cls.add_float_property(input_name,input_attributes)

        elif current_type in ["FLOATVECTOR"]:
            Console.Write(cls.namespace,"Adding a float vector property")
            cls.add_floatvector_property(input_name,input_attributes)

        elif current_type in ["INT","INTEGER"]:
            Console.Write(cls.namespace,"Adding an integer property")
            cls.add_int_property(input_name,input_attributes)

        elif current_type in ["INTVECTOR"]:
            Console.Write(cls.namespace,"Adding an integer vector property")
            cls.add_intvector_property(input_name,input_attributes)

        elif current_type in ["STR","STRING"]:
            Console.Write(cls.namespace,"Adding a string property")
            cls.add_string_property(input_name,input_attributes)

        else:
            Console.Write(cls.namespace,"ERROR: Unknown type defined. Aborting Method")
            return

    #Remove a property from the group
    @classmethod
    def remove_property(cls,input_name: str) -> None:
        """
        Removes a property of a given name from the class

        PARAMETERS:
        -----------

        cls
            references the class itself because this function affects the class

        input_name : str
            This is the name of the property we are removing.

        RETURNS:
        --------

        None
        """
        output_tags: Dict[str,int] = {
            "PropertyCollection":1,
            "remove_property":1
        }
        Console.Set_Tags(cls.namespace,output_tags)
        Console.Write(cls.namespace,"Removing property \"{}\" from {}".format(input_name,type(cls).__name__))
        output_tags["PropertyCollection"] = 2
        output_tags["remove_property"] = 2
        Console.Set_Tags(cls.namespace,output_tags)
        #Do nothing if it doesnt exist
        if input_name not in cls.__annotations__:
            Console.Write(cls.namespace,"ERROR: Property \"{}\" already doesn\'t exist. Aborting Method".format(input_name))
            return

        del cls.__annotations__[input_name]

    #Get property attributes
    @classmethod
    def get_property(cls,input_name: str) -> Dict[str,Any]:
        """
        Takes a property and represents it as a dictionary object

        PARAMETERS:
        -----------

        cls
            references the class itself because this function refrences the class

        input_name : str
            This is the name of the property within this class we are checking out.

        RETURNS:
        --------

        result : Dict[str,Any]
            This is the dictionary representation of the property object
        """
        output_tags: Dict[str,int] = {
            "PropertyCollection":1,
            "get_property":1
        }
        Console.Set_Tags(cls.namespace,output_tags)
        Console.Write(cls.namespace,"Obtaining dictionary attributes of property \"{}\" within {}".format(input_name,type(cls).__name__))
        output_tags["PropertyCollection"] = 2
        output_tags["get_property"] = 2
        Console.Set_Tags(cls.namespace,output_tags)
        result: Dict[str,Any] = {}

        #The name must exist already
        if input_name not in cls.__annotations__:
            Console.Write(cls.namespace,"ERROR: property \"{}\" doesn't exist in {}. Aborting Method. Returning {}".format(input_name,type(cls).__name__,result))
            return result

        #Now that we know the property exists, lets get the defaults for the type
        type_defaults: Dict[str,Any] = {}
        type_options: List[str] = []

        bpy_to_radgui: Dict[str,str] = {
            "name":"TEXT",
            "description":"DESCRIPTION",
            "default":"DEFAULT",
            "min":"MIN",
            "max":"MAX",
            "soft_min":"SOFT_MIN",
            "soft_max":"SOFT_MAX",
            "step":"STEP",
            "precision":"PRECISION",
            "maxlen":"MAX_LEN",
            "size":"SIZE",
            "unit":"UNIT",
            "subtype":"SUBTYPE"
        }

        bpytype_to_radguitype: Dict[str,str] = {
            "BoolProperty":"BOOL",
            "BoolVectorProperty":"BOOLVECTOR",
            "EnumProperty":"ENUM",
            "FloatProperty":"FLOAT",
            "FloatVectorProperty":"FLOATVECTOR",
            "IntProperty":"INT",
            "IntVectorProperty":"INTVECTOR",
            "StringProperty":"STRING"
        }

        current_type: str = cls.__annotations__[input_name][0].__name__
        current_attributes: Dict[str,Any] = cls.__annotations__[input_name][1]

        if current_type in bpytype_to_radguitype:
            result["TYPE"] = bpytype_to_radguitype[current_type]

        else:
            Console.Write(cls.namespace,"ERROR: Weird bpy type \"{}\" for property \"{}\" in {}. Aboring Method. Returning {}".format(current_type,input_name,type(cls).__name__,result))
            return result

        type_defaults = RefProperty.get_defaults(result["TYPE"])
        type_options = RefProperty.get_options(result["TYPE"])
        result_index: str = ""

        #Build up our Dictionary for all items that exist outside of the defaults
        for attribute_index in current_attributes:
            if (attribute_index in bpy_to_radgui) and (attribute_index in type_defaults):
                result_index = bpy_to_radgui[attribute_index]
                if type_defaults[result_index] != current_attributes[attribute_index]:
                    result[result_index] = current_attributes[attribute_index]

        #Filter appropriate Options
        if "options" in current_attributes:
            if set(type_options).difference(set(current_attributes["options"])) != set():
                result["OPTIONS"] = set(current_attributes["options"])

        #Filter event handling
        if "update" in current_attributes:
            if (current_attributes["update"] is not None) and (type_defaults["EVENT_HANDLING"] is False):
                result["EVENT_HANDLING"] = True
            elif (current_attributes["update"] is None) and (type_defaults["EVENT_HANDLING"] is True):
                result["EVENT_HANDLING"] = False

        #We've compiled as much as we could, return the resulting Dictionary
        Console.Write(cls.namespace,"SUCCESS: Property \"{}\" = {}".format(input_name,result))
        return result

    #Set property attributes
    @classmethod
    def set_property(cls,input_name: str,input_attributes: Dict[str,Any]) -> None:
        """
        Configures a given property using a Dictionary object

        PARAMETERS:
        -----------

        cls
            references the class itself because this function affects the class

        input_name : str
            This is the name of the property within this class we are configuring.

        input_attributes : Dict[str,Any]
            This dictionary contains a key-value pair representing the attributes of
            the  property.

        RETURNS:
        --------

        None
        """
        output_tags: Dict[str,int] = {
            "PropertyCollection":1,
            "set_property":1
        }
        Console.Set_Tags(cls.namespace,output_tags)
        Console.Write(cls.namespace,"Setting dictionary attributes of property \"{}\" within {} using attributes {}".format(input_name,type(cls).__name__,input_attributes))
        output_tags["PropertyCollection"] = 2
        output_tags["set_property"] = 2
        Console.Set_Tags(cls.namespace,output_tags)
        #The name must exist already
        if input_name not in cls.__annotations__:
            Console.Write(cls.namespace,"ERROR: Property \"{}\" does not exist in {}. Aboring Method".format(input_name,type(cls).__name__))
            return

        #There's got to be some attributes to configure
        if input_attributes == {}:
            Console.Write(cls.namespace,"ERROR: There are no attributes to define for property \"{}\". Aborting Method".format(input_name))
            return

        #Let's get the type
        current_type: str = cls.__annotations__[input_name][0].__name__
        desired_type: str = ""
        radguitype_to_bpytype: Dict[str,str] = {
            "BOOL":"BoolProperty",
            "BOOLVECTOR":"BoolVectorProperty",
            "ENUM":"EnumProperty",
            "FLOAT":"FloatProperty",
            "FLOATVECTOR":"FloatVectorProperty",
            "INT":"IntProperty",
            "INTVECTOR":"IntVectorProperty",
            "STRING":"StringProperty"
        }

        #Are we changing the type?
        if "TYPE" in input_attributes:
            #Does it even exist?
            desired_type = input_attributes["TYPE"]
            if desired_type in radguitype_to_bpytype:
                #If it's different from what we have, let's just replace the property
                if radguitype_to_bpytype[desired_type] != current_type:
                    Console.Write(cls.namespace,"Attribute Type differs from current type of Property {}. It will be removed, then added as the new type.".format(input_name))
                    cls.remove_property(input_name)
                    cls.add_property(input_name,input_attributes)
                    return
            else:
                #Bad type declared
                Console.Write(cls.namespace,"ERROR: Unknown type \"{}\" given. Aborting Method".format(desired_type))
                return

        #We got here, I guess we've got work to do
        target_property: List[Any] = list(cls.__annotations__[input_name])
        target_attributes: Dict[str,Any] = target_property[1]
        attribute_index: str = ""
        radgui_to_bpy: Dict[str,str] = {
            "TEXT":"name",
            "DESCRIPTION":"description",
            "DEFAULT":"default",
            "MIN":"min",
            "MAX":"max",
            "SOFT_MIN":"soft_min",
            "SOFT_MAX":"soft_max",
            "STEP":"step",
            "PRECISION":"precision",
            "MAX_LEN":"maxlen",
            "SIZE":"size",
            "UNIT":"unit",
            "SUBTYPE":"subtype"
        }

        #Handles most attributes, except event handling
        for params_index in input_attributes:
            if params_index in radgui_to_bpy:
                attribute_index = radgui_to_bpy[params_index]
                if attribute_index in target_attributes:
                    target_attributes[attribute_index] = input_attributes[params_index]

        #Handle event handling here
        if "EVENT_HANDLING" in input_attributes:
            if input_attributes["EVENT_HANDLING"] is True:
                target_attributes["update"] = eval("lambda Part1,Part2: PropertyGroupShell.PropertyUpdate(Part1, Part2, '{}', '{}')".format(cls.namespace,input_name))

            else:
                target_attributes["update"] = None

        #Rebuild Property with new attributes
        cls.__annotations__[input_name] = tuple([target_property[0],target_attributes])
        Console.Write(cls.namespace,"SUCCESS: Updating Property \"{}\" for {} succeeded".format(input_name,type(cls).__name__))

    #Determine if a property is set to handle events
    @classmethod
    def get_event_handling(cls, input_name:str) -> bool:
        """
        Determines if a property in this class has event handling.

        PARAMETERS:
        -----------

        cls
            references the class itself because this function refrences the class

        input_name : str
            This is the name of the property within this class we are checking out.

        RETURNS:
        --------

        result : bool
            * True - The given property has event handling
            * False - The given property does not have event handling
        """
        output_tags: Dict[str,int] = {
            "PropertyCollection":1,
            "get_event_handling":1
        }
        Console.Set_Tags(cls.namespace,output_tags)
        Console.Write(cls.namespace,"Getting event handling attribute of property \"{}\" within {}".format(input_name,type(cls).__name__))
        output_tags["PropertyCollection"] = 2
        output_tags["get_event_handling"] = 2
        Console.Set_Tags(cls.namespace,output_tags)

        result: bool = False

        #Name must exist as a property
        if input_name not in cls.__annotations__:
            Console.Write(cls.namespace,"ERROR: Property \"{}\" doesn't exist in {}. Aborting Method. Returning {}".format(input_name,type(cls).__name__, result))
            return result

        target_property: tuple = cls.__annotations__[input_name]

        if target_property[1]["update"] is not None:
            result = True

        Console.Write(cls.namespace,"SUCCESS: Property \"{}\" in {} has \"EVENT_HANDLING\" = {}".format(input_name,type(cls).__name__, result))
        return result

    #Set Event Handling for a property
    @classmethod
    def set_event_handling(cls,input_name: str,input_value: bool) -> None:
        """
        (FUNCTION DOCSTRING TEMPLATE)

        PARAMETERS:
        -----------

        cls
            references the class itself because this function affects the class

        input_name : str
            This is the name of the property within this class we are configuring
            event handling for.

        input_value : bool
            * True = Changes to this property will be sent to RADGUI's event handler
            * False = The property will not have any event handling

        RETURNS:
        --------

        None
        """
        output_tags: Dict[str,int] = {
            "PropertyCollection":1,
            "set_event_handling":1
        }
        Console.Set_Tags(cls.namespace,output_tags)
        Console.Write(cls.namespace,"Setting event handling attribute of property \"{}\" within {} to {}".format(input_name,type(cls).__name__,input_value))
        output_tags["PropertyCollection"] = 2
        output_tags["set_event_handling"] = 2
        Console.Set_Tags(cls.namespace,output_tags)
        #Name must exist as a property
        if input_name not in cls.__annotations__:
            Console.Write(cls.namespace,"ERROR: Property \"{}\" doesn't exist in {}. Aborting Method".format(input_name,type(cls).__name__))
            return

        cls.set_property(input_name,{"EVENT_HANDLING":input_value})

    #Add property specific to type = Bool
    @classmethod
    def add_bool_property(cls,input_name: str,input_attributes: Dict[str,Any]) -> None:
        """
        adds a blender boolean property to the class annotations with the given input name

        PARAMETERS:
        -----------

        cls
            references the class itself because this function affects the class

        input_name : str
            This will be the name for the new blender boolean property

        input_attributes : Dict[str,Any]
            These will be the attributes given to the blender boolean property

        RETURNS:
        --------

        None
        """
        output_tags: Dict[str,int] = {
            "PropertyCollection":1,
            "add_bool_property":1
        }
        Console.Set_Tags(cls.namespace,output_tags)
        Console.Write(cls.namespace,"Adding boolean property \"{}\" to {} using attributes {}".format(input_name,type(cls).__name__,input_attributes))
        output_tags["PropertyCollection"] = 2
        output_tags["add_bool_property"] = 2
        Console.Set_Tags(cls.namespace,output_tags)

        #Property must have a name
        if input_name.strip() == "":
            Console.Write(cls.namespace,"ERROR: Property has no name. Aborting Method")
            return
        #Property must not already exist
        if input_name in cls.__annotations__:
            Console.Write(cls.namespace,"ERROR: Property \"{}\" already exists in {}. Aborting Method".format(input_name,type(cls).__name__))
            return
        #Property must have a type
        if "TYPE" not in input_attributes:
            Console.Write(cls.namespace,"ERROR: Property \"{}\" needs a type. Aborting Method".format(input_name))
            return
        #Type must also be specific to this function
        if input_attributes["TYPE"].upper() not in ["BOOL","BOOLEAN","BLN"]:
            Console.Write(cls.namespace,"ERROR: Property \"{}\" is not of the correct type. Aborting Method".format(input_name))
            return

        #Fill out default parameters
        params: Dict[str,Any] = RefProperty.get_defaults("BOOL")

        #Override with input if the type matches
        for params_index in params:
            if params_index in input_attributes:
                if type(params[params_index]) == type(input_attributes[params_index]):
                    params[params_index] = input_attributes[params_index]

        #Add the property
        cls.__annotations__.update(
            {
                input_name: bpy.props.BoolProperty(
                    name=params["TEXT"],
                    description=params["DESCRIPTION"],
                    default=params["DEFAULT"],
                    options=params["OPTIONS"],
                    subtype=params["SUBTYPE"]
                )
            }
        )

        #Set event handling if enabled
        if params["EVENT_HANDLING"] is True:
            cls.set_event_handling(input_name,True)

        Console.Write(cls.namespace,"SUCCESS: Property \"{}\" has been created for {}.".format(input_name,type(cls).__name__))

    #Add property specific to type = BoolVector
    @classmethod
    def add_boolvector_property(cls,input_name: str,input_attributes: Dict[str,Any]) -> None:
        """
        adds a blender boolean vector property to the class annotations with the given input name

        PARAMETERS:
        -----------

        cls
            references the class itself because this function affects the class

        input_name : str
            This will be the name for the new blender boolean vector property

        input_attributes : Dict[str,Any]
            These will be the attributes given to the blender boolean vector property

        RETURNS:
        --------

        None
        """
        output_tags: Dict[str,int] = {
            "PropertyCollection":1,
            "add_boolvector_property":1
        }
        Console.Set_Tags(cls.namespace,output_tags)
        Console.Write(cls.namespace,"Adding boolean vector property \"{}\" to {} using attributes {}".format(input_name,type(cls).__name__,input_attributes))
        output_tags["PropertyCollection"] = 2
        output_tags["add_boolvector_property"] = 2
        Console.Set_Tags(cls.namespace,output_tags)

        #Property must have a name
        if input_name.strip() == "":
            Console.Write(cls.namespace,"ERROR: Property has no name. Aborting Method")
            return
        #Property must not already exist
        if input_name in cls.__annotations__:
            Console.Write(cls.namespace,"ERROR: Property \"{}\" already exists in {}. Aborting Method".format(input_name,type(cls).__name__))
            return
        #Property must have a type
        if "TYPE" not in input_attributes:
            Console.Write(cls.namespace,"ERROR: Property \"{}\" needs a type. Aborting Method".format(input_name))
            return
        #Type must also be specific to this function
        if input_attributes["TYPE"].upper() not in ["BOOLVECTOR"]:
            Console.Write(cls.namespace,"ERROR: Property \"{}\" is not of the correct type. Aborting Method".format(input_name))
            return

        #Fill out default parameters
        params: Dict[str,Any] = RefProperty.get_defaults("BOOLVECTOR")

        #Override with input if the type matches
        for params_index in params:
            if params_index in input_attributes:
                if type(params[params_index]) == type(input_attributes[params_index]):
                    params[params_index] = input_attributes[params_index]

        #Add the property
        cls.__annotations__.update(
            {
                input_name:bpy.props.BoolVectorProperty(
                    name=params["TEXT"],
                    description=params["DESCRIPTION"],
                    default=params["DEFAULT"],
                    options=params["OPTIONS"],
                    subtype=params["SUBTYPE"],
                    size=params["SIZE"]
                )
            }
        )

        #Set event handling if enabled
        if params["EVENT_HANDLING"] is True:
            cls.set_event_handling(input_name,True)

        Console.Write(cls.namespace,"SUCCESS: Property \"{}\" has been created for {}.".format(input_name,type(cls).__name__))

    #Add property specific to type = Enum
    @classmethod
    def add_enumerator_property(cls,input_name: str,input_attributes: Dict[str,Any]) -> None:
        """
        adds a blender enumerator property to the class annotations with the given input name

        PARAMETERS:
        -----------

        cls
            references the class itself because this function affects the class

        input_name : str
            This will be the name for the new blender enumerator property

        input_attributes : Dict[str,Any]
            These will be the attributes given to the blender enumerator property

        RETURNS:
        --------

        None
        """
        output_tags: Dict[str,int] = {
            "PropertyCollection":1,
            "add_enumerator_property":1
        }
        Console.Set_Tags(cls.namespace,output_tags)
        Console.Write(cls.namespace,"Adding enumerator property \"{}\" to {} using attributes {}".format(input_name,type(cls).__name__,input_attributes))
        output_tags["PropertyCollection"] = 2
        output_tags["add_enumerator_property"] = 2
        Console.Set_Tags(cls.namespace,output_tags)

        #Property must have a name
        if input_name.strip() == "":
            Console.Write(cls.namespace,"ERROR: Property has no name. Aborting Method")
            return
        #Property must not already exist
        if input_name in cls.__annotations__:
            Console.Write(cls.namespace,"ERROR: Property \"{}\" already exists in {}. Aborting Method".format(input_name,type(cls).__name__))
            return
        #Property must have a type
        if "TYPE" not in input_attributes:
            Console.Write(cls.namespace,"ERROR: Property \"{}\" needs a type. Aborting Method".format(input_name))
            return
        #Type must also be specific to this function
        if input_attributes["TYPE"].upper() not in ["ENUM","ENUMERATOR"]:
            Console.Write(cls.namespace,"ERROR: Property \"{}\" is not of the correct type. Aborting Method".format(input_name))
            return

        #Fill out default parameters
        params: Dict[str,Any] = RefProperty.get_defaults("ENUM")

        #Override with input if the type matches
        for params_index in params:
            if params_index in input_attributes:
                if type(params[params_index]) == type(input_attributes[params_index]):
                    params[params_index] = input_attributes[params_index]

        #Add the property
        cls.__annotations__.update(
            {
                input_name:bpy.props.EnumProperty(
                    items=params["ITEMS"],
                    name=params["TEXT"],
                    description=params["DESCRIPTION"],
                    default=params["DEFAULT"],
                    options=params["OPTIONS"]
                )
            }
        )

        #Set event handling if enabled
        if params["EVENT_HANDLING"] is True:
            cls.set_event_handling(input_name,True)

        Console.Write(cls.namespace,"SUCCESS: Property \"{}\" has been created for {}.".format(input_name,type(cls).__name__))

    #Add property specific to type = Float
    @classmethod
    def add_float_property(cls,input_name: str,input_attributes: Dict[str,Any]) -> None:
        """
        adds a blender float property to the class annotations with the given input name

        PARAMETERS:
        -----------

        cls
            references the class itself because this function affects the class

        input_name : str
            This will be the name for the new blender float property

        input_attributes : Dict[str,Any]
            These will be the attributes given to the blender float property

        RETURNS:
        --------

        None
        """
        output_tags: Dict[str,int] = {
            "PropertyCollection":1,
            "add_float_property":1
        }
        Console.Set_Tags(cls.namespace,output_tags)
        Console.Write(cls.namespace,"Adding float property \"{}\" to {} using attributes {}".format(input_name,type(cls).__name__,input_attributes))
        output_tags["PropertyCollection"] = 2
        output_tags["add_float_property"] = 2
        Console.Set_Tags(cls.namespace,output_tags)

        #Property must have a name
        if input_name.strip() == "":
            Console.Write(cls.namespace,"ERROR: Property has no name. Aborting Method")
            return
        #Property must not already exist
        if input_name in cls.__annotations__:
            Console.Write(cls.namespace,"ERROR: Property \"{}\" already exists in {}. Aborting Method".format(input_name,type(cls).__name__))
            return
        #Property must have a type
        if "TYPE" not in input_attributes:
            Console.Write(cls.namespace,"ERROR: Property \"{}\" needs a type. Aborting Method".format(input_name))
            return
        #Type must also be specific to this function
        if input_attributes["TYPE"].upper() not in ["FLT","FLOAT"]:
            Console.Write(cls.namespace,"ERROR: Property \"{}\" is not of the correct type. Aborting Method".format(input_name))
            return

        #Fill out default parameters
        params: Dict[str,Any] = RefProperty.get_defaults("FLOAT")

        #Override with input if the type matches
        for params_index in params:
            if params_index in input_attributes:
                if type(params[params_index]) == type(input_attributes[params_index]):
                    params[params_index] = input_attributes[params_index]

        #Add the property
        cls.__annotations__.update(
            {
                input_name:bpy.props.FloatProperty(
                    name=params["TEXT"],
                    description=params["DESCRIPTION"],
                    default=params["DEFAULT"],
                    min=params["MIN"],
                    max=params["MAX"],
                    soft_min=params["SOFT_MIN"],
                    soft_max=params["SOFT_MAX"],
                    step=params["STEP"],
                    precision=params["PRECISION"],
                    options=params["OPTIONS"],
                    subtype=params["SUBTYPE"],
                    unit=params["UNIT"]
                )
            }
        )

        #Set event handling if enabled
        if params["EVENT_HANDLING"] is True:
            cls.set_event_handling(input_name,True)

        Console.Write(cls.namespace,"SUCCESS: Property \"{}\" has been created for {}.".format(input_name,type(cls).__name__))

    #Add property specific to type = FloatVector
    @classmethod
    def add_floatvector_property(cls,input_name: str,input_attributes: Dict[str,Any]) -> None:
        """
        adds a blender float vector property to the class annotations with the given input name

        PARAMETERS:
        -----------

        cls
            references the class itself because this function affects the class

        input_name : str
            This will be the name for the new blender float vector property

        input_attributes : Dict[str,Any]
            These will be the attributes given to the blender float vector property

        RETURNS:
        --------

        None
        """
        output_tags: Dict[str,int] = {
            "PropertyCollection":1,
            "add_floatvector_property":1
        }
        Console.Set_Tags(cls.namespace,output_tags)
        Console.Write(cls.namespace,"Adding float vector property \"{}\" to {} using attributes {}".format(input_name,type(cls).__name__,input_attributes))
        output_tags["PropertyCollection"] = 2
        output_tags["add_floatvector_property"] = 2
        Console.Set_Tags(cls.namespace,output_tags)

        #Property must have a name
        if input_name.strip() == "":
            Console.Write(cls.namespace,"ERROR: Property has no name. Aborting Method")
            return
        #Property must not already exist
        if input_name in cls.__annotations__:
            Console.Write(cls.namespace,"ERROR: Property \"{}\" already exists in {}. Aborting Method".format(input_name,type(cls).__name__))
            return
        #Property must have a type
        if "TYPE" not in input_attributes:
            Console.Write(cls.namespace,"ERROR: Property \"{}\" needs a type. Aborting Method".format(input_name))
            return
        #Type must also be specific to this function
        if input_attributes["TYPE"].upper() not in ["FLOATVECTOR"]:
            Console.Write(cls.namespace,"ERROR: Property \"{}\" is not of the correct type. Aborting Method".format(input_name))
            return

        #Fill out default parameters
        params: Dict[str,Any] = RefProperty.get_defaults("FLOATVECTOR")

        #Override with input if the type matches
        for params_index in params:
            if params_index in input_attributes:
                if type(params[params_index]) == type(input_attributes[params_index]):
                    params[params_index] = input_attributes[params_index]

        #Add the property
        cls.__annotations__.update(
            {
                input_name:bpy.props.FloatVectorProperty(
                    name=params["TEXT"],
                    description=params["DESCRIPTION"],
                    default=params["DEFAULT"],
                    min=params["MIN"],
                    max=params["MAX"],
                    soft_min=params["SOFT_MIN"],
                    soft_max=params["SOFT_MAX"],
                    step=params["STEP"],
                    precision=params["PRECISION"],
                    options=params["OPTIONS"],
                    subtype=params["SUBTYPE"],
                    unit=params["UNIT"],
                    size=params["SIZE"]
                )
            }
        )

        #Set event handling if enabled
        if params["EVENT_HANDLING"] is True:
            cls.set_event_handling(input_name,True)

        Console.Write(cls.namespace,"SUCCESS: Property \"{}\" has been created for {}.".format(input_name,type(cls).__name__))

    #Add property specific to type = Integer
    @classmethod
    def add_int_property(cls,input_name: str,input_attributes: Dict[str,Any]) -> None:
        """
        adds a blender integer property to the class annotations with the given input name

        PARAMETERS:
        -----------

        cls
            references the class itself because this function affects the class

        input_name : str
            This will be the name for the new blender integer property

        input_attributes : Dict[str,Any]
            These will be the attributes given to the blender integer property

        RETURNS:
        --------

        None
        """
        output_tags: Dict[str,int] = {
            "PropertyCollection":1,
            "add_int_property":1
        }
        Console.Set_Tags(cls.namespace,output_tags)
        Console.Write(cls.namespace,"Adding integer property \"{}\" to {} using attributes {}".format(input_name,type(cls).__name__,input_attributes))
        output_tags["PropertyCollection"] = 2
        output_tags["add_int_property"] = 2
        Console.Set_Tags(cls.namespace,output_tags)

        #Property must have a name
        if input_name.strip() == "":
            Console.Write(cls.namespace,"ERROR: Property has no name. Aborting Method")
            return
        #Property must not already exist
        if input_name in cls.__annotations__:
            Console.Write(cls.namespace,"ERROR: Property \"{}\" already exists in {}. Aborting Method".format(input_name,type(cls).__name__))
            return
        #Property must have a type
        if "TYPE" not in input_attributes:
            Console.Write(cls.namespace,"ERROR: Property \"{}\" needs a type. Aborting Method".format(input_name))
            return
        #Type must also be specific to this function
        if input_attributes["TYPE"].upper() not in ["INT","INTEGER"]:
            Console.Write(cls.namespace,"ERROR: Property \"{}\" is not of the correct type. Aborting Method".format(input_name))
            return

        #Fill out default parameters
        params: Dict[str,Any] = RefProperty.get_defaults("INT")

        #Override with input if the type matches
        for params_index in params:
            if params_index in input_attributes:
                if type(params[params_index]) == type(input_attributes[params_index]):
                    params[params_index] = input_attributes[params_index]

        #Add the property
        cls.__annotations__.update(
            {
                input_name:bpy.props.IntProperty(
                    name=params["TEXT"],
                    description=params["DESCRIPTION"],
                    default=params["DEFAULT"],
                    min=params["MIN"],
                    max=params["MAX"],
                    soft_min=params["SOFT_MIN"],
                    soft_max=params["SOFT_MAX"],
                    step=params["STEP"],
                    options=params["OPTIONS"],
                    subtype=params["SUBTYPE"]
                )
            }
        )

        #Set event handling if enabled
        if params["EVENT_HANDLING"] is True:
            cls.set_event_handling(input_name,True)

        Console.Write(cls.namespace,"SUCCESS: Property \"{}\" has been created for {}.".format(input_name,type(cls).__name__))

    #Add property specific to type = IntVector
    @classmethod
    def add_intvector_property(cls,input_name: str,input_attributes: Dict[str,Any]) -> None:
        """
        adds a blender integer vector property to the class annotations with the given input name

        PARAMETERS:
        -----------

        cls
            references the class itself because this function affects the class

        input_name : str
            This will be the name for the new blender integer vector property

        input_attributes : Dict[str,Any]
            These will be the attributes given to the blender integer vector property

        RETURNS:
        --------

        None
        """
        output_tags: Dict[str,int] = {
            "PropertyCollection":1,
            "add_intvector_property":1
        }
        Console.Set_Tags(cls.namespace,output_tags)
        Console.Write(cls.namespace,"Adding integer vector property \"{}\" to {} using attributes {}".format(input_name,type(cls).__name__,input_attributes))
        output_tags["PropertyCollection"] = 2
        output_tags["add_intvector_property"] = 2
        Console.Set_Tags(cls.namespace,output_tags)

        #Property must have a name
        if input_name.strip() == "":
            Console.Write(cls.namespace,"ERROR: Property has no name. Aborting Method")
            return
        #Property must not already exist
        if input_name in cls.__annotations__:
            Console.Write(cls.namespace,"ERROR: Property \"{}\" already exists in {}. Aborting Method".format(input_name,type(cls).__name__))
            return
        #Property must have a type
        if "TYPE" not in input_attributes:
            Console.Write(cls.namespace,"ERROR: Property \"{}\" needs a type. Aborting Method".format(input_name))
            return
        #Type must also be specific to this function
        if input_attributes["TYPE"].upper() not in ["INTVECTOR"]:
            Console.Write(cls.namespace,"ERROR: Property \"{}\" is not of the correct type. Aborting Method".format(input_name))
            return

        #Fill out default parameters
        params: Dict[str,Any] = RefProperty.get_defaults("INTVECTOR")

        #Override with input if the type matches
        for params_index in params:
            if params_index in input_attributes:
                if type(params[params_index]) == type(input_attributes[params_index]):
                    params[params_index] = input_attributes[params_index]

        #Add the property
        cls.__annotations__.update(
            {
                input_name:bpy.props.IntVectorProperty(
                    name=params["TEXT"],
                    description=params["DESCRIPTION"],
                    default=params["DEFAULT"],
                    min=params["MIN"],
                    max=params["MAX"],
                    soft_min=params["SOFT_MIN"],
                    soft_max=params["SOFT_MAX"],
                    step=params["STEP"],
                    options=params["OPTIONS"],
                    subtype=params["SUBTYPE"],
                    size=params["SIZE"]
                )
            }
        )

        #Set event handling if enabled
        if params["EVENT_HANDLING"] is True:
            cls.set_event_handling(input_name,True)

        Console.Write(cls.namespace,"SUCCESS: Property \"{}\" has been created for {}.".format(input_name,type(cls).__name__))

    #Add property specific to type = String
    @classmethod
    def add_string_property(cls,input_name: str,input_attributes: Dict[str,Any]) -> None:
        """
        adds a blender string property to the class annotations with the given input name

        PARAMETERS:
        -----------

        cls
            references the class itself because this function affects the class

        input_name : str
            This will be the name for the new blender string property

        input_attributes : Dict[str,Any]
            These will be the attributes given to the blender string property

        RETURNS:
        --------

        None
        """
        output_tags: Dict[str,int] = {
            "PropertyCollection":1,
            "add_string_property":1
        }
        Console.Set_Tags(cls.namespace,output_tags)
        Console.Write(cls.namespace,"Adding string property \"{}\" to {} using attributes {}".format(input_name,type(cls).__name__,input_attributes))
        output_tags["PropertyCollection"] = 2
        output_tags["add_string_property"] = 2
        Console.Set_Tags(cls.namespace,output_tags)

        #Property must have a name
        if input_name.strip() == "":
            Console.Write(cls.namespace,"ERROR: Property has no name. Aborting Method")
            return
        #Property must not already exist
        if input_name in cls.__annotations__:
            Console.Write(cls.namespace,"ERROR: Property \"{}\" already exists in {}. Aborting Method".format(input_name,type(cls).__name__))
            return
        #Property must have a type
        if "TYPE" not in input_attributes:
            Console.Write(cls.namespace,"ERROR: Property \"{}\" needs a type. Aborting Method".format(input_name))
            return
        #Type must also be specific to this function
        if input_attributes["TYPE"].upper() not in ["STRING","STR"]:
            Console.Write(cls.namespace,"ERROR: Property \"{}\" is not of the correct type. Aborting Method".format(input_name))
            return

        #Fill out default parameters
        params: Dict[str,Any] = RefProperty.get_defaults("STRING")

        #Override with input if the type matches
        for params_index in params:
            if params_index in input_attributes:
                if type(params[params_index]) == type(input_attributes[params_index]):
                    params[params_index] = input_attributes[params_index]

        #Add the property
        cls.__annotations__.update(
            {
                input_name:bpy.props.StringProperty(
                    name=params["TEXT"],
                    description=params["DESCRIPTION"],
                    default=params["DEFAULT"],
                    maxlen=params["MAX_LEN"],
                    options=params["OPTIONS"],
                    subtype=params["SUBTYPE"]
                )
            }
        )

        #Set event handling if enabled
        if params["EVENT_HANDLING"] is True:
            cls.set_event_handling(input_name,True)

        Console.Write(cls.namespace,"SUCCESS: Property \"{}\" has been created for {}.".format(input_name,type(cls).__name__))
