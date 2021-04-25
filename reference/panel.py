"""================================================================================================
This module is used as a reference for the rest of RADGUI in the deployment of Panels.

CLASSES:
    RefPanel
================================================================================================"""
from typing import List, Dict, Any
#==================================================#
#Panel Reference Class
#==================================================#

class RefPanel():
    """
    This class holds all relevant information for Properties and PropertyGroup objects

    ATTRIBUTES:
    -----------
        _options : List[str]
            List of available options for a panel
            This is meant to be a read-only resource.

        _region_types : List[str]
            List of regions available for a panel
            This is meant to be a read-only resource.

        _space_types : List[str]
            List of spaces available for a panel
            This is meant to be a read-only resource.

        _defaults : Dict[str,Dict[str,Any]]
            This dictionary holds the default values for each panel
            This is meant to be a read-only resource.

    METHODS:
    --------
        get_defaults : Dict[str,Any]
        get_spaces : List[str]
        get_regions : List[str]
        get_options : List[str]
    """
    _options: List[str] = [
        "DEFAULT_CLOSED",
        "HIDE_HEADER",
        "INSTANCED",
        "HEADER_LAYOUT_EXPAND",
        "DRAW_BOX"
    ]
    _region_types: List[str] = [
        "WINDOW",
        "HEADER",
        "CHANNELS",
        "TEMPORARY",
        "UI",
        "TOOLS",
        "TOOL_PROPS",
        "PREVIEW",
        "HUD",
        "NAVIGATION_BAR",
        "EXECUTE",
        "FOOTER",
        "TOOL_HEADER"
    ]
    _space_types: List[str] = [
        "EMPTY",
        "VIEW_3D",
        "IMAGE_EDITOR",
        "NODE_EDITOR",
        "SEQUENCE_EDITOR",
        "CLIP_EDITOR",
        "DOPESEET_EDITOR",
        "GRAPH_EDITOR",
        "NLA_EDITOR",
        "TEXT_EDITOR",
        "CONSOLE",
        "INFO",
        "TOPBAR",
        "STATUSBAR",
        "OUTLINER",
        "PROPERTIES",
        "FILE_BROWSER",
        "PREFERENCES"
    ]
    _defaults: Dict[str,Any] = {
        "CATEGORY":"",
        "CONTEXT":"",
        "LABEL":"",
        "OPTIONS":"DEFAULT_CLOSED",
        "ORDER":0,
        "OWNER_ID":"",
        "PARENT_ID":"",
        "REGION":"WINDOW",
        "SPACE": "EMPTY",
        "TRANSLATION_CONTEXT":"",
        "POPUP_PANEL_WIDTH":0,
        "TEXT":"",
        "USE_PIN":False
    }

    @classmethod
    def get_defaults(cls) -> Dict[str,Any]:
        """
        Gets the default attributes for a Panel

        PARAMETERS:
        -----------

        cls
            references the class itself

        RETURNS:
        --------

        cls._defaults : Dict[str,Any]
            This Dictionary holds the panel default attributes.
        """
        return cls._defaults

    @classmethod
    def get_spaces(cls) -> List[str]:
        """
        Gets the available spaces for a Panel

        PARAMETERS:
        -----------

        cls
            references the class itself

        RETURNS:
        --------

        cls._space_types : List[str]
            This List holds the available spaces.
        """
        return cls._space_types

    @classmethod
    def get_regions(cls) -> List[str]:
        """
        Gets the available regions for a Panel

        PARAMETERS:
        -----------

        cls
            references the class itself

        RETURNS:
        --------

        cls._region_types : List[str]
            This List holds the available regions.
        """
        return cls._region_types

    @classmethod
    def get_options(cls) -> List[str]:
        """
        Gets the available options for a Panel

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
