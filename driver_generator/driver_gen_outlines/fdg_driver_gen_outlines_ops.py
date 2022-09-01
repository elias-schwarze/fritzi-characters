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


        # This adds the new outline Pass to a Settings Propertygroup stored in a propertycollection in the scene
        item = context.scene.gp_settings.add()
        item.name=pass_name
        setting_index = context.scene.gp_settings.find(pass_name)
        
        item.gp_object=gp
        
        # These are the default Values of the Settings
        item.thick_dist_close = 0.65
        item.thick_dist_far = 2.3
        item.thick_close = 18.0
        item.thick_far = 28.0

        item.crv_max_dist = 0.0
        item.crv_off_dist = -1.0
        item.crv_mode = True
        item.crv_amount = 1.0

        

        modifier_name = "pass_" + str(pass_nr) + "_" + pass_name + "_Thickness"
        
        # This is not used yet. When implemented the user can choose to create a new GP and View layer (or choose existing ones) which get automatically set up
        # to work with the Render pass System from Christoph and Elias. Needs to be implemented in the UI and might also need to setup a lineart Modifier.
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

        
        # A Cam Empty will be created (if there is not already one) and parented to the active Camera.
        # The auto Camera Parenting option might be wanted to be activated, so the distance is always 
        # calculated from the current active Camera.

        if cam_empty is None:
            cam_empty = bpy.data.objects.new(fdg_names.empty_cam, None)

            
            cam_empty.location = cam.location
            cam_empty.rotation_euler = cam.rotation_euler

            bpy.context.collection.objects.link(cam_empty)

            parent_objects(cam, cam_empty)

        

        cam_empty.hide_viewport = True

        # This creates a Thickness Modifier which has a custom Curve attached to it. It can interpolate between
        # the curve affecting the Line or the curve not affecting the line. It takes an amount which will make the
        # dynamic line more prominent (or less prominent)
        curve_modifier = gp.grease_pencil_modifiers.new(modifier_name + "_CURVE", 'GP_THICK')
        item.crv_modifier = modifier_name + "_CURVE"

        curve_modifier.use_custom_curve = True
        curve_modifier.layer_pass = pass_nr
        curve_driver = curve_modifier.driver_add('thickness_factor').driver
        curve_modifier.curve.curves[0].points[0].location = (0.0, 0.625)
        curve_modifier.curve.curves[0].points[1].location = (1.0, 0.625)
        curve_modifier.curve.curves[0].points.new(0.5, 1.0)
        for point in curve_modifier.curve.curves[0].points:
            point.handle_type = 'AUTO'
        curve_modifier.curve.update()

        # The Values which get used here are stored in the FritziGPSetup PropertyGroup in a Collectionproperty in the scene
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

        # This expression calculates the curve amount based on the distance from the camera(empty) to the Character Rig (Head Bone).
        # It uses Linear interpolation between 1 (no Curve) and (1+crv_amount) depending on the distance Values set by the user.
        # The Thickness modifier shows a Curve if the thickness_factor is greater than 1 (2 being the standard Curve). This is weird, but it works.
        # It also scales the curve, so it has to be counterscaled accordingly in the main thickness modifier.
        # If the User chooses the Dynamic Line to be always the same the off distance gets set to -1 and the max distance gets set to 0.
        # Since the Distance to the Camera is always positive this expression then always returns the max Amount.
        curve_driver.expression = "max(1, min(1 + crv_amount, ((1 * (1 - (dist - crv_off_dist) / (crv_max_dist - crv_off_dist))) + ((1 + crv_amount) * (dist - crv_off_dist) / (crv_max_dist - crv_off_dist)) ) ))"

        # This creates the Main Thickness modifier which scales the thickness based on the distance from the Camera(empty) to the Character Rig
        # If the Camera gets closer to the Character the thickness_factor gets lower, so the outline doesnt get too thick.
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

        var = thickness_driver.variables.new()
        var.name = "dist"
        var.type = 'LOC_DIFF'

        target = var.targets[0]
        target.id = cam_empty

        target = var.targets[1]
        target.id = wm.character_rig
        target.bone_target = wm.character_rig_bone

        # This Expression scales the Thickness modifier based on the Distance from Cam to Character and the distance and thickness values given
        # by the user. It also defaults to clamping the maximum thickness, because that is the default wanted behaviour.
        # Clamping modes can be changed from the user in the Settings which will update the Expression in the Driver.
        # The calculated Value will be divided by the thickness from the Curve Thickness Modifier to counterscale the thickness which is used to activate the dynamic Line.
        thickness_driver.expression = "min(far_thick, ((close_thick * (1 - (dist - close_dist) / (far_dist - close_dist))) + (far_thick * (dist - close_dist) / (far_dist - close_dist))))/crv_value"




        self.report({'INFO'}, "Outline thickness automated!")
        return {'FINISHED'}

class FDG_OT_GenerateLineArtPass_OP(Operator):
    bl_idname = "fdg.gen_lineart_pass"
    bl_label = "Generate Lineart Pass"
    bl_description = "Generate a Lineart Pass with a Lineart Modifier and 2 thickness modifiers with Drivers for the thickness of the outline tied to the distance between the camera and the character."
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
        gp = wm.gp_object
        collection = wm.lineart_collection
        #view_layer = context.scene.view_layers.new("pass_" + str(wm.Pass_Number) + "_" + wm.Pass_Name).name
        gp_layer = wm.gp_object.data.layers.new(name="pass_" + str(wm.Pass_Number) + "_" + wm.Pass_Name, set_active = True)
        gp_layer.frames.new(0)
        gp_layer.pass_index = wm.Pass_Number
        gp_layer.use_lights = False
        lineart = gp.grease_pencil_modifiers.new(wm.Pass_Name, 'GP_LINEART')
        lineart.source_type = 'COLLECTION'
        lineart.source_collection = collection
        lineart.target_layer = gp_layer.info
        if gp.data.materials:
            lineart.target_material = gp.data.materials[0]
        lineart.thickness = 1
        lineart.use_intersection_mask = collection.lineart_intersection_mask

        return {'FINISHED'}


def register():
    bpy.utils.register_class(FDG_OT_GenerateOutlineDriver_Op)
    bpy.utils.register_class(FDG_OT_GenerateLineArtPass_OP)

def unregister():
    bpy.utils.unregister_class(FDG_OT_GenerateLineArtPass_OP)
    bpy.utils.unregister_class(FDG_OT_GenerateOutlineDriver_Op)