import bpy
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper, ExportHelper

class FMR_OT_ImportScaleList_OP(Operator, ImportHelper):
    bl_idname = "file.import_scale_list"
    bl_label = "Import a Scale List"
    bl_description = "Import a JSON File with custom character scalings"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        wm = context.window_manager
        item = wm.scale_list.add()
        item.name = "Fritzi"
        item.scale = 0.4

        for area in bpy.context.screen.areas:
            area.tag_redraw()
        
        print(self.filepath)

        return {'FINISHED'}


class FMR_OT_ExportScaleList_OP(Operator, ExportHelper):
    bl_idname = "file.export_scale_list"
    bl_label = "Export a Scale List"
    bl_description = "Export a JSON File with custom character scalings"
    bl_option = {"REGISTER", "UNDO"}

    def execute(self, context):
        print(self.filepath)
        return {'FINISHED'}

class FMR_OT_AddCharacterScale_OP(Operator):
    bl_idname = "object.add_character_scale"
    bl_label = "+"
    bl_description = "Add a character and its scaling to the scale list"
    bl_option = {"REGISTER", "UNDO"}
    def execute(self, context):
        return {'FINISHED'}

class FMR_OT_RemoveCharacterScale_OP(Operator):
    bl_idname = "object.remove_character_scale"
    bl_label = "-"
    bl_description = "Remove a character and its scaling from the scale list"
    bl_option = {"REGISTER", "UNDO"}
    def execute(self, context):
        return {'FINISHED'}


def register():
    bpy.utils.register_class(FMR_OT_ImportScaleList_OP)
    bpy.utils.register_class(FMR_OT_ExportScaleList_OP)
    bpy.utils.register_class(FMR_OT_AddCharacterScale_OP)
    bpy.utils.register_class(FMR_OT_RemoveCharacterScale_OP)

def unregister():
    bpy.utils.unregister_class(FMR_OT_RemoveCharacterScale_OP)
    bpy.utils.unregister_class(FMR_OT_AddCharacterScale_OP)
    bpy.utils.unregister_class(FMR_OT_ExportScaleList_OP)
    bpy.utils.unregister_class(FMR_OT_ImportScaleList_OP)