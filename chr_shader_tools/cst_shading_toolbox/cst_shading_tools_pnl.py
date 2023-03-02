import bpy

from bpy.props import FloatVectorProperty
class CST_PT_ShadingTools_pnl(bpy.types.Panel):

    bl_label = "Shading Tools"
    bl_category = "FCHAR"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_options = {"DEFAULT_CLOSED"}

    bpy.types.WindowManager.shader_color = FloatVectorProperty(name= "Shader Color", subtype= 'COLOR', size=4, default=(0.5, 0.5, 0.5, 1.0))

    def draw(self, context):
        wm = context.window_manager
        layout = self.layout

        
        layout.operator("settings.choose_shader_path")
        layout.operator("settings.choose_eye_shader_path")
        layout.operator("cst.link_character_shader")
        layout.operator("cst.link_eye_shader")
        layout.separator()
        #layout.label(text="Skin Shaders")
        #layout.operator("cst.create_h1_shader")
        #layout.operator("cst.create_h2_shader")
        #layout.operator("cst.create_h3_shader")
        #layout.operator("cst.create_h4_shader")
        #layout.separator()
        layout.operator("cst.create_mouthinside_shader")
        layout.operator("cst.create_tongue_shader")
        layout.separator()
        layout.label(text="Cloth Shader")
        layout.prop(wm, "shader_color")
        layout.operator("cst.create_cloth_shader")


def register():
    bpy.utils.register_class(CST_PT_ShadingTools_pnl)

def unregister():
    bpy.utils.unregister_class(CST_PT_ShadingTools_pnl)