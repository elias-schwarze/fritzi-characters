import bpy
from bpy.types import Operator

class FDG_OT_RemoveShapeDrivers_Op(Operator):
    bl_idname = "object.remove_shape_drivers"
    bl_label = "Remove Drivers from Shapekeys"
    bl_description = "Remove all drivers from all Shapekeys ending with .L or .R on Meshes or Lattices in the given collection or child collections"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

        wm = bpy.context.window_manager

        collection = wm.face_collection

        arma = wm.character_rig

        if arma is None:
            self.report({'WARNING'}, "Please select the Armature!")

        if collection is None:
            self.report({'WARNING'}, "Please select the Collection!")

        self.remove_shape_drivers(collection, arma)

        self.report({'INFO'}, "Removed Shapekey Drivers!")
        return {'FINISHED'}

    
    def remove_shape_drivers(self, collection, armature):
        """Removes all Drivers from Shapekeys ending with .L or .R on all Meshes or Lattices in the given collection, and recursively in all child collections"""
        for child in collection.children:
            self.remove_shape_drivers(child, armature)

        for obj in collection.objects:
            if obj.type == 'MESH' or obj.type == 'LATTICE':

                if obj.data.shape_keys is None:
                    continue
                for key in obj.data.shape_keys.key_blocks:
                    
                    #print(key.name)

                    if key.name.endswith(".L") or key.name.endswith(".R"):
                        key.driver_remove("value")
        
        for area in bpy.context.screen.areas:
            area.tag_redraw()


def register():
    bpy.utils.register_class(FDG_OT_RemoveShapeDrivers_Op)


def unregister():
    bpy.utils.unregister_class(FDG_OT_RemoveShapeDrivers_Op)