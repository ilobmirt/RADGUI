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
from .RADGUI import RADGUI_FACTORY, RADGUI_CONSOLE

#Do some global activities here like loading the JSON Panel File
strCurrentFolder = os.path.dirname(__file__)
RADGUI_FACTORY.LoadJSON(os.path.join(strCurrentFolder,"TestPanel.JSON"))

#Limit the Output of the console by setting a TAG Filter
RADGUI_CONSOLE.OutputFilter = {
    "RADGUI_FACTORY":0,
    "RADGUI_ENGINE":0
}

def register():
    RADGUI_FACTORY.register()

def unregister():
    RADGUI_FACTORY.unregister()

if __name__ == "__main__":
    register()