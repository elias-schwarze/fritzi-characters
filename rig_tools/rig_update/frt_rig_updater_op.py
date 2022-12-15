import bpy
from . import frt_bone_list_io

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
        bone_list = frt_bone_list_io.BoneList().get_bone_list()

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')

        wm.update_rig.select_set(True)
        bpy.context.view_layer.objects.active = wm.update_rig

        bpy.ops.object.mode_set(mode='EDIT')

        self.reparent_bones(wm.update_rig, bone_list)

        bpy.ops.object.mode_set(mode='OBJECT')
        
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

def register():
    bpy.utils.register_class(FRT_OT_RigUpdater_OP)

def unregister():
    bpy.utils.unregister_class(FRT_OT_RigUpdater_OP)