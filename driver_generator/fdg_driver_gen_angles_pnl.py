import bpy

from bpy.props import PointerProperty
from bpy.props import StringProperty


class FDG_PT_GenerateDrivers_pnl(bpy.types.Panel):
    bl_label = "Driver Generator"
    bl_category = "FCHAR Driver Gen"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"DEFAULT_CLOSED"}

    bpy.types.Scene.character_prefix = StringProperty(name="Character Prefix")
    bpy.types.Scene.propertyObject = PointerProperty(
        name="Property Holder", type=bpy.types.Object)
    bpy.types.Scene.object1 = PointerProperty(
        name="Object 1", type=bpy.types.Object)
    bpy.types.Scene.bone1 = StringProperty(name="Bone")
    bpy.types.Scene.object2 = PointerProperty(
        name="Object 2", type=bpy.types.Object)
    bpy.types.Scene.bone2 = StringProperty(name="Bone")

    def draw(self, context):
        scene = context.scene
        layout = self.layout

        # Create a Text Field to enter the current Characters prefix, so the empties can be named with them.
        layout.prop(scene, "character_prefix")

        # Create Search field for first Object (Head) and if this object is an armature create search field for its
        # bones
        box = layout.box()
        box.prop_search(scene, "object1", context.scene,
                        "objects", text='Head')
        ob = bpy.context.scene.object1
        if ob is not None:
            if ob.type == 'ARMATURE':
                box.prop_search(scene, "bone1", ob.data, "bones")

        # Create Search field for second Object (Camera) and if this object is an armature create search field for
        # its bones
        box = layout.box()
        box.prop_search(scene, "object2", context.scene,
                        "objects", text='Camera')
        ob = bpy.context.scene.object2
        if ob is not None:
            if ob.type == 'ARMATURE':
                box.prop_search(scene, "bone2", ob.data, "bones")

        layout.label(text="Select Object to hold custom driven Properties:")
        layout.prop_search(scene, "propertyObject",
                           context.scene, "objects", text='')

        layout.operator("object.generate_drivers")


def register():
    bpy.utils.register_class(FDG_PT_GenerateDrivers_pnl)


def unregister():
    bpy.utils.unregister_class(FDG_PT_GenerateDrivers_pnl)
