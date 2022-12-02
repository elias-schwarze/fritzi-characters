import bpy

class ANM_OT_CopyAnimData_OP(bpy.types.Operator):
    bl_idname = "anm.copy_anim_data"
    bl_label = "Copy selected Animation Data"
    bl_description = "Copies all selected Animation Data from the active to all selected objects"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        selectedObjects = context.selected_objects
        activeObject = context.active_object

        from_anim_data = activeObject.animation_data

        for obj in selectedObjects:
            if obj is activeObject:
                continue
            if not obj.animation_data:
                obj.animation_data_create()
            copy_anim_data(from_anim_data, obj.animation_data)

        return {'FINISHED'}

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
    #new_track.active = track.active
    #new_track.is_override_data = track.is_override_data
    #new_track.is_solo = track.is_solo
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