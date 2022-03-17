import bpy

from bpy.types import Operator

from ...driver_generator.utility_functions.fdg_driver_utils import add_driver_color_simple
from ...driver_generator.utility_functions.fdg_driver_utils import add_driver_float_simple

class CST_OT_selectShaderController_OP(Operator):
    bl_idname = "object.select_shader_controller"
    bl_label = "Link Controller to Character"
    bl_description = "Adds drivers from the Controller Properties to all Meshes in the selected Character Collection, so that the shader can access them."
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

        controllerEmpty = wm.controller_empty
        characterCollection = wm.character_collection

        if controllerEmpty is None:
            self.report({'WARNING'}, "Please select the Controller!")
            return {'CANCELLED'}

        if characterCollection is None:
            self.report({'WARNING'}, "Please select a collection with the Character!")
            return {'CANCELLED'}

        self.search_collection(characterCollection, controllerEmpty)


        self.report({'INFO'}, "Added Controller Drivers!")
        return {'FINISHED'}

    def search_collection(self, collection, controller):
        for child in collection.children:
            self.search_collection(child, controller)

        for object in collection.objects:
            if object.type == 'MESH':
                self.add_properties(object)
                self.add_drivers(object, controller)

    def add_properties(self, object):
        

        object["highlight"] = (1.0, 1.0, 1.0, 0.0)

        ui_data = object.id_properties_ui("highlight")
        ui_data.update(
            description="Highlight Color and Amount",
            default=(1.0, 1.0, 1.0, 0.0)
        )
        

        object["rimlight"] = (1.0, 1.0, 1.0, 0.0)

        ui_data = object.id_properties_ui("rimlight")
        ui_data.update(
            description="Rimlight Color and Amount",
            default=(1.0, 1.0, 1.0, 0.0)
        )

        object["adv_mix_light"] = (1.0, 1.0, 1.0, 0.2)
        ui_data = object.id_properties_ui("adv_mix_light")
        ui_data.update(
            description="The color of the added Loght and mix factor",
            default=(1.0, 1.0, 1.0, 0.2)
        )

        object["adv_mix_shadow"] = (0.0, 0.0, 0.0, 0.2)

        ui_data = object.id_properties_ui("adv_mix_shadow")
        ui_data.update(
            description="The color of the multiplied shadow tint and multiplication amount",
            default=(0.0, 0.0, 0.0, 0.2)
        )

        object["mix_values"] = (0.0, 0.0)

        ui_data.update(
            description="Collection of mix values for advanced mixing and simple mixing",
            default=(0.0, 0.0)
        )
        

        object["main_tint"] = (1.0, 1.0, 1.0, 0.0)

        ui_data.update(
            description="Tint Main Color and Tint amount",
            default=(1.0, 1.0, 1.0, 0.0)
        )


        object["shadow_tint"] = (1.0, 1.0, 1.0, 0.0)

        ui_data.update(
            description="Tint Shadow Color and Tint amount",
            default=(1.0, 1.0, 1.0, 0.0)
        )

    def add_drivers(self, object, controller):
        """Adds the drivers from the custom props of the controller to the given objects custom props"""

        add_driver_color_simple(controller, '["highlight_color"]', object, '["highlight"]')
        add_driver_float_simple(controller, '["highlight_amount"]', object, '["highlight"]', 3)
     
        add_driver_color_simple(controller, '["rimlight_color"]', object, '["rimlight"]')
        add_driver_float_simple(controller, '["rimlight_amount"]', object, '["rimlight"]', 3)
        
        add_driver_color_simple(controller, '["advanced_mix_light_color"]', object, '["adv_mix_light"]')
        add_driver_float_simple(controller, '["advanced_mix_light_amount"]', object, '["adv_mix_light"]', 3)
               
        add_driver_color_simple(controller, '["advanced_mix_shadow_tint"]', object, '["adv_mix_shadow"]')
        add_driver_float_simple(controller, '["advanced_mix_shadow_amount"]', object, '["adv_mix_shadow"]', 3)

        add_driver_float_simple(controller, '["advanced_mix_switch"]', object, '["mix_values"]', 0)

        add_driver_float_simple(controller, '["vector_diffuse_mix"]', object, '["mix_values"]', 1)

        add_driver_color_simple(controller, '["main_color_tint"]', object, '["main_tint"]')
        add_driver_float_simple(controller, '["main_color_tint_amount"]', object, '["main_tint"]', 3)

        add_driver_color_simple(controller, '["shadow_color_tint"]', object, '["shadow_tint"]')
        add_driver_float_simple(controller, '["shadow_color_tint_amount"]', object, '["shadow_tint"]', 3)




def register():
    bpy.utils.register_class(CST_OT_selectShaderController_OP)

def unregister():
    bpy.utils.unregister_class(CST_OT_selectShaderController_OP)