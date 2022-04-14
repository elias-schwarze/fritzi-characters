import bpy

from bpy.props import PointerProperty

class FDG_PT_DriverGenOutlines_pnl(bpy.types.Panel):
    bl_label = "Outline Driver Generator"
    bl_category = "FCHAR"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"DEFAULT_CLOSED"}
    bl_parent_id = "FDG_PT_DriverGenerator_pnl"

    bpy.types.WindowManager.gp_object = PointerProperty(name="Grease Pencil", type = bpy.types.Object)


    def draw(self, context):
        wm = context.window_manager
        layout = self.layout

        layout.prop_search(wm, "character_rig", bpy.data, "objects", text="Character Rig")
        rig = wm.character_rig
        if rig:
            if rig.type == 'ARMATURE':
                layout.prop_search(wm, "character_rig_bone", rig.data, "bones")
                if 'c_root_master.x' in rig.data.bones:
                    wm.character_rig_bone = 'c_root_master.x'

        layout.prop_search(wm, "gp_object", bpy.data, "objects", text="Grease Pencil")

        layout.prop_search(wm, "camera", bpy.data, "objects", text="Camera")

        layout.operator("fdg.gen_outline_driver")
        pass


def register():
    bpy.utils.register_class(FDG_PT_DriverGenOutlines_pnl)

def unregister():
    bpy.utils.unregister_class(FDG_PT_DriverGenOutlines_pnl)