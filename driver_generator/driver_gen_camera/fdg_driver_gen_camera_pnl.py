import bpy

class FDG_PT_CameraUtilities_pnl(bpy.types.Panel):
    bl_label = "Manage Camera"
    bl_category = "FCHAR Driver Gen"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        scene = context.scene
        layout = self.layout

        layout.prop_search(scene, "object2", context.scene, "objects", text="Camera")

        layout.operator("object.link_camera")    


def register():
    bpy.utils.register_class(FDG_PT_CameraUtilities_pnl)


def unregister():
    bpy.utils.unregister_class(FDG_PT_CameraUtilities_pnl)