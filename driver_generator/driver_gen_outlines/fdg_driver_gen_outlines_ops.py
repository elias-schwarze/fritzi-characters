import string
import bpy

from enum import Enum

from bpy.types import Operator
from numpy import char
from ..utility_functions.fdg_driver_utils import *
from ..utility_functions import fdg_names
from .fdg_driver_gen_outlines_pnl import load_defaults

def create_collection_unique(name, parent):
    collection = bpy.data.collections.get(name)
    if not collection:
        collection = bpy.data.collections.new(name)
        parent.children.link(collection)

    return collection

def create_view_layer_unique(name):
    layer = bpy.context.scene.view_layers.get(name)
    if not layer:
        layer = bpy.context.scene.view_layers.new(name)

    return layer

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
        

        if context.scene.gp_settings.get(wm.Pass_Name + "L0"):
            return False

        return True

    def execute(self, context):
        
        scene = context.scene
        settings = scene.gp_defaults
        gp = settings.gp_object
        character_collection = settings.character_collection
        
        mask_bit = self.find_free_mask(context)

        self.create_gp_pass(context, subpass.L0, gp, character_collection, mask_bit)
        self.create_gp_pass(context, subpass.L1, gp, character_collection, mask_bit)
        self.create_gp_pass(context, subpass.L2, gp, character_collection, mask_bit)

        add_auto_link_handler()

        return {'FINISHED'}

    def create_gp_pass(self, context, subpass : subpass, gp, character_collection, mask_bit):
        load_defaults()
        wm = context.window_manager
        scene = context.scene
        default_settings = wm.gp_pass_defaults
        item = scene.gp_settings.add()
        if subpass == subpass.L0:
            pass_name = wm.Pass_Name + "_L0"
            
            L0_settings = default_settings["L0"]
            # These are the default Values of the Settings
            item.thick_dist_close = L0_settings["thick_dist_close"]
            item.thick_dist_far = L0_settings["thick_dist_far"]
            item.thick_close = L0_settings["thick_close"]
            item.thick_far = L0_settings["thick_far"]

            item.crv_max_dist = L0_settings["crv_max_dist"]
            item.crv_off_dist = L0_settings["crv_off_dist"]
            item.crv_mode = L0_settings["crv_mode"]
            item.crv_amount = L0_settings["crv_amount"]

        if subpass == subpass.L1:
            pass_name = wm.Pass_Name + "_L1"
            
            L1_settings = default_settings["L1"]
            # These are the default Values of the Settings
            item.thick_dist_close = L1_settings["thick_dist_close"]
            item.thick_dist_far = L1_settings["thick_dist_far"]
            item.thick_close = L1_settings["thick_close"]
            item.thick_far = L1_settings["thick_far"]

            item.crv_max_dist = L1_settings["crv_max_dist"]
            item.crv_off_dist = L1_settings["crv_off_dist"]
            item.crv_mode = L1_settings["crv_mode"]
            item.crv_amount = L1_settings["crv_amount"]

        if subpass == subpass.L2:
            pass_name = wm.Pass_Name + "_L2"
            
            L2_settings = default_settings["L2"]
            # These are the default Values of the Settings
            item.thick_dist_close = L2_settings["thick_dist_close"]
            item.thick_dist_far = L2_settings["thick_dist_far"]
            item.thick_close = L2_settings["thick_close"]
            item.thick_far = L2_settings["thick_far"]

            item.crv_max_dist = L2_settings["crv_max_dist"]
            item.crv_off_dist = L2_settings["crv_off_dist"]
            item.crv_mode = L2_settings["crv_mode"]
            item.crv_amount = L2_settings["crv_amount"]

        item.name = pass_name
        item.pass_name = pass_name
        item.gp_object=gp

        collection = create_collection_unique(pass_name, character_collection)
        collection.lineart_use_intersection_mask = True
        collection.lineart_intersection_mask[mask_bit] = True
        item.collection = collection

        pass_nr = self.find_free_pass(context)
        item.pass_nr = pass_nr

        gp_layer = gp.data.layers.new(name="pass_" + str(pass_nr) + "_" + pass_name, set_active = True)
        gp_layer.frames.new(0)
        gp_layer.pass_index = pass_nr
        gp_layer.viewlayer_render = scene.gp_defaults.character_view_layer
        gp_layer.use_lights = False
        item.GP_layer = gp_layer.info

        lineart = self.create_lineart(gp, pass_nr, pass_name, collection, gp_layer, mask_bit, True)
        item.lineart = lineart.name

        camera = bpy.context.scene.camera
        cam_empty = link_camera(camera)

        crv_mod, thick_mod = self.createThicknessModifiers(pass_nr, pass_name, gp, context, cam_empty, context.scene.gp_settings.find(item.name))
        item.thick_modifier = thick_mod.name
        item.crv_modifier = crv_mod.name
 

    def find_free_mask(self, context):
        scene = context.scene
        if len(scene.gp_settings) > 0:

            for i in range(1,8):
                if not self.is_mask_used(i, scene.gp_settings): # is mask used has to be added
                    return i
            return -1
        return 1

    def is_mask_used(self, mask_nr, gp_settings):

        for item in gp_settings:
            lineart = item.gp_object.grease_pencil_modifiers.get(item.lineart)
            if lineart.use_intersection_mask[mask_nr]:
                return True
        return False

    def find_free_pass(self, context):
        scene = context.scene
        used_passes = self.get_used_passes(scene.gp_defaults.gp_object)
                       
        for i in range(1, 32767):
            if i not in used_passes:
                return i
        return -1
        

    def get_used_passes(self, gp_object):
        used_passes = []
        for layer in gp_object.data.layers:
            used_passes.append(layer.pass_index)
        return used_passes

    def is_pass_used(self, pass_nr, gp_settings):

        for layer in gp_settings.gp_object.layers:
            if layer.pass_index == pass_nr:
                return True
        return False

    def create_lineart(self, gp, pass_nr, pass_name, source_collection, gp_layer, mask_bit, use_cache = False):
        lineart = gp.grease_pencil_modifiers.new("pass_" + str(pass_nr) + "_" + pass_name, 'GP_LINEART')
        lineart.source_type = 'COLLECTION'
        lineart.source_collection = source_collection
        lineart.target_layer = gp_layer.info
        lineart.target_material = gp.data.materials[0]
        lineart.thickness = 1
        lineart.use_intersection_mask[mask_bit] = True
        lineart.use_geometry_space_chain = True
        lineart.use_intersection_match = True
        if use_cache:
            lineart.use_cache = use_cache
        return lineart

    def getCamEmpty(self):
        cam = bpy.context.window_manager.camera
        cam_empty = bpy.context.scene.objects.get(fdg_names.empty_cam)

        if cam_empty is None:
            cam_empty = bpy.data.objects.new(fdg_names.empty_cam, None)

            
            cam_empty.location = cam.location
            cam_empty.rotation_euler = cam.rotation_euler

            bpy.context.scene.gp_defaults.outline_collection.objects.link(cam_empty)

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

        return curve_modifier, thickness_modifier

