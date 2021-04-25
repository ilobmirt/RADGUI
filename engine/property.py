"""================================================================================================
This module is designed to represent a Property element in code

CLASSES:
    Property
================================================================================================"""
from typing import List, Dict, Any # pylint: disable=unused-import
#==================================================#
#RAD GUI Property Object
#==================================================#

class Property():
    """
    This class holds all the properties of a property as it is to be rendered in Blender

    ATTRIBUTES:
    -----------

        text : str
            Override automatic text of the item

        text_ctxt : str
            Override automatic translation context of the given text

        translate : str
            Translate the given text, when UI translation is enabled

        icon : str
            Override automatic icon of the item

        icon_value : int
            Override automatic icon of the item

        icon_only : bool
            Draw only icons in buttons, no text

        event : bool
            Use button to input key events

        full_event : bool
            Use button to input full events including modifiers

        emboss : bool
            Draw the button itself, not just the icon/text

        expand : bool
            Expand button to show more detail

        slider : bool
            Use slider widget for numeric values

        toggle : int
            For Boolean properties ...
            -1 = Use toggle only when an icon is displayed
            1 = Use toggle over a checkbox

        index : int
            The index of this button, when set a single member of an array can be accessed, when
            set to -1 all array members are used

        invert_checkbox : bool
            Draw checkbox value inverted

        scope : str
            The scope where this property exists

        variable : str
            The name of the property that exists in the project

        namespace : str
            Represents the project's unique identifier.

    METHODS:

        __init__ : None
        to_code : str
    """
    def __init__(self):
        self._defaults: Dict[str,Any] = {
            "TEXT":"",
            "CONTEXT":"",
            "TRANSLATE":"",
            "ICON":"NONE",
            "ICON_VALUE":0,
            "ICON_ONLY":False,
            "EVENT":False,
            "FULL_EVENT":False,
            "EMBOSS":True,
            "EXPAND":False,
            "SLIDER":False,
            "TOGGLE":-1,
            "INDEX":-1,
            "INVERT_CHECKBOX":False
        }

        self.text = self._defaults["TEXT"]
        self.text_ctxt = self._defaults["CONTEXT"]
        self.translate = self._defaults["TRANSLATE"]
        self.icon = self._defaults["ICON"]
        self.icon_value = self._defaults["ICON_VALUE"]
        self.icon_only = self._defaults["ICON_ONLY"]
        self.event = self._defaults["EVENT"]
        self.full_event = self._defaults["FULL_EVENT"]
        self.emboss = self._defaults["EMBOSS"]
        self.expand = self._defaults["EXPAND"]
        self.slider = self._defaults["SLIDER"]
        self.toggle = self._defaults["TOGGLE"]
        self.index = self._defaults["INDEX"]
        self.invert_checkbox = self._defaults["INVERT_CHECKBOX"]

        self.scope: str = ""
        self.variable: str = ""
        self.namespace: str = ""

    @property
    def value(self) -> Dict[str,Any]:
        """
        GETTER: Represents the Property as a Dictionary Object

        PARAMETERS:
        -----------

            self
                References the current instance of the property class

        RETURNS:
        --------

            result : Dict[str,Any]
                This dictionary represents the property and its properties
        """
        result: Dict[str,Any] = {
            "TYPE":"PROPERTY",
            "SCOPE":self.scope,
            "VARIABLE":self.variable
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

        if self.icon_only != self._defaults["ICON_ONLY"]:
            result["ICON_ONLY"] = self.icon_only

        if self.event != self._defaults["EVENT"]:
            result["EVENT"] = self.event

        if self.full_event != self._defaults["FULL_EVENT"]:
            result["FULL_EVENT"] = self.full_event

        if self.emboss != self._defaults["EMBOSS"]:
            result["EMBOSS"] = self.emboss

        if self.expand != self._defaults["EXPAND"]:
            result["EXPAND"] = self.expand

        if self.slider != self._defaults["SLIDER"]:
            result["SLIDER"] = self.slider

        if self.toggle != self._defaults["TOGGLE"]:
            result["TOGGLE"] = self.toggle

        if self.index != self._defaults["INDEX"]:
            result["INDEX"] = self.index

        if self.invert_checkbox != self._defaults["INVERT_CHECKBOX"]:
            result["INVERT_CHECKBOX"] = self.invert_checkbox

        return result

    @value.setter
    def value(self, input_attributes: Dict[str,Any]) -> None:
        """
        SETTER: Configures the Property object from a Dictionary Object

        PARAMETERS:
        -----------

            self
                References the current instance of the Property class

            input_attributes : Dict[str, Any]
                Dictionary object holding the attributes to assign to the property

        RETURNS:
        --------

            None
        """
        #We only assign values if the dict is a Property Type
        if "TYPE" not in input_attributes:
            return

        if "{}".format(input_attributes["TYPE"]).upper() != "PROPERTY":
            return

        #We also only assign the value if it's given a scope and a VARIABLE
        if "SCOPE" not in input_attributes:
            return

        if "VARIABLE" not in input_attributes:
            return

        available_scopes: List[str] = [
            "ARMATURE"
            "BRUSH",
            "CAMERA",
            "COLLECTION",
            "CURVE",
            "LATTICE",
            "LIGHT",
            "LIGHT_PROBE",
            "MATERIAL",
            "MESH",
            "METABALL",
            "OBJECT",
            "PARTICLE_SETTINGS",
            "SCENE",
            "SCREEN",
            "SPEAKER",
            "TEXTURE",
            "WINDOW_MANAGER",
            "WORKSPACE",
            "WORLD"
        ]

        if "{}".format(input_attributes["SCOPE"]).upper() not in available_scopes:
            return

        #Now that we are in the clear, start with the defaults
        self.text = self._defaults["TEXT"]
        self.text_ctxt = self._defaults["CONTEXT"]
        self.translate = self._defaults["TRANSLATE"]
        self.icon = self._defaults["ICON"]
        self.icon_value = self._defaults["ICON_VALUE"]
        self.icon_only = self._defaults["ICON_ONLY"]
        self.event = self._defaults["EVENT"]
        self.full_event = self._defaults["FULL_EVENT"]
        self.emboss = self._defaults["EMBOSS"]
        self.expand = self._defaults["EXPAND"]
        self.slider = self._defaults["SLIDER"]
        self.toggle = self._defaults["TOGGLE"]
        self.index = self._defaults["INDEX"]
        self.invert_checkbox = self._defaults["INVERT_CHECKBOX"]

        #Then, lets go with the custom attributes
        self.scope = input_attributes["SCOPE"]
        self.variable = input_attributes["VARIABLE"]

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

        if "ICON_ONLY" in input_attributes:
            self.icon_only = input_attributes["ICON_ONLY"]

        if "EVENT" in input_attributes:
            self.event = input_attributes["EVENT"]

        if "FULL_EVENT" in input_attributes:
            self.full_event = input_attributes["FULL_EVENT"]

        if "EMBOSS" in input_attributes:
            self.emboss = input_attributes["EMBOSS"]

        if "EXPAND" in input_attributes:
            self.expand = input_attributes["EXPAND"]

        if "SLIDER" in input_attributes:
            self.slider = input_attributes["SLIDER"]

        if "TOGGLE" in input_attributes:
            self.toggle = input_attributes["TOGGLE"]

        if "INDEX" in input_attributes:
            self.index = input_attributes["INDEX"]

        if "INVERT_CHECKBOX" in input_attributes:
            self.invert_checkbox = input_attributes["INVERT_CHECKBOX"]

    def to_code(self,called_by: str = "layout") -> str:
        """
        Represents the Property and its contents as it gets called in code

        PARAMETERS:
        -----------

            self
                References the current instance of the Property class

            called_by : str
                What's calling to draw this Property object?

        RETURNS:
        --------

            result : str
                This is the Property as if it were written in a draw method
        """
        result: str = ""
        data_value: Dict[str,str] = {
            "ARMATURE":"context.armature.{}",
            "BRUSH":"context.brush.{}",
            "CAMERA":"context.camera.{}",
            "COLLECTION":"context.collection.{}",
            "CURVE":"context.curve.{}",
            "LATTICE":"context.lattice.{}",
            "LIGHT":"context.light.{}",
            "LIGHT_PROBE":"context.lightprobe.{}",
            "MATERIAL":"context.material.{}",
            "MESH":"context.mesh.{}",
            "METABALL":"context.meta_ball.{}",
            "OBJECT":"context.object.{}",
            "PARTICLE_SETTINGS":"context.particle_settings.{}",
            "SCENE":"context.scene.{}",
            "SCREEN":"context.screen.{}",
            "SPEAKER":"context.speaker.{}",
            "TEXTURE":"context.texture.{}",
            "WINDOW_MANAGER":"context.window_manager.{}",
            "WORKSPACE":"context.workspace.{}",
            "WORLD":"context.world.{}"
        }

        if (self.scope not in data_value) or (self.namespace == ""):
            return ""

        command_value: str = "{}.prop({}, '{}', text='{}', text_ctxt='{}', translate={}, icon='{}', expand={}, slider={}, toggle={}, icon_only={}, event={}, full_event={}, emboss={}, index={}, icon_value={}, invert_checkbox={})"

        result = command_value.format(
            called_by,
            data_value[self.scope].format(self.namespace),
            self.text,
            self.text_ctxt,
            self.translate,
            self.icon,
            self.expand,
            self.slider,
            self.toggle,
            self.icon_only,
            self.event,
            self.full_event,
            self.emboss,
            self.index,
            self.icon_value,
            self.invert_checkbox
        )

        return result
