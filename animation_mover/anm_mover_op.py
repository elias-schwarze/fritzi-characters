import operator
import bpy
from bpy.types import PropertyGroup, UIList
from bpy.props import StringProperty, CollectionProperty, IntProperty, BoolProperty
from . import Anim_Mover



class ANM_OT_AnimMover_OP(bpy.types.Operator):
    bl_idname = "object.move_animation"
    bl_label = "Move Animation"
    bl_description = "Move all animations in the file a given Amount forwards or backwards"
    bl_options = {"REGISTER", "UNDO"}

    move_type: None
    move_direction: None
    frame_in: None
    frame_out: None
    frame_amount: None

    def execute(self, context):
        
        wm = bpy.context.window_manager
        self.move_type = wm.move_type
        self.move_direction = wm.move_direction
        self.frame_in = wm.frame_in
        self.frame_out = wm.frame_out
        self.frame_amount = wm.frame_amount
        anim_mover = Anim_Mover.Anim_Mover(wm, context)
        if wm.move_keys:
            if anim_mover.check_keys():
                print(bpy.ops.object.show_problem_keys_window('INVOKE_DEFAULT'))
                self.report({'WARNING'}, "Problem Keys")
                return {'CANCELLED'}
        
        anim_mover.move_anim()
        

        self.report({'INFO'}, "No Problem Keys")
        return {'FINISHED'}

class ANM_OT_AnimMoverBefore_OP(bpy.types.Operator):
    bl_idname = "object.move_animation_before"
    bl_label = "Before"
    bl_description = "Only move all Keyframes before a given Frame"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        wm = context.window_manager
        wm.move_type = 'BEFORE'
        

        return {'FINISHED'}

class ANM_OT_AnimMoverAfter_OP(bpy.types.Operator):
    bl_idname = "object.move_animation_after"
    bl_label = "After"
    bl_description = "Only move all Keyframes after a given Frame"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        wm = context.window_manager
        wm.move_type = 'AFTER'
        

        return {'FINISHED'}

class ANM_OT_AnimMoverBetween_OP(bpy.types.Operator):
    bl_idname = "object.move_animation_between"
    bl_label = "Between"
    bl_description = "Only move all Keyframes in a given Frame Range"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        wm = context.window_manager
        wm.move_type = 'BETWEEN'
        

        return {'FINISHED'}

class ANM_OT_AnimMoverBackward_OP(bpy.types.Operator):
    bl_idname = "object.move_animation_backward"
    bl_label = "Backwards"
    bl_description = "Move the Frames Backwards"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        wm = context.window_manager
        wm.move_direction = 'BACKWARD'
        

        return {'FINISHED'}

class ANM_OT_AnimMoverForward_OP(bpy.types.Operator):
    bl_idname = "object.move_animation_forward"
    bl_label = "Forwards"
    bl_description = "Move the Frames Forwards"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        wm = context.window_manager
        wm.move_direction = 'FORWARD'
        

        return {'FINISHED'}

class ANM_OT_ShowProblemKeysWindow_OP(bpy.types.Operator):
    bl_idname = "object.show_problem_keys_window"
    bl_label = "OK"
    bl_description = "Shows a Window with a List of all Problematic Keys"
    bl_options = {"REGISTER", "UNDO"}

    def invoke(self, context, event):
        wm = context.window_manager
        
        return wm.invoke_popup(self,width=600)

    def modal(self, context, event):
        print("HElp")
        if not context.window_manager.show_key_list_window:
            return {'FINISHED'}
        return {'RUNNING_MODAL'}

    def draw(self, context):
        
        wm = context.window_manager
        layout = self.layout
        layout.template_list("ANM_UL_KeyList_Items", "", wm, "key_list", wm, "key_list_index", rows=20)
        row = layout.row()
        row.alert = True
        row.operator("object.problem_keys_accept")
        
    def execute(self, context):
        return {'FINISHED'}


class Problem_Keys(PropertyGroup):
    """ A PropertyGroup which stores all the problematic Keys that were found while moving the Keyframes"""
    object : StringProperty()
    curve : StringProperty()
    frame : StringProperty()

class ANM_UL_KeyList_Items(UIList):
    @classmethod
    def poll(cls, context):
        return True

    def draw_item(self, context, layout, data, item, icon, active_data, active_property, index, flt_flag):
        row = layout.row()
        row = row.split(factor=0.2)
        row.label(text=item.object)
        row = row.split(factor=0.6)
        row.label(text=item.curve)
        row = row.split(factor=0.2)
        row.label(text=item.frame)

class ANM_ProblemKeyWindowAccept_OP(bpy.types.Operator):
    bl_idname = "object.problem_keys_accept"
    bl_label = "Move Keys Anyway"
    bl_description = "Does move Keys despite problems. May result in weird Animation!"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        anim_mover = Anim_Mover.Anim_Mover(bpy.context.window_manager, context)
        anim_mover.move_anim()

        return {'FINISHED'}



def register():
    bpy.utils.register_class(ANM_OT_AnimMover_OP)
    bpy.utils.register_class(ANM_OT_AnimMoverBefore_OP)
    bpy.utils.register_class(ANM_OT_AnimMoverAfter_OP)
    bpy.utils.register_class(ANM_OT_AnimMoverBetween_OP)
    bpy.utils.register_class(ANM_OT_AnimMoverForward_OP)
    bpy.utils.register_class(ANM_OT_AnimMoverBackward_OP)
    bpy.utils.register_class(Problem_Keys)
    bpy.utils.register_class(ANM_UL_KeyList_Items)
    bpy.utils.register_class(ANM_OT_ShowProblemKeysWindow_OP)
    bpy.utils.register_class(ANM_ProblemKeyWindowAccept_OP)
    bpy.types.WindowManager.key_list = CollectionProperty(name= "Key List", type = Problem_Keys)
    bpy.types.WindowManager.key_list_index = IntProperty()

def unregister():
    bpy.utils.unregister_class(ANM_ProblemKeyWindowAccept_OP)
    bpy.utils.unregister_class(ANM_OT_ShowProblemKeysWindow_OP)
    bpy.utils.unregister_class(ANM_UL_KeyList_Items)
    bpy.utils.unregister_class(Problem_Keys)
    bpy.utils.unregister_class(ANM_OT_AnimMoverBackward_OP)
    bpy.utils.unregister_class(ANM_OT_AnimMoverForward_OP)
    bpy.utils.unregister_class(ANM_OT_AnimMoverBetween_OP)
    bpy.utils.unregister_class(ANM_OT_AnimMoverAfter_OP)
    bpy.utils.unregister_class(ANM_OT_AnimMoverBefore_OP)
    bpy.utils.unregister_class(ANM_OT_AnimMover_OP)