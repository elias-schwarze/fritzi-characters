from unicodedata import name
import bpy
import os
from . import fmr_settings
from . import fmr_scale_list_io

import re

from bpy.types import Operator

class FMR_OT_MocapBatchRetarget_Op(Operator):
    bl_idname = "retarget.mocap_batch_retarget"
    bl_label = "Batch Retarget"
    bl_description = "Retarget multiple bvh files onto a character. This creates the needed filestructure on the perforce if it dies not already exist."
    
    @classmethod
    def poll(cls, context):
        return context.window_manager.bvh_files

    def execute(self, context):

        wm = context.window_manager
        settings = fmr_settings.Settings()
        scales = fmr_scale_list_io.ScaleListDict(wm)
        filepath = settings.get_setting("perforce_path")


        scene = context.scene

        if not (os.path.isdir(filepath) and os.path.isdir(os.path.join(filepath, "080_scenes")) and os.path.isdir(os.path.join(filepath, "075_capture"))):
            
            
            bpy.ops.settings.choose_perforce_path('INVOKE_DEFAULT')
            
            self.report({'WARNING'}, "Set Perforce Path first!")
            return {'FINISHED'}
        else:
            #Select BVHS and then create filestructure and retarget

            #check if bvhs are already loaded otherwise exec selection and at the end of loading exec this operator again
            if not wm.bvh_files:
                bpy.ops.retarget.select_bvhs('INVOKE_DEFAULT', filepath = settings.get_setting("perforce_path"))
            else:
                print("Files found")

                char_file_basename = os.path.basename(bpy.data.filepath)

                for bvh in wm.bvh_files:

                    #Create the filestructure
                    dir_path = get_layout_dir(filepath, bvh.name)
                    if not os.path.isdir(dir_path):
                        os.makedirs(dir_path)
                    filename = get_file_name(char_file_basename, bvh.name)
                    
                    #Save the File with proper name into the file structure
                    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(dir_path, filename))

                    #import the bvh (Scaling has to be fetched from scale List!)
                    name = char_file_basename.split("_")[2].lower()
                    scale = scales.get_scale(name)
                    do_auto_scale = False
                    if not scale:
                        scale = 1.0
                        do_auto_scale = True

                    bpy.ops.import_anim.bvh(filepath=bvh.filepath, global_scale=scale)

                    print(name)
                    print(scale)
                    print(do_auto_scale)

                    #retargeting here
                    bvh_arma_name = bvh.name.split(".")[0]
                    scene.source_rig = bvh_arma_name
                    wm.source_rig_pointer = bpy.data.objects[bvh_arma_name]
                    scene.target_rig = wm.target_rig_pointer.name
                    
                    retarget_mocap(context, do_auto_scale)

                    #save after retargeting
                    bpy.ops.wm.save_mainfile()
                    #undo retarget and import before heading to next bvh
                    # delete actions (are named after bvh and one is named after bvh with _remap suffix)
                    # delete bvh
                    # remove retargeted bvh from list
                    # goto next bvh
                    action = bpy.data.actions.get(bvh_arma_name)
                    bpy.data.actions.remove(action, do_unlink=True)
                    action = bpy.data.actions.get(bvh_arma_name + "_remap")
                    bpy.data.actions.remove(action, do_unlink=True)
                    bvh_armature = bpy.data.objects[bvh_arma_name]
                    bpy.data.objects.remove(bvh_armature, do_unlink=True)

                    

            #after each retargeted bvh delete it from the bvh list (Maybe show bvh list in UI)
            #
        

        
        return {'FINISHED'}

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
        wm = context.window_manager
        retarget_mocap(context, wm.auto_scale_check)
        #self.settings = fmr_settings.Settings()
        #wm = context.window_manager
#
        ## Scale Source Mesh to Target Mesh
        #if (wm.auto_scale_check):
        #    bpy.ops.arp.auto_scale()
        #
#
        ## Build Bone List. This will then be overwritten with custom Bone Map
        #
        #bpy.ops.arp.build_bones_list()
#
        ## Import custom Bone List
  #
        #self.load_bone_map(context, self.settings.get_setting("bone_map_path"))
#
#
        ## Redefine Rest Pose
        #bpy.ops.arp.redefine_rest_pose(preserve=True, rest_pose='REST')
#
        #self.select_rest_bones(context)
        #
#
        #bpy.ops.arp.copy_bone_rest()
        #bpy.ops.arp.save_pose_rest()
        #
