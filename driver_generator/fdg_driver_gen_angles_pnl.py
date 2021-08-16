import bpy

from bpy.props import CollectionProperty
from bpy.props import PointerProperty
from bpy.props import StringProperty


class FDG_PT_GenerateDrivers_pnl(bpy.types.Panel):
    bl_label = "Driver Generator"
    bl_category = "FCHAR Driver Gen"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"DEFAULT_CLOSED"}

    bpy.types.Scene.character_prefix = StringProperty(name="Character Prefix")
    
    bpy.types.Scene.object1 = PointerProperty(
        name="Armature", type=bpy.types.Object)
    bpy.types.Scene.bone1 = StringProperty(name="Head Bone")
    bpy.types.Scene.object2 = PointerProperty(
        name="Camera", type=bpy.types.Object)
    bpy.types.Scene.bone2 = StringProperty(name="Bone")

    #bpy.types.Scene.face_collection = PointerProperty(name="Face Collection", type=bpy.types.Collection)

    def draw(self, context):
        scene = context.scene
        layout = self.layout

        #layout.prop_search(scene, "face_collection", bpy.data, "collections")
        
        # Create a Text Field to enter the current Characters prefix, so the empties can be named with them.
        layout.prop(scene, "character_prefix")

        # Create Search field for first Object (Head) and if this object is an armature create search field for its
        # bones
        box = layout.box()
        box.prop_search(scene, "object1", context.scene,
                        "objects", text='Armature')
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

        

        layout.operator("object.generate_drivers")


def register():
    bpy.utils.register_class(FDG_PT_GenerateDrivers_pnl)


def unregister():
    bpy.utils.unregister_class(FDG_PT_GenerateDrivers_pnl)