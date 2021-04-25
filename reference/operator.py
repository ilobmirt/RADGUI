"""================================================================================================
This module is used as a reference for the rest of RADGUI in the deployment of Operators.

CLASSES:
    Operator
================================================================================================"""
from typing import List, Dict, Any
#==================================================#
#Operator Reference Class
#==================================================#

class RefOperator():
    """
    This class holds all relevant information for Properties and PropertyGroup objects

    ATTRIBUTES:
    -----------
        _defaults : Dict[str,Any]
            This dictionary holds the default values for each Operator
            This is meant to be a read-only resource.

        _options : List[str]
            List of available options for an operator
            This is meant to be a read-only resource.

    METHODS:
    --------
        get_defaults : Dict[str,Any]
        get_options : List[str]
    """
    _defaults: Dict[str,Any] = {
        "DESCRIPTION":"",
        "LABEL":"",
        "OPTIONS":"REGISTER",
        "TRANSLATION_CONTEXT":"Operator",
        "UNDO_GROUP":""
    }

    _options: List[str] = [
        "REGISTER",
        "UNDO",
        "UNDO_GROUPED",
        "BLOCKING",
        "MACRO",
        "GRAB_CURSOR",
        "GRAB_CURSOR_X",
        "GRAB_CURSOR_Y",
        "PRESET",
        "INTERNAL"
    ]

    @classmethod
    def get_defaults(cls) -> Dict[str,Any]:
        """
        Gets the default attributes for an Operator

        PARAMETERS:
        -----------

        cls
            references the class itself

        RETURNS:
        --------

        cls._defaults : Dict[str,Any]
            This Dictionary holds the Operator default attributes.
        """
        return cls._defaults

    @classmethod
    def get_options(cls) -> List[str]:
        """
        Gets the available options for an Operator

        PARAMETERS:
        -----------

        cls
            references the class itself

        RETURNS:
        --------

        cls._options : List[str]
            This List holds the available options.
        """
        return cls._options
