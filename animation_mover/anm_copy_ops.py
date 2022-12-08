import bpy
import copy

class ANM_OT_CopyAnimData_OP(bpy.types.Operator):
    bl_idname = "anm.copy_anim_data"
    bl_label = "Copy Animation Data (Keep Drivers)"
    bl_description = "Copies Animation Data from the active to all selected objects, with the exception of drivers"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        selectedObjects = context.selected_objects
        activeObject = context.active_object
       
        # Copy Active object to temporarily store drivers from objects to copy animation to
        active_object_copy = activeObject.copy()
        context.scene.collection.objects.link(active_object_copy)
        

        for object in selectedObjects:
            if object == activeObject:
                continue
              
            # Remove all drivers form active object copy
            if active_object_copy.animation_data and active_object_copy.animation_data.drivers:
                for driver in active_object_copy.animation_data.drivers:
                    active_object_copy.animation_data.drivers.remove(driver)
            # Copy all Drivers from the Target Object on the copy object
            if object.animation_data and object.animation_data.drivers:
                for driver in object.animation_data.drivers:
                    if not active_object_copy.animation_data:
                        active_object_copy.animation_data.create()
                    
                    try:
                        new_driver = active_object_copy.driver_add(driver.data_path, driver.array_index)
                    except:
                        new_driver = active_object_copy.driver_add(driver.data_path)
                    copy_driver(driver, new_driver)

            # Select the target and copy object for the animation link operator
            for obj in context.selected_objects:
                obj.select_set(False)
            object.select_set(True)
            bpy.context.view_layer.objects.active = active_object_copy  
            bpy.ops.object.make_links_data(type='ANIMATION')

        # Remove the temporary copy object from the file after all Objects have the copied animation
        bpy.data.objects.remove(active_object_copy, do_unlink=True)

        # Reset the selection to the original state (Before the Operator was started)
        
        for object in selectedObjects:
            object.select_set(True)

            # Reset the use_nla flag so the animation gets re-evaluated (Otherwise Animation does not update on Linked Objects)
            object.animation_data.use_nla = False
            object.animation_data.use_nla = True

        context.view_layer.objects.active = activeObject

        return {'FINISHED'}

def has_old_targets(driver, old_obj):
    for var in driver.driver.variables:
        for target in var.targets:
            print(target.id.name)
            print(old_obj.name)
            if not target.id or target.id.name == old_obj.name:
                return True
    return False

def copy_driver(old_driver, new_driver):
    
    new_driver.driver.expression = old_driver.driver.expression

    for var in old_driver.driver.variables:
        copy_variable(var, new_driver.driver)
    return new_driver

def copy_variable(old_var, target_driver):
    new_var = target_driver.variables.new()
    new_var.type = old_var.type
    new_var.name = old_var.name

    index = 0
    for target in old_var.targets:
        copy_target(target, new_var, index)
        index = index + 1

def copy_target(old_target, target_variable, index):
    target_variable.targets[index].data_path = old_target.data_path
    target_variable.targets[index].id = old_target.id
    

def copy_anim_data(from_anim_data, to_anim_data):
    to_anim_data.action = from_anim_data.action
    to_anim_data.action_blend_type = from_anim_data.action_blend_type
    to_anim_data.action_extrapolation = from_anim_data.action_extrapolation
    to_anim_data.action_influence = from_anim_data.action_influence
    
    for track in to_anim_data.nla_tracks:
        to_anim_data.nla_tracks.remove(track)

    for track in from_anim_data.nla_tracks:
        copy_nla_track_to_anim_data(track, to_anim_data)

    to_anim_data.use_nla = from_anim_data.use_nla
    to_anim_data.use_pin = from_anim_data.use_pin
    to_anim_data.use_tweak_mode = from_anim_data.use_tweak_mode

def copy_nla_track_to_anim_data(track, anim_data):
    new_track = anim_data.nla_tracks.new()
    
    new_track.lock = track.lock
    new_track.mute = track.mute
    new_track.name = track.name
    new_track.select = track.select
    for strip in track.strips:
        copy_nla_strip_to_track(strip, new_track)

def copy_nla_strip_to_track(strip, track):
    new_strip = track.strips.new(strip.name, strip.frame_start, strip.action)
    new_strip.action = strip.action
    new_strip.action_frame_end = strip.action_frame_end
    new_strip.action_frame_start = strip.action_frame_start
    #new_strip.active = strip.active
    new_strip.blend_in = strip.blend_in
    new_strip.blend_out = strip.blend_out
    new_strip.blend_type = strip.blend_type
    new_strip.extrapolation = strip.extrapolation
    #for fcurve in strip.fcurves:
    #    copy_fcurve_to_strip(fcurve, strip)
    new_strip.frame_end = strip.frame_end
    #new_strip.frame_end_ui = strip.frame_end_ui
    new_strip.frame_start = strip.frame_start
    #new_strip.frame_start_ui = strip.frame_start_ui
    new_strip.mute = strip.mute
    new_strip.name = strip.name
    new_strip.repeat = strip.repeat
    new_strip.scale = strip.scale
    new_strip.select = strip.select
    new_strip.strip_time = strip.strip_time
    #new_strip.type = strip.type
    new_strip.use_animated_influence = strip.use_animated_influence
    new_strip.use_animated_time = strip.use_animated_time
    new_strip.use_animated_time_cyclic = strip.use_animated_time_cyclic
    new_strip.use_auto_blend = strip.use_auto_blend
    new_strip.use_reverse = strip.use_reverse
    new_strip.use_sync_length = strip.use_sync_length



def copy_fcurve_to_strip(fcurve, strip):
    strip.fcurves.append(fcurve)
def register():
    bpy.utils.register_class(ANM_OT_CopyAnimData_OP)

def unregister():
    bpy.utils.unregister_class(ANM_OT_CopyAnimData_OP)