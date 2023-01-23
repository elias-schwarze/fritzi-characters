import bpy
from bpy.types import Panel
class FPB_PT_PropertyBake_pnl(Panel):

    bl_label = "Property Baking"
    bl_category = "FCHAR"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):

        wm = context.window_manager
        layout = self.layout

        layout.operator("fpb.bake_properties")

def register():
    bpy.utils.register_class(FPB_PT_PropertyBake_pnl)

def unregister():
    bpy.utils.unregister_class(FPB_PT_PropertyBake_pnl)