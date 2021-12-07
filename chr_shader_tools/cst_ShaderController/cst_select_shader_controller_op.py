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
        rna_ui = object.get('_RNA_UI')
        if rna_ui is None:
            object['_RNA_UI'] = {}
            rna_ui = object['_RNA_UI']


        object["highlight_col"] = (1.0, 1.0, 1.0)

        rna_ui["highlight_col"] = {
            "description":"Highlight Color",
            "default": (1.0, 1.0, 1.0),
            "min":0.0,
            "max":1.0,
            "subtype":'COLOR'
        }

        object["rimlight_col"] = (1.0, 1.0, 1.0)

        rna_ui["rimlight_col"] = {
            "description":"Rimlight Color",
            "default":(1.0, 1.0, 1.0),
            "min":0.0,
            "max":1.0,
            "subtype":'COLOR'
        }

        object["AdvMixLightCol"] = (1.0, 1.0, 1.0)

        rna_ui["AdvMixLightCol"] = {
            "description":"The color of the added Light",
            "default":(1.0, 1.0, 1.0),
            "min":0.0,
            "max":1.0,
            "subtype":'COLOR'
        }

        object["AdvMixShadowTint"] = (0.0, 0.0, 0.0)

        rna_ui["AdvMixShadowTint"] = {
            "description":"The color of the multiplied shadow tint",
            "default":(0.0, 0.0, 0.0),
            "min":0.0,
            "max":1.0,
            "subtype":'COLOR'
        }

        object["mix_values"] = (0.0, 0.2, 0.2)

        rna_ui["mix_values"] = {
            "description":"Colleciton of mix values for advanced mixing, adv mix light, adv mix shadow",
            "default":(0.0, 0.2, 0.2),
            "min":0.0,
            "max":1.0,
        }

        object["highlight_rimlight_mix_values"] = (0.0, 0.0, 0.0)

        rna_ui["highlight_rimlight_mix_values"] = {
            "description":"Collection of values for highlight amount, rimlight amount and Simple mix factor",
            "default":(0.0, 0.0, 0.0),
        }

    def add_drivers(self, object, controller):
        """Adds the drivers from the custom props of the controller to the given objects custom props"""

        add_driver_color_simple(controller, '["highlight_color"]', object, '["highlight_col"]')
     
        add_driver_color_simple(controller, '["rimlight_color"]', object, '["rimlight_col"]')
        
        add_driver_color_simple(controller, '["advanced_mix_light_color"]', object, '["AdvMixLightCol"]')
               
        add_driver_color_simple(controller, '["advanced_mix_shadow_tint"]', object, '["AdvMixShadowTint"]')

        add_driver_float_simple(controller, '["advanced_mix_switch"]', object, '["mix_values"]', 0)

        add_driver_float_simple(controller, '["advanced_mix_light_amount"]', object, '["mix_values"]', 1)

        add_driver_float_simple(controller, '["advanced_mix_shadow_amount"]', object, '["mix_values"]', 2)

        add_driver_float_simple(controller, '["highlight_amount"]', object, '["highlight_rimlight_mix_values"]', 0)

        add_driver_float_simple(controller, '["rimlight_amount"]', object, '["highlight_rimlight_mix_values"]', 1)

        add_driver_float_simple(controller, '["vector_diffuse_mix"]', object, '["highlight_rimlight_mix_values"]', 2)



def register():
    bpy.utils.register_class(CST_OT_selectShaderController_OP)

def unregister():
    bpy.utils.unregister_class(CST_OT_selectShaderController_OP)