import bpy

from bpy.types import Operator

from bpy.app.handlers import persistent

from ..driver_generator.utility_functions.fdg_driver_utils import append_function_unique, remove_function

class CAV_OT_ActivateAutoToggleCamVisibility_OP(Operator):
    bl_idname = "object.activate_auto_toggle_cam_visibility"
    bl_label = "On"
    bl_description = "Enable Auto Toggle Camera Rig Visibilities on Active Camera change."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.context.scene.auto_visibility_toggle = True
        append_function_unique(bpy.app.handlers.frame_change_pre, on_frame_change_visibility_handler)

        return {'FINISHED'}

class CAV_OT_DeactivateAutoToggleCamVisibility_OP(Operator):
    bl_idname = "object.deactivate_auto_toggle_cam_visibility"
    bl_label = "Off"
    bl_description = "Disable Auto Toggle Camera Rig Visibilities on Active Camera change."
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):
        bpy.context.scene.auto_visibility_toggle = False
        remove_function(bpy.app.handlers.frame_change_pre, on_frame_change_visibility_handler)


        return {'FINISHED'}

@persistent
def on_frame_change_visibility_handler(dummy):
    """Handler which disables all camera collections in the viewport, which do not correspond to the active camera"""
    #print("Yay")
    last_active_camera = bpy.context.window_manager.last_active_camera
    active_camera = bpy.context.scene.camera
    #if last_active_camera is None:
    #    bpy.context.window_manager.last_active_camera = active_camera
    
    if active_camera is last_active_camera:
        return
    bpy.context.window_manager.last_active_camera = active_camera
    #print(active_camera.name)

    for c in bpy.data.collections:
        if c.name.startswith('CAM.') or c.name.startswith('CAM_'):
            
            if c.name.endswith(active_camera.name[-3:]):
                c.hide_viewport = False
            else:
                c.hide_viewport = True
        #print(c.name)


def register():
    bpy.utils.register_class(CAV_OT_ActivateAutoToggleCamVisibility_OP)
    bpy.utils.register_class(CAV_OT_DeactivateAutoToggleCamVisibility_OP)


def unregister():
    bpy.utils.unregister_class(CAV_OT_DeactivateAutoToggleCamVisibility_OP)
    bpy.utils.unregister_class(CAV_OT_ActivateAutoToggleCamVisibility_OP)
