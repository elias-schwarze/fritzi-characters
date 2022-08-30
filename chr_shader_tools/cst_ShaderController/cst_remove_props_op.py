import bpy

from bpy.types import Operator

from ...driver_generator.utility_functions.fdg_driver_utils import remove_property

class CST_OT_removeProps_OP(Operator):
    bl_idname = "object.remove_props"
    bl_label = "Remove Properties"
    bl_description = "Removes Drivers and Properties from all Objects in the given collection including old obsolete ones."
    bl_options = {"REGISTER", "UNDO"}

    propNames = ["highlight_col", "rimlight_col", "AdvMixLightCol", "AdvMixShadowTint", "mix_values",
     "highlight_rimlight_mix_values", "AdvMixFactor", "advMixLightAmount", "AdvMixShadowTint", "highlight_amount",
     "rimlight_amount", "vector_diffuse_mix", "highlight", "rimlight", "adv_mix_light", "adv_mix_shadow", "main_tint", "light_rotation", "shadow_tint"]

    # should only work in object mode
    @classmethod
    def poll(cls, context):
        obj = bpy.context.object

        if obj:
            if obj.mode == "OBJECT":
                return True

        return False

    def execute(self, context):

        wm = bpy.context.window_manager

        characterCollection = wm.character_collection

        if characterCollection is None:
            self.report({'WARNING'}, "Please select a collection with the Character!")
            return {'CANCELLED'}

        self.remove_props_recursive(characterCollection)

        for area in bpy.context.screen.areas:
            area.tag_redraw()

        return {'FINISHED'}


    def remove_props_recursive(self, collection):
        for child in collection.children:
            self.remove_props_recursive(child)

        for object in collection.objects:
            if object.type =='MESH':
                for name in self.propNames:
                    object.driver_remove('["' + name + '"]', 0)
                    object.driver_remove('["' + name + '"]', 1)
                    object.driver_remove('["' + name + '"]', 2)
                    object.driver_remove('["' + name + '"]', 3)
                    remove_property(object, name)

def register():
    bpy.utils.register_class(CST_OT_removeProps_OP)

def unregister():
    bpy.utils.unregister_class(CST_OT_removeProps_OP)