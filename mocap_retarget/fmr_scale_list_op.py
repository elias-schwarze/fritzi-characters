import bpy
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper, ExportHelper
from bpy.props import StringProperty, FloatProperty
from .fmr_scale_list_io import ScaleListDict

class FMR_OT_ImportScaleList_OP(Operator, ImportHelper):
    bl_idname = "file.import_scale_list"
    bl_label = "Import a Scale List"
    bl_description = "Import a JSON File with custom character scalings"
    bl_options = {"REGISTER", "UNDO"}

    filter_glob: StringProperty(default='*.json', options={'HIDDEN'})
    filename_ext: StringProperty(default=".json")

    def execute(self, context):
        wm = context.window_manager
        item = wm.scale_list.add()
        item.name = "Fritzi"
        item.scale = 0.4

        scale_list_io = ScaleListDict()

        scale_list_io.load_scale_list(self.filepath)

        for area in bpy.context.screen.areas:
            area.tag_redraw()
        
        #print(self.filepath)

        return {'FINISHED'}


class FMR_OT_ExportScaleList_OP(Operator, ExportHelper):
    bl_idname = "file.export_scale_list"
    bl_label = "Export a Scale List"
    bl_description = "Export a JSON File with custom character scalings"
    bl_option = {"REGISTER", "UNDO"}

    filter_glob: StringProperty(default='*.json', options={'HIDDEN'})
    filename_ext: StringProperty(default=".json")

    def execute(self, context):
        wm = context.window_manager
        scale_list_io = ScaleListDict()

        scale_list_io.write_scale_list(self.filepath)
        #print(self.filepath)
        return {'FINISHED'}

class FMR_OT_AddCharacterScale_OP(Operator):
    bl_idname = "object.add_character_scale"
    bl_label = "+"
    bl_description = "Add a character and its scaling to the scale list"
    bl_option = {"REGISTER", "UNDO"}

    char_name: StringProperty(name="Name", description="Name of the character which schould be scaled")
    char_scale: FloatProperty(name="Scale", description="scale which the character should be scaled to on import", default=1.0, min=0.0, max=2.0)

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.label(text="Character Name")
        layout.prop(self, "char_name")
        layout.label(text="Character Scale")
        layout.prop(self,"char_scale")

    def execute(self, context):
        scale_list = ScaleListDict()
        scale_list.set_scale(self.char_name, self.char_scale)
        return {'FINISHED'}

class FMR_OT_RemoveCharacterScale_OP(Operator):
    bl_idname = "object.remove_character_scale"
    bl_label = "-"
    bl_description = "Remove a character and its scaling from the scale list"
    bl_option = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.window_manager.scale_list

    def execute(self, context):
        wm = context.window_manager
        scale_list_UI = wm.scale_list
        scale_list = ScaleListDict()
        index = wm.scale_list_index
        name = scale_list_UI[index].character
        scale_list.remove_scale(key=name)
        wm.scale_list_index = min(max(0, index -1), len(scale_list_UI) - 1)
    
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