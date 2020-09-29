#This file  is to show off the RADGUI_EVENT_MANAGER
#These classes were mentioned in TestPanel.JSON

#Event Functions called by RADGUI_EVENT_MANAGER
#Should be a Class Method of the format...
#def FunctionName(cls,InputEvent: Dict[str, Any]) -> None:

from typing import List, Dict, Any
from .RADGUI import RADGUI_EVENT_MANAGER

#==================================================#
#EXAMPLE CLASS #1
#==================================================#
class EXAMPLE_CLASS1():
    @classmethod
    def FunctionA(cls,InputEvent: Dict[str, Any]) -> None:
        print("\n(EXAMPLE_CLASS1.FunctionA):")
        print("Event {} Called from {}".format(InputEvent["EVENT_TYPE"],InputEvent["EVENT_ID"]))
        if("VALUE" in InputEvent):
            print("Value = {}".format(InputEvent["VALUE"]))

    @classmethod
    def FunctionB(cls,InputEvent: Dict[str, Any]) -> None:
        print("\n(EXAMPLE_CLASS1.FunctionB):")
        print("Event {} Called from {}".format(InputEvent["EVENT_TYPE"],InputEvent["EVENT_ID"]))
        if("VALUE" in InputEvent):
            print("Value = {}".format(InputEvent["VALUE"]))

#==================================================#
#EXAMPLE CLASS #2
#==================================================#
class EXAMPLE_CLASS2():
    @classmethod
    def FunctionA(cls,InputEvent: Dict[str, Any]) -> None:
        print("\n(EXAMPLE_CLASS2.FunctionA):")
        print("Event {} Called from {}".format(InputEvent["EVENT_TYPE"],InputEvent["EVENT_ID"]))
        if("VALUE" in InputEvent):
            print("Value = {}".format(InputEvent["VALUE"]))

    @classmethod
    def FunctionB(cls,InputEvent: Dict[str, Any]) -> None:
        print("\n(EXAMPLE_CLASS2.FunctionB):")
        print("Event {} Called from {}".format(InputEvent["EVENT_TYPE"],InputEvent["EVENT_ID"]))
        if("VALUE" in InputEvent):
            print("Value = {}".format(InputEvent["VALUE"]))

#==================================================#
#EXAMPLE CLASS #3
#==================================================#

class Events_Example():

    @classmethod
    def Remove_A_Events(cls,InputEvent: Dict[str,Any]) -> None:
        print("\n(Events_Example.Remove_A_Events): Removing events for button A")
        RADGUI_EVENT_MANAGER.RemoveEvent("CUSTOMCLASSES.Events_Example.Remove_A_Events")

    @classmethod
    def Remove_B_Events(cls,InputEvent: Dict[str,Any]) -> None:
        print("\n(Events_Example.Remove_B_Events): Removing events for button B")
        RADGUI_EVENT_MANAGER.RemoveEvent("CUSTOMCLASSES.Events_Example.Remove_B_Events")

    @classmethod
    def Remove_C_Events(cls,InputEvent: Dict[str,Any]) -> None:
        print("\n(Events_Example.Remove_C_Events): Removing events for button C")
        RADGUI_EVENT_MANAGER.RemoveEvent("CUSTOMCLASSES.Events_Example.Remove_C_Events")

    @classmethod
    def Register_ALL_Events(cls,InputEvent: Dict[str,Any]) -> None:
        print("\n(Events_Example.Register_ALL_Events): Registering Events")

        Events_A: List[Dict[str,Any]] = [
            {
                "EVENT_ID":"btnEVENTSA"
            },
            {
                "EVENT_ID":"btnCLEAR"
            }
        ]

        Events_B: List[Dict[str,Any]] = [
            {
                "EVENT_ID":"btnEVENTSB"
            },
            {
                "EVENT_ID":"btnCLEAR"
            }
        ]

        Events_C: List[Dict[str,Any]] = [
            {
                "EVENT_ID":"btnEVENTSC"
            },
            {
                "EVENT_ID":"btnCLEAR"
            }
        ]

        print("-- Button A")
        RADGUI_EVENT_MANAGER.AddEvent("CUSTOMCLASSES.Events_Example.Remove_A_Events",Events_A)
        print("-- Button B")
        RADGUI_EVENT_MANAGER.AddEvent("CUSTOMCLASSES.Events_Example.Remove_B_Events",Events_B)
        print("-- Button C")
        RADGUI_EVENT_MANAGER.AddEvent("CUSTOMCLASSES.Events_Example.Remove_C_Events",Events_C)