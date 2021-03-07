from bpy.types import Panel
from typing import List, Dict, Any
from . import Engine

#==================================================#
#Panel Shell Class
#==================================================#
class PanelShell(Panel):
    Content: List[Dict[str, Any]] = []

    #Footnote to be replaced with a generated function
    def CompiledDraw(self,Context) -> None:
        pass

    #Occurs whenever the panel gets drawn
    def draw(self,Context) -> None:
        #Content array holds priority over a compiled draw function
        if (self.Content != []):
            Engine.Draw(self,Context,self.Content)
        else:
            self.CompiledDraw(Context)  