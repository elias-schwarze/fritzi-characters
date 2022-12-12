import bpy

class FRT_PT_RigUpdater_PNL(bpy.types.Panel):
    bl_label = "Rig Updater"
    bl_category = "FCHAR"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"DEFAULT_CLOSED"}
    bl_parent_id = "FCHAR_PT_RigTools_pnl"

    def draw(self, context):
        layout = self.layout
        layout.operator("object.update_fritzi_rig")

def register():
    bpy.utils.register_class(FRT_PT_RigUpdater_PNL)

def unregister():
    bpy.utils.unregister_class(FRT_PT_RigUpdater_PNL)