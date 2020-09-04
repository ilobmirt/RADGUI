#Define Plugin Information
bl_info = {
    "name":"RAD GUI Panel Example",
    "description":"Panel generated from the RAD GUI Library",
    "author":"Ilobmirt",
    "version":(1,0),
    "blender":(2,82,0),
    "location":"View3D > UI",
    "support":"COMMUNITY",
    "category":"Object"
}

#Import Libraries
import bpy
import os
from .RADGUI import RADGUI_FACTORY

#Do some global activities here like loading the JSON Panel File
CurrentFolder: str = os.path.dirname(__file__)
RADGUI_FACTORY.LoadJSON(os.path.join(CurrentFolder,"TestPanel.JSON"))

def register():
    RADGUI_FACTORY.Register()

def unregister():
    RADGUI_FACTORY.Unregister()

if __name__ == "__main__":
    register()