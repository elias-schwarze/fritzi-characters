import bpy
import os

from bpy.types import Operator, OperatorFileListElement, PropertyGroup
from bpy.props import CollectionProperty, StringProperty

from .fmr_settings import Settings

from bpy_extras.io_utils import ImportHelper

class FMR_OT_SelectBVHs_OP(Operator, ImportHelper):
    bl_idname = "retarget.select_bvhs"
    bl_label = "Import BVHs"
    files: CollectionProperty(name="File Path", type=OperatorFileListElement)
    directory:  StringProperty(subtype='DIR_PATH')

    filename_ext = ""

    def execute(self, context):
        wm = context.window_manager

        wm.bvh_dir = self.directory
        wm.bvh_files.clear()

        directory = self.directory
        for file_elem in self.files:
            file = wm.bvh_files.add()
            file.name = file_elem.name
            filepath = os.path.join(directory, file_elem.name)
            print(filepath)
        return {'FINISHED'}

class FileList(PropertyGroup):
    name : StringProperty()

def register():
    bpy.utils.register_class(FMR_OT_SelectBVHs_OP)
    bpy.utils.register_class(FileList)

def unregister():
    bpy.utils.unregister_class(FileList)
    bpy.utils.unregister_class(FMR_OT_SelectBVHs_OP)