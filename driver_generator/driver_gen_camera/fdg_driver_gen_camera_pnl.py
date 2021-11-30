import bpy


class FDG_PT_CameraUtilities_pnl(bpy.types.Panel):
    bl_label = "Manage Camera"
    bl_category = "FCHAR"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        scene = context.scene
        layout = self.layout

        box = layout.box()

        box.prop_search(scene, "object2", context.scene,
                        "objects", text="Camera")

        box.operator("object.link_camera")

        layout.separator(factor=1.5)

        box = layout.box()

        box.label(text="Auto link active camera:")

        row = box.row()

        if bpy.context.scene.auto_link_toggle:
            row.operator("object.activate_auto_link_camera", depress=True)
            row.operator("object.deactivate_auto_link_camera", depress=False)

        else:
            row.operator("object.activate_auto_link_camera", depress=False)
            row.operator("object.deactivate_auto_link_camera", depress=True)


def register():
    bpy.utils.register_class(FDG_PT_CameraUtilities_pnl)


def unregister():
    bpy.utils.unregister_class(FDG_PT_CameraUtilities_pnl)
