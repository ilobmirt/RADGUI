"""================================================================================================
This module is designed to generate the functions used in blender's draw method rather than
interpret a whole list of code each time the contents are to be redrawn as was done in previous
versions of the engine class.

CLASSES:
    Engine
================================================================================================"""
from typing import List, Dict, Any
from .content import Content

#==================================================#
#RAD GUI Engine Object
#==================================================#
class Engine():
    """
    This class is to take structured content and uses it to generate methods
    for drawing the structured content.

    ATTRIBUTES:
    -----------

        _collection : Content
            ########

        _namespace : str
            ########

        value : List[Dict[str,Any]]
            ########

        namespace : str
            ########

    METHODS:
    --------

        __init__ : None
        indent :str
        generate : function
    """
    def __init__(self):
        self._collection: Content = Content()
        self._namespace: str = ""

    @staticmethod
    def indent(input_string:str,num_levels:int =1) -> str:
        """
        Increases or Decreases indentation of given text by a certain amount

        PARAMETERS:
        -----------

            input_string : str
                The given string to indent or unindent

            num_levels : int
                The direction and magnitude of our indentation

        RETURNS:
        --------

            result : str
                The given string indented in a positive or negative direction
        """
        result:str = ""
        body_string:str = ""
        tab_positive:str = ""
        tab_negative:str = ""

        if num_levels > 0:
            tab_positive = "".zfill(num_levels).replace("0","\t")
        elif num_levels < 0:
            tab_negative = "".zfill(abs(num_levels)).replace("0","\t")
        else:
            return input_string

        body_string = input_string.replace("\n{}".format(tab_negative),"\n{}".format(tab_positive))
        body_string = body_string.replace(tab_negative,"",1)
        result = tab_positive + "{}".format(body_string)

        return result

    def generate(self):
        """
        Creates a function to be used for Blender's Draw statements

        PARAMETERS:
        -----------

            self
                References the current instance of the Engine class

        RETURNS:
        --------

            result["gen_draw"]
                This is a generated draw method filled with the objects given to it
        """
        compiled_code = None
        result: Dict[str,Any] = {}
        body_string: str = self._collection.to_code()

        function_string = "def gen_draw(self, context):\n\tlayout = self.layout\n{}"
        compiled_code = compile(function_string.format(self.indent(body_string)),"<string>","exec")
        exec(compiled_code,result)

        return result["gen_draw"]

    @property
    def value(self) -> List[Dict[str,Any]]:
        """
        GETTER: Returns a structure representing what gets rendered

        PARAMETERS:
        -----------

            self
                References the current instance of the Engine class

        RETURNS:
        --------

            result : List[Dict[str,Any]]
                This list is a collection of objects and their properties
                to be rendered in the draw function
        """
        return self._collection.value

    @value.setter
    def value(self, input_list: List[Dict[str,Any]]):
        """
        SETTER: generates code and representative objects given a structure

        PARAMETERS:
        -----------

            self
                References the current instance of the Engine class

            input_attributes : List[Dict[str,Any]]
                Given list of objects and their properties to be
                rendered in the draw function

        RETURNS:
        --------

            None
        """
        self._collection.value = input_list

    @property
    def namespace(self) -> str:
        """
        GETTER: gets the namespace of the Engine object

        PARAMETERS:
        -----------

            self
                references the current instance of the Engine class

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
                references the current instance of the Engine class

            input_value
                This is the project identifier to assign to the object

        RETURNS:
        --------

            None
        """
        self._namespace = input_value
        self._collection.namespace = input_value
