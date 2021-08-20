import bpy

from bpy.types import Operator

from ..utility_functions.fdg_driver_utils import add_var
from..utility_functions import fdg_names


class FDG_OT_GenerateShapeDrivers_Op(Operator):
    bl_idname = "object.generate_shape_drivers"
    bl_label = "Add Drivers to Shapekeys"
    bl_description = "Adds drivers to all shapekeys with either suffix .L or .R on objects in the given collection"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):

        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

        collection = context.scene.face_collection

        arma = context.scene.object1

        if arma is None:
            self.report({'WARNING'}, "Please select the Armature!")

        if collection is None:
            self.report({'WARNING'}, "Please select the Collection!")

        self.add_shape_drivers(collection, arma)

        self.report({'INFO'}, "Created Shapekey Drivers!")
        return {'FINISHED'}

    def add_shape_drivers(self, collection, armature):
        """Adds Drivers to all shapekeys which end with .L or .R on all Meshes and Lattices in the given collection, and recursively in all child collections"""
        for child in collection.children:
            self.add_shape_drivers(child, armature)

        for obj in collection.objects:
            if obj.type == 'MESH' or obj.type == 'LATTICE':

                if obj.data.shape_keys is None:
                    continue

                for key in obj.data.shape_keys.key_blocks:
                    
                    if key.name.endswith(".L"):

                        driver = key.driver_add("value").driver
                        add_var(driver, armature, "shapesLeft", type='SINGLE_PROP',
                                rna_data_path='pose.bones["' + fdg_names.hidden_controller_bone + '"]["' + fdg_names.prop_shapes_left + '"]')
                        driver.expression = "shapesLeft"

                    if key.name.endswith(".R"):

                        driver = key.driver_add("value").driver
                        add_var(driver, armature, "shapesRight", type='SINGLE_PROP',
                                rna_data_path='pose.bones["' + fdg_names.hidden_controller_bone + '"]["' + fdg_names.prop_shapes_right + '"]')
                        driver.expression = "shapesRight"


def register():
    bpy.utils.register_class(FDG_OT_GenerateShapeDrivers_Op)


def unregister():
    bpy.utils.unregister_class(FDG_OT_GenerateShapeDrivers_Op)
