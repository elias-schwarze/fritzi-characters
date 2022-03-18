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

        if characterName is None or characterName == "":
            self.report({'WARNING'}, "Please give a Character Name!")
            return {'CANCELLED'}

        emptyController = bpy.data.objects.new(characterName + "_ShaderController", None)

        bpy.context.scene.collection.objects.link(emptyController)

        emptyController.empty_display_size = 2
        emptyController.empty_display_type = 'PLAIN_AXES'

        add_properties(emptyController)

        wm.controller_empty = emptyController

        self.report({'INFO'}, "Added Shader Controller!")
        return {'FINISHED'}

class CST_OT_UpdateShaderController_OP(Operator):
    bl_idname = "object.update_shader_controller"
    bl_label = "Update Shader Controller"
    bl_description = "Updates the shader controller (and link to the character) with all new properties that may have been added"
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

        emptyController = wm.controller_empty

        add_properties(emptyController)

        bpy.ops.object.select_shader_controller()

        return {'FINISHED'}



def add_properties(controller):

    emptyController = controller

   
    if 'vector_diffuse_mix' not in emptyController:    
        emptyController["vector_diffuse_mix"] = 0.0

    ui_data = emptyController.id_properties_ui("vector_diffuse_mix")
    ui_data.update(min=0.0)
    ui_data.update(max=1.0)
    ui_data.update(soft_min=0.0)
    ui_data.update(soft_max=1.0)
    ui_data.update(description="Mix Amount of Vector shading vs Diffuse shading")
    ui_data.update(default=0.0)

    if "highlight_amount" not in emptyController:
        emptyController["highlight_amount"] = 0.0

    ui_data = emptyController.id_properties_ui("highlight_amount")
    ui_data.update(min=0.0)
    ui_data.update(soft_min=0.0)
    ui_data.update(description="Brightness of the highlights")
    ui_data.update(default=0.0)
        
    if "highlight_color" not in emptyController:
       emptyController["highlight_color"] = (1.0, 1.0, 1.0)

    ui_data = emptyController.id_properties_ui("highlight_color")
    ui_data.update(min=0.0)
    ui_data.update(max=1.0)
    ui_data.update(soft_min=0.0)
    ui_data.update(soft_max=1.0)
    ui_data.update(description="Highlight Color")
    ui_data.update(default=(1.0, 1.0, 1.0))
    ui_data.update(subtype='COLOR')
        
    if "rimlight_amount" not in emptyController:
        emptyController["rimlight_amount"] = 0.0

    ui_data = emptyController.id_properties_ui("rimlight_amount")
    ui_data.update(min=0.0)
    ui_data.update(soft_min=0.0)
    ui_data.update(description="Brightness of the rimlights")
    ui_data.update(default=0.0)
        
    if "rimlight_color" not in emptyController:
        emptyController["rimlight_color"] = (1.0, 1.0, 1.0)

    ui_data = emptyController.id_properties_ui("rimlight_color")
    ui_data.update(min=0.0)
    ui_data.update(max=1.0)
    ui_data.update(soft_min=0.0)
    ui_data.update(soft_max=1.0)
    ui_data.update(description="Rimlight Color")
    ui_data.update(default=(1.0, 1.0, 1.0))
    ui_data.update(subtype='COLOR')
        
    if "advanced_mix_switch" not in emptyController:
        emptyController["advanced_mix_switch"] = 0.0

    ui_data = emptyController.id_properties_ui("advanced_mix_switch")
    ui_data.update(min=0.0)
    ui_data.update(max=1.0)
    ui_data.update(soft_min=0.0)
    ui_data.update(soft_max=1.0)
    ui_data.update(description="Turns Advanced mixing on and off")
    ui_data.update(default=0.0)
        
    if "advanced_mix_light_amount" not in emptyController:
        emptyController["advanced_mix_light_amount"] = 0.2

    ui_data = emptyController.id_properties_ui("advanced_mix_light_amount")
    ui_data.update(min=0.0)
    ui_data.update(max=1.0)
    ui_data.update(soft_min=0.0)
    ui_data.update(soft_max=1.0)
    ui_data.update(description="How much light gets added to the light regions")
    ui_data.update(default=0.2)
        
    if "advanced_mix_light_color" not in emptyController:
        emptyController["advanced_mix_light_color"] = (1.0, 1.0, 1.0)

    ui_data = emptyController.id_properties_ui("advanced_mix_light_color")
    ui_data.update(min=0.0)
    ui_data.update(max=1.0)
    ui_data.update(soft_min=0.0)
    ui_data.update(soft_max=1.0)
    ui_data.update(description="The color of the added Light")
    ui_data.update(default=(1.0, 1.0, 1.0))
    ui_data.update(subtype='COLOR')
        
    if "advanced_mix_shadow_amount" not in emptyController:
        emptyController["advanced_mix_shadow_amount"] = 0.2

    ui_data = emptyController.id_properties_ui("advanced_mix_shadow_amount")
    ui_data.update(min=0.0)
    ui_data.update(max=1.0)
    ui_data.update(soft_min=0.0)
    ui_data.update(soft_max=1.0)
    ui_data.update(description="How much shadow tint gets multiplied to the dark regions")
    ui_data.update(default=0.2)
        
    if "advanced_mix_shadow_tint" not in emptyController:
        emptyController["advanced_mix_shadow_tint"] = (0.0, 0.0, 0.0)

    ui_data = emptyController.id_properties_ui("advanced_mix_shadow_tint")
    ui_data.update(min=0.0)
    ui_data.update(max=1.0)
    ui_data.update(soft_min=0.0)
    ui_data.update(soft_max=1.0)
    ui_data.update(description="The color of the multiplied shadow tint")
    ui_data.update(default=(0.0, 0.0, 0.0))
    ui_data.update(subtype='COLOR')
        
    if "main_color_tint" not in emptyController:
        emptyController["main_color_tint"] = (1.0, 1.0, 1.0)

    ui_data = emptyController.id_properties_ui("main_color_tint")
    ui_data.update(min=0.0)
    ui_data.update(max=2.0)
    ui_data.update(soft_min=0.0)
    ui_data.update(soft_max=2.0)
    ui_data.update(description="Color to tint the main Color of a Character")
    ui_data.update(default=(1.0, 1.0, 1.0))
    ui_data.update(subtype='COLOR')

    if "main_color_tint_amount" not in emptyController:
        emptyController["main_color_tint_amount"] = (0.0)

    ui_data = emptyController.id_properties_ui("main_color_tint_amount")
    ui_data.update(min=0.0)
    ui_data.update(max=1.0)
    ui_data.update(soft_min=0.0)
    ui_data.update(soft_max=1.0)
    ui_data.update(description="Amount of tint being applied to the main Color")
    ui_data.update(default=0.0)

    if "shadow_color_tint" not in emptyController:
        emptyController["shadow_color_tint"] = (1.0, 1.0, 1.0)

    ui_data = emptyController.id_properties_ui("shadow_color_tint")
    ui_data.update(min=0.0)
    ui_data.update(max=2.0)
    ui_data.update(soft_min=0.0)
    ui_data.update(soft_max=2.0)
    ui_data.update(description="Color ot tint the shadow color of a Character")
    ui_data.update(default=(1.0, 1.0, 1.0))
    ui_data.update(subtype='COLOR')

    if "shadow_color_tint_amount" not in emptyController:
        emptyController["shadow_color_tint_amount"] = (0.0)

    ui_data = emptyController.id_properties_ui("shadow_color_tint_amount")
    ui_data.update(min=0.0)
    ui_data.update(max=1.0)
    ui_data.update(soft_min=0.0)
    ui_data.update(soft_max=1.0)
    ui_data.update(description="Amount of tint being applied to the shadow Color")
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
    emptyController.property_overridable_library_set('["shadow_color_tint"]', True)
    emptyController.property_overridable_library_set('["shadow_color_tint_amount"]', True)

def register():
    bpy.utils.register_class(CST_OT_CreateShaderController_OP)
    bpy.utils.register_class(CST_OT_UpdateShaderController_OP)

def unregister():
    bpy.utils.unregister_class(CST_OT_UpdateShaderController_OP)
    bpy.utils.unregister_class(CST_OT_CreateShaderController_OP)