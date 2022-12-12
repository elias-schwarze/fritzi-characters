import bpy
from . import frt_bone_list_io

class FRT_OT_RigUpdater_OP(bpy.types.Operator):
    bl_idname = "object.update_fritzi_rig"
    bl_label = "Update Fritzi Rig"
    bl_description = "Updates the Bone Hierarchy with the new Bones"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bone_list = frt_bone_list_io.BoneList().get_bone_list()
        return {'FINISHED'}

def register():
    bpy.utils.register_class(FRT_OT_RigUpdater_OP)

def unregister():
    bpy.utils.unregister_class(FRT_OT_RigUpdater_OP)