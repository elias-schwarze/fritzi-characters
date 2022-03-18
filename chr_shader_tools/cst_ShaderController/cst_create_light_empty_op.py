from math import degrees
import bpy

from bpy.types import Operator

class CST_OT_CreateLightEmpty_OP(Operator):
    bl_idname = "object.create_light_empty"
    bl_label = "Create Light Empty"
    bl_description = "Creates an empty which can be rotated to set the direction of the light on a character"
    bl_options = {"REGISTER", "UNDO"}

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

        characterName = wm.character_name

        if characterName is None or characterName is "":
            self.report({'WARNING'}, "Please give a Character Name!")
            return {'CANCELLED'}

        lightEmpty = bpy.data.objects.new(characterName + "_lgt_empty", None)

        lightEmpty.empty_display_size = 1
        lightEmpty.empty_display_type = 'SINGLE_ARROW'



        lightEmpty.rotation_euler = (0.0, -2.3, -1.3)
        lightEmpty.location = (0.0, 0.0, 2.0)

        bpy.context.scene.collection.objects.link(lightEmpty)

        wm.light_empty = lightEmpty

        self.report({'INFO'}, "Added Light Empty!")
        return {'FINISHED'}


def register():
    bpy.utils.register_class(CST_OT_CreateLightEmpty_OP)

def unregister():
    bpy.utils.unregister_class(CST_OT_CreateLightEmpty_OP)