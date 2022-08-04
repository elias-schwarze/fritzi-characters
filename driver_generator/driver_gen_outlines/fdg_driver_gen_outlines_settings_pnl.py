import bpy

class  FDG_PT_DriverOutlinesSettings_pnl(bpy.types.Panel):
    bl_label = "Outline Settings"
    bl_category = "FCHAR"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"DEFAULT_CLOSED"}
    bl_parent_id = "FDG_PT_DriverGenOutlines_pnl"