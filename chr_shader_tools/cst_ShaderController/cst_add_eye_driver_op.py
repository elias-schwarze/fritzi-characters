import bpy
from bpy.types import Operator
from ...driver_generator.utility_functions.fdg_driver_utils import add_var

class CST_OT_addEyeDrivers_OP(Operator):
    bl_idname = "object.add_eye_drivers"
    bl_label = "Link eyes to the rig"
    bl_description = "Adds drivers from the Rig to both eyes, so that the shader can access them."
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        wm = context.window_manager

        if not wm.character_rig:
            return False

        if not wm.eye_left:
            return False
        
        if not wm.eye_right:
            return False

    def execute(self, context):

        wm = context.window_manager

        rig = wm.character_rig
        eye_l = wm.eye_left
        eye_r = wm.eye_right


    def add_properties(eye, is_left_eye: bool):
        suffix = ".r"
        if is_left_eye:
            suffix = ".l"

        eye["position_scale" + suffix] = (0.5, 0.5, 1.0, 1.0)
        
        eye["rotation" + suffix] = (0.0)

    def add_drivers(eye, is_left_eye: bool, wm):
        suffix = ".r"
        if is_left_eye:
            suffix = ".l"

        driver = eye.driver_add("position_scale" + suffix, 0).driver
        add_var(driver, source=wm.character_rig, name="pos", transform_type='LOC_Y', transform_space='LOCAL_SPACE', source_bone="ctl_eye.L")
        add_var(driver, source=wm.character_rig, name="pos", transform_type='LOC_Y', transform_space='LOCAL_SPACE', source_bone="ctl_eye.L")
        add_var(driver, source=wm.character_rig, name="pos", transform_type='LOC_Y', transform_space='LOCAL_SPACE', source_bone="ctl_eye.L")


def register():
    bpy.utils.register_class(CST_OT_addEyeDrivers_OP)

def unregister():
    bpy.utils.unregister_class(CST_OT_addEyeDrivers_OP)