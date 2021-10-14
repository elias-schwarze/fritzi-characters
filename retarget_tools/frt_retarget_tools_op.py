import bpy
from math import radians
from mathutils import Vector

from bpy.types import Operator

class FRT_OT_Retarget_Op(Operator):

    bl_idname = "object.retarget"
    bl_label = "Retarget Animation"
    bl_description = "Retarget FK to IK Animation. Please use only on Frame 0 or in Rest Position Frame."
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        
        #rig muss im fk modus sein sonst funktioniert dasuebertragen nicht!!!!!!!!!!!!!
        frame_sta = bpy.context.scene.num7 
        frame_ende = bpy.context.scene.num8

        rig_input = bpy.context.scene.object7.name
        rig_mocap = bpy.context.scene.object8.name

        #bones fk
        hand_l_fk = 'hand.l'
        hand_r_fk = 'hand.r'

        pole_target_l_fk = 'forearm_stretch.l'
        pole_target_r_fk = 'forearm_stretch.r'

        #bones ik
        hand_l_ik = 'c_hand_ik.l'
        hand_r_ik = 'c_hand_ik.r'

        pole_l_ik = 'c_arms_pole.l'
        pole_r_ik = 'c_arms_pole.r'

        #Empty names
        hand_l_empty = 'hand_l_empty'
        hand_r_empty = 'hand_r_empty'

        pole_l_empty = 'pole_l_empty'
        pole_r_empty = 'pole_r_empty'

        m_thumb1_l = 'LeftHandThumb1'
        m_thumb2_l = 'LeftHandThumb2'
        m_thumb3_l = 'LeftHandThumb3'

        m_thumb1_r = 'RightHandThumb1'
        m_thumb2_r = 'RightHandThumb2'
        m_thumb3_r = 'RightHandThumb3'

        thumb1_l = 'c_thumb1.l'
        thumb2_l = 'c_thumb2.l'
        thumb3_l = 'c_thumb3.l'

        thumb1_r = 'c_thumb1.r'
        thumb2_r = 'c_thumb2.r'
        thumb3_r = 'c_thumb3.r'

        thumb1_l_empty = 'thumb1_l_empty'
        thumb2_l_empty = 'thumb2_l_empty'
        thumb3_l_empty = 'thumb3_l_empty'

        thumb1_r_empty = 'thumb1_r_empty'
        thumb2_r_empty = 'thumb2_r_empty'
        thumb3_r_empty = 'thumb3_r_empty'


        #creates constraint for empties for the hands
        def addCopyRotLoc(rig, bone):
            obj = bpy.context.active_object
            constraint = obj.constraints.new(type='COPY_ROTATION')
            target_obj = bpy.data.objects[rig]
            target_bone = bone
            constraint.target = target_obj
            constraint.subtarget = target_bone

            constraint = obj.constraints.new(type='COPY_LOCATION')
            constraint.target = target_obj
            constraint.subtarget = target_bone 
            
        def addCopyRotLocThumb(rig, bone):
            obj = bpy.context.active_object
            constraint = obj.constraints.new(type='COPY_ROTATION')
            target_obj = bpy.data.objects[rig]
            target_bone = bone
            constraint.target = target_obj
            constraint.subtarget = target_bone
            obj.constraints["Copy Rotation"].mix_mode = 'OFFSET'

            constraint = obj.constraints.new(type='COPY_LOCATION')
            constraint.target = target_obj
            constraint.subtarget = target_bone 
            
        #add child of constraint for the pole empty
        def addChildOf(rig, bone):
            obj = bpy.context.active_object
            constraint = obj.constraints.new(type='CHILD_OF')
            target_obj = bpy.data.objects[rig]
            target_bone = bone
            constraint.target = target_obj
            constraint.subtarget = target_bone
            bpy.context.active_object.constraints[0].inverse_matrix  #selbe wie set inverse
            #bpy.context.active_object.constraints[0].inverse_matrix # zweimal clear inverse???
            
        def bakeActionObj():
            bpy.ops.nla.bake(frame_start=frame_sta, frame_end=frame_ende, visual_keying=True, clear_constraints=True, clear_parents=True, use_current_action=True, bake_types={'OBJECT'})

            
        def EnterPoseMode(rig):
            
            bpy.ops.object.select_all(action='DESELECT')
            
            ob =  bpy.data.objects[rig]
            bpy.context.view_layer.objects.active = ob 
            ob.select_set(True)
            bpy.ops.object.mode_set(mode='POSE')
            
        def EnterEditMode(rig):
            
            bpy.ops.object.select_all(action='DESELECT')
            
            ob =  bpy.data.objects[rig]
            bpy.context.view_layer.objects.active = ob 
            ob.select_set(True)
            bpy.ops.object.mode_set(mode='EDIT')

        def createEmpty(name, type, radi, loc, rot):
            bpy.ops.object.empty_add(type=type,radius=radi,location = loc, rotation = rot)
            bpy.context.active_object.name = name
            
            

        def BakeFKAction(rig, hand_loc_l, hand_loc_r, pole_loc_l, pole_loc_r):
            #left arm Empties
            #hand
            createEmpty(hand_l_empty, 'PLAIN_AXES', 0.2, hand_loc_l, (0,0,0))
            addCopyRotLoc(rig_input, hand_l_fk)

            #bake
            bakeActionObj()

            #pole
            createEmpty(pole_l_empty, 'ARROWS', 0.2, pole_loc_l, (0,0,0))
            addChildOf(rig_input, pole_target_l_fk)

            #bake
            bakeActionObj()


            #right arm Empties
            #hand
            createEmpty(hand_r_empty, 'PLAIN_AXES', 0.2, hand_loc_r, (0,0,0)) 
            addCopyRotLoc(rig_input, hand_r_fk)
            
            #bake
            bakeActionObj()

            #pole
            createEmpty(pole_r_empty, 'ARROWS', 0.2, pole_loc_r, (0,0,0))
            addChildOf(rig_input, pole_target_r_fk)

            #bake animation to empties
            bakeActionObj()

        
        
    #add copy rotation copy location to ik hand and pole

        def addCopyRotLocBone(rig, bone, empty):
            obj = bpy.data.objects[rig].pose.bones[bone]
            constraint = obj.constraints.new(type='COPY_ROTATION')
            target_obj = bpy.data.objects[empty]
            constraint.target = target_obj

            constraint = obj.constraints.new(type='COPY_LOCATION')
            constraint.target = target_obj 
            
        def copyLocBone(rig, bone, empty):
            obj = bpy.data.objects[rig].pose.bones[bone]
            constraint = obj.constraints.new(type='COPY_LOCATION')
            target_obj = bpy.data.objects[empty]
            constraint.target = target_obj
            
        def copyRotBone(rig, bone, empty):
            obj = bpy.data.objects[rig].pose.bones[bone]
            constraint = obj.constraints.new(type='COPY_ROTATION')
            target_obj = bpy.data.objects[empty]
            constraint.target = target_obj
            
        def boneMakeActive(bone):
            boneToSelect = bpy.data.objects[rig_input].pose.bones[bone].bone
            bpy.context.object.data.bones.active = boneToSelect
            #Select in viewport
            boneToSelect.select = True

        def ikConstraints():

            #left arm
            #hand
            addCopyRotLocBone(rig_input, hand_l_ik, hand_l_empty)
            
            #pole
            copyLocBone(rig_input, pole_l_ik, pole_l_empty)
            
            #right arm
            #hand
            addCopyRotLocBone(rig_input, hand_r_ik, hand_r_empty)
            
            #pole
            copyLocBone(rig_input, pole_r_ik, pole_r_empty)
            
            
            ##############bake action to ik bones
            EnterPoseMode(rig_input)
            
            ##hands
            boneMakeActive(hand_l_ik)
            bpy.ops.nla.bake(frame_start=frame_sta, frame_end=frame_ende, visual_keying=True, use_current_action=True, bake_types={'POSE'})
            bpy.ops.constraint.delete(constraint="Copy Location", owner='BONE')
            bpy.ops.constraint.delete(constraint="Copy Rotation", owner='BONE')
            
            boneMakeActive(hand_r_ik)
            bpy.ops.nla.bake(frame_start=frame_sta, frame_end=frame_ende, visual_keying=True, use_current_action=True, bake_types={'POSE'})
            bpy.ops.constraint.delete(constraint="Copy Location", owner='BONE')
            bpy.ops.constraint.delete(constraint="Copy Rotation", owner='BONE')    
            
            ##poles
            boneMakeActive(pole_l_ik)
            bpy.ops.nla.bake(frame_start=frame_sta, frame_end=frame_ende, visual_keying=True, use_current_action=True, bake_types={'POSE'})
            bpy.ops.constraint.delete(constraint="Copy Location", owner='BONE')
            
                
            boneMakeActive(pole_r_ik)
            bpy.ops.nla.bake(frame_start=frame_sta, frame_end=frame_ende, visual_keying=True, use_current_action=True, bake_types={'POSE'})
            bpy.ops.constraint.delete(constraint="Copy Location", owner='BONE')


        def deleteEmpties(empty):
            
            object_to_delete = bpy.data.objects[empty]
            bpy.data.objects.remove(object_to_delete, do_unlink=True)
            
        def createThumbEmpties():
            
            createEmpty(thumb1_l_empty, 'PLAIN_AXES', 0.05, (0,0,0), (0,radians(-90),0))
            addCopyRotLocThumb(rig_mocap, m_thumb1_l)
            createEmpty(thumb2_l_empty, 'PLAIN_AXES', 0.05, (0,0,0), (0,radians(-90),0))
            addCopyRotLocThumb(rig_mocap, m_thumb2_l)
            createEmpty(thumb3_l_empty, 'PLAIN_AXES', 0.05, (0,0,0), (0,radians(-90),0))
            addCopyRotLocThumb(rig_mocap, m_thumb3_l)
            
            createEmpty(thumb1_r_empty, 'PLAIN_AXES', 0.05, (0,0,0), (0,radians(90),0))
            addCopyRotLocThumb(rig_mocap, m_thumb1_r)
            createEmpty(thumb2_r_empty, 'PLAIN_AXES', 0.05, (0,0,0), (0,radians(90),0))
            addCopyRotLocThumb(rig_mocap, m_thumb2_r)
            createEmpty(thumb3_r_empty, 'PLAIN_AXES', 0.05, (0,0,0), (0,radians(90),0))
            addCopyRotLocThumb(rig_mocap, m_thumb3_r)
            
        def thumbBoneConstraints():
            #print('hello')
            copyRotBone(rig_input, thumb1_l, thumb1_l_empty)
            copyRotBone(rig_input, thumb2_l, thumb2_l_empty)
            copyRotBone(rig_input, thumb3_l, thumb3_l_empty)
            
            copyRotBone(rig_input, thumb1_r, thumb1_r_empty)
            copyRotBone(rig_input, thumb2_r, thumb2_r_empty)
            copyRotBone(rig_input, thumb3_r, thumb3_r_empty)
            
        def bakeThumbs(thumb):
            boneMakeActive(thumb)
            bpy.ops.nla.bake(frame_start=frame_sta, frame_end=frame_ende, visual_keying=True, use_current_action=True, bake_types={'POSE'})
            bpy.ops.constraint.delete(constraint="Copy Rotation", owner='BONE')
            

        EnterEditMode(rig_input)
        ##noch schauen ob rotation kopieren sinn macht fuer die pole empties    
        hand_loc_l = bpy.data.objects.get(rig_input).data.edit_bones[hand_l_fk].head
        #print(hand_loc_l)

        hand_loc_r = bpy.data.objects.get(rig_input).data.edit_bones[hand_r_fk].head
        #print(hand_loc_r)

        pole_loc_l = bpy.data.objects.get(rig_input).data.edit_bones[pole_target_l_fk].head + Vector((-0.05, 0.2, 0))

        pole_loc_r = bpy.data.objects.get(rig_input).data.edit_bones[pole_target_r_fk].head + Vector((0.05, 0.2, 0))


        bpy.ops.object.mode_set(mode='OBJECT')

        BakeFKAction(rig_input, hand_loc_l, hand_loc_r, pole_loc_l, pole_loc_r)

        ikConstraints()

        bpy.ops.object.mode_set(mode='OBJECT')

        ###delete empties for arms
        deleteEmpties(hand_l_empty)
        deleteEmpties(hand_r_empty)

        deleteEmpties(pole_l_empty)
        deleteEmpties(pole_r_empty)

        ####transferThumb animation####


        createThumbEmpties()
        thumbBoneConstraints()

        EnterPoseMode(rig_input)
        bakeThumbs(thumb1_l)
        bakeThumbs(thumb2_l)
        bakeThumbs(thumb3_l)

        bakeThumbs(thumb1_r)
        bakeThumbs(thumb2_r)
        bakeThumbs(thumb3_r)


        bpy.ops.object.mode_set(mode='OBJECT')

        ###delete Thumb empties
        deleteEmpties(thumb1_l_empty)
        deleteEmpties(thumb2_l_empty)
        deleteEmpties(thumb3_l_empty)

        deleteEmpties(thumb1_r_empty)
        deleteEmpties(thumb2_r_empty)
        deleteEmpties(thumb3_r_empty)

        return{'FINISHED'}





def register():
    bpy.utils.register_class(FRT_OT_Retarget_Op)

def unregister():
    bpy.utils.unregister_class(FRT_OT_Retarget_Op)
