"""================================================================================================
This module and the classes within represent the Blender Python Panel used in a standard project.

The project module will call upon this module to create a custom class based off of PanelShell.
The project module will then pass Namespace and Dict information to this new class.

CLASSES:
    PanelShellMeta
    PanelShell

================================================================================================"""
from typing import List, Dict, Any
import bpy
from reference.panel import RefPanel
from engine.engine import Engine
from Console import Console


class PanelShellMeta(type):
    """
    A metaclass to allow for getters and setters to work on a class level rather than an instance level

    ATTRIBUTES:
    -----------

    value : Dict[str,Any]
        Represents the Panel through a dictionary object. Used in loading or saving to RADGUI projects.

    namespace : str
        Represents the uniqe project identifier this panel is to exist in. All items in a RADGUI
        project will share this namespace.
    """
    #Convert Panel into a Dictionary
    @property
    def value(cls) -> Dict[str,Any]:
        """
        Class Getter for PanelShell.value. Collects the properties of the class and represents itself as
        a dictionary oject.

            PARAMETERS:
            -----------

            cls : PanelShellMeta
                Implicitly refrences to the class

            RETURNS:
            --------

            result : Dict[str,Any]
                A dictionary object of one key representing bl_idname. Inside that single key is a
                dictionary that represents the properties found in a panel object.

        """
        output_tags: Dict[str,int] = {
            "PanelShell":1,
            "get_value":1
        }
        Console.Set_Tags(cls._namespace,output_tags)
        Console.Write(cls._namespace,"Getting Dictionary value of \"{}\" Panel".format(cls._project_id))
        output_tags["PanelShell"] = 2
        output_tags["get_value"] = 2
        Console.Set_Tags(cls._namespace,output_tags)

        #Start with basic structure of Panel
        #Blender IDs will make use of the generated namespaces to keep unique
        #bl_idname = "OBJECT_PT_" + "radgui_project_***(GENERATED HEX UUID)*********_" + "IDNAME"
        #ProjectID: str = cls.bl_idname.split("_")[-1]
        owner_id: str = cls.bl_owner_id.split("_")[-1]
        parent_id: str = cls.bl_parent_id.split("_")[-1]

        result: Dict[str,Dict[str,Any]] = {}
        panel_defaults: Dict[str,Any] = RefPanel.get_defaults()

        #Fill our current status with properties of our panel
        current_stats: Dict[str,Any] = {
            "CATEGORY":cls.bl_category,
            "CONTEXT":cls.bl_context,
            "LABEL":cls.bl_label,
            "OPTIONS":cls.bl_options,
            "ORDER":cls.bl_order,
            "OWNER_ID":owner_id,
            "PARENT_ID":parent_id,
            "REGION":cls.bl_region_type,
            "SPACE": cls.bl_space_type,
            "TRANSLATION_CONTEXT":cls.bl_translation_context,
            "POPUP_PANEL_WIDTH":cls.bl_ui_units_x,
            "TEXT":cls.text,
            "USE_PIN":cls.use_pin
        }

        #Now build on the differences
        for current_attribute in panel_defaults:
            if current_stats[current_attribute] != panel_defaults[current_attribute]:
                result[cls._project_id][current_attribute] = current_stats[current_attribute]

        #And now add contents
        result[cls._project_id]["CONTENT"] = cls._content.value

        Console.Write(cls._namespace,"SUCCESS: Panel \"{}\" as a dictionary value of {}".format(cls._project_id,result))
        return result

    #Configure this object using a dictionary
    @value.setter
    def value(cls, input_attributes: Dict[str,Any]) -> None:
        """
        Class Setter for PanelShell.value. Takes a dictionary object and configures the class from it.

            PARAMETERS:
            -----------

            cls : PanelShellMeta
                Implicitly refrences to the class

            input_attributes: Dict[str,Any]
                This is the dictionary object given to configure the panel object

            RETURNS:
            --------

            None
        """
        output_tags: Dict[str,int] = {
            "PanelShell":1,
            "set_value":1
        }
        Console.Set_Tags(cls._namespace,output_tags)
        Console.Write(cls._namespace,"Setting Dictionary value of Panel using attributes - {}".format(input_attributes))
        output_tags["PanelShell"] = 2
        output_tags["set_value"] = 2
        Console.Set_Tags(cls._namespace,output_tags)

        #input_attributes should only have one key representing bl_idname
        attribute_keys: List[str] = list(input_attributes.keys())
        if len(attribute_keys) > 0:
            Console.Write(cls._namespace,"ERROR: Input Attributes should only represent one object. Aborting Method")
            return

        temp_id:str = attribute_keys[0]
        if (temp_id.strip() == "") or (temp_id.isalnum is False) or (temp_id[0].isalpha is False):
            Console.Write(cls._namespace,"ERROR: Bad bl_idname given in Input Attributes. Aborting Method")
            return
        else:
            cls._project_id = temp_id

        panel_defaults: Dict[str,Any] = RefPanel.get_defaults()

        #ID_NAME
        cls.bl_idname = "OBJECT_PT_{}_{}".format(cls._namespace.upper(),cls._project_id)

        #CATEGORY
        if "CATEGORY" in input_attributes[cls._project_id]:
            cls.bl_category = input_attributes[cls._project_id]["CATEGORY"]
        else:
            cls.bl_category = panel_defaults["CATEGORY"]

        #CONTEXT
        if "CONTEXT" in input_attributes[cls._project_id]:
            cls.bl_context = input_attributes[cls._project_id]["CONTEXT"]
        else:
            cls.bl_context = panel_defaults["CONTEXT"]

        #LABEL
        if "LABEL" in input_attributes[cls._project_id]:
            cls.bl_label = input_attributes[cls._project_id]["LABEL"]
        else:
            cls.bl_label = panel_defaults["LABEL"]

        #OPTIONS
        if "OPTIONS" in input_attributes[cls._project_id]:
            if input_attributes[cls._project_id]["OPTIONS"] in RefPanel.get_options():
                cls.bl_options = input_attributes[cls._project_id]["OPTIONS"]
            else:
                Console.Write(cls._namespace,"WARNING: Option \"{}\" is not a valid option. Using default value \"{}\"".format(input_attributes[cls._project_id]["OPTIONS"],panel_defaults["OPTIONS"]))
                cls.bl_options = panel_defaults["OPTIONS"]
        else:
            cls.bl_options = panel_defaults["OPTIONS"]

        #ORDER
        if "ORDER" in input_attributes[cls._project_id]:
            cls.bl_order = input_attributes[cls._project_id]["ORDER"]
        else:
            cls.bl_order = panel_defaults["ORDER"]

        #OWNER_ID
        if "OWNER_ID" in input_attributes[cls._project_id]:
            cls.bl_owner_id = "OBJECT_PT_{}_{}".format(cls._namespace.upper(),input_attributes[cls._project_id]["OWNER_ID"])
        else:
            cls.bl_owner_id = panel_defaults["OWNER_ID"]

        #PARENT_ID
        if "PARENT_ID" in input_attributes[cls._project_id]:
            cls.bl_parent_id = "OBJECT_PT_{}_{}".format(cls._namespace.upper(),input_attributes[cls._project_id]["PARENT_ID"])
        else:
            cls.bl_parent_id = panel_defaults["PARENT_ID"]

        #REGION
        if "REGION" in input_attributes[cls._project_id]:
            if input_attributes[cls._project_id]["REGION"] in RefPanel.get_regions():
                cls.bl_region_type = input_attributes[cls._project_id]["REGION"]
            else:
                Console.Write(cls._namespace,"WARNING: Region \"{}\" is not a valid region. Using default value \"{}\"".format(input_attributes[cls._project_id]["REGION"],panel_defaults["REGION"]))
                cls.bl_region_type = panel_defaults["REGION"]
        else:
            cls.bl_region_type = panel_defaults["REGION"]

        #SPACE
        if "SPACE" in input_attributes[cls._project_id]:
            if input_attributes[cls._project_id]["SPACE"] in RefPanel.get_spaces():
                cls.bl_space_type = input_attributes[cls._project_id]["SPACE"]
            else:
                Console.Write(cls._namespace,"WARNING: Space Type \"{}\" is not a valid space type. Using default value \"{}\"".format(input_attributes[cls._project_id]["SPACE"],panel_defaults["SPACE"]))
                cls.bl_space_type = panel_defaults["SPACE"]
        else:
            cls.bl_space_type = panel_defaults["SPACE"]

        #TRANSLATION_CONTEXT
        if "TRANSLATION_CONTEXT" in input_attributes[cls._project_id]:
            cls.bl_translation_context = input_attributes[cls._project_id]["TRANSLATION_CONTEXT"]
        else:
            cls.bl_translation_context = panel_defaults["TRANSLATION_CONTEXT"]

        #POPUP_PANEL_WIDTH
        if "POPUP_PANEL_WIDTH" in input_attributes[cls._project_id]:
            cls.bl_ui_units_x = input_attributes[cls._project_id]["POPUP_PANEL_WIDTH"]
        else:
            cls.bl_ui_units_x = panel_defaults["POPUP_PANEL_WIDTH"]

        #TEXT
        if "TEXT" in input_attributes[cls._project_id]:
            cls.text = input_attributes[cls._project_id]["TEXT"]
        else:
            cls.text = panel_defaults["TEXT"]

        #USE_PIN
        if "USE_PIN" in input_attributes[cls._project_id]:
            cls.use_pin = input_attributes[cls._project_id]["USE_PIN"]
        else:
            cls.use_pin = panel_defaults["USE_PIN"]

        #CONTENT
        if "CONTENT" in input_attributes[cls._project_id]:
            cls._content.value = input_attributes[cls._project_id]["CONTENT"]
        else:
            cls._content.value = []

        #Update Draw Method
        cls.draw = cls._content.Generate()

    #Obtain the namespace through the class getter
    @property
    def namespace(cls) -> str:
        """
        Class Getter for PanelShell.namespace. Indirect reference to the
        Panel's namespace in the RADGUI project.

            PARAMETERS:
            -----------

            cls : PanelShellMeta
                Implicitly refrences to the class

            RETURNS:
            --------

            cls._namespace : str
                Private variable for the Panel's namespace.
        """
        return cls._namespace

    #Set the namespace for the class and its contents through the setter
    @namespace.setter
    def namespace(cls, input_value: str) -> None:
        """
        Class Setter for PanelShell.namespace. When set, also propagates namespace to cls._content

            PARAMETERS:
            -----------

            cls : PanelShellMeta
                Implicitly refrences to the class

            input_value : str
                Contains the namespace to assign to panel and its contents.

            RETURNS:
            --------

            None
        """
        cls._namespace = input_value
        cls._content.namespace = input_value


class PanelShell(bpy.types.Panel , metaclass=PanelShellMeta):
    """
    Represents a Panel class used in a Blender Project.

    ATTRIBUTES:
    -----------

    _namespace : str
        Private variable for the Panel's namespace. Use the getter/setter "namespace" instead.

    _project_id : str
        Private variable of the Panel's ID brought in from the RADGUI project dictionary.
        Used in bl_idname.

    _content : Engine
        Private instance of the RADGUI Engine class. This will hold an abstract of the objects to render
        and on command creates the code that will update our draw method.

    METHODS:
    --------

    draw : None

    """
    _namespace: str = ""
    _project_id: str = ""
    _content: Engine = Engine()

    #Occurs whenever the panel gets drawn
    def draw(self, context: 'Context') -> None:
        pass
