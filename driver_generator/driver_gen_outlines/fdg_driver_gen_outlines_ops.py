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
        if wm.gp_auto_advanced_toggle:
            if not wm.do_create_gp_layer and not wm.gp_layer:
                return False

            if not wm.do_create_view_layer and not wm.view_layer:
                return False

            if wm.do_create_view_layer and not wm.new_view_layer_name:
                return False

        if context.scene.gp_settings.get(wm.Pass_Name):
            return False

        return True

    def execute(self, context):
        wm = context.window_manager
        
        cam = wm.camera
        gp = wm.gp_object
        pass_nr = wm.Pass_Number
        pass_name = wm.Pass_Name
        cam_empty = bpy.context.scene.objects.get(fdg_names.empty_cam)

        item = context.scene.gp_settings.add()
        item.name=pass_name
        setting_index = context.scene.gp_settings.find(pass_name)
        
        item.gp_object=gp
        
        item.thick_dist_close = 1.0
        item.thick_dist_far = 2.0
        item.thick_close = 1.0
        item.thick_far = 2.0

        item.crv_max_dist = 0.0
        item.crv_off_dist = -1.0
        item.crv_mode = True
        item.crv_amount = 1.0

        

        modifier_name = "pass_" + str(pass_nr) + "_" + pass_name + "_Thickness"
        
        if wm.gp_auto_advanced_toggle:

            view_layer : string
            if wm.do_create_view_layer:
                view_layer = context.scene.view_layers.new(wm.new_view_layer_name).name
            else:
                view_layer = wm.view_layer

            item.view_layer = view_layer

            gp_layer = None
            if wm.do_create_gp_layer:
                gp_layer = wm.gp_object.data.layers.new(name=pass_name, set_active = True)
                gp_layer.frames.new(0)
                gp_layer.pass_index = pass_nr
                gp_layer.use_lights = False
                gp_layer.viewlayer_render = view_layer
            else:
                gp_layer = wm.gp_layer

            item.GP_layer = gp_layer.info

        print(modifier_name)

        if cam_empty is None:
            cam_empty = bpy.data.objects.new(fdg_names.empty_cam, None)

            
            cam_empty.location = cam.location
            cam_empty.rotation_euler = cam.rotation_euler

            bpy.context.collection.objects.link(cam_empty)

            parent_objects(cam, cam_empty)

        

        cam_empty.hide_viewport = True

        add_custom_property(gp, "Close Distance", default=8.0, prop_min=-1000.0, prop_max=1000.0)
        add_custom_property(gp, "Far Distance", default=23.5, prop_min=-1000.0, prop_max=1000.0)
        add_custom_property(gp, "Close Thickness", default=24.0, prop_min=0.0, prop_max=1000.0, description="The thickness multiplier applied at the minimum (close) distance")
        add_custom_property(gp, "Far Thickness", default=30.0, prop_min=0.0, prop_max=1000.0, description="The thickness multiplier applied at the maximum (far) distance.")

        add_custom_property(gp, "Curve Start Distance", default=8.0, prop_min=-1000.0, prop_max=1000.0, description="The Distance at which the Custom Curve is fully applied")
        add_custom_property(gp, "Curve End Distance", default=10.0, prop_min=-1000.0, prop_max=1000.0, description="The Distance at which the Custom Curve is completely off")
        
        gp["Grease Pencil Name"] = gp.name

        

        curve_modifier = gp.grease_pencil_modifiers.new(modifier_name + "_CURVE", 'GP_THICK')
        item.crv_modifier = modifier_name + "_CURVE"

        curve_modifier.use_custom_curve = True
        curve_modifier.layer_pass = pass_nr
        curve_driver = curve_modifier.driver_add('thickness_factor').driver
        curve_modifier.curve.curves[0].points.new(0.0, 0.0)
        curve_modifier.curve.curves[0].points.new(0.5, 1.0)
        curve_modifier.curve.curves[0].points.new(1.0, 0.0)
        curve_modifier.curve.update()

        data_path_start = '["gp_settings"][' + str(setting_index) + ']'
        add_var(curve_driver, context.scene, "crv_max_dist", type='SINGLE_PROP', rna_data_path=data_path_start + '["crv_max_dist"]', id_type='SCENE')
        add_var(curve_driver, context.scene, "crv_off_dist", type='SINGLE_PROP', rna_data_path=data_path_start + '["crv_off_dist"]', id_type='SCENE')
        add_var(curve_driver, context.scene, "crv_amount", type='SINGLE_PROP', rna_data_path=data_path_start + '["crv_amount"]', id_type='SCENE')

        var = curve_driver.variables.new()
        var.name = "dist"
        var.type = 'LOC_DIFF'

        target = var.targets[0]
        target.id = cam_empty

        target = var.targets[1]
        target.id = wm.character_rig
        target.bone_target = wm.character_rig_bone

        curve_driver.expression = "max(1, min(1 + crv_amount, ((1 * (1 - (dist - crv_off_dist) / (crv_max_dist - crv_off_dist))) + ((1 + crv_amount) * (dist - crv_off_dist) / (crv_max_dist - crv_off_dist)) ) ))"

        thickness_modifier = gp.grease_pencil_modifiers.new(modifier_name + "_MAIN", 'GP_THICK')
        item.thick_modifier = modifier_name + "_MAIN"
        thickness_modifier.layer_pass = pass_nr
        
        thickness_driver = thickness_modifier.driver_add('thickness_factor').driver
        data_path_start = '["gp_settings"][' + str(setting_index) + ']'
        add_var(thickness_driver, context.scene, "far_dist", type='SINGLE_PROP', rna_data_path=data_path_start + '["thick_dist_far"]', id_type='SCENE')
        add_var(thickness_driver, context.scene, "close_dist", type='SINGLE_PROP', rna_data_path=data_path_start + '["thick_dist_close"]', id_type='SCENE')
        add_var(thickness_driver, context.scene, "close_thick", type='SINGLE_PROP', rna_data_path=data_path_start + '["thick_close"]', id_type='SCENE')
        add_var(thickness_driver, context.scene, "far_thick", type='SINGLE_PROP', rna_data_path=data_path_start + '["thick_far"]', id_type='SCENE')
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

        thickness_driver.expression = "min(far_thick, ((close_thick * (1 - (dist - close_dist) / (far_dist - close_dist))) + (far_thick * (dist - close_dist) / (far_dist - close_dist))))/crv_value"




        self.report({'INFO'}, "Outline thickness automated!")
        return {'FINISHED'}


def register():
    bpy.utils.register_class(FDG_OT_GenerateOutlineDriver_Op)

def unregister():
    bpy.utils.unregister_class(FDG_OT_GenerateOutlineDriver_Op)