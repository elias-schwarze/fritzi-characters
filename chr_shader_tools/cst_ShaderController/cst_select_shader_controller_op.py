import bpy

from bpy.types import Operator
from ...driver_generator.utility_functions.fdg_driver_utils import remove_driver_variables

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

        controllerEmpty = context.scene.controller_empty
        characterCollection = context.scene.character_collection

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

        object["vector_diffuse_mix"] = 0.0

        rna_ui["vector_diffuse_mix"] = {
            "description":"Mix Amount of Vector shading vs Diffuse shading",
            "default":0.0,
            "min":0.0,
            "max":1.0
        }

        object["highlight_amount"] = 0.0

        rna_ui["highlight_amount"] = {
            "description":"Brightness of the highlights",
            "default":0.0,
            
        }

        object["highlight_col"] = (1.0, 1.0, 1.0)

        rna_ui["highlight_col"] = {
            "description":"Highlight Color",
            "default": (1.0, 1.0, 1.0),
            "min":0.0,
            "max":1.0,
            "subtype":'COLOR'
        }

        object["rimlight_amount"] = 0.0

        rna_ui["rimlight_amount"] = {
            "description":"Brightness of the rimlights",
            "default":0.0
        }

        object["rimlight_col"] = (1.0, 1.0, 1.0)

        rna_ui["rimlight_col"] = {
            "description":"Rimlight Color",
            "default":(1.0, 1.0, 1.0),
            "min":0.0,
            "max":1.0,
            "subtype":'COLOR'
        }

    def add_drivers(self, object, controller):

        driverMix = object.driver_add('["vector_diffuse_mix"]').driver
        driverMix.type = 'AVERAGE'

        #Removes all variables from the driver from earlier links, so no duplicates are created
        remove_driver_variables(driverMix)
        var = driverMix.variables.new()
        var.name = "Mix"
        var.type = 'SINGLE_PROP'
        target = var.targets[0]
        target.id = controller
        target.data_path = '["vector_diffuse_mix"]'

        driverHighlightAmount = object.driver_add('["highlight_amount"]').driver
        driverHighlightAmount.type ='AVERAGE'
        remove_driver_variables(driverHighlightAmount)
        var = driverHighlightAmount.variables.new()
        var.name = "Amount"
        var.type = 'SINGLE_PROP'
        target = var.targets[0]
        target.id = controller
        target.data_path = '["highlight_amount"]'

        driverHighlightRed = object.driver_add('["highlight_col"]', 0).driver
        driverHighlightRed.type = 'AVERAGE'
        remove_driver_variables(driverHighlightRed)
        var = driverHighlightRed.variables.new()
        var.name = "Red"
        var.type = 'SINGLE_PROP'
        target = var.targets[0]
        target.id = controller
        target.data_path = '["highlight_color"][0]'

        driverHighlightGreen = object.driver_add('["highlight_col"]', 1).driver
        driverHighlightGreen.type = 'AVERAGE'
        remove_driver_variables(driverHighlightGreen)
        var = driverHighlightGreen.variables.new()
        var.name = "Green"
        var.type = 'SINGLE_PROP'
        target = var.targets[0]
        target.id = controller
        target.data_path = '["highlight_color"][1]'

        driverHighlightBlue = object.driver_add('["highlight_col"]', 2).driver
        driverHighlightBlue.type = 'AVERAGE'
        remove_driver_variables(driverHighlightBlue)
        var = driverHighlightBlue.variables.new()
        var.name = "Blue"
        var.type = 'SINGLE_PROP'
        target = var.targets[0]
        target.id = controller
        target.data_path = '["highlight_color"][2]'

        driverRimlightAmount = object.driver_add('["rimlight_amount"]').driver
        driverRimlightAmount.type ='AVERAGE'
        remove_driver_variables(driverRimlightAmount)
        var = driverRimlightAmount.variables.new()
        var.name = "Amount"
        var.type = 'SINGLE_PROP'
        target = var.targets[0]
        target.id = controller
        target.data_path = '["rimlight_amount"]'

        driverRimlightRed = object.driver_add('["rimlight_col"]', 0).driver
        driverRimlightRed.type = 'AVERAGE'
        remove_driver_variables(driverRimlightRed)
        var = driverRimlightRed.variables.new()
        var.name = "Red"
        var.type = 'SINGLE_PROP'
        target = var.targets[0]
        target.id = controller
        target.data_path = '["rimlight_color"][0]'

        driverRimlightGreen = object.driver_add('["rimlight_col"]', 1).driver
        driverRimlightGreen.type = 'AVERAGE'
        remove_driver_variables(driverRimlightGreen)
        var = driverRimlightGreen.variables.new()
        var.name = "Green"
        var.type = 'SINGLE_PROP'
        target = var.targets[0]
        target.id = controller
        target.data_path = '["rimlight_color"][1]'

        driverRimlightBlue = object.driver_add('["rimlight_col"]', 2).driver
        driverRimlightBlue.type = 'AVERAGE'
        remove_driver_variables(driverRimlightBlue)
        var = driverRimlightBlue.variables.new()
        var.name = "Blue"
        var.type = 'SINGLE_PROP'
        target = var.targets[0]
        target.id = controller
        target.data_path = '["rimlight_color"][2]'


def register():
    bpy.utils.register_class(CST_OT_selectShaderController_OP)

def unregister():
    bpy.utils.unregister_class(CST_OT_selectShaderController_OP)