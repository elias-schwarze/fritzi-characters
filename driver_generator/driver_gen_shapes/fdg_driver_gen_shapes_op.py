import bpy

from bpy.types import Operator

from ..utility_functions.fdg_driver_utils import add_var

class FDG_OT_GenerateShapeDrivers_Op(Operator):
    bl_idname = "object.generate_shape_drivers"
    bl_label = "Add Drivers to Shapes"
    bl_description = "Adds drivers to all shapekeys with either suffix .L or .R on objects in the given collection"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):

        collection = context.scene.face_collection

        arma = context.scene.object1

        if arma is None:
            self.report({'WARNING'}, "Please select the Armature!")

        if collection is None:
            self.report({'WARNING'}, "Please select the Collection!")

        self.search_collection(collection, arma)
        
        self.report({'INFO'}, "Created Shape Drivers!")
        return {'FINISHED'}

    def search_collection(self, collection, armature):
        for child in collection.children:
            self.search_collection(child, armature)
        
        for obj in collection.objects:
            if obj.type == 'MESH':
                for key in obj.data.shape_keys.key_blocks:
                    print(key.name)
                    
                    if key.name.endswith(".L"):
                        
                        driver = key.driver_add("value").driver

                        add_var(driver, armature, "shapesLeft", type='SINGLE_PROP', rna_data_path='pose.bones["Driven_Props"]["shapesLeft"]')

                        driver.expression = "shapesLeft"

                    if key.name.endswith(".R"):

                        driver = key.driver_add("value").driver

                        add_var(driver, armature, "shapesRight", type='SINGLE_PROP', rna_data_path='pose.bones["Driven_Props"]["shapesRight"]')

                        driver.expression = "shapesRight"

                        

def register():
    bpy.utils.register_class(FDG_OT_GenerateShapeDrivers_Op)

def unregister():
    bpy.utils.unregister_class(FDG_OT_GenerateShapeDrivers_Op)