import bpy

from bpy.types import Panel

class FDG_PT_Retarget_Panel_pnl(Panel):
    bl_label = "Retarget Tools"
    bl_category = "Retarget"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
       layout = self.layout

       col = layout.column()
       col.operator("object.retarget")


def register():
    bpy.utils.register_class(FDG_PT_Retarget_Panel_pnl)

def unregister():
    bpy.utils.unregister_class(FDG_PT_Retarget_Panel_pnl)

