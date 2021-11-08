import bpy

from bpy.types import Operator

class CST_OT_VectorLightSelector_OP(Operator):
    bl_idname = "object.select_light_empty"
    bl_label = "Select Light Empty"
    bl_description = "Adds driver from the Light empty to all Meshes in the selected Collection, so that the Shader knows the light direction"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        lightEmpty = context.scene.light_empty
        characterCollection = context.scene.character_collection

        if lightEmpty is None:
            self.report({'WARNING'}, "Please select the Empty!")

        if characterCollection is None:
            self.report({'WARNING'}, "Please select a collection with the Character!")

        self.add_light_drivers(characterCollection, lightEmpty)
        for area in bpy.context.screen.areas:
            area.tag_redraw()

        self.report({'INFO'}, "Added Light Drivers!")
        return {'FINISHED'}

    def add_light_drivers(self, collection, light):
        for child in collection.children:
            self.add_light_drivers(child, light)

        for obj in collection.objects:
            if obj.type == 'MESH':
                rna_ui = obj.get('_RNA_UI')
                if rna_ui is None:
                    obj['_RNA_UI'] = {}
                    rna_ui = obj['_RNA_UI']
                obj["light_rotation"] = (0.0, 0.0, 0.0)
                rna_ui["light_rotation"] = {"description":"Light Rotation",
                  "default": (0.0, 0.0, 0.0),
                  "min":-10000,
                  "max":10000}

                driver_rot_x = obj.driver_add('["light_rotation"]', 0).driver
                driver_rot_x.type = 'AVERAGE'
                var = driver_rot_x.variables.new()
                var.name = "rot_x"
                var.type = "TRANSFORMS"
                target = var.targets[0]
                target.id = light
                target.transform_type = 'ROT_X'
                target.transform_space = 'WORLD_SPACE'

                driver_rot_y = obj.driver_add('["light_rotation"]', 1).driver
                driver_rot_y.type = 'AVERAGE'
                var = driver_rot_y.variables.new()
                var.name = "rot_y"
                var.type = "TRANSFORMS"
                target = var.targets[0]
                target.id = light
                target.transform_type = 'ROT_Y'
                target.transform_space = 'WORLD_SPACE'

                driver_rot_z = obj.driver_add('["light_rotation"]', 2).driver
                driver_rot_z.type = 'AVERAGE'
                var = driver_rot_z.variables.new()
                var.name = "rot_z"
                var.type = "TRANSFORMS"
                target = var.targets[0]
                target.id = light
                target.transform_type = 'ROT_Z'
                target.transform_space = 'WORLD_SPACE'


                
                

def register():
    bpy.utils.register_class(CST_OT_VectorLightSelector_OP)

def unregister():
    bpy.utils.unregister_class(CST_OT_VectorLightSelector_OP)