import bpy

from bpy.types import Operator

class FDG_OT_GenerateShapeDrivers_Op(Operator):
    bl_idname = "object.generate_shape_drivers"
    bl_label = "Add Drivers to Shapes"
    bl_description = "Adds drivers to all shapekeys with either suffix .L or .R on objects in the given collection"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):

        collection = context.scene.face_collection

        self.search_collection(collection)
        

        return {'FINISHED'}

    def search_collection(self, collection):
        for child in collection.children:
            self.search_collection(child)
        
        for obj in collection.objects:
            if obj.type == 'MESH':
                for key in obj.data.shape_keys.key_blocks:
                    print(key.name)
        

def register():
    bpy.utils.register_class(FDG_OT_GenerateShapeDrivers_Op)

def unregister():
    bpy.utils.unregister_class(FDG_OT_GenerateShapeDrivers_Op)