class FDG_OT_RemoveLineArtPass_OP(Operator):
    bl_idname = "fdg.remove_lineart_pass"
    bl_label = "Remove Lineart Pass"
    bl_description = "Removes the currently in the Add-On selected Lineart pass from the file. This includes gp_layer and Modifiers on the gp_object."
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        scene = context.scene
        wm = context.window_manager

        settings = scene.gp_settings.get(wm.gp_auto_enum)

        if settings.collection:
            settings.collection.name = settings.collection.name + "_old"

        gp_object = settings.gp_object
        if gp_object:

            # Remove the modifiers if they are in the settings
            if settings.lineart:
                lineart = gp_object.grease_pencil_modifiers.get(settings.lineart)
                if lineart:
                    gp_object.grease_pencil_modifiers.remove(lineart)
            
            if settings.thick_modifier:
                thick_modifier = gp_object.grease_pencil_modifiers.get(settings.thick_modifier)
                if thick_modifier:
                    thick_modifier.driver_remove('thickness_factor')
                    gp_object.grease_pencil_modifiers.remove(thick_modifier)
            
            if settings.crv_modifier:
                crv_modifier = gp_object.grease_pencil_modifiers.get(settings.crv_modifier)
                if crv_modifier:
                    crv_modifier.driver_remove('thickness_factor')
                    gp_object.grease_pencil_modifiers.remove(crv_modifier)

            # Remove the Grease Pencil layer if it is in the settings
            if settings.GP_layer:
                layer = gp_object.data.layers.get(settings.GP_layer)
                if layer:
                    gp_object.data.layers.remove(layer)

        key = scene.gp_settings.find(settings.name)
        scene.gp_settings.remove(key)

        return {'FINISHED'}

