import bpy
from . import fdg_names
from bpy.app.handlers import persistent

def add_var(driver, source, name, transform_type='', transform_space = 'WORLD_SPACE', type='TRANSFORMS', source_bone="", rna_data_path="", id_type=""):
    """Adds an input variable to a driver, types can be 'TRANSFORMS' or 'SINGLE_PROP'"""
    if source is not None:
        var = driver.variables.new()
        var.name = name
        var.type = type
        if type == 'SINGLE_PROP':
            target = var.targets[0]
            if id_type:
                target.id_type = id_type
            target.id = source
            target.data_path = rna_data_path
        else:
            target = var.targets[0]
            target.id = source
            if source.type == 'ARMATURE':
                target.bone_target = source_bone
            target.transform_type = transform_type
            target.transform_space = transform_space


def add_custom_property(prop_holder, name, default=0.0, prop_min=0.0, prop_max=1.0, description=''):
    """Adds a custom property to an object"""
    prop_holder[name] = default

    prop_ui = prop_holder.id_properties_ui(name)
    prop_ui.update(min= prop_min)
    prop_ui.update(max= prop_max)
    prop_ui.update(soft_min= prop_min)
    prop_ui.update(soft_max= prop_max)
    prop_ui.update(description= description)

    for area in bpy.context.screen.areas:
        area.tag_redraw()


def parent_objects(parent, child, parent_bone_name=''):
    """Parents a child object to a parent object, or to a Bone belonging to the Parent if it is an Armature"""
    bpy.ops.object.select_all(action='DESELECT')
    child.select_set(True)
    parent.select_set(True)

    if parent.type == 'ARMATURE' and parent_bone_name != '':
        bpy.context.view_layer.objects.active = parent
        bpy.ops.object.mode_set(mode='EDIT')
        parent.data.edit_bones.active = parent.data.edit_bones[parent_bone_name]
        bpy.ops.object.mode_set(mode='OBJECT')

        bpy.ops.object.select_all(action='DESELECT')
        child.select_set(True)
        parent.select_set(True)
        bpy.context.view_layer.objects.active = parent

        bpy.ops.object.parent_set(type='BONE', keep_transform=True)

    else:
        bpy.context.view_layer.objects.active = parent
        bpy.ops.object.parent_set(keep_transform=True)

    bpy.ops.object.select_all(action='DESELECT')


def append_function_unique(function_list, function):
    """Appends a unique copy of a function to a handler"""
    remove_function(function_list, function)
    function_list.append(function)


def remove_function(function_list, function):
    """Removes all copies of a function from a function handler"""
    fn_name = function.__name__
    fn_module = function.__module__

    for i in range(len(function_list) - 1, -1, -1):
        if function_list[i].__name__ == fn_name and function_list[i].__module__ == fn_module:
            del function_list[i]

def remove_driver_variables(driver):
    """Removes all Variables from a driver"""
    for var in driver.variables:
        driver.variables.remove(var)

def add_driver_float_simple(driving_object, driving_prop_name, driven_object, driven_prop_name, driven_prop_index=-1):
    """Adds a simple driver of type Average from the driving prop to the driven prop"""
    if driven_prop_index != -1:
        driver = driven_object.driver_add(driven_prop_name, driven_prop_index).driver
    else:
        driver = driven_object.driver_add(driven_prop_name).driver
    
    driver.type = 'AVERAGE'

    #Removes all variables from the driver, so there are no duplicate variables
    remove_driver_variables(driver)
    var = driver.variables.new()
    var.name = "Amount"
    var.type = 'SINGLE_PROP'
    target = var.targets[0]
    target.id = driving_object
    target.data_path = driving_prop_name

def add_driver_color_simple(driving_object, driving_prop_name, driven_object, driven_prop_name):
    """Adds simple drivers of type Average form the RGB Values of the driving prop to the RGB values of the driven prop"""

    add_driver_float_simple(driving_object, driving_prop_name + "[0]", driven_object, driven_prop_name, 0)

    add_driver_float_simple(driving_object, driving_prop_name + "[1]", driven_object, driven_prop_name, 1)

    add_driver_float_simple(driving_object, driving_prop_name + "[2]", driven_object, driven_prop_name, 2)

def remove_property(object, prop_name):
    """Tries to remove property with the given name from the given object if it exists"""

    prop_value = object.get(prop_name)
    if prop_value is not None:
        del object[prop_name]

def link_camera(camera):
    if camera is None:
        return

    cam_empties = [value for key, value in bpy.context.scene.objects.items() if fdg_names.empty_cam.lower() in key.lower()]
    
    if len(cam_empties) == 0 or len(cam_empties) > 1:
        
        for cam_empty in cam_empties:
            bpy.data.objects.remove(cam_empty, do_unlink=True)
        collection = bpy.context.scene.gp_defaults.outline_collection
        cam_empty = bpy.data.objects.new(fdg_names.empty_cam, None)
        collection.objects.link(cam_empty)

        loc, rot, scale = camera.matrix_world.decompose()
        cam_empty.location = loc
        cam_empty.rotation_euler = rot.to_euler()
        
        parent_objects(camera, cam_empty)
        cam_empty.hide_viewport = True
        cam_empty.hide_render = True
    else:
        cam_empty = cam_empties[0]
        if cam_empty.parent is camera:
            return cam_empty

        cam_empty.hide_viewport = False
        cam_empty.parent = None
        loc, rot, scale = camera.matrix_world.decompose()
        cam_empty.location = loc
        cam_empty.rotation_euler = rot.to_euler()
        

        parent_objects(camera, cam_empty)
        cam_empty.hide_viewport = True
        cam_empty.hide_render = True

    return cam_empty

current_handler_version = 1

def add_auto_link_handler():
    bpy.context.scene.auto_link_toggle = True
    bpy.context.scene.auto_link_version = current_handler_version
    append_function_unique(bpy.app.handlers.frame_change_pre, frame_change_handler_link_camera)

def remove_auto_link_handler():
    bpy.context.scene.auto_link_toggle = False
    bpy.context.scene.auto_link_version = -1
    remove_function(bpy.app.handlers.frame_change_pre, frame_change_handler_link_camera)
    
    fn_name = "frame_change_handler"
    fn_module = "Fritzi-Characters.driver_generator.driver_gen_camera.fdg_driver_gen_camera_op"
    function_list = bpy.app.handlers.frame_change_pre
    for i in range(len(function_list) - 1, -1, -1):
        if function_list[i].__name__ == fn_name and function_list[i].__module__ == fn_module:
            del function_list[i]

@persistent
def frame_change_handler_link_camera(dummy):
    """Handler which gathers the active camera and links the camera empty to it"""
    camera = bpy.context.scene.camera
    link_camera(camera)


