import bpy, uuid
from typing import List, Dict, Any
from . import PropertyGroupShell, OperatorShell, PanelShell

#==================================================#
#RADGUI Project
#==================================================#

class Project():

    #Initialize
    def __init__(self):
        self.Namespace: str = "radgui_project{}".format(uuid.uuid4().hex)
        self.Events: Dict[str,Any] = {
            "STRICT":False,
            "CONTENT":{}
        }
        self.PropertyGroups: Dict[str,Any] = {
            "OBJECT":None,
            "SCENE":None
        }
        self.Operators: Dict[str,Any] = {}
        self.Panels: Dict[str,Any] = {}

    #Load project from a Dictionary
    def Set_Dict(self, InputStructure: Dict[str,Any]) -> None:
        pass

    #Convert project to a Dictionary
    def Get_Dict(self) -> Dict[str,Any]:
        
        Result: Dict[Any,Any] = {
            "TYPE":"RADGUI_PROJECT",
            "BODY":{}
        }

        return Result

    #Add a property group
    def Add_PropertyGroup(self,InputScope: str,InputAttributes: Dict[str,Any]) -> None:
        #We can't proceed if scope isnt legal
        if InputScope.upper() not in ["OBJECT","SCENE"]:
            pass

    #Remove a property group
    def Remove_PropertyGroup(self,InputScope: str) -> None:
        #Only bother with the appropriate scope
        if InputScope.upper() in ["OBJECT","SCENE"]:
            bpy.utils.unregister_class(self.PropertyGroups[InputScope.upper()])
            self.PropertyGroups.pop(InputScope.upper())
            
    #Add an operator
    def Add_Operator(self,InputName: str,InputAttributes: Dict[str,Any]) -> None:
        pass

    #Remove an operator
    def Remove_Operator(self,InputName: str) -> None:
        if InputName in self.Operators:
            bpy.utils.unregister_class(self.Operators[InputName])
            self.Operators.pop(InputName)

    #Add a panel
    def Add_Panel(self,InputName: str,InputAttributes: Dict[str,Any]) -> None:
        pass

    #Remove a panel
    def Remove_Panel(self,InputName: str) -> None:
        if InputName in self.Panels:
            bpy.utils.unregister_class(self.Panels[InputName])
            self.Panels.pop(InputName)