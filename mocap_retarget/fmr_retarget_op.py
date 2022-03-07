from fileinput import close
import bpy
import json
import os
from . import fmr_settings

from bpy.types import Operator

class FMR_OT_MocapRetarget_OP(Operator):
    bl_idname = "object.mocap_retarget"
    bl_label = "Retarget Mocap"
    bl_description = "Use Auto-Rig-Pro to retarget Mocap to Control Rigs"
    bl_options = {"REGISTER","UNDO"}

    settings = None
    json_path = os.path.join(
            os.path.dirname(__file__),
            "fmr_settings.json")

    # should only work in object mode
    @classmethod
    def poll(cls, context):
        obj = bpy.context.object

        if obj:
            if obj.mode == "OBJECT":
                return True

        return False

    def execute(self, context):
        
        self.settings = fmr_settings.Settings()
        wm = context.window_manager

        # Scale Source Mesh to Target Mesh
        if (wm.auto_scale_check):
            bpy.ops.arp.auto_scale()
        

        # Build Bone List. This will then be overwritten with custom Bone Map
        
        bpy.ops.arp.build_bones_list()

        # Import custom Bone List
  
        self.load_bone_map(context, self.settings.get_setting("bone_map_path"))


        # Redefine Rest Pose
        bpy.ops.arp.redefine_rest_pose(preserve=True, rest_pose='REST')

        self.select_rest_bones(context)
        

        bpy.ops.arp.copy_bone_rest()
        bpy.ops.arp.save_pose_rest()
        

        # Retarget
        start, end = context.window_manager.source_rig_pointer.animation_data.action.frame_range
        bpy.ops.arp.retarget(frame_start=start, frame_end=end, interpolation_type='BEZIER', handle_type='AUTO_CLAMPED')


        self.report({'INFO'}, "Finished Retargeting Mocap!")
        return {'FINISHED'}


    def load_bone_map(self, context, bone_map_path):

        try:
            bpy.ops.arp.import_config(filepath=bone_map_path)
            
        except Exception:
            bone_map_path = os.path.join(os.path.join(os.path.dirname(__file__),"BoneMap"),"IKlegFKarm.bmap")
            self.settings.set_setting("bone_map_path", bone_map_path)
            
            try:
                bpy.ops.arp.import_config(filepath=bone_map_path)

            except Exception:
                return False

        return True

    

    def select_rest_bones(self, context):
        wm = context.window_manager

        for myBone in wm.source_rig_pointer.pose.bones:
            myBone.bone.select = True

        myBone = wm.source_rig_pointer.pose.bones["RightFoot"]
        myBone.bone.select = False
        myBone = wm.source_rig_pointer.pose.bones["LeftFoot"]
        myBone.bone.select = False


def register():
    bpy.utils.register_class(FMR_OT_MocapRetarget_OP)

def unregister():
    bpy.utils.unregister_class(FMR_OT_MocapRetarget_OP)