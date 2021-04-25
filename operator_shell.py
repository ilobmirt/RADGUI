"""================================================================================================
This module and the classes within represent the Blender Python Operator used in a standard
project.

CLASSES:
    OperatorShellMeta
    OperatorShell
================================================================================================"""
from typing import Dict, List, Any
import typing
import bpy
from property_collection import PropertyCollection
from Console import Console
from EventManager import EventManager
from reference.operator import RefOperator
from engine.engine import Engine

#==================================================#
#Operator Shell Meta Class
#==================================================#
class OperatorShellMeta(type):
    """...
    """
    @property
    def value(cls) -> Dict[str,Any]:
        """...
        """
        output_tags: Dict[str,int] = {
            "OperatorShell":1,
            "get_value":1
        }
        Console.Set_Tags(cls._namespace,output_tags)
        Console.Write(cls._namespace,"Getting Dictionary value of \"{}\" Operator".format(cls._project_id))
        output_tags["OperatorShell"] = 2
        output_tags["get_value"] = 2
        Console.Set_Tags(cls._namespace,output_tags)

        result: Dict[str,Any] = {}
        return result

    @value.setter
    def value(cls,input_attributes: Dict[str,Any]) -> None:
        """...
        """
        output_tags: Dict[str,int] = {
            "OperatorShell":1,
            "set_value":1
        }
        Console.Set_Tags(cls._namespace,output_tags)
        Console.Write(cls._namespace,"Setting Dictionary value of Operator using attributes - {}".format(input_attributes))
        output_tags["OperatorShell"] = 2
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

        operator_defaults: Dict[str,Any] = RefOperator.get_defaults()

        #BL_IDNAME - "namespace.project_id"
        cls.bl_idname = "{}.{}".format(cls._namespace,cls._project_id).lower()

        #BL_DESCRIPTION
        if "DESCRIPTION" in input_attributes[cls._project_id]:
            cls.bl_description = input_attributes[cls._project_id]["DESCRIPTION"]
        else:
            cls.bl_description = operator_defaults["DESCRIPTION"]

        #BL_LABEL
        if "LABEL" in input_attributes[cls._project_id]:
            cls.bl_label = input_attributes[cls._project_id]["LABEL"]
        else:
            cls.bl_label = operator_defaults["LABEL"]

        #BL_OPTIONS
        if "OPTIONS" in input_attributes[cls._project_id]:
            if input_attributes[cls._project_id]["OPTIONS"] in RefOperator.get_options():
                cls.bl_options = input_attributes[cls._project_id]["OPTIONS"]
            else:
                Console.Write(cls._namespace,"WARNING: Option \"{}\" is not a valid option. Using default value \"{}\"".format(input_attributes[cls._project_id]["OPTIONS"],operator_defaults["OPTIONS"]))
                cls.bl_options = operator_defaults["OPTIONS"]
        else:
            cls.bl_options = operator_defaults["OPTIONS"]

        #BL_TRANSLATION_CONTEXT
        if "TRANSLATION_CONTEXT" in input_attributes[cls._project_id]:
            cls.bl_translation_context = input_attributes[cls._project_id]["TRANSLATION_CONTEXT"]
        else:
            cls.bl_translation_context = operator_defaults["TRANSLATION_CONTEXT"]

        #BL_UNDO_GROUP
        if "UNDO_GROUP" in input_attributes[cls._project_id]:
            cls.bl_undo_group = input_attributes[cls._project_id]["UNDO_GROUP"]
        else:
            cls.bl_undo_group = operator_defaults["UNDO_GROUP"]

    @property
    def namespace(cls) -> str:
        """...
        """
        return cls._namespace

    @namespace.setter
    def namespace(cls, input_value: str) -> None:
        """...
        """
        cls._namespace = input_value
        cls._Content.namespace = input_value


#==================================================#
#Operator Shell Class
#==================================================#
class OperatorShell(bpy.types.Operator, PropertyCollection, metaclass=OperatorShellMeta):
    """...
    """
    _namespace: str = ""
    _Content: Engine = Engine()
    _project_id: str = ""
    EventID: bpy.props.StringProperty(name="event_id")

    def execute(self, context : 'Context') -> typing.Union[typing.Set[int], typing.Set[str]]:
        """...
        """
        output_tags: Dict[str,int] = {
            "OperatorShell":1,
            "execute":1
        }
        Console.Set_Tags(self._namespace,output_tags)
        Console.Write(self._namespace,"Button "+str(self.__class__)+" Pressed!")

        if self.EventID != "":

            generated_event : Dict[str, Any] = {
                "EVENT_ID":self.EventID,
                "OBJECT_TYPE":"BUTTON",
                "CONTEXT":context,
                "EVENT_TYPE":"BUTTON_PRESSED"
            }

            EventManager.HandleEvent(self._namespace,generated_event)

        return {'FINISHED'}

    def invoke(self, context, event):
        """...
        """
        return self.execute(context)

    def draw(self, context: 'Context'):
        """...
        """
        layout = self.layout
        col = layout.column()
        col.label(text="Property Dialog:")
        
        for index in self.__annotations__:
            col.prop(self, index)
            col.row()
