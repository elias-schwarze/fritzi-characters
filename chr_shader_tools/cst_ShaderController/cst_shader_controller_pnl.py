import bpy
from bpy.props import PointerProperty, StringProperty


class CST_PT_ShaderController_pnl(bpy.types.Panel):
    bl_label = "Shader Controller"
    bl_category = "FCHAR"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"DEFAULT_CLOSED"}

    bpy.types.WindowManager.character_name = StringProperty(name="Character Name")
    bpy.types.WindowManager.controller_empty = PointerProperty(
        name="Shader Controller", type=bpy.types.Object)
    bpy.types.WindowManager.character_collection = PointerProperty(
        name="Character Collection", type=bpy.types.Collection)

    def draw(self, context):
        
        wm = context.window_manager
        layout = self.layout

        layout.prop(wm, "character_name")
        layout.operator("object.create_shader_controller")

        layout.prop_search(wm, "controller_empty",
                           context.scene, "objects", text="Shader Controller")
        layout.prop_search(wm, "character_collection",
                           bpy.data, "collections", text="Character Collection")
        layout.operator("object.select_shader_controller")


def register():
    bpy.utils.register_class(CST_PT_ShaderController_pnl)


def unregister():
    bpy.utils.unregister_class(CST_PT_ShaderController_pnl)
