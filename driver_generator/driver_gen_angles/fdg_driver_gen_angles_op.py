import bpy
import mathutils

from bpy.types import Operator

from ..utility_functions.fdg_driver_utils import add_var
from ..utility_functions.fdg_driver_utils import parent_objects
from ..utility_functions.fdg_driver_utils import add_custom_property

from ..utility_functions import fdg_names

class FDG_OT_GenerateDrivers_Op(Operator):
    bl_idname = "object.generate_drivers"
    bl_label = "Generate Drivers"
    bl_description = "Generate all drivers necessary to then control the blendshapes for 2D fakes. Sets up a controller for the Animator as well."
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):

        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

        wm = bpy.context.window_manager

        prefix = wm.character_prefix
        arma = wm.character_rig
        head_bone_name = wm.character_head_bone
        cam = wm.camera

        if prefix == "":
            self.report({'WARNING'}, "Please enter a Character Prefix!")
            return {'CANCELLED'}

        if arma is None:
            self.report({'WARNING'}, "Please select the Armature!")
            return {'CANCELLED'}     

        if head_bone_name == "":
            self.report({'WARNING'}, "Please select the Head Bone!")
            return {'CANCELLED'}

        if cam is None:
            self.report({'WARNING'}, "Please select the Camera!")
            return {'CANCELLED'}

        if cam.type != 'CAMERA':
            self.report({'WARNING'}, "Please select a Camera!")

        # Create an Empty at the Base of the Head Bone and parent it to the Head Bone
        head_empty = bpy.data.objects.get(prefix + "." + fdg_names.empty_head)

        if head_empty is not None:
            bpy.data.objects.remove(head_empty, do_unlink=True)

        head_empty = bpy.data.objects.new(prefix + "." + fdg_names.empty_head, None)

        if arma.type == 'ARMATURE' and head_bone_name != '':
            head_empty.location = arma.location + \
                arma.data.bones[head_bone_name].head
        else:
            head_empty.location = arma.location

        bpy.context.collection.objects.link(head_empty)

        parent_objects(arma, head_empty, head_bone_name)

        head_empty.hide_viewport = True

        # Create an Empty at the Camera and parent it to the Camera
        cam_empty = bpy.context.scene.objects.get(fdg_names.empty_cam)
        if cam_empty is None:
            cam_empty = bpy.data.objects.new(fdg_names.empty_cam, None)

            
            cam_empty.location = cam.location
            cam_empty.rotation_euler = cam.rotation_euler

            bpy.context.collection.objects.link(cam_empty)

            parent_objects(cam, cam_empty)

        cam_empty.hide_viewport = True

        # Create two Bones as controllers for the Drivers, one hidden for driven Properties and one not hidden with animatable properties for the animator

        hidden_controller_bone_name = fdg_names.hidden_controller_bone
        visible_controller_bone_name = fdg_names.visible_controller_bone

        # bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = arma
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)

        edit_bones = arma.data.edit_bones
        b = edit_bones.get(hidden_controller_bone_name)
        if b is not None:
            edit_bones.remove(b)

        b = edit_bones.new(hidden_controller_bone_name)

        b.head = head_empty.location + mathutils.Vector((1.0, 0.0, 0.0))
        b.tail = head_empty.location + mathutils.Vector((1.0, -1.0, 0.0))

        b = edit_bones.get(visible_controller_bone_name)
        if b is not None:
            edit_bones.remove(b)

        b = edit_bones.new(visible_controller_bone_name)

        b.head = head_empty.location + mathutils.Vector((2.0, 0.0, 0.0))
        b.tail = head_empty.location + mathutils.Vector((2.0, -1.0, 0.0))

        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

        # Add custom properties to the control bones

        hidden_controller_pose_bone = arma.pose.bones[hidden_controller_bone_name]
        visible_controller_pose_bone = arma.pose.bones[visible_controller_bone_name]

        arma.data.bones[hidden_controller_bone_name].layers[29] = True
        arma.data.bones[hidden_controller_bone_name].layers[0] = False
        
        arma.data.bones[visible_controller_bone_name].layers[30] = True
        arma.data.bones[visible_controller_bone_name].layers[0] = False


        arma.data.layers[30] = True
        arma.data.layers[29] = False
        

        # Hidden Controller

        add_custom_property(hidden_controller_pose_bone, fdg_names.prop_angle_x, prop_min=-180.0,
                            prop_max=180.0, description="Angle between head and Camera around x axis")

        add_custom_property(hidden_controller_pose_bone, fdg_names.prop_angle_z, prop_min=-180.0,
                            prop_max=180.0, description="Angle between head and Camera around x axis")

        add_custom_property(hidden_controller_pose_bone,
                            fdg_names.prop_up_down_normalize, prop_min=-180.0, prop_max=180.0)

        add_custom_property(hidden_controller_pose_bone,
                            fdg_names.prop_shapes_left, prop_min=0.0, prop_max=1.0)

        add_custom_property(hidden_controller_pose_bone,
                            fdg_names.prop_shapes_right, prop_min=0.0, prop_max=1.0)

        # Visible Controller

        add_custom_property(visible_controller_pose_bone,
                            fdg_names.prop_bias, prop_min=-150.0, prop_max=150.0)

        add_custom_property(visible_controller_pose_bone,
                            fdg_names.prop_blend, default=10.0, prop_min=1.0, prop_max=89.0)

        add_custom_property(visible_controller_pose_bone,
                            fdg_names.prop_blendUpDown, default=10.0, prop_min=1.0, prop_max=10.0)

        add_custom_property(visible_controller_pose_bone,
                            fdg_names.prop_driverSwitch, default=1.0, prop_min=0.0, prop_max=1.0)

        # Add drivers to the hidden control bone

        driver_x = hidden_controller_pose_bone.driver_add(
            '["' + fdg_names.prop_angle_x + '"]').driver
        driver_z = hidden_controller_pose_bone.driver_add(
            '["' + fdg_names.prop_angle_z + '"]').driver
        driver_normalize = hidden_controller_pose_bone.driver_add(
            '["' + fdg_names.prop_up_down_normalize + '"]').driver
        driver_shapes_left = hidden_controller_pose_bone.driver_add(
            '["' + fdg_names.prop_shapes_left + '"]').driver
        driver_shapes_right = hidden_controller_pose_bone.driver_add(
            '["' + fdg_names.prop_shapes_right + '"]').driver

        # Add variables to driver around the x axis
        add_var(driver_x, head_empty, "head_loc_x", transform_type='LOC_X')
        add_var(driver_x, head_empty, "head_loc_y", transform_type='LOC_Y')
        add_var(driver_x, head_empty, "head_loc_z", transform_type='LOC_Z')

        add_var(driver_x, head_empty, "head_rot_x", transform_type='ROT_X')
        add_var(driver_x, head_empty, "head_rot_y", transform_type='ROT_Y')
        add_var(driver_x, head_empty, "head_rot_z", transform_type='ROT_Z')

        add_var(driver_x, cam_empty, "cam_loc_x", transform_type='LOC_X')
        add_var(driver_x, cam_empty, "cam_loc_y", transform_type='LOC_Y')
        add_var(driver_x, cam_empty, "cam_loc_z", transform_type='LOC_Z')

        # Add variables to driver around the z axis
        add_var(driver_z, head_empty, "head_loc_x", transform_type='LOC_X')
        add_var(driver_z, head_empty, "head_loc_y", transform_type='LOC_Y')
        add_var(driver_z, head_empty, "head_loc_z", transform_type='LOC_Z')

        add_var(driver_z, head_empty, "head_rot_x", transform_type='ROT_X')
        add_var(driver_z, head_empty, "head_rot_y", transform_type='ROT_Y')
        add_var(driver_z, head_empty, "head_rot_z", transform_type='ROT_Z')

        add_var(driver_z, cam_empty, "cam_loc_x", transform_type='LOC_X')
        add_var(driver_z, cam_empty, "cam_loc_y", transform_type='LOC_Y')
        add_var(driver_z, cam_empty, "cam_loc_z", transform_type='LOC_Z')

        # add variables to normalize driver
        add_var(driver_normalize, arma, "angle_x", type='SINGLE_PROP',
                rna_data_path='pose.bones["' + fdg_names.hidden_controller_bone + '"]["' + fdg_names.prop_angle_x + '"]')
        add_var(driver_normalize, arma, "angle_z", type='SINGLE_PROP',
                rna_data_path='pose.bones["' + fdg_names.hidden_controller_bone + '"]["' + fdg_names.prop_angle_z + '"]')
        add_var(driver_normalize, arma, "bias", type='SINGLE_PROP',
                rna_data_path='pose.bones["' + fdg_names.visible_controller_bone + '"]["' + fdg_names.prop_bias + '"]')

        # add variables to the shapes drivers
        # LEFT
        add_var(driver_shapes_left, arma, "angle_z", type='SINGLE_PROP',
                rna_data_path='pose.bones["' + fdg_names.hidden_controller_bone + '"]["' + fdg_names.prop_angle_z + '"]')
        add_var(driver_shapes_left, arma, "bias", type='SINGLE_PROP',
                rna_data_path='pose.bones["' + fdg_names.visible_controller_bone + '"]["' + fdg_names.prop_bias + '"]')
        add_var(driver_shapes_left, arma, "blend", type='SINGLE_PROP',
                rna_data_path='pose.bones["' + fdg_names.visible_controller_bone + '"]["' + fdg_names.prop_blend + '"]')
        add_var(driver_shapes_left, arma, "blendUpDown", type='SINGLE_PROP',
                rna_data_path='pose.bones["' + fdg_names.visible_controller_bone + '"]["' + fdg_names.prop_blendUpDown + '"]')
        add_var(driver_shapes_left, arma, "upDownNormalize", type='SINGLE_PROP',
                rna_data_path='pose.bones["' + fdg_names.hidden_controller_bone + '"]["' + fdg_names.prop_up_down_normalize + '"]')
        add_var(driver_shapes_left, arma, "driverSwitch", type='SINGLE_PROP',
                rna_data_path='pose.bones["' + fdg_names.visible_controller_bone + '"]["' + fdg_names.prop_driverSwitch + '"]')

        # RIGHT
        add_var(driver_shapes_right, arma, "angle_z", type='SINGLE_PROP',
                rna_data_path='pose.bones["' + fdg_names.hidden_controller_bone + '"]["' + fdg_names.prop_angle_z + '"]')
        add_var(driver_shapes_right, arma, "bias", type='SINGLE_PROP',
                rna_data_path='pose.bones["' + fdg_names.visible_controller_bone + '"]["' + fdg_names.prop_bias + '"]')
        add_var(driver_shapes_right, arma, "blend", type='SINGLE_PROP',
                rna_data_path='pose.bones["' + fdg_names.visible_controller_bone + '"]["' + fdg_names.prop_blend + '"]')
        add_var(driver_shapes_right, arma, "blendUpDown", type='SINGLE_PROP',
                rna_data_path='pose.bones["' + fdg_names.visible_controller_bone + '"]["' + fdg_names.prop_blendUpDown + '"]')
        add_var(driver_shapes_right, arma, "upDownNormalize", type='SINGLE_PROP',
                rna_data_path='pose.bones["' + fdg_names.hidden_controller_bone + '"]["' + fdg_names.prop_up_down_normalize + '"]')
        add_var(driver_shapes_right, arma, "driverSwitch", type='SINGLE_PROP',
                rna_data_path='pose.bones["' + fdg_names.visible_controller_bone + '"]["' + fdg_names.prop_driverSwitch + '"]')

        # Add the expressions to the drivers
        driver_x.expression = "degrees(angle_x_func(head_loc_x, head_loc_y, head_loc_z, cam_loc_x, cam_loc_y, cam_loc_z, head_rot_x, head_rot_y, head_rot_z)) "
        driver_z.expression = "degrees(angle_z_func(head_loc_x, head_loc_y, head_loc_z, cam_loc_x, cam_loc_y, cam_loc_z, head_rot_x, head_rot_y, head_rot_z)) "
        driver_normalize.expression = "2*-angle_x if angle_z>0+bias and angle_x>0 else 2*angle_x if angle_z<0+bias and angle_x >0 else 2*angle_x if angle_z>0+bias and angle_x <0 else 2*-angle_x if angle_x<0 and angle_z<0+bias else 0"

        driver_shapes_left.expression = "(1-((-blend-(angle_z-bias))/(90-blend))-((upDownNormalize/blendUpDown)/15) if angle_z-bias <-blend else -(angle_z-bias)/blend-((upDownNormalize/blendUpDown)/15) if angle_z-bias <=0 and angle_z-bias>=-blend else 0) * driverSwitch"
        driver_shapes_right.expression = "(1+((blend-(angle_z-bias))/(90-blend))-((-upDownNormalize/blendUpDown)/15) if angle_z-bias >blend else ((angle_z-bias)/blend)-((-upDownNormalize/blendUpDown)/15) if angle_z-bias >=0 and angle_z-bias<=blend else 0) * driverSwitch"

        self.report({'INFO'}, "Generated Drivers!")
        return {'FINISHED'}


def register():
    bpy.utils.register_class(FDG_OT_GenerateDrivers_Op)


def unregister():
    bpy.utils.unregister_class(FDG_OT_GenerateDrivers_Op)
