import bpy

from bpy.types import Armature, Panel
from bpy.props import PointerProperty, IntProperty


class FDG_PT_Retarget_Panel_pnl(Panel):
    bl_label = "Retarget Tools"
    bl_category = "FCHAR"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"DEFAULT_CLOSED"}

    bpy.types.Scene.object7 = PointerProperty(
        name="Armature", type=Armature)

    bpy.types.Scene.object8 = PointerProperty(
        name="Mocap Armature", type=Armature)

    #bpy.types.Scene.num7 = IntProperty(name='Frame Start', default= 0, min= 0, step=1)
    #bpy.types.Scene.num8 = IntProperty(name='Frame End', default= 500, min= 0, step=1)

    def draw(self, context):
        scene = context.scene
        layout = self.layout

        box = layout.box()
        box.prop_search(scene, "object7", context.scene,
                        "objects", text="Character Armature")

        box = layout.box()
        box.prop_search(scene, "object8", context.scene,
                        "objects", text="Mocap Armature")

        #row = layout.row()
        #row.prop(scene, "num7")
        #row.prop(scene, "num8")

        col = layout.column()
        col.operator("object.retarget")


def register():
    bpy.utils.register_class(FDG_PT_Retarget_Panel_pnl)


def unregister():
    bpy.utils.unregister_class(FDG_PT_Retarget_Panel_pnl)
