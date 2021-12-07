import bpy

from bpy.props import BoolProperty, PointerProperty
from bpy.props import StringProperty


class FDG_PT_GenerateDrivers_pnl(bpy.types.Panel):
    bl_label = "Driver Generator"
    bl_category = "FCHAR"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"DEFAULT_CLOSED"}

    bpy.types.WindowManager.character_prefix = StringProperty(name="Character Prefix")

    bpy.types.WindowManager.object1 = PointerProperty(
        name="Armature", type=bpy.types.Object)
    bpy.types.WindowManager.bone1 = StringProperty(name="Head Bone")
    bpy.types.WindowManager.object2 = PointerProperty(
        name="Camera", type=bpy.types.Object)
    

    def draw(self, context):
        wm = context.window_manager
        layout = self.layout

        # Create a Text Field to enter the current Characters prefix, so the empties can be named with them.
        layout.prop(wm, "character_prefix")

        # Create Search field for first Object (Head) and if this object is an armature create search field for its
        # bones
        box = layout.box()
        box.prop_search(wm, "object1", context.scene,
                        "objects", text="Armature")
        ob = wm.object1
        if ob is not None:
            if ob.type == 'ARMATURE':
                box.prop_search(wm, "bone1", ob.data, "bones")

        # Create Search field for second Object (Camera)
        box = layout.box()
        box.prop_search(wm, "object2", context.scene,
                        "objects", text="Camera")
        ob = wm.object2

        row = layout.row()
        row.operator("object.generate_drivers")
        row.operator("object.remove_drivers")


def register():
    bpy.utils.register_class(FDG_PT_GenerateDrivers_pnl)


def unregister():
    bpy.utils.unregister_class(FDG_PT_GenerateDrivers_pnl)
