"""================================================================================================
This module is designed to display a prompt to get a string valued response from the user.

CLASSES:
    InputDialog
================================================================================================"""
import uuid
from typing import List, Dict, Any # pylint: disable=unused-import
import bpy
from bpy.types import UILayout
from radgui_system import System as radguiSystem
from event_manager import EventManager

#==================================================#
#RADGUI Message Dialog
#==================================================#
class InputDialog(bpy.types.Operator):
    """
    This class is a subclass of the Blender Operator designed specifically to...
    * Display a message to the user like a dialog

    ATTRIBUTES:
    -----------

        bl_idname
            Unique id of the class registered in blender

        bl_label
            Message of the title for the dialog box

        dialog_id:uuid.UUID
            Unique id of the class ragistered in RADGUI

        project_id:uuid.UUID
            Unique project id this dialog is associated with.
            Required for event handling

        event_id:str
            Name based id of the event generated for the project.
            Required for event handling

        value:str
            To hold the value of user input when given by the user

        (Annotations to be added later from RADGUI_SYSTEM)

        message:str
            The plain text message to display within the body

        width:int
            The width of the dialog box to display

    """
    bl_idname = ""
    bl_label = ""

    __annotations__: Dict[str,Any] = {}

    dialog_id:uuid.UUID = None
    project_id:uuid.UUID = None
    event_id:str = ""
    message:str = ""
    width:int = 400
    value:str = ""

    def generate_event(self,event_type:str,context: Any) -> None:
        """
        Generates an event for the RADGUI event handler.

        PARAMETERS:
        -----------

            self:
                References the instance of the class itself

            event_type:
                Type of event to generate for the event handler
                Either "EXECUTE" or "CANCEL"

            context: Any
                References the context in which this event was generated

        RETURNS:
        --------

            None
        """
        event_type = event_type.strip().upper()
        if (self.project_id is None) or (self.event_id is "") or (event_type not in ["EXECUTE","CANCEL"]):
            return

        #Generate event
        generated_event:Dict[str,Any] = {
            "EVENT_TYPE":f"DIALOG_{event_type}",
            "PROJECT_ID":self.project_id,
            "EVENT_ID":self.event_id,
            "VALUE":self.value,
            "CONTEXT":context
        }

        EventManager.handle_event(self.project_id,generated_event)

    def execute(self, context) -> None:
        """
        The user clicked on the "OK" button within the dialog

        PARAMETERS:
        -----------

            self:
                Represents the instance of the class itself

            context:
                Represents the context of the event itself

        RETURNS:
        --------

            None
        """

        if "input_string" in self.__annotations__:
            self.value = getattr(self,"input_string")

        self.generate_event("EXECUTE",context)
        radguiSystem.dialog_cleanup(self.dialog_id)
        return {'FINISHED'}

    def cancel(self, context) -> None:
        """
        The user clicked outside of the dialog or pressed escape on the keyboard

        PARAMETERS:
        -----------

            self:
                Represents the instance of the class itself

            context:
                Represents the context of the event itself

        RETURNS:
        --------

            None
        """
        self.generate_event("CANCEL",context)
        radguiSystem.dialog_cleanup(self.dialog_id)

    def invoke(self, context, event) -> None:
        """
        Generates the dialog itself. Invoked from the system class

        PARAMETERS:
        -----------

            self:
                Represents the instance of the class itself

            context:
                Represents the context of the event itself

            event:
                Represents the event itself

        RETURNS:
        --------

            None
        """
        return context.window_manager.invoke_props_dialog(self, width = self.width)

    def draw(self, context) -> None:
        """
        Called whenever the dialog is drawn on the screen

        PARAMETERS:
        -----------

            self:
                References the instance of the class itself

            context:
                References the context of the event itself

        RETURNS:
        --------

            None
        """
        layout:UILayout = self.layout
        if "input_string" in self.__annotations__:
            layout.prop(self,"input_string")
        else:
            layout.label(text=f"{self.message}:")
            layout.label(text = "(To Developer- Something went wrong. Where's the \"input_string\" property?)")
