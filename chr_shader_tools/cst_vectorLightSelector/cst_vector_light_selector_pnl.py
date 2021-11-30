import bpy
from bpy.props import PointerProperty


class CST_PT_VecorLightSelector_pnl(bpy.types.Panel):
    bl_label = "Select Light Empty"
    bl_category = "FCHAR"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"DEFAULT_CLOSED"}

    bpy.types.Scene.light_empty = PointerProperty(
        name="Light Empty", type=bpy.types.Object)
    bpy.types.Scene.character_collection = PointerProperty(
        name="Character Collection", type=bpy.types.Collection)

    def draw(self, context):
        scene = context.scene
        layout = self.layout

        layout.prop_search(scene, "light_empty", context.scene,
                           "objects", text='Light Empty')
        layout.prop_search(scene, "character_collection",
                           bpy.data, "collections", text='Character Collection')

        layout.operator("object.select_light_empty")


def register():
    bpy.utils.register_class(CST_PT_VecorLightSelector_pnl)


def unregister():
    bpy.utils.unregister_class(CST_PT_VecorLightSelector_pnl)