class FDG_OT_GenerateCollections_OP(Operator):
    bl_idname = "fdg.gen_lineart_collections"
    bl_label = "Generate Standard Collections"
    bl_description = "Generates all the needed Collections for the Lineart Setup"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        scene = context.scene
        gp_defaults = scene.gp_defaults
        if not gp_defaults.default_view_layer:
            return False
        if not gp_defaults.environment_view_layer:
            return False
        if not gp_defaults.character_view_layer:
            return False
        if not gp_defaults.extra_view_layer:
            return False

        return True
        
    def execute(self, context):
        scene = context.scene
        wm = context.window_manager

        outline_collection = create_collection_unique("OUTLINES", bpy.context.scene.collection)

        objects_collection = create_collection_unique("OUTLINE_groups", bpy.context.scene.collection)
        objects_collection.lineart_usage = 'INCLUDE'
        environment_collection = create_collection_unique("ENVIRONMENTS", objects_collection)
        environment_collection.lineart_usage = 'INCLUDE'
        environment_L0_collection = create_collection_unique("ENVIRONMENTS_L0", environment_collection)
        environment_L0_collection.lineart_usage = 'INCLUDE'
        environment_L0_collection.lineart_use_intersection_mask = True
        environment_L0_collection.lineart_intersection_mask[0] = True
        
        environment_L1_collection = create_collection_unique("ENVIRONMENTS_L1", environment_collection)
        environment_L1_collection.lineart_usage = 'INCLUDE'
        environment_L1_collection.lineart_use_intersection_mask = True
        environment_L1_collection.lineart_intersection_mask[0] = True
        
        environment_L2_collection = create_collection_unique("ENVIRONMENTS_L2", environment_collection)
        environment_L2_collection.lineart_usage = 'INCLUDE'
        environment_L2_collection.lineart_use_intersection_mask = True
        environment_L2_collection.lineart_intersection_mask[0] = True
        
        character_collection = create_collection_unique("CHARACTERS", objects_collection)
        character_collection.lineart_usage = 'INCLUDE'
        excluded_collection = create_collection_unique("OBJECTS_Excluded", objects_collection)
        excluded_collection.lineart_usage = 'EXCLUDE'
        nointersection_collection = create_collection_unique("OBJECTS_NoIntersection", objects_collection)
        nointersection_collection.lineart_usage = 'NO_INTERSECTION'
        extraobjects_collection = create_collection_unique("EXTRA_CharacterObjects", objects_collection)
        extraobjects_collection.lineart_usage = 'EXCLUDE'

        self.set_collection_visibility(context)

        gp_data = bpy.data.grease_pencils.new("OUTLINES_scene")
        gp_ob = bpy.data.objects.new("OUTLINES_scene", gp_data)
        outline_collection.objects.link(gp_ob)
        gp_ob.show_in_front = True
        gp_data.pixel_factor = 0.1

        gp_layer_L0 = gp_data.layers.new(name="pass_1_ENVIRONMENTS_L0", set_active=True)
        gp_layer_L0.frames.new(0)
        gp_layer_L0.pass_index = 1
        gp_layer_L0.use_lights = False
        gp_layer_L0.viewlayer_render = scene.gp_defaults.environment_view_layer

        gp_layer_L1 = gp_data.layers.new(name="pass_2_ENVIRONMENTS_L1", set_active=True)
        gp_layer_L1.frames.new(0)
        gp_layer_L1.pass_index = 2
        gp_layer_L1.use_lights = False
        gp_layer_L1.viewlayer_render = scene.gp_defaults.environment_view_layer

        gp_layer_L2 = gp_data.layers.new(name="pass_3_ENVIRONMENTS_L2", set_active=True)
        gp_layer_L2.frames.new(0)
        gp_layer_L2.pass_index = 3
        gp_layer_L2.use_lights = False
        gp_layer_L2.viewlayer_render = scene.gp_defaults.environment_view_layer

        gp_mat = bpy.data.materials.new("Black")

        bpy.data.materials.create_gpencil_data(gp_mat)
        gp_data.materials.append(gp_mat)

        lineart_L0 = gp_ob.grease_pencil_modifiers.new("pass_1_ENVIRONMENTS_L0", 'GP_LINEART')
        lineart_L0.source_collection = environment_L0_collection
        lineart_L0.target_layer = gp_layer_L0.info
        lineart_L0.target_material = gp_mat
        lineart_L0.smooth_tolerance = 0.1
        lineart_L0.split_angle = 0.523599
        lineart_L0.use_fuzzy_intersections = True
        lineart_L0.thickness = 1
        lineart_L0.use_intersection_mask[0] = True
        lineart_L0.use_geometry_space_chain = True
        lineart_L0.use_intersection_match = True

        lineart_L1 = gp_ob.grease_pencil_modifiers.new("pass_2_ENVIRONMENTS_L1", 'GP_LINEART')
        lineart_L1.source_type = 'COLLECTION'
        lineart_L1.source_collection = environment_L1_collection
        lineart_L1.target_layer = gp_layer_L1.info
        lineart_L1.target_material = gp_mat
        lineart_L1.thickness = 1
        lineart_L1.use_intersection_mask[0] = True
        lineart_L1.use_geometry_space_chain = True
        lineart_L1.use_intersection_match = True
        lineart_L1.use_cache = True

        lineart_L2 = gp_ob.grease_pencil_modifiers.new("pass_3_ENVIRONMENTS_L2", 'GP_LINEART')
        lineart_L2.source_type = 'COLLECTION'
        lineart_L2.source_collection = environment_L1_collection
        lineart_L2.target_layer = gp_layer_L2.info
        lineart_L2.target_material = gp_mat
        lineart_L2.thickness = 1
        lineart_L2.use_intersection_mask[0] = True
        lineart_L2.use_geometry_space_chain = True
        lineart_L2.use_intersection_match = True
        lineart_L2.use_cache = True        


        curve_modifier_L0 = gp_ob.grease_pencil_modifiers.new("pass_1_ENVIRONMENTS_CURVE_L0", 'GP_THICK')
        
        curve_modifier_L0.thickness_factor = 18.0
        curve_modifier_L0.use_custom_curve = True
        curve_modifier_L0.layer_pass = 1
        curve_modifier_L0.curve.curves[0].points[0].location = (0.0, 0.5)
        curve_modifier_L0.curve.curves[0].points[1].location = (1.0, 0.5)
        curve_modifier_L0.curve.curves[0].points.new(0.5, 1.0)
        for point in curve_modifier_L0.curve.curves[0].points:
            point.handle_type = 'AUTO'
        curve_modifier_L0.curve.update()


        curve_modifier_L1 = gp_ob.grease_pencil_modifiers.new("pass_2_ENVIRONMENTS_CURVE_L1", 'GP_THICK')
        
        curve_modifier_L1.thickness_factor = 12.0
        curve_modifier_L1.use_custom_curve = True
        curve_modifier_L1.layer_pass = 2
        curve_modifier_L1.curve.curves[0].points[0].location = (0.0, 0.5)
        curve_modifier_L1.curve.curves[0].points[1].location = (1.0, 0.5)
        curve_modifier_L1.curve.curves[0].points.new(0.5, 1.0)
        for point in curve_modifier_L1.curve.curves[0].points:
            point.handle_type = 'AUTO'
        curve_modifier_L1.curve.update()


        curve_modifier_L2 = gp_ob.grease_pencil_modifiers.new("pass_3_ENVIRONMENTS_CURVE_L2", 'GP_THICK')
        
        curve_modifier_L2.thickness_factor = 6.0
        curve_modifier_L2.use_custom_curve = True
        curve_modifier_L2.layer_pass = 3
        curve_modifier_L2.curve.curves[0].points[0].location = (0.0, 0.5)
        curve_modifier_L2.curve.curves[0].points[1].location = (1.0, 0.5)
        curve_modifier_L2.curve.curves[0].points.new(0.5, 1.0)
        for point in curve_modifier_L2.curve.curves[0].points:
            point.handle_type = 'AUTO'
        curve_modifier_L2.curve.update()
            
        # Here be Curve Settings
        
        scene.gp_defaults.gp_object = gp_ob
        scene.gp_defaults.outline_collection = outline_collection
        scene.gp_defaults.objects_collection = objects_collection
        scene.gp_defaults.environment_collection = environment_collection
        scene.gp_defaults.environment_L0_collection = environment_L0_collection
        scene.gp_defaults.environment_L1_collection = environment_L1_collection
        scene.gp_defaults.environment_L2_collection = environment_L2_collection
        scene.gp_defaults.character_collection = character_collection
        scene.gp_defaults.excluded_collection = excluded_collection
        scene.gp_defaults.nointersection_collection = nointersection_collection
        scene.gp_defaults.extraobjects_collection = extraobjects_collection
        scene.gp_defaults.gp_material = gp_mat.name
        scene.gp_defaults.environment_layer_L0 = gp_layer_L0.info
        scene.gp_defaults.environment_layer_L1 = gp_layer_L1.info
        scene.gp_defaults.environment_layer_L2 = gp_layer_L2.info
        scene.gp_defaults.environment_L0_lineart = lineart_L0.name
        scene.gp_defaults.environment_L0_thickness = curve_modifier_L0.name
        scene.gp_defaults.environment_L1_lineart = lineart_L1.name
        scene.gp_defaults.environment_L1_thickness = curve_modifier_L1.name
        scene.gp_defaults.environment_L2_lineart = lineart_L2.name
        scene.gp_defaults.environment_L2_thickness = curve_modifier_L2.name
        scene.gp_defaults.mask_counter = 0

        return {'FINISHED'}

    def set_collection_visibility(self, context):
        scene = context.scene

        environment_view_layer_collections = scene.view_layers[scene.gp_defaults.environment_view_layer].layer_collection
        self.set_layer_collections_visibility(context, environment_view_layer_collections, {"OUTLINES"})

        character_view_layer_collections = scene.view_layers[scene.gp_defaults.character_view_layer].layer_collection
        self.set_layer_collections_visibility(context, character_view_layer_collections, {"OUTLINES"})

        extra_view_layer_collections = scene.view_layers[scene.gp_defaults.extra_view_layer].layer_collection
        self.set_layer_collections_visibility(context, extra_view_layer_collections, {"OUTLINE_groups", "EXTRA_CharacterObjects"})
        
    
    def set_layer_collections_visibility(self, context, collection, include_names):
        for child in collection.children:
            
            
            if child.name in include_names:
                child.exclude = False
                
                self.set_layer_collections_visibility(context, child, include_names)
            else:
                child.exclude = True
               
