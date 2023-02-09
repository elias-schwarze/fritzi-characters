import bpy
from bpy.types import Panel

class FCT_PT_Tools_PNL(Panel):
    bl_label = "Tools"
    bl_category = "FCHAR"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        
        layout.operator("fct.delete_nla")

def register():
    bpy.utils.register_class(FCT_PT_Tools_PNL)

def unregister():
    bpy.utils.unregister_class(FCT_PT_Tools_PNL)
