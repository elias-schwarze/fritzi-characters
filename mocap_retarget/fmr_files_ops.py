import bpy
import os

from bpy.types import Operator, OperatorFileListElement, PropertyGroup
from bpy.props import CollectionProperty, StringProperty

from .fmr_settings import Settings

from bpy_extras.io_utils import ImportHelper

class FMR_OT_SelectBVHs_OP(Operator, ImportHelper):
    bl_idname = "retarget.select_bvhs"
    bl_label = "Select BVHs"
    files: CollectionProperty(name="File Path", type=OperatorFileListElement)
    directory:  StringProperty(subtype='DIR_PATH')

    filename_ext = ""

    def execute(self, context):
        wm = context.window_manager

        
        wm.bvh_files.clear()

        directory = self.directory
        for file_elem in self.files:
            file = wm.bvh_files.add()
            file.name = file_elem.name
            filepath = os.path.join(directory, file_elem.name)
            file.filepath = filepath
            print(filepath)
        return {'FINISHED'}

class FileList(PropertyGroup):
    name : StringProperty()
    filepath : StringProperty()

class FMR_OT_AddBvh_OP(Operator, ImportHelper):
    bl_idname = "object.add_bvh"
    bl_label = "+"
    bl_description = "Add a bvh file to the list"
    bl_option = {"REGISTER", "UNDO"}

    files: CollectionProperty(name="File Path", type= OperatorFileListElement)
    directory: StringProperty(subtype='DIR_PATH')

    filename_ext = ""

    def execute(self, context):
        wm = context.window_manager

        directory = self.directory
        for file_elem in self.files:
            file = wm.bvh_files.add()
            file.name = file_elem.name
            filepath = os.path.join(directory, file_elem.name)
            file.filepath = filepath

        return {'FINISHED'}

class FMR_OT_RemoveBvh_OP(Operator):
    bl_idname = "retarget.remove_bvh"
    bl_label = "-"
    bl_description = "Remove a BVH from the list"
    bl_option = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.window_manager.bvh_files

    def execute(self, context):
        wm = context.window_manager
        bvh_files = wm.bvh_files
        index = wm.bvh_files_index
        bvh_files.remove(index)
        wm.bvh_files_index = min(max(0, index - 1), len(bvh_files) - 1)

        return {'FINISHED'}

class FMR_OT_SelectCharacter_OP(Operator, ImportHelper):
    bl_idname = "retarget.select_char_file"
    bl_label = "Load Character"
    bl_description = "Select the character Rig File on which to retarget the MoCap files"
    bl_option = {"REGISTER", "UNDO"}

    def execute(self, context):
        path = self.filepath
        file = os.path.basename(path)
        root, ext = os.path.splitext(path)

        wm = context.window_manager
        

        print(file)
        print(path)
        print(ext)

        if file and ext == '.blend':
            wm.char_file_path = path
            bpy.ops.wm.open_mainfile(filepath=path)


        return {'FINISHED'}


def register():
    bpy.utils.register_class(FMR_OT_SelectBVHs_OP)
    bpy.utils.register_class(FileList)
    bpy.utils.register_class(FMR_OT_AddBvh_OP)
    bpy.utils.register_class(FMR_OT_RemoveBvh_OP)
    bpy.utils.register_class(FMR_OT_SelectCharacter_OP)

def unregister():
    bpy.utils.unregister_class(FMR_OT_SelectCharacter_OP)
    bpy.utils.unregister_class(FMR_OT_RemoveBvh_OP)
    bpy.utils.unregister_class(FMR_OT_AddBvh_OP)
    bpy.utils.unregister_class(FileList)
    bpy.utils.unregister_class(FMR_OT_SelectBVHs_OP)