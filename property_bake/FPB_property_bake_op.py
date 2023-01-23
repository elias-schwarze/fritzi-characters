import bpy
from bpy.types import Operator

class FPB_OT_PropertyBake_OP(Operator):
    bl_idname = "fpb.bake_properties"
    bl_label = "Bake Ik/Fk Properties"
    bl_description = "Bakes all the Ik/Fk switches on a character into the current action"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        wm = context.window_manager

        return {'FINISHED'}


def register():
    bpy.utils.register_class(FPB_OT_PropertyBake_OP)

def unregister():
    bpy.utils.unregister_class(FPB_OT_PropertyBake_OP)