"""================================================================================================
This module is used as a reference for the rest of RADGUI in the deployment of Properties and
PropertyGroups.

CLASSES:
    RefProperty

================================================================================================"""
from typing import List, Dict, Any
import sys
import bpy
#==================================================#
#Property Reference Class
#==================================================#

class RefProperty():
    """
    This class holds all relevant information for Properties and PropertyGroup objects

    ATTRIBUTES:
    -----------
        _scope : Dict[str,Any]
            A dictionary containing all known areas PropertyGroup objects can be a part of.
            This is meant to be a read-only resource.

        _units : Dict[str,List[str]]
            The keys represent the available types of unit for each property.
            The List is a list of all object types that can make use of that unit type.
            This is meant to be a read-only resource.

        _options : Dict[str,List[str]]
            The keys represent the available options for each property.
            The List is a list of all object types that can make use of that option.
            This is meant to be a read-only resource.

        _subtypes : Dict[str,List[str]]
            The keys represent the available subtypes for each property.
            the List is a list of all object types that can make use of that subtype.
            This is meant to be a read-only resource.

        _defaults : Dict[str,Dict[str,Any]]
            This dictionary holds the default values for each property type
            This is meant to be a read-only resource.

    METHODS:
    --------
        get_scopes : Dict[str,Any]
        get_units : List[str]
        get_options : List[str]
        get_subtypes : List[str]
        get_defaults : Dict[str,Any]
    """
    _scope: Dict[str,Any] = {
        #"ACTION":"Action",
        "ARMATURE":bpy.types.Armature,
        "BRUSH":bpy.types.Brush,
        #"CACHE_FILE":"CacheFile",
        "CAMERA":bpy.types.Camera,
        "COLLECTION":bpy.types.Collection,
        "CURVE":bpy.types.Curve,
        #"FREESTYLE_LINE_STYLE":"FreestyleLineStyle",
        #"GREASE_PENCIL":"GreasePencil",
        #"IMAGE":"Image",
        #"KEY":"Key",
        "LATTICE":bpy.types.Lattice,
        #"LIBRARY":"Library",
        "LIGHT":bpy.types.Light,
        "LIGHT_PROBE":bpy.types.LightProbe,
        #"MASK":"Mask",
        "MATERIAL":bpy.types.Material,
        "MESH":bpy.types.Mesh,
        "METABALL":bpy.types.MetaBall,
        #"MOVIE_CLIP":"Movieclip",
        #"NODE_TREE":"NodeTree",
        "OBJECT":bpy.types.Object,
        #"PAINT_CURVE":"PaintCurve",
        #"PALETTE":"Palette",
        "PARTICLE_SETTINGS":bpy.types.ParticleSettings,
        "SCENE":bpy.types.Scene,
        "SCREEN":bpy.types.Screen,
        #"SOUND":"Sound",
        "SPEAKER":bpy.types.Speaker,
        #"TEXT":"Text",
        "TEXTURE":bpy.types.Texture,
        #"VECTOR_FONT":"VectorFont",
        #"VOLUME":bpy.types.Volume,
        "WINDOW_MANAGER":bpy.types.WindowManager,
        "WORKSPACE":bpy.types.WorkSpace,
        "WORLD":bpy.types.World
    }
    _units: Dict[str,List[str]] = {
        "NONE":[
            "FLOAT",
            "FLOATVECTOR"
        ],
        "LENGTH":[
            "FLOAT",
            "FLOATVECTOR"
        ],
        "AREA":[
            "FLOAT",
            "FLOATVECTOR"
        ],
        "VOLUME":[
            "FLOAT",
            "FLOATVECTOR"
        ],
        "ROTATION":[
            "FLOAT",
            "FLOATVECTOR"
        ],
        "TIME":[
            "FLOAT",
            "FLOATVECTOR"
        ],
        "VELOCITY":[
            "FLOAT",
            "FLOATVECTOR"
        ],
        "ACCELERATION":[
            "FLOAT",
            "FLOATVECTOR"
        ],
        "MASS":[
            "FLOAT",
            "FLOATVECTOR"
        ],
        "CAMERA":[
            "FLOAT",
            "FLOATVECTOR"
        ],
        "POWER":[
            "FLOAT",
            "FLOATVECTOR"
        ]
    }
    _options: Dict[str,List[str]] = {
        "HIDDEN":[
            "BOOL",
            "BOOLVECTOR",
            "ENUM",
            "FLOAT",
            "FLOATVECTOR",
            "INT",
            "INTVECTOR",
            "STRING"
            ],
        "SKIP_SAVE":[
            "BOOL",
            "BOOLVECTOR",
            "ENUM",
            "FLOAT",
            "FLOATVECTOR",
            "INT",
            "INTVECTOR",
            "STRING"
            ],
        "ANIMATABLE":[
            "BOOL",
            "BOOLVECTOR",
            "ENUM",
            "FLOAT",
            "FLOATVECTOR",
            "INT",
            "INTVECTOR",
            "STRING"
            ],
        "ENUM_FLAG":[
            "ENUM"
            ],
        "LIBRARY_EDITABLE":[
            "BOOL",
            "BOOLVECTOR",
            "ENUM",
            "FLOAT",
            "FLOATVECTOR",
            "INT",
            "INTVECTOR",
            "STRING"
            ],
        "PROPORTIONAL":[
            "BOOL",
            "BOOLVECTOR",
            "FLOAT",
            "FLOATVECTOR",
            "INT",
            "INTVECTOR",
            "STRING"
            ],
        "TEXTEDIT_UPDATE":[
            "BOOL",
            "BOOLVECTOR",
            "FLOAT",
            "FLOATVECTOR",
            "INT",
            "INTVECTOR",
            "STRING"
            ]
    }
    _subtypes: Dict[str, List[str]] = {
        "FILE_PATH":[
            "STRING"
        ],
        "DIR_PATH":[
            "STRING"
        ],
        "FILE_NAME":[
            "STRING"
        ],
        "BYTE_STRING":[
            "STRING"
        ],
        "PASSWORD":[
            "STRING"
        ],
        "COLOR":[
            "BOOLVECTOR",
            "FLOATVECTOR",
            "INTVECTOR"
        ],
        "TRANSLATION":[
            "BOOLVECTOR",
            "FLOATVECTOR",
            "INTVECTOR"
        ],
        "DIRECTION":[
            "BOOLVECTOR",
            "FLOATVECTOR",
            "INTVECTOR"
        ],
        "VELOCITY":[
            "BOOLVECTOR",
            "FLOATVECTOR",
            "INTVECTOR"
        ],
        "ACCELERATION":[
            "BOOLVECTOR",
            "FLOATVECTOR",
            "INTVECTOR"
        ],
        "MATRIX":[
            "BOOLVECTOR",
            "FLOATVECTOR",
            "INTVECTOR"
        ],
        "EULER":[
            "BOOLVECTOR",
            "FLOATVECTOR",
            "INTVECTOR"
        ],
        "QUATERNION":[
            "BOOLVECTOR",
            "FLOATVECTOR",
            "INTVECTOR"
        ],
        "AXISANGLE":[
            "BOOLVECTOR",
            "FLOATVECTOR",
            "INTVECTOR"
        ],
        "XYZ":[
            "BOOLVECTOR",
            "FLOATVECTOR",
            "INTVECTOR"
        ],
        "XYZ_LENGTH":[
            "BOOLVECTOR",
            "FLOATVECTOR",
            "INTVECTOR"
        ],
        "COLOR_GAMMA":[
            "BOOLVECTOR",
            "FLOATVECTOR",
            "INTVECTOR"
        ],
        "COORDINATES":[
            "BOOLVECTOR",
            "FLOATVECTOR",
            "INTVECTOR"
        ],
        "LAYER":[
            "BOOLVECTOR",
            "FLOATVECTOR",
            "INTVECTOR"
        ],
        "LAYER_MEMBER":[
            "BOOLVECTOR",
            "FLOATVECTOR",
            "INTVECTOR"
        ],
        "PIXEL":[
            "BOOL",
            "FLOAT",
            "INT"
        ],
        "UNSIGNED":[
            "BOOL",
            "FLOAT",
            "INT"
        ],
        "PERCENTAGE":[
            "BOOL",
            "FLOAT",
            "INT"
        ],
        "FACTOR":[
            "BOOL",
            "FLOAT",
            "INT"
        ],
        "ANGLE":[
            "BOOL",
            "FLOAT",
            "INT"
        ],
        "TIME":[
            "BOOL",
            "FLOAT",
            "INT"
        ],
        "DISTANCE":[
            "BOOL",
            "FLOAT",
            "INT"
        ],
        "DISTANCE_CAMERA":[
            "BOOL",
            "FLOAT",
            "INT"
        ],
        "POWER":[
            "BOOL",
            "FLOAT",
            "INT"
        ],
        "TEMPERATURE":[
            "BOOL",
            "FLOAT",
            "INT"
        ],
        "NONE":[
            "BOOL",
            "BOOLVECTOR",
            "FLOAT",
            "FLOATVECTOR",
            "INT",
            "INTVECTOR",
            "STRING"
        ]
    }
    _defaults: Dict[str,Dict[str,Any]] = {
            "BOOL":{
                "TEXT":"",
                "DESCRIPTION":"",
                "DEFAULT":False,
                "OPTIONS":set('ANIMATABLE'),
                "SUBTYPE":'NONE',
                "EVENT_HANDLING":False
            },
            "BOOLVECTOR":{
                "TEXT":"",
                "DESCRIPTION":"",
                "DEFAULT":[False,False,False],
                "OPTIONS":set('ANIMATABLE'),
                "SUBTYPE":'NONE',
                "SIZE":3,
                "EVENT_HANDLING":False
            },
            "ENUM":{
                "ITEMS":[],
                "TEXT":"",
                "DESCRIPTION":"",
                "DEFAULT":None,
                "OPTIONS":set('ANIMATABLE'),
                "EVENT_HANDLING":False
            },
            "FLOAT":{
                "TEXT":"",
                "DESCRIPTION":"",
                "DEFAULT":0.0,
                "MIN":-3.402823e38,
                "MAX":3.402823e38,
                "SOFT_MIN":-3.402823e38,
                "SOFT_MAX":3.402823e38,
                "STEP":3,
                "PRECISION":2,
                "OPTIONS":set('ANIMATABLE'),
                "SUBTYPE":'NONE',
                "UNIT":'NONE',
                "EVENT_HANDLING":False
            },
            "FLOATVECTOR":{
                "TEXT":"",
                "DESCRIPTION":"",
                "DEFAULT":[0.0,0.0,0.0],
                "MIN":sys.float_info.min,
                "MAX":sys.float_info.max,
                "SOFT_MIN":sys.float_info.min,
                "SOFT_MAX":sys.float_info.max,
                "STEP":3,
                "PRECISION":2,
                "OPTIONS":set('ANIMATABLE'),
                "SUBTYPE":'NONE',
                "UNIT":'NONE',
                "SIZE":3,
                "EVENT_HANDLING":False
            },
            "INT":{
                "TEXT":"",
                "DESCRIPTION":"",
                "DEFAULT":0,
                "MIN":-2147483648,
                "MAX":2147483647,
                "SOFT_MIN":-2147483648,
                "SOFT_MAX":2147483647,
                "STEP":1,
                "OPTIONS":set('ANIMATABLE'),
                "SUBTYPE":'NONE',
                "EVENT_HANDLING":False
            },
            "INTVECTOR":{
                "TEXT":"",
                "DESCRIPTION":"",
                "DEFAULT":[0,0,0],
                "MIN":-2147483648,
                "MAX":2147483647,
                "SOFT_MIN":-2147483648,
                "SOFT_MAX":2147483647,
                "STEP":1,
                "OPTIONS":set('ANIMATABLE'),
                "SUBTYPE":'NONE',
                "SIZE":3,
                "EVENT_HANDLING":False
            },
            "STRING":{
                "TEXT":"",
                "DESCRIPTION":"",
                "DEFAULT":"",
                "MAX_LEN":0,
                "OPTIONS":set('ANIMATABLE'),
                "SUBTYPE":'NONE',
                "EVENT_HANDLING":False
            },
            "OTHER":{}
        }

    #Get a Dict of the available scopes PropertyGroups can reside in
    @classmethod
    def get_scopes(cls) -> Dict[str,Any]:
        """
        Gets the available scopes a PropertyGroup can exist in

        PARAMETERS:
        -----------

        cls
            references the class itself

        RETURNS:
        --------

        cls._scope : Dict[str,Any]
            This dictionary holds a translation dict for the available scopes.
        """
        return cls._scope

    #Get a List of units from the supplied type
    @classmethod
    def get_units(cls,input_type: str) -> List[str]:
        """
        Gets the available units from a given property type

        PARAMETERS:
        -----------

        cls
            references the class itself

        input_type : str
            This is the type of property given in the reference

        RETURNS:
        --------

        results : List[str]
            This list holds the units that are available for the given type
        """
        results: List[str] = []

        for index in cls._units:
            if input_type in cls._units[index]:
                results.append(index)

        return results

    #Get a List of options from the supplied type
    @classmethod
    def get_options(cls,input_type: str) -> List[str]:
        """
        Gets the available options from a given property type

        PARAMETERS:
        -----------

        cls
            references the class itself

        input_type : str
            This is the type of property given in the reference

        RETURNS:
        --------

        results : List[str]
            This list holds the options that are available for the given type
        """
        results: List[str] = []

        for index in cls._options:
            if input_type in cls._options[index]:
                results.append(index)

        return results

    #Get a List of subtypes from the supplied type
    @classmethod
    def get_subtypes(cls,input_type: str) -> List[str]:
        """
        Gets the available subtypes from a given property type

        PARAMETERS:
        -----------

        cls
            references the class itself

        input_type : str
            This is the type of property given in the reference

        RETURNS:
        --------

        results : List[str]
            This list holds the subtypes that are available for the given type
        """
        results: List[str] = []

        for index in cls._subtypes:
            if input_type in cls._subtypes[index]:
                results.append(index)

        return results

    #Get default dictionary properties
    @classmethod
    def get_defaults(cls,input_type: str) -> Dict[str,Any]:
        """
        Gets the default attributes from a given property type

        PARAMETERS:
        -----------

        cls
            references the class itself

        input_type : str
            This is the type of property given in the reference

        RETURNS:
        --------

        cls._defaults[""] : Dict[str,Any]
            This dictionary holds the attributes that are default for the given type
        """
        current_type = input_type.upper()

        if current_type in ["BOOL","BOOLEAN","BLN"]:
            return cls._defaults["BOOL"]

        elif current_type in ["BOOLVECTOR"]:
            return cls._defaults["BOOLVECTOR"]

        elif current_type in ["ENUM","ENUMERATOR"]:
            return cls._defaults["ENUM"]

        elif current_type in ["FLT","FLOAT"]:
            return cls._defaults["FLOAT"]

        elif current_type in ["FLOATVECTOR"]:
            return cls._defaults["FLOATVECTOR"]

        elif current_type in ["INT","INTEGER"]:
            return cls._defaults["INT"]

        elif current_type in ["INTVECTOR"]:
            return cls._defaults["INTVECTOR"]

        elif current_type in ["STR","STRING"]:
            return cls._defaults["STRING"]

        else:
            return cls._defaults["OTHER"]
