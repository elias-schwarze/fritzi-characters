import bpy
from typing import Iterable, Any, Tuple


def signal_last(it:Iterable[Any]) -> Iterable[Tuple[bool, Any]]:
    iterable = iter(it)
    ret_var = next(iterable)
    for val in iterable:
        yield False, ret_var
        ret_var = val
    yield True, ret_var

def update_dependencies_all_drivers():
    for obj in bpy.data.objects:
        if obj.animation_data:
            #print(obj.name)
            for FCurve in obj.animation_data.drivers:
                driver = FCurve.driver
                driver.expression += " "
                driver.expression = driver.expression[:-1]

def remove_override(object: bpy.types.ID, property: bpy.types.IDOverrideLibraryProperty):
    """Removes the given OverrideLibraryProperty from the Override Library of the given object and sets
    it Value to the Value of the linked Reference Object (The original value of the linked Object)"""
    full_path = 'object.' + property.rna_path
    full_ref_path = 'object.override_library.reference.' + property.rna_path
    exec(full_path + ' = ' + full_ref_path)
    object.override_library.properties.remove(property)