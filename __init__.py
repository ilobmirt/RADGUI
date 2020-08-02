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
from .RADGUI import RAD_GUI_FACTORY

#Do some global activities here like loading the JSON Panel File
strCurrentFolder = os.path.dirname(__file__)
RAD_GUI_FACTORY.LoadJSON(os.path.join(strCurrentFolder,"TestPanel.JSON"))

def register():
    RAD_GUI_FACTORY.register()

def unregister():
    RAD_GUI_FACTORY.unregister()

if __name__ == "__main__":
    register()