"""================================================================================================
This module is designed to represent an operator element and its content in code.

CLASSES:
    Operator
================================================================================================"""
from typing import List, Dict, Any  # pylint: disable=unused-import
#==================================================#
#RAD GUI Operator Object
#==================================================#

class Operator():
    """
    This class holds all the properties of the Operator as it is to be rendered in Blender

    ATTRIBUTES:
    -----------

        _defaults : Dict[str, Any]
            default values of the parameters given to an operator.
            Meant to be a read only value.

        text : str
            Override automatic text of the item

        text_ctxt : str
            Override automatic translation context of the given text

        translate : bool
            Translate the given text, when UI translation is enabled

        icon : str
            Override automatic icon of the item

        icon_value : int
            Override automatic icon of the item

        emboss : bool
            Draw the button itself, not just the icon/text

        depress : bool
            Draw pressed in

        operator_id : str
            Identifier of the operator

        namespace : str
            Represents the project's unique identifier

        value : Dict[str, Any]
            Getter: Represents the Operator as a Dictionary object
            Setter: Configures the Operator object

    METHODS:
    --------

        __init__ : None
        to_code : str
    """
    def __init__(self):
        self._defaults: Dict[str,Any] = {
            "TEXT":"",
            "CONTEXT":"",
            "TRANSLATE":True,
            "ICON":"NONE",
            "ICON_VALUE":0,
            "EMBOSS":True,
            "DEPRESS":False,
            "ID":""
        }

        self.text = self._defaults["TEXT"]
        self.text_ctxt = self._defaults["CONTEXT"]
        self.translate = self._defaults["TRANSLATE"]
        self.icon = self._defaults["ICON"]
        self.icon_value = self._defaults["ICON_VALUE"]
        self.emboss = self._defaults["EMBOSS"]
        self.depress = self._defaults["DEPRESS"]
        self.operator_id = self._defaults["ID"]

        #To be set from Parent
        self.namespace: str = ""

    @property
    def value(self) -> Dict[str,Any]:
        """
        GETTER: Represent the Operator as a Dictionary Object

        PARAMETERS:
        -----------

            self
                References the current instance of the Operator class

        RETURNS:
        --------

            result : Dict[str,Any]
                This dictionary represents the Operator and its properties
        """
        result: Dict[str, Any] = {
            "TYPE":"OPERATOR"
        }

        if self.text != self._defaults["TEXT"]:
            result["TEXT"] = self.text

        if self.text_ctxt != self._defaults["CONTEXT"]:
            result["CONTEXT"] = self.text_ctxt

        if self.translate != self._defaults["TRANSLATE"]:
            result["TRANSLATE"] = self.translate

        if self.icon != self._defaults["ICON"]:
            result["ICON"] = self.icon

        if self.icon_value != self._defaults["ICON_VALUE"]:
            result["ICON_VALUE"] = self.icon_value

        if self.emboss != self._defaults["EMBOSS"]:
            result["EMBOSS"] = self.emboss

        if self.depress != self._defaults["DEPRESS"]:
            result["DEPRESS"] = self.depress

        if self.operator_id != self._defaults["ID"]:
            result["ID"] = self.operator_id

        return result

    @value.setter
    def value(self, input_attributes: Dict[str,Any]) -> None:
        """
        SETTER: Configures the Operator object from a Dictionary object

        PARAMETERS:
        -----------

            self
                References the current instance of the Operator class

            input_attributes : Dict[str, Any]
                Dictionary object holding the attributes to assign to the Operator object

        RETURNS:
        --------

            None
        """
        #We only assign values if the dict is a Button Type
        if "TYPE" not in input_attributes:
            return

        if "{}".format(input_attributes["TYPE"]).upper() != "OPERATOR":
            return

        #Now that we are in the clear, start with the defaults
        self.text = self._defaults["TEXT"]
        self.text_ctxt = self._defaults["CONTEXT"]
        self.translate = self._defaults["TRANSLATE"]
        self.icon = self._defaults["ICON"]
        self.icon_value = self._defaults["ICON_VALUE"]
        self.emboss = self._defaults["EMBOSS"]
        self.depress = self._defaults["DEPRESS"]
        self.operator_id = self._defaults["ID"]

        #Then, lets go with the custom attributes
        if "TEXT" in input_attributes:
            self.text = input_attributes["TEXT"]

        if "CONTEXT" in input_attributes:
            self.text_ctxt = input_attributes["CONTEXT"]

        if "TRANSLATE" in input_attributes:
            self.translate = input_attributes["TRANSLATE"]

        if "ICON" in input_attributes:
            self.icon = input_attributes["ICON"]

        if "ICON_VALUE" in input_attributes:
            self.icon_value = input_attributes["ICON_VALUE"]

        if "EMBOSS" in input_attributes:
            self.emboss = input_attributes["EMBOSS"]

        if "DEPRESS" in input_attributes:
            self.depress = input_attributes["DEPRESS"]

        if "ID" in input_attributes:
            self.operator_id = input_attributes["ID"]

    def to_code(self,called_by: str = "layout") -> str:
        """
        Represents the Operator as it gets called in code

        PARAMETERS:
        -----------

            self
                References the current instance of the Operator class

            called_by : str
                What's calling to draw this Operator object?

        RETURNS:
        --------

            result : str
                This is the Operator as if it were written in a draw method
        """
        result: str = "{}.operator('{}', text='{}', text_ctxt='{}', translate={}, icon='{}', emboss={}, depress={}, icon_value={})".format(
            called_by,
            "{}.{}".format(self.namespace,self.operator_id).lower(),
            self.text,
            self.text_ctxt,
            self.translate,
            self.icon,
            self.emboss,
            self.depress,
            self.icon_value
        )

        return result
