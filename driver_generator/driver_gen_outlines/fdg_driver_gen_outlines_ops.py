import string
import bpy

from enum import Enum

from bpy.types import Operator
from ..utility_functions.fdg_driver_utils import *
from ..utility_functions import fdg_names

def create_collection_unique(name, parent):
    collection = bpy.data.collections.get(name)
    if not collection:
        collection = bpy.data.collections.new(name)
        parent.children.link(collection)

    return collection

class subpass(Enum):
    L0 = 0
    L1 = 1
    L2 = 2

class FDG_OT_GenerateLineArtPass_OP(Operator):
    bl_idname = "fdg.gen_lineart_pass"
    bl_label = "Generate Lineart Pass"
    bl_description = "Generate a Lineart Pass with a Lineart Modifier and 2 thickness modifiers with Drivers for the thickness of the outline tied to the distance between the camera and the character."
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        wm = context.window_manager
        if not (wm.Pass_Name and wm.character_rig and wm.camera):
            return False
        

        if context.scene.gp_pass_settings.get(wm.Pass_Name + "L0"):
            return False

        return True

    def execute(self, context):
        
        scene = context.scene
        settings = scene.gp_settings
        gp = settings.gp_object
        character_collection = settings.character_collection
        
        mask_bit = self.find_free_mask(context)

        self.create_gp_pass(context, subpass.L0, gp, character_collection, mask_bit)
        self.create_gp_pass(context, subpass.L1, gp, character_collection, mask_bit)
        self.create_gp_pass(context, subpass.L2, gp, character_collection, mask_bit)


        return {'FINISHED'}

    def create_gp_pass(self, context, subpass : subpass, gp, character_collection, mask_bit):
        wm = context.window_manager
        scene = context.scene
        item = scene.gp_pass_settings.add()
        if subpass == subpass.L0:
            pass_name = wm.Pass_Name + "_L0"
            
            # These are the default Values of the Settings
            item.thick_dist_close = 0.65
            item.thick_dist_far = 2.3
            item.thick_close = 18.0
            item.thick_far = 28.0

            item.crv_max_dist = 0.0
            item.crv_off_dist = -1.0
            item.crv_mode = True
            item.crv_amount = 1.0

        if subpass == subpass.L1:
            pass_name = wm.Pass_Name + "_L1"
            
            # These are the default Values of the Settings
            item.thick_dist_close = 0.65
            item.thick_dist_far = 2.3
            item.thick_close = 18.0
            item.thick_far = 28.0

            item.crv_max_dist = 0.0
            item.crv_off_dist = -1.0
            item.crv_mode = True
            item.crv_amount = 1.0

        if subpass == subpass.L2:
            pass_name = wm.Pass_Name + "_L2"
            
            # These are the default Values of the Settings
            item.thick_dist_close = 0.65
            item.thick_dist_far = 2.3
            item.thick_close = 18.0
            item.thick_far = 28.0

            item.crv_max_dist = 0.0
            item.crv_off_dist = -1.0
            item.crv_mode = True
            item.crv_amount = 1.0

        item.name = pass_name
        item.pass_name = pass_name
        item.gp_object=gp

        collection = create_collection_unique(pass_name, character_collection)
        item.collection = collection

        pass_nr = self.find_free_pass(context)
        item.pass_nr = pass_nr

        gp_layer = gp.data.layers.new(name="pass_" + str(pass_nr) + "_" + pass_name, set_active = True)
        gp_layer.frames.new(0)
        gp_layer.pass_index = pass_nr
        gp_layer.use_lights = False
        item.GP_layer = gp_layer.info

        lineart = self.create_lineart(gp, pass_nr, pass_name, collection, gp_layer, mask_bit)
        item.lineart = lineart.name

        cam_empty = self.getCamEmpty()

        crv_mod, thick_mod = self.createThicknessModifiers(pass_nr, pass_name, gp, context, cam_empty, context.scene.gp_pass_settings.find(item.name))
        item.thick_modifier = thick_mod.name
        item.crv_modifier = crv_mod.name
 

    def find_free_mask(self, context):
        scene = context.scene
        if len(scene.gp_pass_settings) > 0:

            for i in range(1,8):
                if not self.is_mask_used(i, scene.gp_pass_settings): # is mask used has to be added
                    return i
            return -1
        return 1

    def is_mask_used(self, mask_nr, gp_pass_settings):

        for item in gp_pass_settings:
            lineart = item.gp_object.grease_pencil_modifiers.get(item.lineart)
            if lineart.use_intersection_mask[mask_nr]:
                return True
        return False

    def find_free_pass(self, context):
        scene = context.scene
        if len(scene.gp_pass_settings) > 0:
                        
            for i in range(1, 101):
                if not self.is_pass_used(i, scene.gp_pass_settings):
                    return i
            return -1
        return 1

    def is_pass_used(self, pass_nr, gp_pass_settings):

        for item in gp_pass_settings:
            if item.pass_nr == pass_nr:
                return True
        return False

    def create_lineart(self, gp, pass_nr, pass_name, source_collection, gp_layer, mask_bit):
        lineart = gp.grease_pencil_modifiers.new(pass_name, 'GP_LINEART')
        lineart.source_type = 'COLLECTION'
        lineart.source_collection = source_collection
        lineart.target_layer = gp_layer.info
        lineart.target_material = gp.data.materials[0]
        lineart.thickness = 1
        lineart.use_intersection_mask[mask_bit] = True
        return lineart

    def getCamEmpty(self):
        cam = bpy.context.window_manager.camera
        cam_empty = bpy.context.scene.objects.get(fdg_names.empty_cam)

        if cam_empty is None:
            cam_empty = bpy.data.objects.new(fdg_names.empty_cam, None)

            
            cam_empty.location = cam.location
            cam_empty.rotation_euler = cam.rotation_euler

            bpy.context.scene.gp_settings.outline_collection.objects.link(cam_empty)

            parent_objects(cam, cam_empty)
        cam_empty.hide_viewport = True
        return cam_empty

    def createThicknessModifiers(self, pass_nr, pass_name, gp, context, cam_empty, setting_index):
        wm = context.window_manager
        
        
        modifier_name = "pass_" + str(pass_nr) + "_" + pass_name + "_Thickness"
        # This creates a Thickness Modifier which has a custom Curve attached to it. It can interpolate between
        # the curve affecting the Line or the curve not affecting the line. It takes an amount which will make the
        # dynamic line more prominent (or less prominent)
        curve_modifier = gp.grease_pencil_modifiers.new(modifier_name + "_CURVE", 'GP_THICK')
        

        curve_modifier.use_custom_curve = True
        curve_modifier.layer_pass = pass_nr
        curve_driver = curve_modifier.driver_add('thickness_factor').driver
        curve_modifier.curve.curves[0].points[0].location = (0.0, 0.625)
        curve_modifier.curve.curves[0].points[1].location = (1.0, 0.625)
        curve_modifier.curve.curves[0].points.new(0.5, 1.0)
        for point in curve_modifier.curve.curves[0].points:
            point.handle_type = 'AUTO'
        curve_modifier.curve.update()

        # The Values which get used here are stored in the fritziGPPass PropertyGroup in a Collectionproperty in the scene
        data_path_start = '["gp_pass_settings"][' + str(setting_index) + ']'
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
        
        thickness_modifier.layer_pass = pass_nr
        
        thickness_driver = thickness_modifier.driver_add('thickness_factor').driver
        data_path_start = '["gp_pass_settings"][' + str(setting_index) + ']'
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

        return curve_modifier, thickness_modifier

