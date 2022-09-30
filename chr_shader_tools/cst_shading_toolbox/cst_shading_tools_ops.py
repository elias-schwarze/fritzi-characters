import bpy

from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper
from ...mocap_retarget.fmr_settings import Settings

class CST_OT_ChooseShaderPath_OP(Operator, ImportHelper):
    bl_idname = "settings.choose_shader_path"
    bl_label = "Select Character Shader"
    bl_description = "Select the .blend file with the Fritzi Character Shader"

    def execute(self, context):
        settings = Settings()
        settings.set_setting("shader_path", self.filepath)

        self.report({'INFO'}, "Path set!")

        return {'FINISHED'}

class CST_OT_LinkCharacterShader_OP(Operator):
    bl_idname = "cst.link_character_shader"
    bl_label = "Link Character Shader"
    bl_description = "Links the Character Shader into the file."

    def execute(self, context):
        settings = Settings()
        filepath = settings.get_setting("shader_path")

        with bpy.data.libraries.load(filepath, link = True, relative = True) as (data_from, data_to):
            data_to.node_groups = ["shader-Fritzi_Characters"]

        return {'FINISHED'}

def add_shader(context, rgb: tuple[float, float, float, float], shadowHSV: tuple[float, float, float] = (5.0, 1.0, 1.0)):
    mat = context.material
    tree = mat.node_tree
    for node in tree.nodes:
        node.select = False
    rgb_node = mat.node_tree.nodes.new("ShaderNodeRGB")
    hsv_node = mat.node_tree.nodes.new("ShaderNodeHueSaturation")
    fritzi_shader_node = mat.node_tree.nodes.new("ShaderNodeGroup")    
    fritzi_shader_node.node_tree = bpy.data.node_groups.get("shader-Fritzi_Characters")

    # Node linking

    tree.links.new(rgb_node.outputs["Color"], hsv_node.inputs["Color"])
    tree.links.new(hsv_node.outputs["Color"], fritzi_shader_node.inputs["MainColor"])

    # Position

    rgb_node.location = (-165, 0)
    fritzi_shader_node.location = (175, 0)
    fritzi_shader_node.width = 200

    # Settings

    rgb_node.outputs[0].default_value = rgb
    fritzi_shader_node.inputs["ShadowHue"].default_value = shadowHSV[0]
    fritzi_shader_node.inputs["ShadowSaturation"].default_value = shadowHSV[1]
    fritzi_shader_node.inputs["ShadowValue"].default_value = shadowHSV[2]


class CST_OT_CreateH1Shader_OP(Operator):
    bl_idname = "cst.create_h1_shader"
    bl_label = "H1 Skin Shader"
    bl_description = "Creates the Skin Shader Setup for the H1 Skin Tone"

    def execute(self, context):

        add_shader(context, (1.000000, 0.791298, 0.637597, 1.000000), (4.6, 1.61, 0.72))
        
        return bpy.ops.transform.translate('INVOKE_DEFAULT')

class CST_OT_CreateH2Shader_OP(Operator):
    bl_idname = "cst.create_h2_shader"
    bl_label = "H2 Skin Shader"
    bl_description = "Creates the Skin Shader Setup for the H2 Skin Tone"

    def execute(self, context):
        add_shader(context, (1.000000, 0.701102, 0.558341, 1.000000), (4.75, 1.475, 0.63))
        return bpy.ops.transform.translate('INVOKE_DEFAULT')

class CST_OT_CreateH3Shader_OP(Operator):
    bl_idname = "cst.create_h3_shader"
    bl_label = "H3 Skin Shader"
    bl_description = "Creates the Skin Shader Setup for the H3 Skin Tone"

    def execute(self, context):
        add_shader(context, (0.973445, 0.637597, 0.508881, 1.000000), (4.8, 1.25, 0.6))
        return bpy.ops.transform.translate('INVOKE_DEFAULT')

class CST_OT_CreateH4Shader_OP(Operator):
    bl_idname = "cst.create_h4_shader"
    bl_label = "H4 Skin Shader"
    bl_description = "Creates the Skin Shader Setup for the H4 Skin Tone"

    def execute(self, context):
        add_shader(context, (1.000000, 0.846873, 0.701102, 1.000000), (4.6, 1.61, 0.63))
        return bpy.ops.transform.translate('INVOKE_DEFAULT')

class CST_OT_CreateClothShader_OP(Operator):
    bl_idname = "cst.create_cloth_shader"
    bl_label = "Cloth Shader"
    bl_description = "Creates a cloth shader setup with the given color"

    def execute(self, context):
        add_shader(context, context.window_manager.shader_color)
        return bpy.ops.transform.translate('INVOKE_DEFAULT')


def register():
    bpy.utils.register_class(CST_OT_ChooseShaderPath_OP)
    bpy.utils.register_class(CST_OT_LinkCharacterShader_OP)
    bpy.utils.register_class(CST_OT_CreateH1Shader_OP)
    bpy.utils.register_class(CST_OT_CreateH2Shader_OP)
    bpy.utils.register_class(CST_OT_CreateH3Shader_OP)
    bpy.utils.register_class(CST_OT_CreateH4Shader_OP)
    bpy.utils.register_class(CST_OT_CreateClothShader_OP)

def unregister():
    bpy.utils.unregister_class(CST_OT_CreateClothShader_OP)
    bpy.utils.unregister_class(CST_OT_CreateH4Shader_OP)
    bpy.utils.unregister_class(CST_OT_CreateH3Shader_OP)
    bpy.utils.unregister_class(CST_OT_CreateH2Shader_OP)
    bpy.utils.unregister_class(CST_OT_CreateH1Shader_OP)
    bpy.utils.unregister_class(CST_OT_LinkCharacterShader_OP)
    bpy.utils.unregister_class(CST_OT_ChooseShaderPath_OP)