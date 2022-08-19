import bpy

class FDG_PT_DriverGenerator_pnl(bpy.types.Panel):
    bl_label = "Driver Generator"
    bl_category = "FCHAR"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"DEFAULT_CLOSED"}
    
    def draw(self, context):
        

        pass


def register():
    bpy.utils.register_class(FDG_PT_DriverGenerator_pnl)

def unregister():
    bpy.utils.unregister_class(FDG_PT_DriverGenerator_pnl)