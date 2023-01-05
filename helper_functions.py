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
            print(obj.name)
            for FCurve in obj.animation_data.drivers:
                driver = FCurve.driver
                driver.expression += " "
                driver.expression = driver.expression[:-1]