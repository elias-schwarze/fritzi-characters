import bpy

from bpy.types import Operator

class CST_OT_CreateShaderController_OP(Operator):
    bl_idname = "object.create_shader_controller"
    bl_label = "Create Shader Controller"
    bl_descritption = "Creates an Empty with controls for the shaders of one character"
    bl_options = {"REGISTER", "UNDO"}

    # should only work in object mode
    @classmethod
    def poll(cls, context):
        obj = bpy.context.object

        if obj:
            if obj.mode == "OBJECT":
                return True

        return False


    def execute(self, context):
        
        wm = bpy.context.window_manager

        characterName = wm.character_name

        if characterName is None:
            self.report({'WARNING'}, "Please give a Character Name!")
            return {'CANCELLED'}

        emptyController = bpy.data.objects.new(characterName + "ShaderController", None)

        bpy.context.scene.collection.objects.link(emptyController)

        emptyController.empty_display_size = 2
        emptyController.empty_display_type = 'PLAIN_AXES'

        rna_ui = emptyController.get('_RNA_UI')
        if rna_ui is None:
            emptyController['_RNA_UI'] = {}
            rna_ui = emptyController['_RNA_UI']

        emptyController["vector_diffuse_mix"] = 0.0

        rna_ui["vector_diffuse_mix"] = {
            "description":"Mix Amount of Vector shading vs Diffuse shading",
            "default":0.0,
            "min":0.0,
            "max":1.0,
            "soft_min":0.0,
            "soft_max":1.0
        }

        emptyController["highlight_amount"] = 0.0

        rna_ui["highlight_amount"] = {
            "description":"Brightness of the highlights",
            "default":0.0,
            "min":0.0,
            "soft_min":0.0
            
        }

        emptyController["highlight_color"] = (1.0, 1.0, 1.0)

        rna_ui["highlight_color"] = {
            "description":"Highlight Color",
            "default": (1.0, 1.0, 1.0),
            "min":0.0,
            "max":1.0,
            "subtype":'COLOR',
            "soft_min":0.0,
            "soft_max":1.0
        }

        emptyController["rimlight_amount"] = 0.0

        rna_ui["rimlight_amount"] = {
            "description":"Brightness of the rimlights",
            "default":0.0,
            "min":0.0,
            "soft_min":0.0
        }

        emptyController["rimlight_color"] = (1.0, 1.0, 1.0)

        rna_ui["rimlight_color"] = {
            "description":"Rimlight Color",
            "default":(1.0, 1.0, 1.0),
            "min":0.0,
            "max":1.0,
            "subtype":'COLOR',
            "soft_min":0.0,
            "soft_max":1.0
        }

        emptyController["advanced_mix_switch"] = 0.0

        rna_ui["advanced_mix_switch"] = {
            "description":"Turns Advanced mixing on and off",
            "default":0.0,
            "min":0.0,
            "max":1.0,
            "soft_min":0.0,
            "soft_max":1.0
        }

        emptyController["advanced_mix_light_amount"] = 0.2

        rna_ui["advanced_mix_light_amount"] = {
            "description":"How much light gets added to the light regions",
            "default":0.2,
            "min":0.0,
            "max":1.0,
            "soft_min":0.0,
            "soft_max":1.0
        }

        emptyController["advanced_mix_light_color"] = (1.0, 1.0, 1.0)

        rna_ui["advanced_mix_light_color"] = {
            "description":"The color of the added Light",
            "default":(1.0, 1.0, 1.0),
            "min":0.0,
            "max":1.0,
            "subtype":'COLOR',
            "soft_min":0.0,
            "soft_max":1.0
        }

        emptyController["advanced_mix_shadow_amount"] = 0.2

        rna_ui["advanced_mix_shadow_amount"] = {
            "description":"How much shadow tint gets multiplied to the dark regions",
            "default":0.2,
            "min":0.0,
            "max":1.0,
            "soft_min":0.0,
            "soft_max":1.0
        }

        emptyController["advanced_mix_shadow_tint"] = (0.0, 0.0, 0.0)

        rna_ui["advanced_mix_shadow_tint"] = {
            "description":"The color of the multiplied shadow tint",
            "default":(0.0, 0.0, 0.0),
            "min":0.0,
            "max":1.0,
            "subtype":'COLOR',
            "soft_min":0.0,
            "soft_max":1.0
        }

        emptyController.property_overridable_library_set('["vector_diffuse_mix"]', True)
        emptyController.property_overridable_library_set('["highlight_amount"]', True)
        emptyController.property_overridable_library_set('["highlight_color"]', True)
        emptyController.property_overridable_library_set('["rimlight_amount"]', True)
        emptyController.property_overridable_library_set('["rimlight_color"]', True)
        emptyController.property_overridable_library_set('["advanced_mix_switch"]', True)
        emptyController.property_overridable_library_set('["advanced_mix_light_amount"]', True)
        emptyController.property_overridable_library_set('["advanced_mix_light_color"]', True)
        emptyController.property_overridable_library_set('["advanced_mix_shadow_amount"]', True)
        emptyController.property_overridable_library_set('["advanced_mix_shadow_tint"]', True)

        wm.controller_empty = emptyController

        self.report({'INFO'}, "Added Shader Controller!")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(CST_OT_CreateShaderController_OP)

def unregister():
    bpy.utils.unregister_class(CST_OT_CreateShaderController_OP)