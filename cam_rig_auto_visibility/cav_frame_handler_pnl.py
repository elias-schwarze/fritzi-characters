import bpy

from bpy.props import BoolProperty, PointerProperty

class CAV_PT_CamVisibility_pnl(bpy.types.Panel):
    bl_label = "Auto Cam Visibility"
    bl_category = "FCHAR"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"DEFAULT_CLOSED"}

    bpy.types.Scene.auto_visibility_toggle = BoolProperty(default=False)
    bpy.types.Scene.cameras_collection = PointerProperty(name="Cam Collection", type=bpy.types.Collection)
    bpy.types.WindowManager.last_active_camera = PointerProperty(name="Camera", type=bpy.types.Object)
    def draw(self, context):
        wm = context.window_manager
        layout = self.layout

        box = layout.box()
        box.label(text="Auto Toggle Camera Rig Visibility:")
        row = box.row()

        if bpy.context.scene.auto_visibility_toggle:
            row.operator("object.activate_auto_toggle_cam_visibility", depress=True)
            row.operator("object.deactivate_auto_toggle_cam_visibility", depress=False)

        else:
            row.operator("object.activate_auto_toggle_cam_visibility", depress=False)            
            row.operator("object.deactivate_auto_toggle_cam_visibility", depress=True)

        box.prop_search(context.scene, "cameras_collection", bpy.data, "collections", text="Cam Collection")


def register():
    bpy.utils.register_class(CAV_PT_CamVisibility_pnl)
def unregister():
    bpy.utils.unregister_class(CAV_PT_CamVisibility_pnl)