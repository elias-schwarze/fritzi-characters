from fileinput import close
import bpy
import json
import os

from bpy.types import Operator

class FMR_OT_MocapRetarget_OP(Operator):
    bl_idname = "object.mocap_retarget"
    bl_label = "Retarget Mocap"
    bl_description = "Use Auto-Rig-Pro to retarget Mocap to Control Rigs"
    bl_options = {"REGISTER"}

    settings = {}
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

        # Scale Source Mesh to Target Mesh
        self.report({'INFO'}, "Scaling Source Armature!")
        bpy.ops.arp.auto_scale()
        

        # Build Bone List. This will then be overwritten with custom Bone Map
        self.report({'INFO'}, "Finished Scaling Source Armature. Building Bone List!")
        bpy.ops.arp.build_bones_list()

        # Import custom Bone List
        self.report({'INFO'}, "finished Building Bone List. Fetching Bone Map Location!")
        print(os.path.dirname(__file__))

        with open(self.json_path, 'r') as f:
            self.settings = json.load(f)
            f.close()

        print(self.settings["bone_map_path"])
        bone_map_path = self.settings["bone_map_path"]
        self.load_bone_map(context, bone_map_path)



        
        
        self.report({'INFO'}, "Fetched Bone Map Lcoation. Importing Bone Map!")
        #bpy.ops.arp.import_config(filepath=bone_map_path)

        # Redefine Rest Pose
        self.report({'INFO'}, "Imported Bone Map. Redefining Rest Pose!")
        bpy.ops.arp.redefine_rest_pose(preserve=True, rest_pose='REST')

        self.report({'INFO'}, "Selecting Pose Bones!")
        wm = context.window_manager

        for myBone in wm.source_rig_pointer.pose.bones:
            myBone.bone.select = True

        myBone = wm.source_rig_pointer.pose.bones["RightFoot"]
        myBone.bone.select = False
        myBone = wm.source_rig_pointer.pose.bones["LeftFoot"]
        myBone.bone.select = False

        self.report({'INFO'}, "Copying Bone Rotations!")
        bpy.ops.arp.copy_bone_rest()
        self.report({'INFO'}, "Saving Rest Position!")
        bpy.ops.arp.save_pose_rest()
        

        # Retarget
        start, end = wm.source_rig_pointer.animation_data.action.frame_range
        self.report({'INFO'}, "Finished redefining Rest Pose. Retargeting Mocap!")
        bpy.ops.arp.retarget(frame_start=start, frame_end=end, interpolation_type='BEZIER', handle_type='AUTO_CLAMPED')


        self.report({'INFO'}, "Finished Retargeting Mocap!")
        return {'FINISHED'}


    def load_bone_map(self, context, bone_map_path):

        try:
            bpy.ops.arp.import_config(filepath=bone_map_path)
            
        except Exception:
            bone_map_path = os.path.join(os.path.join(os.path.dirname(__file__),"BoneMap"),"IKlegFKarm.bmap")
            with open(self.json_path, 'w') as f:
                self.settings["bone_map_path"] = bone_map_path
                json.dump(self.settings, f)
                f.close()
            try:
                bpy.ops.arp.import_config(filepath=bone_map_path)

            except Exception:
                return False

        return True


def register():
    bpy.utils.register_class(FMR_OT_MocapRetarget_OP)

def unregister():
    bpy.utils.unregister_class(FMR_OT_MocapRetarget_OP)