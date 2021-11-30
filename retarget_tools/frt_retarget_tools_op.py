import bpy
from math import radians

from bpy.types import Operator


class FRT_OT_Retarget_Op(Operator):

    bl_idname = "object.retarget"
    bl_label = "Retarget Thumbs"
    bl_description = "Retarget the thumbs from Mocap to Character Rig."
    bl_options = {"REGISTER", "UNDO"}

    # should only work in object mode and if both armatures are not null
    @classmethod
    def poll(cls, context):

        if (bpy.context.window_manager.retargetArmature is None):
            return False

        if (bpy.context.window_manager.mocapSourceArmature is None):
            return False

        if (bpy.context.window_manager.mocapSourceArmature == bpy.context.window_manager.retargetArmature):
            return False

        obj = context.object
        if not obj:
            return True
        if obj:
            if obj.mode == "OBJECT":
                return True
        return False

    def execute(self, context):

        frame_sta = bpy.context.scene.frame_start
        frame_ende = bpy.context.scene.frame_end

        #frame_sta = bpy.context.scene.num7
        #frame_ende = bpy.context.scene.num8

        rig_input = bpy.context.window_manager.retargetArmature.name
        rig_mocap = bpy.context.window_manager.mocapSourceArmature.name

        # Empty names

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

        def EnterPoseMode(rig):
            bpy.ops.object.select_all(action='DESELECT')

            ob = bpy.data.objects[rig]
            bpy.context.view_layer.objects.active = ob
            ob.select_set(True)
            bpy.ops.object.mode_set(mode='POSE')

        def createEmpty(name, type, radi, loc, rot):
            bpy.ops.object.empty_add(
                type=type, radius=radi, location=loc, rotation=rot)
            bpy.context.active_object.name = name

        def copyRotBone(rig, bone, empty):
            obj = bpy.data.objects[rig].pose.bones[bone]
            constraint = obj.constraints.new(type='COPY_ROTATION')
            target_obj = bpy.data.objects[empty]
            constraint.target = target_obj

        # selects Bones without deselecting already selected
        def boneMakeActive(bone):
            boneToSelect = bpy.data.objects[rig_input].pose.bones[bone].bone
            bpy.context.object.data.bones.active = boneToSelect
            #Select in viewport
            boneToSelect.select = True

        def deleteEmpties(empty):

            object_to_delete = bpy.data.objects[empty]
            bpy.data.objects.remove(object_to_delete, do_unlink=True)

        def createThumbEmpties():

            createEmpty(thumb1_l_empty, 'PLAIN_AXES', 0.05,
                        (0, 0, 0), (0, radians(-90), 0))
            addCopyRotLocThumb(rig_mocap, m_thumb1_l)
            createEmpty(thumb2_l_empty, 'PLAIN_AXES', 0.05,
                        (0, 0, 0), (0, radians(-90), 0))
            addCopyRotLocThumb(rig_mocap, m_thumb2_l)
            createEmpty(thumb3_l_empty, 'PLAIN_AXES', 0.05,
                        (0, 0, 0), (0, radians(-90), 0))
            addCopyRotLocThumb(rig_mocap, m_thumb3_l)

            createEmpty(thumb1_r_empty, 'PLAIN_AXES', 0.05,
                        (0, 0, 0), (0, radians(90), 0))
            addCopyRotLocThumb(rig_mocap, m_thumb1_r)
            createEmpty(thumb2_r_empty, 'PLAIN_AXES', 0.05,
                        (0, 0, 0), (0, radians(90), 0))
            addCopyRotLocThumb(rig_mocap, m_thumb2_r)
            createEmpty(thumb3_r_empty, 'PLAIN_AXES', 0.05,
                        (0, 0, 0), (0, radians(90), 0))
            addCopyRotLocThumb(rig_mocap, m_thumb3_r)

        def thumbBoneConstraints():
            copyRotBone(rig_input, thumb1_l, thumb1_l_empty)
            copyRotBone(rig_input, thumb2_l, thumb2_l_empty)
            copyRotBone(rig_input, thumb3_l, thumb3_l_empty)

            copyRotBone(rig_input, thumb1_r, thumb1_r_empty)
            copyRotBone(rig_input, thumb2_r, thumb2_r_empty)
            copyRotBone(rig_input, thumb3_r, thumb3_r_empty)

        def bakeThumbs():
            bpy.ops.pose.select_all(action='DESELECT')

            boneMakeActive(thumb1_l)
            boneMakeActive(thumb2_l)
            boneMakeActive(thumb3_l)

            boneMakeActive(thumb1_r)
            boneMakeActive(thumb2_r)
            boneMakeActive(thumb3_r)

            bpy.ops.nla.bake(frame_start=frame_sta, frame_end=frame_ende,
                             visual_keying=True, use_current_action=True, bake_types={'POSE'})
            bpy.ops.constraint.delete(constraint="Copy Rotation", owner='BONE')

        bpy.ops.object.mode_set(mode='OBJECT')

        ####transferThumb animation####

        createThumbEmpties()
        thumbBoneConstraints()

        EnterPoseMode(rig_input)
        bakeThumbs()

        bpy.ops.object.mode_set(mode='OBJECT')

        # delete Thumb empties
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
