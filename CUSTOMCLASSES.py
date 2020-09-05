#This file  is to show off the RADGUI_EVENT_MANAGER
#These classes were mentioned in TestPanel.JSON

#Event Functions called by RADGUI_EVENT_MANAGER
#Should be a Class Method of the format...
#def FunctionName(cls,InputEvent: Dict[str, Any]) -> None:

from typing import List, Dict, Any

#==================================================#
#EXAMPLE CLASS #1
#==================================================#
class EXAMPLE_CLASS1():
    @classmethod
    def FunctionA(cls,InputEvent: Dict[str, Any]) -> None:
        print("(EXAMPLE_CLASS1.FunctionA):")
        print("Event {} Called from {}".format(InputEvent["EVENT_TYPE"],InputEvent["EVENT_ID"]))

    @classmethod
    def FunctionB(cls,InputEvent: Dict[str, Any]) -> None:
        print("(EXAMPLE_CLASS1.FunctionB):")
        print("Event {} Called from {}".format(InputEvent["EVENT_TYPE"],InputEvent["EVENT_ID"]))

#==================================================#
#EXAMPLE CLASS #2
#==================================================#
class EXAMPLE_CLASS2():
    @classmethod
    def FunctionA(cls,InputEvent: Dict[str, Any]) -> None:
        print("(EXAMPLE_CLASS2.FunctionA):")
        print("Event {} Called from {}".format(InputEvent["EVENT_TYPE"],InputEvent["EVENT_ID"]))

    @classmethod
    def FunctionB(cls,InputEvent: Dict[str, Any]) -> None:
        print("(EXAMPLE_CLASS2.FunctionB):")
        print("Event {} Called from {}".format(InputEvent["EVENT_TYPE"],InputEvent["EVENT_ID"]))