#
        ## Retarget
        #start, end = context.window_manager.source_rig_pointer.animation_data.action.frame_range
        #bpy.ops.arp.retarget(frame_start=start, frame_end=end, interpolation_type='BEZIER', handle_type='AUTO_CLAMPED')


        self.report({'INFO'}, "Finished Retargeting Mocap!")
        return {'FINISHED'}




def load_bone_map(context, bone_map_path, settings):

    try:
        bpy.ops.arp.import_config(filepath=bone_map_path)
            
    except Exception:
        bone_map_path = os.path.join(os.path.join(os.path.dirname(__file__),"BoneMap"),"IKlegFKarm.bmap")
        settings.set_setting("bone_map_path", bone_map_path)
            
        try:
            bpy.ops.arp.import_config(filepath=bone_map_path)

        except Exception:
            return False

    return True

    

def select_rest_bones(context):
    wm = context.window_manager
    scene = bpy.context.scene
    
    for myBone in bpy.data.objects[scene.source_rig].pose.bones:
        myBone.bone.select = True

    myBone = bpy.data.objects[scene.source_rig].pose.bones["RightFoot"]
    myBone.bone.select = False
    myBone = bpy.data.objects[scene.source_rig].pose.bones["LeftFoot"]
    myBone.bone.select = False

def retarget_mocap(context, do_auto_scale=True):

    settings = fmr_settings.Settings()

    wm = context.window_manager

    # Scale Source Mesh to Target Mesh
    if do_auto_scale:
        bpy.ops.arp.auto_scale()
    
    # Build Bone List. This will then be overwritten with custom Bone Map
    
    bpy.ops.arp.build_bones_list()

    # Import custom Bone List

    load_bone_map(context, settings.get_setting("bone_map_path"), settings)

    # Redefine Rest Pose

    bpy.ops.arp.redefine_rest_pose(preserve=True, rest_pose='REST')
    select_rest_bones(context)
    
    bpy.ops.arp.copy_bone_rest()
    bpy.ops.arp.save_pose_rest()
    
    # Retarget
    start, end = context.window_manager.source_rig_pointer.animation_data.action.frame_range
    bpy.ops.arp.retarget(frame_start=start, frame_end=end, interpolation_type='BEZIER', handle_type='AUTO_CLAMPED')
    return True


def get_layout_dir(perforce_path, bvh_file):
    dir_path = perforce_path
    print(dir_path)
    dir_path = os.path.join(dir_path, "080_scenes")
    dir_path = os.path.join(dir_path, "010_layout")
    dir_path = os.path.join(dir_path, "s01_e0" + get_episode(bvh_file))
    dir_path = os.path.join(dir_path, "sq" + get_sequence(bvh_file))
    dir_path = os.path.join(dir_path, "Re-Target")

    return dir_path
   

def get_file_name(char_file, bvh_file):
    char_parts = char_file.split("_")
    filename = ""
    for i in range(0,3):
        filename = filename + char_parts[i] + "_"

    filename = filename + get_sequence(bvh_file)
    filename = filename + "_p" + get_part(bvh_file)
    filename = filename + "_m" + get_mocap(bvh_file)
    filename = filename + "_t" + get_take(bvh_file)
    filename = filename + ".blend"
    
    return filename

def get_episode(bvh_file):
    return bvh_file[0]

def get_sequence(bvh_file):
    parts = bvh_file.split("-")
    sequence = parts[0].split("_")[0]
    return sequence
    # nachfragen wie sequences mit a, b etc behandelt werden sollen insbesondere mit unterschiedlichen Formatierungen.
    # es gibt z.b ###a, ###_a, ### a.

def get_part(bvh_file):
    parts = bvh_file.split("-")
    for string in parts[0].split("_"):

        if string.startswith('part'):
            length = len(string)
            part = string[4:length]
            if len(part) == 1:
                return "0" + part
            return part
        
    return '01'

def get_mocap(bvh_file):
    parts = bvh_file.split("-")
    for string in parts[0].split("_"):

        if string.startswith('mc'):
            length = len(string)
            mocap = string[2:length]
            if len(mocap) == 1:
                return "0" + mocap
            if len(mocap) == 2 and re.match('[a-z]', mocap[1]):
                return "0" + mocap
            return string[2:length]

    return '01'

def get_take(bvh_file):
    parts = bvh_file.split("-")
    take = parts[1].split("_")[0]
    length = len(take)
    return take[1:length]


def register():
    bpy.utils.register_class(FMR_OT_MocapBatchRetarget_Op)
    bpy.utils.register_class(FMR_OT_MocapRetarget_OP)

def unregister():
    bpy.utils.unregister_class(FMR_OT_MocapRetarget_OP)
    bpy.utils.unregister_class(FMR_OT_MocapBatchRetarget_Op)