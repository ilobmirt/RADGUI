from bpy.types import PropertyGroup, Scene as bpyScene, Object as bpyObject
from bpy.props import PointerProperty
from typing import Dict,Any
from . import EventManager

#==================================================#
#Property Shell Class
#==================================================#
class PropertyGroupShell(PropertyGroup):
    Domain: str = ""
    Scope: str = "SCENE"

    @staticmethod
    def PropertyUpdate(Object, Context, PropertyName) -> None:

        GeneratedEvent : Dict[str, Any] = {
                "EVENT_ID":PropertyName,
                "EVENT_CLASS":Object,
                "CONTEXT":Context,
                "OBJECT_TYPE":"VARIABLE",
                "EVENT_TYPE":"VARIABLE_CHANGED",
                "VALUE":getattr(Object,PropertyName)
            }
            
        EventManager.HandleEvent(GeneratedEvent)

    @classmethod
    def register(cls) -> None:
        if (cls.Domain != ""):
            if (cls.Scope.upper() == "SCENE"):
                setattr(bpyScene,cls.Domain,PointerProperty(type=cls))
            elif (cls.Scope.upper() == "OBJECT"):
                setattr(bpyObject,cls.Domain,PointerProperty(type=cls))

    @classmethod
    def unregister(cls) -> None:
        if (cls.Domain != ""):
            if (cls.Scope.upper() == "SCENE"):
                if hasattr(bpyScene,cls.Domain) == True:
                    delattr(bpyScene,cls.Domain)
            elif (cls.Scope.upper() == "OBJECT"):
                if hasattr(bpyObject,cls.Domain) == True:
                    delattr(bpyObject,cls.Domain)