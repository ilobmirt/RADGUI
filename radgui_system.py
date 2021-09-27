"""================================================================================================
This module is designed to be a high level interface for RADGUI based projects currently it can...
    * Create unique RADGUI projects
    * Create interactive dialog boxes

CLASSES:
    System
================================================================================================"""
import uuid
from typing import List, Dict, Any # pylint: disable=unused-import
import bpy
from radgui_console import Console
from project.project import Project
from dialog.message_dialog import MessageDialog
from dialog.file_dialog import FileDialog

#==================================================#
#RAD GUI System Manager
#==================================================#

class System():
    """
    This class is used to generate RADGUI projects and provide interactive blender dialogs

    ATTRIBUTES:
    -----------

        __unique_project_ids: LIST[uuid.UUID]
            A collection of unique project ids running right now

        __dialog_collection: Dict[uuid.UUID,Any]
            A collection of dialog boxes waiting to be interacted with

        __current_dialog_id:uuid.UUID
            The unique id of the dialog currently being displayed

    METHODS:
    --------

        create_project: Project
        remove_project_id: bool
        message_dialog: None
        dialog_cleanup: None
        __dialog_handler: None
        register: None
        unregister: None
    """
    __unique_project_ids: List[uuid.UUID] = []
    __dialog_collection: Dict[uuid.UUID,Any] = {}
    __current_dialog_id:uuid.UUID = None

    @classmethod
    def create_project(cls, **input_args) -> Project:
        """
        Creates a new RADGUI project instance with a uniqe id.
        If it is a project based off of existing data, will provide it to the new project.
        Otherwise, it will be a blank project.

        PARAMETERS:
        -----------

            cls:
                Represents the class itself.

            **input_args:
                A variable list of arguments passed to it.
                The list that this program will look at is the following...

                * filename -
                    This project will be populated by the information given in a JSON file

                * json -
                    This project will be populated by the information given in a Dictionary

        RETURNS:
        --------

            None

        """
        result: Project = None
        generated_uuid:uuid.UUID = None

        Console.set_write_tags(None,{"RADGUI_SYSTEM",1})
        Console.write(None,"(RADGUI_SYSTEM) Creating a new project instance")
        Console.set_write_tags(None,{"RADGUI_SYSTEM",2})

        #We just want to be sure we randomly get a unique id
        while True:

            generated_uuid = uuid.uuid4()

            if generated_uuid not in cls.__unique_project_ids:
                break

        #We get a File based / JSON based / Blank project
        if "filename" in input_args:
            result = Project(id=generated_uuid,filename=input_args["filename"])
            Console.write(None,f"(RADGUI_SYSTEM) New blank project loaded from \"{input_args['filename']}\" with a UUID of \"{generated_uuid}\"")
        elif "json" in input_args:
            result = Project(id=generated_uuid,json=input_args["json"])
            Console.write(None,f"(RADGUI_SYSTEM) New project created from json with a UUID of \"{generated_uuid}\"")
        else:
            result = Project(id=generated_uuid)
            Console.write(None,f"(RADGUI_SYSTEM) New blank project created with a UUID of \"{generated_uuid}\"")

        #Append project ID to list
        cls.__unique_project_ids.append(generated_uuid)

        return result

    @classmethod
    def remove_project_id(cls,input_project_id:uuid.UUID) -> bool:
        """
        This will remove a project id from the list of unique ids registered in RADGUI.
        Typically, this is called from the Project instances themselves as they clean up.
        This will free up the id for other projects.

        PARAMETERS:
        -----------

            cls:
                Represents the class itself.

            input_project_id:uuid.UUID
                This is the unique id of the project to remove from the system

        RETURNS:
        --------

            result:bool
                Returns if the project id removal was successful or not
        """
        result:bool = False

        Console.set_write_tags(None,{"RADGUI_SYSTEM",1})
        Console.write(None,f"(RADGUI_SYSTEM) Removing project instance \"{input_project_id}\"")
        Console.set_write_tags(None,{"RADGUI_SYSTEM",2})

        if input_project_id in cls.__unique_project_ids:
            cls.__unique_project_ids.remove(input_project_id)
            result = True
            Console.write(None,f"(RADGUI_SYSTEM) Project \"{input_project_id}\" removed from system")

        return result

    @classmethod
    def message_dialog(cls,**input_args) -> None:
        """
        Generate a temporary message dialog class with the purpose of displaying a message

        PARAMETERS:
        -----------

            cls:
                Represents the class itself

            **input_args:
                A variable list of arguments passed to it.
                The list that this program will look at is the following...

                * title: str -
                    Mandatory. The words used in the title of the dialog box.

                * message: str -
                    Mandatory. The message used in the dialog body

                * width: int -
                    The width in pixels that the dialog will take

                * project_id: uuid.UUID -
                    The unique id of the project this dialog is associated with.
                    Used in event handling.

                * event_id: str -
                    The name of the event to generate.
                    Used in event handling

        RETURNS:
        --------

            None
        """
        Console.set_write_tags(None,{"RADGUI_SYSTEM",1})
        Console.write(None,"(RADGUI_SYSTEM) Creating a temporary message dialog")
        Console.set_write_tags(None,{"RADGUI_SYSTEM",2})

        if ("title" not in input_args) or ("message" not in input_args):
            Console.write(None,"(RADGUI_SYSTEM) No title or message provided to the message dialog")
            return

        input_title:str = input_args["title"]
        input_message:str = input_args["message"]

        input_width:int = 400
        if "width" in input_args:
            input_width = input_args["width"]

        input_project_id:uuid.UUID = None
        if "project_id" in input_args:
            input_project_id = input_args["project_id"]

        input_event_id:str = ""
        if "event_id" in input_args:
            input_event_id = input_args["event_id"]

        autogen_id: uuid.UUID = None
        while True:
            autogen_id = uuid.uuid4()
            if autogen_id not in cls.__dialog_collection:
                break

        autogen_idname:str = f"radgui_.dialog_{autogen_id.hex}"
        autogen_classname:str = f"OPERATOR_OT_{autogen_id.hex}_MESSAGE_DIALOG"
        autogen_attributes:Dict[str,Any] = {
            "bl_idname":autogen_idname,
            "bl_label":input_title,
            "message":input_message,
            "width":input_width,
            "dialog_id":autogen_id,
            "project_id":input_project_id,
            "event_id":input_event_id
        }
        autogen_class = type(autogen_classname,(MessageDialog,),autogen_attributes)

        Console.write(None,f"(RADGUI_SYSTEM) Message dialog \"{autogen_id.hex}\" created titled \"{input_title}\" with the message of \"{input_message}\"")

        cls.__dialog_collection.update({autogen_id:autogen_class})
        cls.__dialog_handler()

    @classmethod
    def file_dialog(cls,**input_args) -> None:
        """
        Generate a file/folder selection dialog for the user.

        PARAMETERS:
        -----------

            cls:
                Represents the class itself

            **input_args:
                A variable list of arguments passed to it.
                The list that this program will look at is the following...

                * title: str -
                    Mandatory. The words used in the title of the dialog box.

                * message: str -
                    Mandatory. The message used in the dialog body

                * project_id: uuid.UUID -
                    Mandatory. The unique id of the project this dialog is associated with.
                    Used in event handling.

                * event_id: str -
                    Mandatory. The name of the event to generate.
                    Used in event handling

                * is_folder: bool -
                    Determines if the dialog selects the folder rather than a file.
                    Default = False

                * filter_list: List[str] -
                    String List to filter out the contents of the folder.
                    Default = ["*.*"] meaning all files are allowed

        RETURNS:
        --------

            None
        """
        Console.set_write_tags(None,{"RADGUI_SYSTEM",1})
        Console.write(None,"(RADGUI_SYSTEM) Creating a temporary file/folder selection dialog")
        Console.set_write_tags(None,{"RADGUI_SYSTEM",2})

        if ("title" not in input_args) or ("message" not in input_args):
            Console.write(None,"(RADGUI_SYSTEM) No title or message provided to the file/folder dialog")
            return

        if ("project_id" not in input_args) or ("event_id" not in input_args):
            Console.write(None,"(RADGUI_SYSTEM) No event information provided to the file/folder dialog")
            return

        input_title:str = input_args["title"]
        input_message:str = input_args["message"]
        input_project_id:uuid.UUID = input_args["project_id"]
        input_event_id:str = input_args["event_id"]

        input_is_folder:bool = False
        if "is_folder" in input_args:
            input_is_folder = input_args["is_folder"]

        input_filter_list:str = "*.*"
        if "filter_list" in input_args:
            input_is_folder = ";".join(input_args["filter_list"])

        autogen_id: uuid.UUID = None
        while True:
            autogen_id = uuid.uuid4()
            if autogen_id not in cls.__dialog_collection:
                break

        autogen_idname:str = f"radgui_.dialog_{autogen_id.hex}"
        autogen_classname:str = f"OPERATOR_OT_{autogen_id.hex}_FILE_DIALOG"
        autogen_annotations: Dict[str,Any] = {
            "filter_glob": bpy.props.StringProperty(
                    default=input_filter_list,
                    options={'HIDDEN'}
                    )
        }

        if input_is_folder is True:
            autogen_annotations.update(
                {
                    "directory":bpy.props.StringProperty(
                        subtype='DIR_PATH',
                        description=input_message
                        )
                }
            )
        else:
            autogen_annotations.update(
                {
                    "filepath":bpy.props.StringProperty(
                        subtype='FILE_PATH',
                        description=input_message
                        )
                }
            )
        autogen_attributes:Dict[str,Any] = {
            "bl_idname":autogen_idname,
            "bl_label":input_title,
            "dialog_id":autogen_id,
            "project_id":input_project_id,
            "event_id":input_event_id,
            "__annotations__":autogen_annotations
        }

        autogen_class = type(autogen_classname,(FileDialog,),autogen_attributes)

        Console.write(None,f"(RADGUI_SYSTEM) File/Folder dialog \"{autogen_id.hex}\" created titled \"{input_title}\"")

        cls.__dialog_collection.update({autogen_id:autogen_class})
        cls.__dialog_handler()

    @classmethod
    def input_dialog(cls,**input_args) -> None:
        """..."""

    @classmethod
    def login_dialog(cls,**input_args) -> None:
        """..."""

    @classmethod
    def dialog_cleanup(cls,input_dialog_id:uuid.UUID) -> None:
        """
        Removes a dialog from the dialog collection.
        If it was registered, would also unregister it from Blender.

        PARAMETERS:
        -----------

            cls:
                Represents the class itself.

            input_dialog_id:uuid.UUID
                The unique id of the dialog to remove from the system.

        RETURNS:
        --------

            None
        """
        Console.set_write_tags(None,{"RADGUI_SYSTEM",1})
        Console.write(None,f"(RADGUI_SYSTEM) Removing temporary message dialog \"{input_dialog_id}\"")
        Console.set_write_tags(None,{"RADGUI_SYSTEM",2})

        if input_dialog_id == cls.__current_dialog_id:
            bpy.utils.unregister_class(cls.__dialog_collection[input_dialog_id])
            cls.__current_dialog_id = None
            Console.write(None,"(RADGUI_SYSTEM) Class has been unregisterd from Blender")

        cls.__dialog_collection.pop(input_dialog_id)

        if (len(cls.__dialog_collection) > 0) and (cls.__current_dialog_id is None):
            cls.__dialog_handler()

    @classmethod
    def __dialog_handler(cls) -> None:
        """
        Called after dialog creation and removal. This method loads up the first available dialog
        and registers it with Blender before displaying it.

        PARAMETERS:
        -----------

            cls:
                Represents the class itself.

        RETURNS:
        --------

            None
        """
        Console.set_write_tags(None,{"RADGUI_SYSTEM",1})
        Console.write(None,"(RADGUI_SYSTEM) Loading and displaying the next available dialog")
        Console.set_write_tags(None,{"RADGUI_SYSTEM",2})

        #Do nothing if we have nothing to proccess or are still displaying dialogs
        if len(cls.__dialog_collection) <= 0:
            Console.write(None,"(RADGUI_SYSTEM) No dialogs are available to load")
            return

        if cls.__current_dialog_id is not None:
            Console.write(None,f"(RADGUI_SYSTEM) The system is currently busy displaying another dialog. The currently displayed dialog should have an id of \"{cls.__current_dialog_id.hex}\"")
            return

        #So we have items to display, lets get the first one on our list
        first_dialog_id:uuid.UUID = list(cls.__dialog_collection.keys())[0]
        dialog_idname:str = cls.__dialog_collection[first_dialog_id].bl_idname
        cls.__current_dialog_id = first_dialog_id
        bpy.utils.register_class(cls.__dialog_collection[first_dialog_id])
        Console.write(None,f"(RADGUI_SYSTEM) New dialog loaded with an id of \"{first_dialog_id.hex}\"")
        eval(f"bpy.ops.{dialog_idname}('INVOKE_DEFAULT')")

    @classmethod
    def register(cls) -> None:
        """
        Sets up RADGUI preset objects upon class creation

        PARAMETERS:
        -----------

            cls:
                Represents the class itself.

        RETURNS:
        --------

            None
        """

    @classmethod
    def unregister(cls) -> None:
        """
        Cleans up RADGUI preset objects upon class destruction

        PARAMETERS:
        -----------

            cls:
                Represents the class itself.

        RETURNS:
        --------

            None
        """
