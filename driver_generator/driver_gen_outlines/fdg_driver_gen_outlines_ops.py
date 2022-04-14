import bpy

from bpy.types import Operator
from ..utility_functions.fdg_driver_utils import *
from ..utility_functions import fdg_names

class FDG_OT_GenerateOutlineDriver_Op(Operator):
    bl_idname = "fdg.gen_outline_driver"
    bl_label = "Generate Outline Driver"
    bl_description = "Generate a Driver for the thickness of the outline compared to the distance between the camera and the character."
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        wm = context.window_manager

        cam = wm.camera
        gp = wm.gp_object
        cam_empty = bpy.context.scene.objects.get(fdg_names.empty_cam)

        if cam_empty is None:
            cam_empty = bpy.data.objects.new(fdg_names.empty_cam, None)

            
            cam_empty.location = cam.location
            cam_empty.rotation_euler = cam.rotation_euler

            bpy.context.collection.objects.link(cam_empty)

            parent_objects(cam, cam_empty)

        cam_empty.hide_viewport = True

        add_custom_property(gp, "Min Distance", default=1.0, prop_min=-100.0, prop_max=100.0)
        add_custom_property(gp, "Max Distance", default=5.5, prop_min=-100.0, prop_max=100.0)
        add_custom_property(gp, "Min Thickness", default=0.85, prop_min=0.0, prop_max=100.0, description="The minimum thickness multiplier applied at the minimum distance")
        add_custom_property(gp, "Max Thickness", default=1.8, prop_min=0.0, prop_max=100.0, description="The maximum thickness multiplier applied at the maximum distance.")

        add_custom_property(gp, "Curve Start Distance", default=2.0, prop_min=-100.0, prop_max=100.0)
        add_custom_property(gp, "Curve End Distance", default=4.0, prop_min=-100.0, prop_max=100.0)
        
        gp["Grease Pencil Name"] = gp.name

        


        driver = gp.data.driver_add('pixel_factor').driver

        add_var(driver, gp, "min_thick", type='SINGLE_PROP', rna_data_path='["Min Thickness"]')
        add_var(driver, gp, "max_thick", type='SINGLE_PROP', rna_data_path='["Max Thickness"]')
        add_var(driver, gp, "min_dist", type='SINGLE_PROP', rna_data_path='["Min Distance"]')
        add_var(driver, gp, "max_dist", type='SINGLE_PROP', rna_data_path='["Max Distance"]')

        var = driver.variables.new()
        var.name = "dist"
        var.type = 'LOC_DIFF'

        target = var.targets[0]
        target.id = cam_empty

        target = var.targets[1]
        target.id = wm.character_rig
        target.bone_target = wm.character_rig_bone

        driver.expression = "(min_thick * (1 - (dist - min_dist) / (max_dist - min_dist))) + (max_thick * (dist - min_dist) / (max_dist - min_dist))"

        p2 = gp.grease_pencil_modifiers["Thickness"].curve.curves[0].points[2]
        print(p2.location[0])
        #driver = p2.driver_add('[location][0]').driver



        self.report({'INFO'}, "Outline thickness automated!")
        return {'FINISHED'}


def register():
    bpy.utils.register_class(FDG_OT_GenerateOutlineDriver_Op)

def unregister():
    bpy.utils.unregister_class(FDG_OT_GenerateOutlineDriver_Op)