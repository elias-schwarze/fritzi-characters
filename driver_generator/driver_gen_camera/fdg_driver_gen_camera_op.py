import bpy

from bpy.types import Operator

from bpy.app.handlers import persistent
from ..utility_functions.fdg_driver_utils import append_function_unique
from ..utility_functions.fdg_driver_utils import remove_function
from ..utility_functions.fdg_driver_utils import parent_objects
from ..utility_functions import fdg_names


class FDG_OT_LinkCamera_Op(Operator):
    bl_idname = "object.link_camera"
    bl_label = "Link this Camera"
    bl_description = "Link all Generated Drivers to this Camera"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):

        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        
        cam = bpy.context.scene.object2

        if cam is None:
            self.report({'WARNING'}, "Please select the Camera!")
            return {'CANCELLED'}

        link_camera(cam)

        self.report({'INFO'}, "Camera Linked!")
        return {'FINISHED'}

class FDG_OT_ActivateAutoLinkCamera_Op(Operator):
    bl_idname = "object.activate_auto_link_camera"
    bl_label = "Auto Link On"
    bl_description = "Auto link camera toggle on"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.context.scene.auto_link_toggle = True
        append_function_unique(bpy.app.handlers.frame_change_pre, frame_change_handler)

        return {'FINISHED'}

class FDG_OT_DeactivateAutoLinkCamera_Op(Operator):
    bl_idname = "object.deactivate_auto_link_camera"
    bl_label = "Auto Link Off"
    bl_description = "Auto link camera toggle off"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.context.scene.auto_link_toggle = False
        remove_function(bpy.app.handlers.frame_change_pre, frame_change_handler)

        return {'FINISHED'}


@persistent
def frame_change_handler(dummy):
    """Handler which gathers the active camera and links the camera empty to it"""
    camera = bpy.context.scene.camera
    link_camera(camera)

def link_camera(camera):
    """Sets the camera empty position to the position of the given camera and parents the empty to the camera. If there is no camera empty in the scene, it will be created"""

    cam_empty = bpy.context.scene.objects.get(fdg_names.emtpy_cam)

    if cam_empty is None:
            
        cam_empty = bpy.data.objects.new(fdg_names.emtpy_cam, None)

        cam_empty.location = camera.location

        bpy.context.collection.objects.link(cam_empty)

        parent_objects(camera, cam_empty)
        cam_empty.hide_viewport = True
    else:
        cam_empty.hide_viewport = False
        cam_empty.parent = None
        cam_empty.location = camera.location
        cam_empty.rotation_euler = camera.rotation_euler

        parent_objects(camera, cam_empty)
        cam_empty.hide_viewport = True

def register():
    bpy.utils.register_class(FDG_OT_LinkCamera_Op)
    bpy.utils.register_class(FDG_OT_ActivateAutoLinkCamera_Op)
    bpy.utils.register_class(FDG_OT_DeactivateAutoLinkCamera_Op)

def unregister():
    bpy.utils.unregister_class(FDG_OT_DeactivateAutoLinkCamera_Op)
    bpy.utils.unregister_class(FDG_OT_ActivateAutoLinkCamera_Op)
    bpy.utils.unregister_class(FDG_OT_LinkCamera_Op)