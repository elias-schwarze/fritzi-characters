import bpy
from bpy.app.handlers import persistent

class FCHAR_OT_Alert_Lineart_InFront_Op(bpy.types.Operator):

    bl_idname = "utils.alert_lineart_infront"
    bl_label = "Lineart InFront Alert"
    bl_description = "Alerts user if Fritzi lineart is not in front"
    bl_options = {'INTERNAL'}

    def invoke(self, context, event):
        self.report({'WARNING'}, "Fritzi Lineart is NOT in Front!")
        return context.window_manager.invoke_props_dialog(self, width=600)
    
    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.label(text="Fritzi Lineart is NOT in front!")
        col.label(text="Certain lineart features might not be working as expected!")

    def execute(self, context):
        return {'FINISHED'}
    
@persistent
def alert_lineart_infront_postLoad_handler(dummy):
    gp_ob = bpy.context.scene.gp_defaults.gp_object
    if not gp_ob:
        return
    
    if not gp_ob.show_in_front:
        bpy.ops.utils.alert_lineart_infront('INVOKE_DEFAULT')

    return {'FINISHED'}

def register():
    bpy.utils.register_class(FCHAR_OT_Alert_Lineart_InFront_Op)
    bpy.app.handlers.load_post.append(alert_lineart_infront_postLoad_handler)

def unregister():
    bpy.app.handlers.load_post.remove(alert_lineart_infront_postLoad_handler)
    bpy.utils.unregister_class(FCHAR_OT_Alert_Lineart_InFront_Op)
    