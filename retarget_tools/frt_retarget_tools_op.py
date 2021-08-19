import bpy
from math import radians

from bpy.types import Operator

class FRT_OT_Retarget_Op(Operator):

    bl_idname = "object.retarget"
    bl_label = "Retarget Animation"
    bl_description = "Retarget FK to IK Animation."
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        #automatisch limit constraint für mocap rig damit keine UEberstreckung des Ellbogen passiert
        #copy bone roll von allen Bones bis auf die Fuesse
        frame_start = 0  #schauen ob die gleichen Variablen Namen Probleme machen(entweder feste frameanzahl oder aus der Szene abfragen?) 
        frame_end = 1250 

        rig_input = 'rig'

        #bones fk
        hand_l_fk = 'hand_l'
        hand_r_fk = 'hand_r'

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
            
        def bakeActionObj(frame_start, frame_end):
            bpy.ops.nla.bake(frame_start=frame_start, frame_end=frame_end, visual_keying=True, clear_constraints=True, clear_parents=True, use_current_action=True, bake_types={'OBJECT'})


            
        def EnterPoseMode(rig):
            
            bpy.ops.object.select_all(action='DESELECT')
            
            ob =  bpy.data.objects[rig]
            bpy.context.view_layer.objects.active = ob 
            ob.select_set(True)
            bpy.ops.object.mode_set(mode='POSE')
            

        def SelectBoneAndBake(rig, bone, frameStart, frameEnd):
            #select bone
            ob =  bpy.data.objects[rig]
            
            bpy.ops.pose.select_all(action='DESELECT')
            ob_bone =  ob.data.bones[bone]
            #ob_bone =  bpy.data.objects['rig'].data.bones['c_hand_ik.l']
            ob_bone.select = True
            
            #bake animation
            bpy.ops.nla.bake(frame_start=frameStart, frame_end=frameEnd, visual_keying=True, clear_constraints=True, clear_parents=True, use_current_action=True, bake_types={'POSE'})


        def BakeFKAction():
            #left arm Empties
            #hand
            #!!!location of empty needs to be determined by snapping to the selected bone
            bpy.ops.object.empty_add(type='PLAIN_AXES',radius=0.2,location=(0.351683,0.014795,0.844833))
            bpy.context.active_object.name = hand_l_empty
            
            addCopyRotLoc(rig_input, hand_l_fk)

            #bake
            bakeActionObj(frame_start, frame_end)

            #pole
            bpy.ops.object.empty_add(type='ARROWS',radius=0.2,location=(0.146159,0.30138,1.10733), rotation=(radians(-128.581),radians(6.37706),radians(83.2389)))
            bpy.context.active_object.name = 'pole_l_empty'

            addChildOf(rig_input, pole_target_l_fk)

            #bake
            bakeActionObj(frame_start, frame_end)


            #right arm Empties
            #hand
            bpy.ops.object.empty_add(type='PLAIN_AXES',radius=0.2,location=(-0.351683,0.014795,0.844833))
            bpy.context.active_object.name = 'hand_r_empty'
            
            addCopyRotLoc(rig_input, hand_r_fk)
            
            #bake
            bpy.ops.nla.bake(frame_start=0, frame_end=1250, visual_keying=True, clear_constraints=True, clear_parents=True, use_current_action=True, bake_types={'OBJECT'})

            #pole
            bpy.ops.object.empty_add(type='ARROWS',radius=0.2,location=(-0.146159,0.30138,1.10733), rotation=(radians(-128.581),radians(-6.37706),radians(-83.2389)))
            bpy.context.active_object.name = 'pole_r_empty'

            addChildOf(rig_input, pole_target_r_fk)

            #bake animation to empties
            bakeActionObj(frame_start, frame_end)



        #switch fk arms to ik arms(mal schauen ob das gut automatisch geht)

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

        def ikConstraints():

            #left arm
            #hand
            addCopyRotLocBone(rig_input, hand_l_ik, hand_l_empty)
            
            #pole
            copyLocBone(rig_input, pole_l_ik, pole_l_empty)
            
            obj = bpy.data.objects["rig"].pose.bones["c_arms_pole.l"]
            constraint = obj.constraints.new(type='COPY_LOCATION')
            target_obj = bpy.data.objects['pole_l'] ##change name after testing
            constraint.target = target_obj
            
            #bake action to ik bones
            
            obj.nla.bake(frame_start=0, frame_end=1250, visual_keying=True, clear_constraints=True, clear_parents=True, use_current_action=True, bake_types={'OBJECT'})
            
            #right arm
            #hand
            addCopyRotLocBone(rig_input, hand_r_ik, hand_r_empty)

        def deleteEmpties():
            
            object_to_delete = bpy.data.objects['hand_l']
            bpy.data.objects.remove(object_to_delete, do_unlink=True)
            
            object_to_delete = bpy.data.objects['hand_r']
            bpy.data.objects.remove(object_to_delete, do_unlink=True)
            
            object_to_delete = bpy.data.objects['pole_l']
            bpy.data.objects.remove(object_to_delete, do_unlink=True)
            
            object_to_delete = bpy.data.objects['pole_r']
            bpy.data.objects.remove(object_to_delete, do_unlink=True)


            


            BakeFKAction()    
            ikConstraints()
            SelectBoneAndBake( 'rig', 'c_hand_ik.l', 0, 400)

            bpy.ops.object.mode_set(mode='OBJECT')

            #delete empties for arms
            deleteEmpties()



            #create empties for thumbs and constraints

            #adjust empty roll -90 degree to compensate for overrotatted thumb(legacy offset ist needed in the copy rotation constraint)

            #same steps as above from here

def register():
    bpy.utils.register_class(FRT_OT_Retarget_Op)

def unregister():
    bpy.utils.unregister_class(FRT_OT_Retarget_Op)
