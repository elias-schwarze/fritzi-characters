# This script defines functions to be used directly in driver expressions to
# extend the built-in set of python functions.
#
# This can be executed on manually or set to 'Register' to
# initialize the functions on file load.

import bpy
import mathutils
import math
from bpy.app.handlers import persistent
from ..utility_functions.fdg_driver_utils import append_function_unique


# this function returns the vector between two points. The direction is from point1 to point2
def vector_head_cam(head_loc_x, head_loc_y, head_loc_z, cam_loc_x, cam_loc_y, cam_loc_z):
    vec_head_cam = mathutils.Vector(
        (cam_loc_x - head_loc_x, cam_loc_y - head_loc_y, cam_loc_z - head_loc_z))

    return vec_head_cam


# this function translates the vector from head to camera from world-space into the local space of the head-bone.
def to_local_head(vec_head_cam, head_rot_x, head_rot_y, head_rot_z):
    rot = mathutils.Euler((-head_rot_x, -head_rot_y, -head_rot_z))

    vec_head_cam.rotate(rot)

    return vec_head_cam


# this function calculates the angle between the head bone and the camera around the local z axis of the head. (It returns a Positive angle if the camera is right of the head, negative angle if the camera is left of the head)
def angle_z(head_loc_x, head_loc_y, head_loc_z, cam_loc_x, cam_loc_y, cam_loc_z, head_rot_x, head_rot_y, head_rot_z):
    head_forward = mathutils.Vector((0, -1))

    vec_head_cam = vector_head_cam(
        head_loc_x, head_loc_y, head_loc_z, cam_loc_x, cam_loc_y, cam_loc_z)
    vec_head_cam = to_local_head(
        vec_head_cam, head_rot_x, head_rot_y, head_rot_z)

    vec_head_cam_xy = mathutils.Vector((vec_head_cam.x, vec_head_cam.y))

    vec_head_cam_xy = vec_head_cam_xy.normalized()

    dot_product = vec_head_cam_xy.dot(head_forward)

    angle = math.acos(dot_product)

    if (vec_head_cam.x < 0):
        angle = angle * -1

    return angle


# this function calculates the angle between the head bone and the camera around the local x axis of the head. (It returns a Positive angle if the camera is above the head, negative angle if the camera is below of the head)
def angle_x(head_loc_x, head_loc_y, head_loc_z, cam_loc_x, cam_loc_y, cam_loc_z, head_rot_x, head_rot_y, head_rot_z):
    head_forward = mathutils.Vector((1, 0))

    vec_head_cam = vector_head_cam(
        head_loc_x, head_loc_y, head_loc_z, cam_loc_x, cam_loc_y, cam_loc_z)
    vec_head_cam = to_local_head(
        vec_head_cam, head_rot_x, head_rot_y, head_rot_z)

    length_xy = math.sqrt(pow(vec_head_cam.x, 2) + pow(vec_head_cam.y, 2))

    angle = math.atan(vec_head_cam.z / length_xy)

    return angle


@persistent
def load_handler(dummy):
    bpy.app.driver_namespace["angle_x_func"] = angle_x
    bpy.app.driver_namespace["angle_z_func"] = angle_z


# Add functions defined in this script into the drivers namespace.
def register():
    append_function_unique(bpy.app.handlers.load_post, load_handler)
    bpy.app.driver_namespace["angle_x_func"] = angle_x
    bpy.app.driver_namespace["angle_z_func"] = angle_z


def unregister():
    # remove_function(bpy.app.handlers.load_post, load_handler)
    bpy.app.driver_namespace["angle_x_func"] = None
    bpy.app.driver_namespace["angle_z_func"] = None
