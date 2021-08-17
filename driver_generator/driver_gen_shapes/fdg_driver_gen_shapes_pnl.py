import bpy

from bpy.props import PointerProperty

class FDG_PT_GenerateShapeDrivers_pnl(bpy.types.Panel):
    bl_label = "Add Drivers to Shapekeys"
    bl_category = "FCHAR Driver Gen"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"DEFAULT_CLOSED"}

    bpy.types.Scene.face_collection = PointerProperty(name="Face Collection", type=bpy.types.Collection)

    def draw(self, context):
        scene = context.scene
        layout = self.layout

        layout.prop_search(scene, "face_collection", bpy.data, "collections")

        layout.operator("object.generate_shape_drivers")

def register():
    bpy.utils.register_class(FDG_PT_GenerateShapeDrivers_pnl)

def unregister():
    bpy.utils.unregister_class(FDG_PT_GenerateShapeDrivers_pnl)