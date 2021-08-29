"""================================================================================================
This module handles project messaging intelligently allowing for programmers the ability to debug
their project. This module can filter and adjust the verbosity of programming messages allowing
developers to control the detail and category of the code that occurs in debug output.

This offers a more flexible tool than a simple print to console.

CLASSES:
    Console
================================================================================================"""
from typing import Dict, List, Any # pylint: disable=unused-import
import bpy

#==================================================#
#RAD GUI Console
#==================================================#
class Console():
    """
    This class is to intelligently output messages to the appropriate medium.

    ATTRIBUTES:
    -----------

        _output_filter: Dict[ str,Dict[ str,int ] ]
            Filter of output. Limiting any message to a certain number
            of categories up to a certain verbosity level.
            [project_id] --> {"category label",verbosity level}

        _write_tags: Dict[ str,Dict[str,int] ]
            The category and verbosity level of output by project.
            [project_id] --> {"category label",verbosity level}

        _output_medium: Dict[ str,str ]
            The output medium per project.
            Valid mediums are:
                * CONSOLE   - Standard OS console output
                * BLENDER   - Blender's internal python console
                * FILE      - Plain Text File

        _output_file: Dict[ str,str ]
            The path to the file being written to by project id.

    METHODS:
    --------

        set_write_tags: None
        set_filter: None
        set_medium: None
        add_project_id: None
        remove_project_id: None
        _print_blender: None
        _print_file: None
        write: None

    """
    _output_filter: Dict[ str,Dict[ str,int ] ] = {}
    _write_tags: Dict[ str,Dict[str,int] ] = {}
    _output_medium: Dict[ str,str ] = {}
    _output_file: Dict[ str,str ] = {}

    @classmethod
    def set_write_tags(cls, input_project_id: str, input_tags: Dict[ str,int ]) -> None:
        """
        Set the writing tags for radgui console output.
        These tags will be used with console.write

        PARAMETERS:
        -----------

            cls:
                Represents the Console class itself

            input_project_id: str
                Unique Project ID in which write tags are being set

            input_tags: Dict[ str,int ]
                Defines the write tags the project will use for output
                The category will be the key and its value will be the level of
                verbosity. Higher values represent more verbose messages.

        RETURNS:
        --------

            None

        """
        input_project_id = input_project_id.strip()

        if input_project_id == "":
            return

        if input_project_id not in cls._write_tags:
            return

        cls._write_tags[input_project_id] = input_tags

    @classmethod
    def set_filter(cls, input_project_id: str, input_filters: Dict[ str,int ]) -> None:
        """
        Set the filters for project output by category and level of verbosity.
        These filters will be used with console.write

        PARAMETERS:
        -----------

            cls:
                Represents the Console class itself

            input_project_id: str
                Unique Project ID in which write filters are being set

            input_filters: Dict[ str,int ]
                Defines the filters the project will use for output
                The category will be the key and its value will be the level of
                verbosity. Higher values represent more verbose messages.

        RETURNS:
        --------

            None

        """
        if input_project_id not in cls._output_filter:
            return

        cls._output_filter[input_project_id] = input_filters

    @classmethod
    def set_medium(cls, input_project_id: str, input_medium: str, input_filename: str = "") -> None:
        """
        Sets the medium of output the project will use for output.

        PARAMETERS:
        -----------

            cls:
                Represents the Console class itself

            input_project_id: str
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
        input_project_id = input_project_id.strip()
        input_medium = input_medium.strip()
        input_filename = input_filename.strip()

        if input_project_id not in cls._output_medium:
            return

        if input_medium not in ["CONSOLE","BLENDER","FILE"]:
            return

        if (input_medium == "FILE") and (input_filename == ""):
            return

        if (input_medium == "FILE") and (input_filename != ""):
            cls._output_file[input_project_id] = input_filename

        cls._output_medium[input_project_id] = input_medium

    @classmethod
    def add_project_id(cls, input_project_id: str) -> None:
        """
        Adds a project to the console

        PARAMETERS:
        -----------

            cls:
                Represents the Console class itself

            input_project_id: str
                Unique Project ID in which to be added to console

        RETURNS:
        --------

            None

        """
        input_project_id = input_project_id.strip()

        if (input_project_id in cls._output_filter) or (input_project_id in cls._write_tags) or (input_project_id in cls._output_medium) or (input_project_id in cls._output_file):
            return

        cls._output_filter[input_project_id] = {}
        cls._write_tags[input_project_id] = {}
        cls._output_medium[input_project_id] = "CONSOLE"
        cls._output_file[input_project_id] = ""

    @classmethod
    def remove_project_id(cls, input_project_id) -> None:
        """
        Removes a project from the console

        PARAMETERS:
        -----------

            cls:
                Represents the Console class itself

            input_project_id: str
                Unique Project ID in which to be removed from the console

        RETURNS:
        --------

            None

        """
        input_project_id = input_project_id.strip()

        if input_project_id in cls._output_filter:
            cls._output_filter.pop(input_project_id)
        if input_project_id in cls._write_tags:
            cls._write_tags.pop(input_project_id)
        if input_project_id in cls._output_medium:
            cls._output_medium.pop(input_project_id)
        if input_project_id in cls._output_file:
            cls._output_file.pop(input_project_id)

    @classmethod
    def _print_blender(cls,input_message: str) -> None:
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
    def _print_file(cls, input_message: str, input_filename: str) -> None:
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
    def write(cls,input_project_id: str, input_message: str) -> None:
        """
        Outputs a message if project's write tags meets its output filters

        PARAMETERS:
        -----------

            cls:
                Represents the Console class itself

            input_project_id: str
                Unique Project ID to compare its write tags to its output filters

            input_message: str
                The message string to write out to the project's set medium

        RETURNS:
        --------

            None

        """

        #We need the Filter and Tag information before we go any further
        if (input_project_id in cls._output_filter) or (input_project_id in cls._write_tags) or (input_project_id in cls._output_medium) or (input_project_id in cls._output_file):
            return

        can_write: bool = False
        write_key: str = ""
        write_value: int = 0
        output_message: str = f"[NAMESPACE \"{input_project_id}\", TAGS {cls._write_tags[input_project_id]}] - {input_message}"

        #Determine if message is to be written in screen
        #No filter or Tags = All Permitted
        if(cls._output_filter[input_project_id] != {}) and (cls._write_tags[input_project_id] != {}):
            for write_key, write_value in cls._write_tags[input_project_id].items():
                if write_key in cls._output_filter[input_project_id]:
                    if write_value <= cls._output_filter[input_project_id][write_key]:
                        can_write = True
                        break
        else:
            can_write = True

        if can_write is True:
            if cls._output_medium[input_project_id] == "CONSOLE":
                print(output_message)
            if cls._output_medium[input_project_id] == "BLENDER":
                cls._print_blender(output_message)
            if cls._output_medium[input_project_id] == "FILE":
                cls._print_file(output_message,cls._output_file[input_project_id])
