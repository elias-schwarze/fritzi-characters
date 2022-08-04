import string
import bpy

from bpy.types import Operator
from ..utility_functions.fdg_driver_utils import *
from ..utility_functions import fdg_names

class FDG_OT_GenerateOutlineDriver_Op(Operator):
    bl_idname = "fdg.gen_outline_driver"
    bl_label = "Generate Outline Driver"
    bl_description = "Generate a Driver for the thickness of the outline tied to the distance between the camera and the character."
    bl_options = {"REGISTER", "UNDO"}
    
    @classmethod
    def poll(cls, context):
        wm = context.window_manager
        if not (wm.gp_object and wm.Pass_Name and wm.character_rig and wm.camera):
            return False
        
        if not wm.do_create_gp_layer and not wm.gp_layer:
            return False

        if not wm.do_create_view_layer and not wm.view_layer:
            return False

        if wm.do_create_view_layer and not wm.new_view_layer_name:
            return False

        return True

    def execute(self, context):
        wm = context.window_manager
        
        cam = wm.camera
        gp = wm.gp_object
        pass_nr = wm.Pass_Number
        pass_name = wm.Pass_Name
        cam_empty = bpy.context.scene.objects.get(fdg_names.empty_cam)

        modifier_name = "pass_" + str(pass_nr) + "_" + pass_name + "_Thickness"
        view_layer : string
        if wm.do_create_view_layer:
            view_layer = context.scene.view_layers.new(wm.new_view_layer_name).name
        else:
            view_layer = wm.view_layer
        
        gp_layer = None
        if wm.do_create_gp_layer:
            layer = wm.gp_object.data.layers.new(name=pass_name)
            layer.pass_index = pass_nr
            layer.use_lights = False
            layer.viewlayer_render = view_layer


        print(modifier_name)

        if cam_empty is None:
            cam_empty = bpy.data.objects.new(fdg_names.empty_cam, None)

            
            cam_empty.location = cam.location
            cam_empty.rotation_euler = cam.rotation_euler

            bpy.context.collection.objects.link(cam_empty)

            parent_objects(cam, cam_empty)

        

        cam_empty.hide_viewport = True

        add_custom_property(gp, "Min Distance", default=8.0, prop_min=-1000.0, prop_max=1000.0)
        add_custom_property(gp, "Max Distance", default=23.5, prop_min=-1000.0, prop_max=1000.0)
        add_custom_property(gp, "Min Thickness", default=24.0, prop_min=0.0, prop_max=1000.0, description="The minimum thickness multiplier applied at the minimum distance")
        add_custom_property(gp, "Max Thickness", default=30.0, prop_min=0.0, prop_max=1000.0, description="The maximum thickness multiplier applied at the maximum distance.")

        add_custom_property(gp, "Curve Start Distance", default=8.0, prop_min=-1000.0, prop_max=1000.0)
        add_custom_property(gp, "Curve End Distance", default=10.0, prop_min=-1000.0, prop_max=1000.0)
        
        gp["Grease Pencil Name"] = gp.name

        

        curve_modifier = gp.grease_pencil_modifiers.new(modifier_name + "_CURVE", 'GP_THICK')

        curve_modifier.use_custom_curve = True
        curve_modifier.layer_pass = pass_nr
        curve_driver = curve_modifier.driver_add('thickness_factor').driver
        curve_modifier.curve.curves[0].points.new(0.0, 0.0)
        curve_modifier.curve.curves[0].points.new(0.5, 1.0)
        curve_modifier.curve.curves[0].points.new(1.0, 0.0)
        curve_modifier.curve.update()

        add_var(curve_driver, gp, "crv_start_dist", type='SINGLE_PROP', rna_data_path='["Curve Start Distance"]')
        add_var(curve_driver, gp, "crv_end_dist", type='SINGLE_PROP', rna_data_path='["Curve End Distance"]')

        var = curve_driver.variables.new()
        var.name = "dist"
        var.type = 'LOC_DIFF'

        target = var.targets[0]
        target.id = cam_empty

        target = var.targets[1]
        target.id = wm.character_rig
        target.bone_target = wm.character_rig_bone

        curve_driver.expression = "max(1, min(2, ((1 * (1 - (dist - crv_end_dist) / (crv_start_dist - crv_end_dist))) + (2 * (dist - crv_end_dist) / (crv_start_dist - crv_end_dist)) ) ))"

        thickness_modifier = gp.grease_pencil_modifiers.new(modifier_name + "_MAIN", 'GP_THICK')

        thickness_modifier.layer_pass = pass_nr
        
        thickness_driver = thickness_modifier.driver_add('thickness_factor').driver

        add_var(thickness_driver, gp, "max_thick", type='SINGLE_PROP', rna_data_path='["Max Thickness"]')
        add_var(thickness_driver, gp, "min_thick", type='SINGLE_PROP', rna_data_path='["Min Thickness"]')
        add_var(thickness_driver, gp, "min_dist", type='SINGLE_PROP', rna_data_path='["Min Distance"]')
        add_var(thickness_driver, gp, "max_dist", type='SINGLE_PROP', rna_data_path='["Max Distance"]')
        add_var(thickness_driver, gp, "crv_value", type='SINGLE_PROP', rna_data_path='grease_pencil_modifiers["'+ modifier_name + '_CURVE"].thickness_factor')

        #var = thickness_driver.variables.new()
        #var.name = "crv_value"
        #var.type = 'SINGLE_PROP'


        var = thickness_driver.variables.new()
        var.name = "dist"
        var.type = 'LOC_DIFF'

        target = var.targets[0]
        target.id = cam_empty

        target = var.targets[1]
        target.id = wm.character_rig
        target.bone_target = wm.character_rig_bone

        thickness_driver.expression = "((min_thick * (1 - (dist - min_dist) / (max_dist - min_dist))) + (max_thick * (dist - min_dist) / (max_dist - min_dist)))/crv_value"




        self.report({'INFO'}, "Outline thickness automated!")
        return {'FINISHED'}


def register():
    bpy.utils.register_class(FDG_OT_GenerateOutlineDriver_Op)

def unregister():
    bpy.utils.unregister_class(FDG_OT_GenerateOutlineDriver_Op)