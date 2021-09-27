"""================================================================================================
This module is designed to obtain a directory/file to load/save from the user.

CLASSES:
    FileDialog
================================================================================================"""
import uuid
from typing import List, Dict, Any # pylint: disable=unused-import
import bpy
from radgui_system import System as radguiSystem
from event_manager import EventManager

#==================================================#
#RADGUI File Dialog
#==================================================#
class FileDialog(bpy.types.Operator):
    """
    This class is a subclass of the Blender Operator designed specifically to...
    * Obtain a file/folder path for loading or saving files

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
            The value taken from user input

        (Annotations to be added later from RADGUI_SYSTEM)

        filepath: StringProperty ('FILE_PATH')
            ####

        directory: StringProperty ('DIR_PATH')
            ####

    """
    bl_idname = ""
    bl_label = ""

    __annotations__: Dict[str,Any] = {}

    dialog_id:uuid.UUID = None
    project_id:uuid.UUID = None
    event_id:str = ""
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
        if "filepath" in self.__annotations__:
            self.value = getattr(self,"filepath")

        if "directory" in self.__annotations__:
            self.value = getattr(self,"directory")

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
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
