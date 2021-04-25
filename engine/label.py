"""================================================================================================
This module is designed to represent a Label element in code.

CLASSES:
    Label
================================================================================================"""
from typing import List, Dict, Any # pylint: disable=unused-import

#==================================================#
#RAD GUI Label Object
#==================================================#

class Label():
    """
    This class holds all the properties of the row as it is to be rendered in Blender

    ATTRIBUTES:
    -----------
        _defaults : Dict[str, Any]
            default values of the parameters given to a row.
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

        value : Dict[str,Any]
            Getter: Represents the row as a Dictionary object
            Setter: Configures the row object

    METHODS:
    --------

        __init__ : None
        to_code : str
    """
    def __init__(self):
        #Set defaults
        self._defaults: Dict[str,Any] = {
            "TEXT":"",
            "CONTEXT":"",
            "TRANSLATE":True,
            "ICON":"NONE",
            "ICON_VALUE":0
        }

        self.text = self._defaults["TEXT"]
        self.text_ctxt = self._defaults["CONTEXT"]
        self.translate = self._defaults["TRANSLATE"]
        self.icon = self._defaults["ICON"]
        self.icon_value = self._defaults["ICON_VALUE"]

    @property
    def value(self) -> Dict[str,Any]:
        """
        GETTER: Represent the label as a Dictionary Object

        PARAMETERS:
        -----------

            self
                References the current instance of the label class

        RETURNS:
        --------

            result : Dict[str,Any]
                This dictionary represents the label and its properties
        """
        result: Dict[str,Any] = {
            "TYPE":"LABEL"
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

        return result

    @value.setter
    def value(self,input_attributes: Dict[str,Any]) -> None:
        """
        SETTER: Configures the label object from a Dictionary object

        PARAMETERS:
        -----------

            self
                References the current instance of the label class

            input_attributes : Dict[str, Any]
                Dictionary object holding the attributes to assign to the label object

        RETURNS:
        --------

            None
        """
        #We only assign values if the dict is a Label Type
        if "TYPE" not in input_attributes:
            return

        if "{}".format(input_attributes["TYPE"]).upper() != "LABEL":
            return

        #Now that we are in the clear, start with the defaults
        self.text = self._defaults["TEXT"]
        self.text_ctxt = self._defaults["CONTEXT"]
        self.translate = self._defaults["TRANSLATE"]
        self.icon = self._defaults["ICON"]
        self.icon_value = self._defaults["ICON_VALUE"]

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

    def to_code(self,called_by: str = "layout") -> str:
        """
        Represents the label as it gets called in code

        PARAMETERS:
        -----------

            self
                References the current instance of the label class

            called_by : str
                What's calling to draw this label object?

        RETURNS:
        --------

            result : str
                This is the label as if it were written in a draw method
        """
        result: str = "{}.label(text='{}', text_ctxt='{}', translate={}, icon='{}', icon_value={})".format(
            called_by,
            self.text,
            self.text_ctxt,
            self.translate,
            self.icon,
            self.icon_value
            )

        return result