class FDG_OT_GenerateViewLayers_OP(Operator):
    bl_idname = "fdg.gen_view_layers"
    bl_label = "Generate Standard View Layers"
    bl_description = "Generates all the needed View Layers for the Lineart Setup"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):

        self.create_view_layers(context)
        
        return {'FINISHED'}
    
    def create_view_layers(self, context):
        scene = context.scene

        bpy.context.window.view_layer.name = "3d"
        layer = context.scene.view_layers.get("3d")
        layer.use_pass_combined = True
        layer.use_pass_z = True
        layer.eevee.use_pass_volume_direct = True
        layer.use_pass_environment = True
        layer.use_pass_ambient_occlusion = True
        layer.use_pass_cryptomatte_object = True
        layer.use_pass_cryptomatte_asset = True
        layer.pass_cryptomatte_depth = 2
        layer.use_pass_cryptomatte_accurate = True
        scene.gp_defaults.default_view_layer = context.window.view_layer.name

        layer = create_view_layer_unique("lines_environment")
        layer.use_pass_combined = True
        layer.use_pass_z = True
        scene.gp_defaults.environment_view_layer = layer.name

        layer = create_view_layer_unique("lines_characters")
        layer.use_pass_combined = True
        layer.use_pass_z = True
        scene.gp_defaults.character_view_layer = layer.name

        layer = create_view_layer_unique("lines_extra")
        layer.use_pass_combined = True
        layer.use_pass_z = True
        scene.gp_defaults.extra_view_layer = layer.name

