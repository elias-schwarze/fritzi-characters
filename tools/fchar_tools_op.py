import bpy

from bpy.types import Operator

class FCT_OT_DeleteNla_OP(Operator):
    bl_idname = "fct.delete_nla"
    bl_label = "Delete Selected Strips"
    bl_description = "Deletes all selected NLA Strips on only the ACTIVE object."
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):

        obj = context.active_object
        for track in obj.animation_data.nla_tracks:
            for strip in track.strips:
                if strip.select:
                    track.strips.remove(strip)

        return {'FINISHED'}

def register():
    bpy.utils.register_class(FCT_OT_DeleteNla_OP)

def unregister():
    bpy.utils.unregister_class(FCT_OT_DeleteNla_OP)