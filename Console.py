import bpy
from typing import Dict, List, Any

#==================================================#
#RAD GUI Console
#==================================================#
class Console():
    __OutputFilter: Dict[str,Dict[str,int]] = {}
    __WriteTags: Dict[str,Dict[str,int]] = {}
    __OutputMedium: Dict[str,str] = {}
    __OutputFile: Dict[str,str] = {}

    @classmethod
    def Set_Tags(cls, InputNamespace: str, InputTags: Dict[str,int]) -> None:
        if InputNamespace not in cls.__WriteTags:
            return

        cls.__WriteTags[InputNamespace] = InputTags

    @classmethod
    def Set_Filter(cls, InputNamespace: str, InputFilters: Dict[str,int]) -> None:
        if InputNamespace not in cls.__OutputFilter:
            return

        cls.__OutputFilter[InputNamespace] = InputFilters

    @classmethod
    def Set_Medium(cls, InputNamespace: str, InputMedium: str, InputFilename: str = "") -> None:
        if InputNamespace not in cls.__OutputMedium:
            return

        if InputMedium not in ["CONSOLE","BLENDER","FILE"]:
            return

        if (InputMedium == "FILE") and (InputFilename == ""):
            return

        cls.__OutputMedium[InputNamespace] = InputMedium

    @classmethod
    def Add_Namespace(cls, InputNamespace: str) -> None:
        if (InputNamespace in cls.__OutputFilter) or (InputNamespace in cls.__WriteTags) or (InputNamespace in cls.__OutputMedium) or (InputNamespace in cls.__OutputFile):
            return

        cls.__OutputFilter[InputNamespace] = {}
        cls.__WriteTags[InputNamespace] = {}
        cls.__OutputMedium[InputNamespace] = "CONSOLE"
        cls.__OutputFile[InputNamespace] = ""

    @classmethod
    def Remove_Namespace(cls, InputNamespace) -> None:
        if InputNamespace in cls.__OutputFilter:
            cls.__OutputFilter.pop(InputNamespace)
        if InputNamespace in cls.__WriteTags:
            cls.__WriteTags.pop(InputNamespace)
        if InputNamespace in cls.__OutputMedium:
            cls.__OutputMedium.pop(InputNamespace)
        if InputNamespace in cls.__OutputFile:
            cls.__OutputFile.pop(InputNamespace)

    @classmethod
    def __PrintBlender(cls,InputMessage: str) -> None:
        AvailableWindows: List[bpy.types.Window] = bpy.context.window_manager.windows
        CurrentScreen: bpy.types.Screen = None
        AvailableAreas : List[bpy.types.Area] = []
        Target: Dict[str,Any] = {}

        for CurrentWindow in AvailableWindows:
            CurrentScreen = CurrentWindow.screen
            AvailableAreas = CurrentScreen.areas

            for CurrentArea in AvailableAreas:
                if CurrentArea.type == "CONSOLE":
                    Target = {
                        "window":CurrentWindow,
                        "screen":CurrentScreen,
                        "area":CurrentArea
                    }
                    bpy.ops.console.scrollback_append(Target,text=InputMessage,type="OUTPUT")

    @classmethod
    def __PrintFile(cls, InputMessage: str, InputFilename: str) -> None:
        with open(InputFilename,"a") as OutputFile:
            OutputFile.write(InputMessage)

    @classmethod
    def Write(cls,InputNamespace: str, InputMessage: str) -> None:

        #We need the Filter and Tag information before we go any further
        if (InputNamespace in cls.__OutputFilter) or (InputNamespace in cls.__WriteTags) or (InputNamespace in cls.__OutputMedium) or (InputNamespace in cls.__OutputFile):
            return

        CanWrite: bool = False
        WriteKey: str = ""
        WriteValue: int = 0
        OutputMessage: str = "[NAMESPACE \"{}\", TAGS {}] - {}".format(InputNamespace,cls.__WriteTags[InputNamespace],InputMessage)

        #Determine if message is to be written in screen
        #No filter or Tags = All Permitted
        if(cls.__OutputFilter[InputNamespace] != {}) and (cls.__WriteTags[InputNamespace] != {}):
            for WriteKey, WriteValue in cls.__WriteTags[InputNamespace].items():
                if (WriteKey in cls.__OutputFilter[InputNamespace]):
                    if (WriteValue <= cls.__OutputFilter[InputNamespace][WriteKey]):
                        CanWrite = True
                        break
        else:
            CanWrite = True
        
        if(CanWrite == True):
            if cls.__OutputMedium[InputNamespace] == "CONSOLE":
                print(OutputMessage)
            if cls.__OutputMedium[InputNamespace] == "BLENDER":
                cls.__PrintBlender(OutputMessage)
            if cls.__OutputMedium[InputNamespace] == "FILE":
                cls.__PrintFile(OutputMessage,cls.__OutputFile[InputNamespace])