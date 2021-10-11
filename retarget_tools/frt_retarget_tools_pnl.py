import bpy

from bpy.types import EnumPropertyItem, Panel
from bpy.props import PointerProperty, IntProperty

class FDG_PT_Retarget_Panel_pnl(Panel):
    bl_label = "Retarget Tools"
    bl_category = "Retarget"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"DEFAULT_CLOSED"}

    bpy.types.Scene.object7 = PointerProperty(
    name="Armature", type=bpy.types.Object)

    bpy.types.Scene.object8 = PointerProperty(
    name="Mocap Armature", type=bpy.types.Object)

    bpy.types.Scene.num1 = IntProperty(name='Frame Start', default=0, min= 0, step=1)
    bpy.types.Scene.num2 = IntProperty(name='Frame End', default=500, min= 0, step=1)

    def draw(self, context):
       scene = context.scene
       layout = self.layout

       col = layout.column()
       col.operator("object.retarget")

       box = layout.box()
       box.prop_search(scene, "object7", context.scene, 
       "objects", text="Armature")

       box = layout.box()
       box.prop_search(scene, "object8", context.scene, 
       "objects", text="Mocap Armature")

       row = layout.row()
       row.prop(scene, "num1")
       row.prop(scene, "num2")


def register():
    bpy.utils.register_class(FDG_PT_Retarget_Panel_pnl)

def unregister():
    bpy.utils.unregister_class(FDG_PT_Retarget_Panel_pnl)

