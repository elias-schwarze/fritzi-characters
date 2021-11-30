import bpy

from bpy.types import Armature, Panel
from bpy.props import PointerProperty, IntProperty


class FDG_PT_Retarget_Panel_pnl(Panel):
    bl_label = "Retarget Tools"
    bl_category = "FCHAR"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"DEFAULT_CLOSED"}

    bpy.types.WindowManager.retargetArmature = PointerProperty(
        name="Target Armature", type=Armature)

    bpy.types.WindowManager.mocapSourceArmature = PointerProperty(
        name="Mocap Source Armature", type=Armature)

    bpy.types.WindowManager.frame_start = IntProperty(
        name='Start:', default=0, min=0, step=1)

    bpy.types.WindowManager.frame_end = IntProperty(
        name='End:', default=500, min=0, step=1)

    #bpy.types.Scene.num7 = IntProperty(name='Frame Start', default= 0, min= 0, step=1)
    #bpy.types.Scene.num8 = IntProperty(name='Frame End', default= 500, min= 0, step=1)

    def draw(self, context):
        layout = self.layout

        box = layout.box()
        box.prop_search(data=bpy.context.window_manager, property="retargetArmature", search_data=bpy.data,
                        search_property="armatures", text="Character Target Armature")

        box = layout.box()
        box.prop_search(data=bpy.context.window_manager, property="mocapSourceArmature", search_data=bpy.data,
                        search_property="armatures", text="Mocap Source Armature")

        row = layout.row()
        row.prop(bpy.context.window_manager, "frame_start")
        row.prop(bpy.context.window_manager, "frame_end")

        col = layout.column()
        col.operator("object.retarget")


def register():
    bpy.utils.register_class(FDG_PT_Retarget_Panel_pnl)


def unregister():
    bpy.utils.unregister_class(FDG_PT_Retarget_Panel_pnl)