class FDG_OT_UpdateCamEmpties_OP(Operator):
    bl_idname = "fdg.update_cam_empties"
    bl_label = "Update Cam References"
    bl_description = "Updates the cam empties on the grease_pencil_thickness_modifiers"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        for driver in scene.gp_settings[0].gp_object.animation_data.drivers:
            print(driver.data_path)
            for var in driver.driver.variables:
                print(var.name)
                if var.name == "dist":
                    var.targets[0].id = link_camera(bpy.context.scene.camera)
                    for target in var.targets:
                        
                        print(target.data_path)
                        print(target.id_type)
                        print(target.id)
        return {'FINISHED'}

def register():
    bpy.utils.register_class(FDG_OT_GenerateLineArtPass_OP)
    bpy.utils.register_class(FDG_OT_RemoveLineArtPass_OP)
    bpy.utils.register_class(FDG_OT_GenerateCollections_OP)
    bpy.utils.register_class(FDG_OT_GenerateViewLayers_OP)
    bpy.utils.register_class(FDG_OT_UpdateCamEmpties_OP)

def unregister():
    bpy.utils.unregister_class(FDG_OT_UpdateCamEmpties_OP)
    bpy.utils.unregister_class(FDG_OT_GenerateViewLayers_OP)
    bpy.utils.unregister_class(FDG_OT_GenerateCollections_OP)
    bpy.utils.unregister_class(FDG_OT_RemoveLineArtPass_OP)
    bpy.utils.unregister_class(FDG_OT_GenerateLineArtPass_OP)