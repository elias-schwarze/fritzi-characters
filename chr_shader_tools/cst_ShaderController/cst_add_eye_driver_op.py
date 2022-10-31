import bpy
from bpy.types import Operator
from ...driver_generator.utility_functions.fdg_driver_utils import add_var, remove_driver_variables

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

        return True

    def execute(self, context):

        wm = context.window_manager

        rig = wm.character_rig
        eye_l = wm.eye_left
        eye_r = wm.eye_right

        self.add_properties(eye_l, True)
        self.add_properties(eye_r, False)

        self.add_drivers(eye_l, True, wm)
        self.add_drivers(eye_r, False, wm)

        return {'FINISHED'}


    def add_properties(self, eye, is_left_eye: bool):
        suffix = ".R"
        if is_left_eye:
            suffix = ".L"

        eye["position_scale" + suffix] = (0.5, 0.5, 1.0, 1.0)
        
        eye["rotation" + suffix] = (0.0)

    def add_drivers(self, eye, is_left_eye: bool, wm):
        
        suffix = ".R"
        if is_left_eye:
            
            suffix = ".L"

        # Location X

        driver = eye.driver_add('["position_scale' + suffix + '"]', 0).driver
        remove_driver_variables(driver)
        add_var(driver, source=wm.character_rig, name="target", transform_type='LOC_X', transform_space='LOCAL_SPACE', source_bone="ctl_eye" + suffix)
        
        driver.expression = "target*(50) + 0.5"


        # Location Y
        driver = eye.driver_add('["position_scale' + suffix + '"]', 1).driver
        remove_driver_variables(driver)
        add_var(driver, source=wm.character_rig, name="target", transform_type='LOC_Z', transform_space='LOCAL_SPACE', source_bone="ctl_eye" + suffix)
        add_var(driver, source=wm.character_rig, name="up", transform_type='LOC_Z', transform_space='LOCAL_SPACE', source_bone="eye_up" + suffix)
        add_var(driver, source=wm.character_rig, name="down", transform_type='LOC_Z', transform_space='LOCAL_SPACE', source_bone="eye_down" + suffix)

        driver.expression = "(0.5 + (-50)*target) + (12.1*up) + (2.99*down)"

        # Scale X

        driver = eye.driver_add('["position_scale' + suffix + '"]', 2).driver
        remove_driver_variables(driver)
        add_var(driver, source=wm.character_rig, name="target", transform_type='SCALE_X', transform_space='LOCAL_SPACE', source_bone="eye_track" + suffix)

        driver.expression = "target"

        # Scale Y

        driver = eye.driver_add('["position_scale' + suffix + '"]', 3).driver
        remove_driver_variables(driver)
        add_var(driver, source=wm.character_rig, name="target", transform_type='SCALE_Z', transform_space='LOCAL_SPACE', source_bone="eye_track" + suffix)
        add_var(driver, source=wm.character_rig, name="up", transform_type='LOC_Z', transform_space='LOCAL_SPACE', source_bone="eye_up" + suffix)
        add_var(driver, source=wm.character_rig, name="down", transform_type='LOC_Z', transform_space='LOCAL_SPACE', source_bone="eye_down" + suffix)

        driver.expression = "target * (1 + 40.59*up) * (1 - 13.73*down)"

        # Rotation Z

        driver = eye.driver_add('["rotation' + suffix + '"]').driver
        remove_driver_variables(driver)
        add_var(driver, source=wm.character_rig, name="target", transform_type='ROT_Y', transform_space='LOCAL_SPACE', source_bone="eye_track" + suffix)

        driver.expression = "target"


def register():
    bpy.utils.register_class(CST_OT_addEyeDrivers_OP)

def unregister():
    bpy.utils.unregister_class(CST_OT_addEyeDrivers_OP)