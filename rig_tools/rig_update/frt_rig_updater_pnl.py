import bpy
from bpy.props import PointerProperty

def poll_armature(self, object):
    if object.type == 'ARMATURE':
        return True
    return False

class FRT_PT_RigUpdater_PNL(bpy.types.Panel):
    bl_label = "Rig Updater"
    bl_category = "FCHAR"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"DEFAULT_CLOSED"}
    bl_parent_id = "FCHAR_PT_RigTools_pnl"

    bpy.types.WindowManager.update_rig = PointerProperty(name="Armature", type=bpy.types.Object, poll=poll_armature)

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager
        layout.prop_search(wm, "update_rig", bpy.data, "objects")
        layout.operator("object.update_fritzi_rig")
        layout.separator()
        layout.label(text="Utils")
        layout.operator("object.rig_inverse")
        layout.operator("object.update_dependencies")

def register():
    bpy.utils.register_class(FRT_PT_RigUpdater_PNL)

def unregister():
    bpy.utils.unregister_class(FRT_PT_RigUpdater_PNL)