import bpy

from bpy.types import Operator

from bpy.app.handlers import persistent
from ..utility_functions.fdg_driver_utils import append_function_unique
from ..utility_functions.fdg_driver_utils import remove_function
from ..utility_functions.fdg_driver_utils import parent_objects, link_camera, add_auto_link_handler, remove_auto_link_handler
from ..utility_functions import fdg_names


class FDG_OT_LinkCamera_Op(Operator):
    bl_idname = "object.link_camera"
    bl_label = "Link this Camera"
    bl_description = "Link all Generated Drivers to this Camera"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        

        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        
        wm = bpy.context.window_manager

        cam = wm.camera

        if cam is None:
            self.report({'WARNING'}, "Please select the Camera!")
            return {'CANCELLED'}

        if cam.type != 'CAMERA':
            self.report({'WARNING'}, "Please select a Camera!")

        link_camera(cam)

        self.report({'INFO'}, "Camera Linked!")
        return {'FINISHED'}

class FDG_OT_ActivateAutoLinkCamera_Op(Operator):
    bl_idname = "object.activate_auto_link_camera"
    bl_label = "Auto Link On"
    bl_description = "Auto link camera toggle on"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        add_auto_link_handler()

        return {'FINISHED'}

class FDG_OT_DeactivateAutoLinkCamera_Op(Operator):
    bl_idname = "object.deactivate_auto_link_camera"
    bl_label = "Auto Link Off"
    bl_description = "Auto link camera toggle off"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        remove_auto_link_handler()

        return {'FINISHED'}


@persistent
def frame_change_handler(dummy):
    """Handler which gathers the active camera and links the camera empty to it"""
    camera = bpy.context.scene.camera
    link_camera(camera)


def register():
    bpy.utils.register_class(FDG_OT_LinkCamera_Op)
    bpy.utils.register_class(FDG_OT_ActivateAutoLinkCamera_Op)
    bpy.utils.register_class(FDG_OT_DeactivateAutoLinkCamera_Op)

def unregister():
    bpy.utils.unregister_class(FDG_OT_DeactivateAutoLinkCamera_Op)
    bpy.utils.unregister_class(FDG_OT_ActivateAutoLinkCamera_Op)
    bpy.utils.unregister_class(FDG_OT_LinkCamera_Op)