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


        emptyController["testProp"] = 1.0

        ui_data = emptyController.id_properties_ui("testProp")
        #ui_data.update(min=0.1)
        #ui_data.update(max=1.1)
        #ui_data.update(soft_min=0.1)
        #ui_data.update(soft_max=1.1)
        #ui_data.update(description="ein Testproperty")
        #ui_data.update(default=0.55)
        ui_data.update(min=0.1, max=1.1, soft_min=0.1, soft_max=1.1, description="Ein Testproperty", default=0.55)

        emptyController["vector_diffuse_mix"] = 0.0

        ui_data = emptyController.id_properties_ui("vector_diffuse_mix")
        ui_data.update(min=0.0)
        ui_data.update(max=1.0)
        ui_data.update(soft_min=0.0)
        ui_data.update(soft_max=1.0)
        ui_data.update(description="Mix Amount of Vector shading vs Diffuse shading")
        ui_data.update(default=0.0)


        emptyController["highlight_amount"] = 0.0

        ui_data = emptyController.id_properties_ui("highlight_amount")
        ui_data.update(min=0.0)
        ui_data.update(soft_min=0.0)
        ui_data.update(description="Brightness of the highlights")
        ui_data.update(default=0.0)
        

        emptyController["highlight_color"] = (1.0, 1.0, 1.0)

        ui_data = emptyController.id_properties_ui("highlight_color")
        ui_data.update(min=0.0)
        ui_data.update(max=1.0)
        ui_data.update(soft_min=0.0)
        ui_data.update(soft_max=1.0)
        ui_data.update(description="Highlight Color")
        ui_data.update(default=(1.0, 1.0, 1.0))
        ui_data.update(subtype='COLOR')
        

        emptyController["rimlight_amount"] = 0.0

        ui_data = emptyController.id_properties_ui("rimlight_amount")
        ui_data.update(min=0.0)
        ui_data.update(soft_min=0.0)
        ui_data.update(description="Brightness of the rimlights")
        ui_data.update(default=0.0)
        

        emptyController["rimlight_color"] = (1.0, 1.0, 1.0)

        ui_data = emptyController.id_properties_ui("rimlight_color")
        ui_data.update(min=0.0)
        ui_data.update(max=1.0)
        ui_data.update(soft_min=0.0)
        ui_data.update(soft_max=1.0)
        ui_data.update(description="Rimlight Color")
        ui_data.update(default=(1.0, 1.0, 1.0))
        ui_data.update(subtype='COLOR')
        

        emptyController["advanced_mix_switch"] = 0.0

        ui_data = emptyController.id_properties_ui("advanced_mix_switch")
        ui_data.update(min=0.0)
        ui_data.update(max=1.0)
        ui_data.update(soft_min=0.0)
        ui_data.update(soft_max=1.0)
        ui_data.update(description="Turns Advanced mixing on and off")
        ui_data.update(default=0.0)
        

        emptyController["advanced_mix_light_amount"] = 0.2

        ui_data = emptyController.id_properties_ui("advanced_mix_light_amount")
        ui_data.update(min=0.0)
        ui_data.update(max=1.0)
        ui_data.update(soft_min=0.0)
        ui_data.update(soft_max=1.0)
        ui_data.update(description="How much light gets added to the light regions")
        ui_data.update(default=0.2)
        

        emptyController["advanced_mix_light_color"] = (1.0, 1.0, 1.0)

        ui_data = emptyController.id_properties_ui("advanced_mix_light_color")
        ui_data.update(min=0.0)
        ui_data.update(max=1.0)
        ui_data.update(soft_min=0.0)
        ui_data.update(soft_max=1.0)
        ui_data.update(description="The color of the added Light")
        ui_data.update(default=(1.0, 1.0, 1.0))
        ui_data.update(subtype='COLOR')
        

        emptyController["advanced_mix_shadow_amount"] = 0.2

        ui_data = emptyController.id_properties_ui("advanced_mix_shadow_amount")
        ui_data.update(min=0.0)
        ui_data.update(max=1.0)
        ui_data.update(soft_min=0.0)
        ui_data.update(soft_max=1.0)
        ui_data.update(description="How much shadow tint gets multiplied to the dark regions")
        ui_data.update(default=0.2)
        

        emptyController["advanced_mix_shadow_tint"] = (0.0, 0.0, 0.0)

        ui_data = emptyController.id_properties_ui("advanced_mix_shadow_tint")
        ui_data.update(min=0.0)
        ui_data.update(max=1.0)
        ui_data.update(soft_min=0.0)
        ui_data.update(soft_max=1.0)
        ui_data.update(description="The color of the multiplied shadow tint")
        ui_data.update(default=(0.0, 0.0, 0.0))
        ui_data.update(subtype='COLOR')
        

        emptyController["main_color_tint"] = (1.0, 1.0, 1.0)

        ui_data = emptyController.id_properties_ui("main_color_tint")
        ui_data.update(min=0.0)
        ui_data.update(max=2.0)
        ui_data.update(soft_min=0.0)
        ui_data.update(soft_max=2.0)
        ui_data.update(description="Color to tint the main Color of a Character")
        ui_data.update(default=(1.0, 1.0, 1.0))
        ui_data.update(subtype='COLOR')


        emptyController["main_color_tint_amount"] = (0.0)

        ui_data = emptyController.id_properties_ui("main_color_tint_amount")
        ui_data.update(min=0.0)
        ui_data.update(max=1.0)
        ui_data.update(soft_min=0.0)
        ui_data.update(soft_max=1.0)
        ui_data.update(description="Amount of tint being applied to the main Color")
        ui_data.update(default=0.0)
        

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
        emptyController.property_overridable_library_set('["main_color_tint"]', True)
        emptyController.property_overridable_library_set('["main_color_tint_amount"]', True)

        wm.controller_empty = emptyController

        self.report({'INFO'}, "Added Shader Controller!")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(CST_OT_CreateShaderController_OP)

def unregister():
    bpy.utils.unregister_class(CST_OT_CreateShaderController_OP)