class FDG_OT_GenerateCollections_OP(Operator):
    bl_idname = "fdg.gen_lineart_collections"
    bl_label = "Generate Standard Collections"
    bl_description = "Generates all the needed Collections for the Lineart Setup"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        wm = context.window_manager

        outline_collection = create_collection_unique("OUTLINES", bpy.context.scene.collection)

        objects_collection = create_collection_unique("OUTLINE_groups", bpy.context.scene.collection)
        environment_collection = create_collection_unique("ENVIRONMENTS", objects_collection)
        character_collection = create_collection_unique("CHARACTERS", objects_collection)
        excluded_collection = create_collection_unique("OBJECTS_Excluded", objects_collection)
        nointersection_collection = create_collection_unique("OBJECTS_NoIntersection", objects_collection)

        gp_data = bpy.data.grease_pencils.new("OUTLINES_scene")
        gp_ob = bpy.data.objects.new("OUTLINES_scene", gp_data)
        outline_collection.objects.link(gp_ob)
        gp_ob.show_in_front = True

        gp_layer = gp_data.layers.new(name="ENVIRONMENTS", set_active=True)
        gp_layer.frames.new(0)

        gp_mat = bpy.data.materials.new("gp_mat")

        bpy.data.materials.create_gpencil_data(gp_mat)
        gp_data.materials.append(gp_mat)

        lineart = gp_ob.grease_pencil_modifiers.new("pass_0_ENVIRONMENTS", 'GP_LINEART')
        lineart.source_collection = environment_collection
        lineart.target_layer = gp_layer.info
        lineart.target_material = gp_mat
        lineart.smooth_tolerance = 0.0
        lineart.thickness = 1
        lineart.use_intersection_mask[0] = True

        curve_modifier = gp_ob.grease_pencil_modifiers.new("pass_0_ENVIRONMENTS_CURVE", 'GP_THICK')
        
        curve_modifier.use_custom_curve = True
        curve_modifier.layer_pass = 0
        curve_modifier.curve.curves[0].points[0].location = (0.0, 0.625)
        curve_modifier.curve.curves[0].points[1].location = (1.0, 0.625)
        curve_modifier.curve.curves[0].points.new(0.5, 1.0)
        for point in curve_modifier.curve.curves[0].points:
            point.handle_type = 'AUTO'
        curve_modifier.curve.update()
            
        # Here be Curve Settings
        
        scene.gp_settings.gp_object = gp_ob
        scene.gp_settings.outline_collection = outline_collection
        scene.gp_settings.objects_collection = objects_collection
        scene.gp_settings.environment_collection = environment_collection
        scene.gp_settings.character_collection = character_collection
        scene.gp_settings.excluded_collection = excluded_collection
        scene.gp_settings.nointersection_collection = nointersection_collection
        scene.gp_settings.gp_material = gp_mat.name
        scene.gp_settings.environment_layer = gp_layer.info
        scene.gp_settings.environment_lineart = lineart.name
        scene.gp_settings.environment_thickness = curve_modifier.name
        scene.gp_settings.mask_counter = 0

        return {'FINISHED'}

def register():
    bpy.utils.register_class(FDG_OT_GenerateLineArtPass_OP)
    bpy.utils.register_class(FDG_OT_GenerateCollections_OP)

def unregister():
    bpy.utils.unregister_class(FDG_OT_GenerateCollections_OP)
    bpy.utils.unregister_class(FDG_OT_GenerateLineArtPass_OP)