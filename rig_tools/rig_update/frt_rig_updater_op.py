import bpy
from . import frt_bone_list_io
from ...helper_functions import update_dependencies_all_drivers

class FRT_OT_RigUpdater_OP(bpy.types.Operator):
    bl_idname = "object.update_fritzi_rig"
    bl_label = "Update Fritzi Rig"
    bl_description = "Updates the Bone Hierarchy with the new Bones"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        wm = context.window_manager

        if not wm.update_rig:
            return False

        return True

    def execute(self, context):
        wm = context.window_manager
        bone_list_io = frt_bone_list_io.BoneList()
        bone_list = bone_list_io.get_bone_list()
        constraint_update_list = bone_list_io.get_constraint_update_list()
        constraint_add_list = bone_list_io.get_constraint_add_list()

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')

        wm.update_rig.select_set(True)
        bpy.context.view_layer.objects.active = wm.update_rig

        bpy.ops.object.mode_set(mode='EDIT')

        self.reparent_bones(wm.update_rig, bone_list)
        

        bpy.ops.object.mode_set(mode='OBJECT')
        
        self.update_constraints(constraint_update_list, wm.update_rig)

        self.add_constraints(wm.update_rig, constraint_add_list)

        update_dependencies_all_drivers()
        return {'FINISHED'}

    def reparent_bones(self, armature, bone_list):
        for entry in bone_list:
            
            
            
            bone_names = entry["children_list"]            
            old_parent_name = entry["old_parent_name"]
            new_parent_name = entry["new_parent_name"]
            mirrored_list = self.mirror_bone_list(bone_names)
            mirrored_old_parent_name = None
            if old_parent_name:
                mirrored_old_parent_name = old_parent_name.replace(".l", ".r")
            mirrored_new_parent_name = new_parent_name.replace(".l", ".r")

            
            
            if entry["children_list"] == "*":
                bone_names = self.bone_list_from_children(armature, old_parent_name)
                mirrored_list = self.bone_list_from_children(armature, mirrored_old_parent_name)
            
            for bone_name in bone_names:
                self.parent_bone(armature, bone_name, new_parent_name)

            if entry["do_mirror"]:
                for bone_name in mirrored_list:
                    self.parent_bone(armature, bone_name, mirrored_new_parent_name)    
            

    def bone_list_from_children(self, armature, parent_bone_name):
        children_list = []
        for bone in armature.data.edit_bones[parent_bone_name].children:
            children_list.append(bone.name)
        
        return children_list

    def mirror_bone_list(self, bone_list):
        mirrored_list = []
        for name in bone_list:
            mirrored_list.append(name.replace(".l", ".r"))
        return mirrored_list

    def parent_bone(self, armature, bone_name, parent_name):
        #if bpy.context.object.mode == 'EDIT':
        bone = armature.data.edit_bones[bone_name]
        bone.use_connect = False
        bone.parent = armature.data.edit_bones[parent_name]

    def update_constraints(self, constraint_list, armature):
        for entry in constraint_list:
            #print("-----------------------------")
            bone_name = entry["bone_name"]
            #print("Bone: " + bone_name)
            pose_bone = armature.pose.bones[bone_name]

            if entry["constraints"] == "ALL_INVERSE":
                for constraint in pose_bone.constraints:
                    if constraint.type == 'CHILD_OF':
                        constraint.set_inverse_pending = True
                continue

            for constraint_data in entry["constraints"]:
                name = constraint_data["constraint_name"]
                constraint = pose_bone.constraints[name]
                type = constraint_data["constraint_type"]
                
                self.update_constraint(constraint, type, armature, constraint_data["target_bone_name"])

                if constraint_data["do_mirror"]:
                    mirror_bone = armature.pose.bones[bone_name.replace(".l", ".r")]
                    constraint = mirror_bone.constraints[name]
                    mirror_target = constraint_data["target_bone_name"].replace(".l", ".r")
                    self.update_constraint(constraint, type, armature, mirror_target)

    def update_constraint(self, constraint, type, armature, target_bone):
        #print("Constraint: " + constraint.name)
        #print("Type: " + type)
        #print("Target: " + target_bone)
        if type == 'IK':
            constraint.pole_target = armature
            constraint.pole_subtarget = target_bone
        else:
            constraint.target = armature
            constraint.subtarget = target_bone
        if type == 'CHILD_OF':
            constraint.set_inverse_pending = True

    def add_constraints(self, armature, constraint_list):
        for entry in constraint_list:
            bone_name = entry["bone_name"]
            mirror_bone_name = bone_name.replace(".l", ".r")
            pose_bone = armature.pose.bones[bone_name]
            mirror_bone = armature.pose.bones[mirror_bone_name]

            for constraint_data in entry["constraints"]:
                self.add_constraint(armature, constraint_data, pose_bone, mirror_bone)

    def add_constraint(self, armature, constraint_data, pose_bone, mirror_bone):
        type = constraint_data["constraint_type"]
        constraint = pose_bone.constraints.new(type)
        
        constraint_name = constraint_data["constraint_name"]
        target = armature
        subtarget = constraint_data["bone"]
        do_mirror = constraint_data["do_mirror"]
        target_space = constraint_data["target_space"]
        owner_space = constraint_data["owner_space"]

        constraint.name = constraint_name
        constraint.target = target
        constraint.subtarget = subtarget


        if do_mirror:
            mirror_constraint = mirror_bone.constraints.new(type)
            mirror_name = constraint_name.replace(".l", ".r")
            mirror_subtarget = subtarget.replace(".l", ".r")

            mirror_constraint.name = mirror_name
            mirror_constraint.target = target
            mirror_constraint.subtarget = mirror_subtarget
        
        if type in ['COPY_TRANSFORMS', 'COPY_ROTATION']:
            
            mix = constraint_data["mix"]
            
            
            constraint.mix_mode = mix
            constraint.target_space = target_space
            constraint.owner_space = owner_space

            if do_mirror:
                
                mirror_constraint.mix_mode = mix
                mirror_constraint.target_space = target_space
                mirror_constraint.owner_space = owner_space

        if type == 'COPY_LOCATION':
            if "head_tail" in constraint_data:
                constraint.head_tail = constraint_data["head_tail"]
            constraint.target_space = target_space
            constraint.owner_space = owner_space

            if do_mirror:
                if "head_tail" in constraint_data:
                    mirror_constraint.head_tail = constraint_data["head_tail"]
                mirror_constraint.target_space = target_space
                mirror_constraint.owner_space = owner_space

        if type == 'DAMPED_TRACK':
            track_axis = constraint_data["track_axis"]
            constraint.track_axis = track_axis

            if do_mirror:
                mirror_constraint.track_axis = track_axis


def register():
    bpy.utils.register_class(FRT_OT_RigUpdater_OP)

def unregister():
    bpy.utils.unregister_class(FRT_OT_RigUpdater_OP)