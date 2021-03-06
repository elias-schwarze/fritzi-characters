import bpy

from bpy.types import Operator

from ...driver_generator.utility_functions.fdg_driver_utils import remove_driver_variables

class CST_OT_VectorLightSelector_OP(Operator):
    bl_idname = "object.select_light_empty"
    bl_label = "Link Light to Character"
    bl_description = "Adds driver from the Light empty to all Meshes in the selected Collection, so that the Shader knows the light direction"
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
        
        lightEmpty = wm.light_empty
        characterCollection = wm.character_collection
        characterRig = wm.character_rig
        characterRigBone = wm.character_rig_bone

        if lightEmpty is None:
            self.report({'WARNING'}, "Please select the Empty!")
            return {'CANCELLED'}

        if characterCollection is None:
            self.report({'WARNING'}, "Please select a collection with the Character!")
            return {'CANCELLED'}

        if characterRig:
            constraint = lightEmpty.constraints.new(type='CHILD_OF')
            constraint.target = characterRig
            if characterRigBone:
                constraint.subtarget = characterRigBone

            constraint.use_rotation_x = False
            constraint.use_rotation_y = False
            constraint.use_rotation_z = False
            constraint.use_scale_x = False
            constraint.use_scale_y = False
            constraint.use_scale_z = False
            constraint.set_inverse_pending = True



        self.add_light_drivers(characterCollection, lightEmpty)
        
        # Have to redraw all areas, so that the new properties are visible to the user
        for area in bpy.context.screen.areas:
            area.tag_redraw()

        self.report({'INFO'}, "Added Light Drivers!")
        return {'FINISHED'}

    def add_light_drivers(self, collection, light):
        """Recursively searches the collection and all child collections for Meshes and adds a light rotation vector property to them, which is driven by the rotation of the light empty"""
        for child in collection.children:
            self.add_light_drivers(child, light)

        for obj in collection.objects:
            if obj.type == 'MESH':
                
                obj["light_rotation"] = (0.0, 0.0, 0.0)
                ui_data = obj.id_properties_ui("light_rotation")
                ui_data.update(
                    description="Light Rotation",
                    default=(0.0, 0.0, 0.0),
                    min=-10000,
                    max=10000
                )

                driver_rot_x = obj.driver_add('["light_rotation"]', 0).driver
                driver_rot_x.type = 'AVERAGE'

                remove_driver_variables(driver_rot_x)
                var = driver_rot_x.variables.new()
                var.name = "rot_x"
                var.type = "TRANSFORMS"
                target = var.targets[0]
                target.id = light
                target.transform_type = 'ROT_X'
                target.transform_space = 'WORLD_SPACE'

                driver_rot_y = obj.driver_add('["light_rotation"]', 1).driver
                driver_rot_y.type = 'AVERAGE'
                remove_driver_variables(driver_rot_y)
                var = driver_rot_y.variables.new()
                var.name = "rot_y"
                var.type = "TRANSFORMS"
                target = var.targets[0]
                target.id = light
                target.transform_type = 'ROT_Y'
                target.transform_space = 'WORLD_SPACE'

                driver_rot_z = obj.driver_add('["light_rotation"]', 2).driver
                driver_rot_z.type = 'AVERAGE'
                remove_driver_variables(driver_rot_z)
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