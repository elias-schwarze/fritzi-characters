import bpy

from bpy.types import Operator

from ..utility_functions import fdg_names


class FDG_OT_RemoveDrivers_Op(Operator):
    bl_idname = "object.remove_drivers"
    bl_label = "Remove Drivers"
    bl_description = "Remove all drivers, controllers and empties which where created for the 2D Fakes, with the excetion of the shapekey drivers. To remove them use the remove option in the shapekey Panel."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

        wm = bpy.context.window_manager

        prefix = wm.character_prefix
        arma = wm.object1
        head_bone_name = wm.bone1
        cam = wm.object2

        if prefix == "":
            self.report({'WARNING'}, "Please enter a Character Prefix!")
            return {'CANCELLED'}

        if arma is None:
            self.report({'WARNING'}, "Please select the Armature!")
            return {'CANCELLED'}     

        if head_bone_name == "":
            self.report({'WARNING'}, "Please select the Head Bone!")
            return {'CANCELLED'}

        if cam is None:
            self.report({'WARNING'}, "Please select the Camera!")
            return {'CANCELLED'}

        hidden_controller_pose_bone = arma.pose.bones.get(fdg_names.hidden_controller_bone)

        if hidden_controller_pose_bone is not None:
        
            hidden_controller_pose_bone.driver_remove('["' + fdg_names.prop_angle_x + '"]')
            hidden_controller_pose_bone.driver_remove('["' + fdg_names.prop_angle_z + '"]')
            hidden_controller_pose_bone.driver_remove('["' + fdg_names.prop_shapes_left + '"]')
            hidden_controller_pose_bone.driver_remove('["' + fdg_names.prop_shapes_right + '"]')
            hidden_controller_pose_bone.driver_remove('["' + fdg_names.prop_up_down_normalize + '"]')

        bpy.ops.object.mode_set(mode='EDIT', toggle=False)

        hidden_controller_edit_bone = arma.data.edit_bones.get(fdg_names.hidden_controller_bone)
         
        if hidden_controller_edit_bone is not None:
            arma.data.edit_bones.remove(hidden_controller_edit_bone)
    
        visible_controller_edit_bone = arma.data.edit_bones.get(fdg_names.visible_controller_bone)
    
        if visible_controller_edit_bone is not None:
            arma.data.edit_bones.remove(visible_controller_edit_bone)
        
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

        empty_cam = bpy.data.objects.get(fdg_names.emtpy_cam)

        if empty_cam is not None:
            bpy.data.objects.remove(empty_cam, do_unlink=True)

        empty_head = bpy.data.objects.get(prefix + "." + fdg_names.empty_head)

        if empty_head is not None:
            bpy.data.objects.remove(empty_head, do_unlink=True)







        self.report({'INFO'}, "Removed Drivers!")
        return {'FINISHED'}


def register():
    bpy.utils.register_class(FDG_OT_RemoveDrivers_Op)


def unregister():
    bpy.utils.unregister_class(FDG_OT_RemoveDrivers_Op)