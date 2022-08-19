import bpy

from bpy.props import BoolProperty, PointerProperty
from bpy.props import StringProperty


class FDG_PT_GenerateAngleDrivers_pnl(bpy.types.Panel):
    bl_label = "Angle Driver Generator"
    bl_category = "FCHAR"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"DEFAULT_CLOSED"}
    bl_parent_id = "FDG_PT_DriverGenerator_pnl"

    bpy.types.WindowManager.character_prefix = StringProperty(name="Character Prefix")

    bpy.types.WindowManager.character_rig = PointerProperty(
        name="Armature", type=bpy.types.Object)
    bpy.types.WindowManager.character_head_bone = StringProperty(name="Head Bone")
    bpy.types.WindowManager.camera = PointerProperty(
        name="Camera", type=bpy.types.Object)
    

    def draw(self, context):
        wm = context.window_manager
        layout = self.layout

        # Create a Text Field to enter the current Characters prefix, so the empties can be named with them.
        layout.prop(wm, "character_prefix")

        # Create Search field for first Object (Head) and if this object is an armature create search field for its
        # bones
        box = layout.box()
        box.prop_search(wm, "character_rig", context.scene,
                        "objects", text="Armature")
        ob = wm.character_rig
        if ob is not None:
            if ob.type == 'ARMATURE':
                box.prop_search(wm, "character_head_bone", ob.data, "bones")

        # Create Search field for second Object (Camera)
        box = layout.box()
        box.prop_search(wm, "camera", context.scene,
                        "objects", text="Camera")
        ob = wm.camera

        row = layout.row()
        row.operator("object.generate_drivers")
        row.operator("object.remove_drivers")


def register():
    bpy.utils.register_class(FDG_PT_GenerateAngleDrivers_pnl)


def unregister():
    bpy.utils.unregister_class(FDG_PT_GenerateAngleDrivers_pnl)
