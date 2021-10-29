"""================================================================================================
This module handles project messaging intelligently allowing for programmers the ability to debug
their project. This module can filter and adjust the verbosity of programming messages allowing
developers to control the detail and category of the code that occurs in debug output.

This offers a more flexible tool than a simple print to console.

CLASSES:
    Console
================================================================================================"""
from typing import Dict, List, Any # pylint: disable=unused-import
import uuid
import bpy

#==================================================#
#RAD GUI Console
#==================================================#
class Console():
    """
    This class is to intelligently output messages to the appropriate medium.

    ATTRIBUTES:
    -----------

        __output_filter: Dict[ uuid.UUID,Dict[ str,int ] ]
            Filter of output. Limiting any message to a certain number
            of categories up to a certain verbosity level.
            [project_id] --> {"category label",verbosity level}

        __write_tags: Dict[ uuid.UUID,Dict[str,int] ]
            The category and verbosity level of output by project.
            [project_id] --> {"category label",verbosity level}

        __output_medium: Dict[ uuid.UUID,str ]
            The output medium per project.
            Valid mediums are:
                * CONSOLE   - Standard OS console output
                * BLENDER   - Blender's internal python console
                * FILE      - Plain Text File

        __output_file: Dict[ uuid.UUID,str ]
            The path to the file being written to by project id.

    METHODS:
    --------

        set_write_tags: None
        set_filter: None
        set_medium: None
        add_project_id: None
        remove_project_id: None
        __print_blender: None
        __print_file: None
        write: None

    """
    __output_filter: Dict[ uuid.UUID,Dict[ str,int ] ] = {}
    __write_tags: Dict[ uuid.UUID,Dict[str,int] ] = {}
    __output_medium: Dict[ uuid.UUID,str ] = {}
    __output_file: Dict[ uuid.UUID,str ] = {}

    @classmethod
    def set_write_tags(cls, input_project_id: uuid.UUID, input_tags: Dict[ str,int ]) -> None:
        """
        Set the writing tags for radgui console output.
        These tags will be used with console.write

        PARAMETERS:
        -----------

            cls:
                Represents the Console class itself

            input_project_id: uuid.UUID
                Unique Project ID in which write tags are being set

            input_tags: Dict[ str,int ]
                Defines the write tags the project will use for output
                The category will be the key and its value will be the level of
                verbosity. Higher values represent more verbose messages.

        RETURNS:
        --------

            None

        """
        if input_project_id not in cls.__write_tags:
            return

        cls.__write_tags[input_project_id] = input_tags

    @classmethod
    def set_filter(cls, input_project_id: uuid.UUID, input_filters: Dict[ str,int ]) -> None:
        """
        Set the filters for project output by category and level of verbosity.
        These filters will be used with console.write

        PARAMETERS:
        -----------

            cls:
                Represents the Console class itself

            input_project_id: uuid.UUID
                Unique Project ID in which write filters are being set

            input_filters: Dict[ str,int ]
                Defines the filters the project will use for output
                The category will be the key and its value will be the level of
                verbosity. Higher values represent more verbose messages.

        RETURNS:
        --------

            None

        """
        if input_project_id not in cls.__output_filter:
            return

        cls.__output_filter[input_project_id] = input_filters

    @classmethod
    def get_filter(cls,input_project_id:uuid.UUID) -> Dict[str,int]:
        """
        """
        result: Dict[str,int] = {}

        if input_project_id not in cls.__output_filter:
            return result
        
        result = cls.__output_filter[input_project_id]

        return result

    @classmethod
    def set_medium(cls, input_project_id: uuid.UUID, input_medium: str, input_filename: str = "") -> None:
        """
        Sets the medium of output the project will use for output.

        PARAMETERS:
        -----------

            cls:
                Represents the Console class itself

            input_project_id: uuid.UUID
                Unique Project ID in which the output medium is being set

            input_medium: str
                The desired medium which the project should be set.
                Valid mediums are:
                    * CONSOLE   - Standard OS console output
                    * BLENDER   - Blender's internal python console
                    * FILE      - Plain Text File

            input_filename: str
                If the desired medium is a file based output, where it will be output to

        RETURNS:
        --------

            None

        """
        input_medium = input_medium.strip().upper()
        input_filename = input_filename.strip()

        if input_project_id not in cls.__output_medium:
            return

        if input_medium not in ["CONSOLE","BLENDER","FILE"]:
            return

        if (input_medium == "FILE") and (input_filename == ""):
            return

        if (input_medium == "FILE") and (input_filename != ""):
            cls.__output_file[input_project_id] = input_filename

        cls.__output_medium[input_project_id] = input_medium

    @classmethod
    def get_medium(cls,input_project_id:uuid.UUID) -> str:
        """
        """
        result:str = ""

        if input_project_id not in cls.__output_medium:
            return result

        result = cls.__output_medium[input_project_id]

        return result

    @classmethod
    def add_project_id(cls, input_project_id: uuid.UUID) -> None:
        """
        Adds a project to the console

        PARAMETERS:
        -----------

            cls:
                Represents the Console class itself

            input_project_id: uuid.UUID
                Unique Project ID in which to be added to console

        RETURNS:
        --------

            None

        """
        if (input_project_id in cls.__output_filter) or (input_project_id in cls.__write_tags) or (input_project_id in cls.__output_medium) or (input_project_id in cls.__output_file):
            return

        cls.__output_filter[input_project_id] = {}
        cls.__write_tags[input_project_id] = {}
        cls.__output_medium[input_project_id] = "CONSOLE"
        cls.__output_file[input_project_id] = ""

    @classmethod
    def remove_project_id(cls, input_project_id: uuid.UUID) -> None:
        """
        Removes a project from the console

        PARAMETERS:
        -----------

            cls:
                Represents the Console class itself

            input_project_id: uuid.UUID
                Unique Project ID in which to be removed from the console

        RETURNS:
        --------

            None

        """
        if input_project_id in cls.__output_filter:
            cls.__output_filter.pop(input_project_id)
        if input_project_id in cls.__write_tags:
            cls.__write_tags.pop(input_project_id)
        if input_project_id in cls.__output_medium:
            cls.__output_medium.pop(input_project_id)
        if input_project_id in cls.__output_file:
            cls.__output_file.pop(input_project_id)

    @classmethod
    def __print_blender(cls,input_message: str) -> None:
        """
        Output a message to the blender python console

        PARAMETERS:
        -----------

            cls:
                Represents the Console class itself

            input_message: str
                The message string to write out to the blender python console

        RETURNS:
        --------

            None

        """
        available_windows: List[bpy.types.Window] = bpy.context.window_manager.windows
        current_screen: bpy.types.Screen = None
        available_areas : List[bpy.types.Area] = []
        #target_info: Dict[str,Any] = {}

        for current_window in available_windows:
            current_screen = current_window.screen
            available_areas = current_screen.areas

            for current_area in available_areas:
                if current_area.type == "CONSOLE":
                    #target_info = {
                    #    "window":current_window,
                    #    "screen":current_screen,
                    #    "area":current_area
                    #}
                    #bpy.ops.console.scrollback_append(target_info,text=input_message,type="OUTPUT")
                    bpy.ops.console.scrollback_append(text=input_message,type="OUTPUT")

    @classmethod
    def __print_file(cls, input_message: str, input_filename: str) -> None:
        """
        Appends a message to a destination file

        PARAMETERS:
        -----------

            cls:
                Represents the Console class itself

            input_message: str
                The message string to write out to the file

            input_filename: str
                Location of the file to write out to

        RETURNS:
        --------

            None

        """
        with open(input_filename,"a") as output_file:
            output_file.write(input_message)

    @classmethod
    def write(cls,input_project_id: uuid.UUID, input_message: str) -> None:
        """
        Outputs a message if project's write tags meets its output filters

        PARAMETERS:
        -----------

            cls:
                Represents the Console class itself

            input_project_id: uuid.UUID
                Unique Project ID to compare its write tags to its output filters

            input_message: str
                The message string to write out to the project's set medium

        RETURNS:
        --------

            None

        """

        #We need the Filter and Tag information before we go any further
        if (input_project_id not in cls.__output_filter) or (input_project_id not in cls.__write_tags) or (input_project_id not in cls.__output_medium) or (input_project_id not in cls.__output_file):
            return

        can_write: bool = False
        write_key: str = ""
        write_value: int = 0
        output_message: str = f"[PROJECT UUID \"{str(input_project_id)}\", TAGS {cls.__write_tags[input_project_id]}] - {input_message}"

        #Determine if message is to be written in screen
        #No filter or Tags = All Permitted
        if(cls.__output_filter[input_project_id] != {}) and (cls.__write_tags[input_project_id] != {}):
            for write_key, write_value in cls.__write_tags[input_project_id].items():
                if write_key in cls.__output_filter[input_project_id]:
                    if write_value <= cls.__output_filter[input_project_id][write_key]:
                        can_write = True
                        break
        else:
            can_write = True

        if can_write is True:
            if cls.__output_medium[input_project_id] == "CONSOLE":
                print(output_message)
            if cls.__output_medium[input_project_id] == "BLENDER":
                cls.__print_blender(output_message)
            if cls.__output_medium[input_project_id] == "FILE":
                cls.__print_file(output_message,cls.__output_file[input_project_id])

    @classmethod
    def register(cls):
        """
        Reserves space for system messages. UUID = None

        PARAMETERS:
        -----------

            cls:
                Represents the class itself.

        RETURNS:
        --------

            None
        """
        cls.__output_filter = {
            None:{}
        }
        cls.__write_tags = {
            None:{}
        }
        cls.__output_medium = {
            None:"CONSOLE"
        }
        cls.__output_file = {
            None:""
        }
