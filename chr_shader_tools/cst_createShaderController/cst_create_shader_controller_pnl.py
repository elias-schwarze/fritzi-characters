import bpy
from bpy.props import StringProperty


class CST_PT_CreateShaderController_pnl(bpy.types.Panel):
    bl_label = "Shader Controller"
    bl_category = "FCHAR Shader Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"DEFAULT_CLOSED"}

    bpy.types.Scene.character_name = StringProperty(name="Character Name")

    def draw(self, context):
        scene = context.scene
        layout = self.layout

        layout.prop(scene, "character_name")
        layout.operator("object.create_shader_controller")

def register():
    bpy.utils.register_class(CST_PT_CreateShaderController_pnl)

def unregister():
    bpy.utils.unregister_class(CST_PT_CreateShaderController_pnl)