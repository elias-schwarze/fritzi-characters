import bpy
import mathutils

from bpy.types import Operator

from ..utility_functions.fdg_driver_utils import parent_objects

class FDG_OT_LinkCamera_Op(Operator):
    bl_idname = "object.link_camera"
    bl_label = "Link this Camera"
    bl_description = "Link all Generated Drivers to this Camera"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        
        cam = bpy.context.scene.object2

        if cam is None:
            self.report({'WARNING'}, "Please select the Camera!")
            return {'CANCELLED'}

        cam_empty = bpy.context.scene.objects.get("Empty.cam")

        if cam_empty is None:
            print("Test")
            cam_empty = bpy.data.objects.new("Empty.cam", None)

            cam_empty.location = cam.location

            bpy.context.collection.objects.link(cam_empty)

            parent_objects(cam, cam_empty)
            cam_empty.hide_viewport = True
        else:
            cam_empty.hide_viewport = False
            cam_empty.parent = None
            cam_empty.location = cam.location
            cam_empty.rotation_euler = cam.rotation_euler

            parent_objects(cam, cam_empty)
            cam_empty.hide_viewport = True

        self.report({'INFO'}, "Camera Linked!")
        return {'FINISHED'}


def register():
    bpy.utils.register_class(FDG_OT_LinkCamera_Op)

def unregister():
    bpy.utils.unregister_class(FDG_OT_LinkCamera_Op)