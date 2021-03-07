from bpy.types import Operator
from bpy.props import StringProperty
from typing import Dict,Any
from . import Console, EventManager

#==================================================#
#Operator Shell Class
#==================================================#
class OperatorShell(Operator):
    
    EventID: StringProperty()

    def CompiledExecute(self,Context) -> None:
        Console.WriteTags = {"OPERATOR":1}
        Console.Write("Button "+str(self.__class__)+" Pressed!")

        if (self.EventID != ""):

            GeneratedEvent : Dict[str, Any] = {
                "EVENT_ID":self.EventID,
                "OBJECT_TYPE":"BUTTON",
                "CONTEXT":Context,
                "EVENT_TYPE":"BUTTON_PRESSED"
            }
            
            EventManager.HandleEvent(GeneratedEvent)

    def execute(self,Context) -> Any:
        self.CompiledExecute(Context)
        return {'FINISHED'}