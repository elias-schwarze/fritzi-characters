import bpy
from bpy.types import Panel

class FCHAR_PT_RigTools_pnl(bpy.types.Panel):
    bl_label = "Rig Tools"
    bl_category = "FCHAR"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        col = layout.column()

        col.operator("armature.create_spine_master")

        

def register():
    bpy.utils.register_class(FCHAR_PT_RigTools_pnl)

def unregister():
    bpy.utils.unregister_class(FCHAR_PT_RigTools_pnl)