"""================================================================================================
This module is designed to represent a column element and its content in code.

CLASSES:
    Column
================================================================================================"""
from typing import List, Dict, Any # pylint: disable=unused-import
import uuid
from .content import Content
#==================================================#
#RAD GUI Column Object
#==================================================#

class Column():
    """

    ATTRIBUTES:
    -----------

    _defaults : Dict[str, Any]
            default values of the parameters given to a column.
            Meant to be a read only value.

    align : bool
        Align buttons to each other

    heading : str
        Heading, Label to insert into the layout for this sub-layout

    heading_ctxt : str
        Override automatic translation context of the given heading

    translate : bool
        Translate the given heading, when UI translation is enabled

    _collection : Content
        Elements within the row will be contained here

    namespace : str
        Getter: Represents the project's unique identifier.
        Setter: Updates the namespace and updates namespace of contents.

    value : Dict[str,Any]
        Getter: Represents the column as a Dictionary object
        Setter: Configures the column object

    METHODS:
    --------

        __init__ : None
        to_code : str
    """
    def __init__(self):
        #Set defaults
        self._defaults: Dict[str,Any] = {
            "ALIGN":False,
            "HEADING":"",
            "CONTEXT":"",
            "TRANSLATE":True
        }

        self.align = self._defaults["ALIGN"]
        self.heading = self._defaults["HEADING"]
        self.heading_ctxt = self._defaults["CONTEXT"]
        self.translate = self._defaults["TRANSLATE"]

        #Placeholder for other objects referenced by this object
        self._collection: Content = Content()
        self._namespace: str = ""
        self._var_id = "COLUMN_VAR_{}".format(uuid.uuid4().hex.upper())

    @property
    def namespace(self) -> str:
        """
        GETTER: gets the namespace of the column object

        PARAMETERS:
        -----------

            self
                references the current instance of the column class

        RETURNS:
        --------

            self._namespace : str
                holding the current value of the project identifier
        """
        return self._namespace

    @namespace.setter
    def namespace(self,input_value: str) -> None:
        """
        SETTER: Assigns the project identifier to itself and its contents

        PARAMETERS:
        -----------

            self
                references the current instance of the column class

            input_value
                This is the project identifier to assign to the object

        RETURNS:
        --------

            None
        """
        self._namespace = input_value
        self._collection.namespace = self._namespace

    @property
    def value(self) -> Dict[str,Any]:
        """
        GETTER: Represent the column as a Dictionary Object

        PARAMETERS:
        -----------

            self
                References the current instance of the column class

        RETURNS:
        --------

            result : Dict[str,Any]
                This dictionary represents the column and its properties
        """
        result: Dict[str,Any] = {
            "TYPE":"COLUMN"
        }

        if self.align != self._defaults["ALIGN"]:
            result["ALIGN"] = self.align

        if self.heading != self._defaults["HEADING"]:
            result["HEADING"] = self.heading

        if self.heading_ctxt != self._defaults["CONTEXT"]:
            result["CONTEXT"] = self.heading_ctxt

        if self.translate != self._defaults["TRANSLATE"]:
            result["TRANSLATE"] = self.translate

        if self._collection.length() != 0:
            result["CONTENT"] = self._collection.value

        return result

    @value.setter
    def value(self, input_attributes: Dict[str,Any]) -> None:
        """
        SETTER: Configures the column object from a Dictionary object

        PARAMETERS:
        -----------

            self
                References the current instance of the column class

            input_attributes : Dict[str, Any]
                Dictionary object holding the attributes to assign to the column object

        RETURNS:
        --------

            None
        """
        #We only assign values if the dict is a Column Type
        if "TYPE" not in input_attributes:
            return

        if "{}".format(input_attributes["TYPE"]).upper() != "COLUMN":
            return

        #Now that we are in the clear, start with the defaults
        self.align = self._defaults["ALIGN"]
        self.heading = self._defaults["HEADING"]
        self.heading_ctxt = self._defaults["CONTEXT"]
        self.translate = self._defaults["TRANSLATE"]
        self._collection.value = []

        #Then, let's go with the custom attributes
        if "ALIGN" in input_attributes:
            self.align = input_attributes["ALIGN"]

        if "HEADING" in input_attributes:
            self.heading = input_attributes["HEADING"]

        if "CONTEXT" in input_attributes:
            self.heading_ctxt = input_attributes["CONTEXT"]

        if "TRANSLATE" in input_attributes:
            self.translate = input_attributes["TRANSLATE"]

        if "CONTENT" in input_attributes:
            self._collection.value = input_attributes["CONTENT"]

    def to_code(self,called_by: str = "layout") -> str:
        """
        Represents the column and its contents as it gets called in code

        PARAMETERS:
        -----------

            self
                References the current instance of the column class

            called_by : str
                What's calling to draw this column object?

        RETURNS:
        --------

            result : str
                This is the column and its content as if it were written in a draw method
        """
        result: str = ""
        assign_prefix: str = ""
        content_code: str = ""
        code_call: str = "{}.column(align={}, heading='{}', heading_ctxt='{}', translate={})".format(
            called_by,
            self.align,
            self.heading,
            self.heading_ctxt,
            self.translate
        )

        #If we have content, we generate it with this statement
        if self._collection is not None:
            assign_prefix = "{} = ".format(self._var_id)
            content_code = "\n" + self._collection.to_code(self._var_id)

        result = assign_prefix + code_call + code_call + content_code

        return result
