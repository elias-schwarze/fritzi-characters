import bpy

from . import fmr_retarget_pnl
from . import fmr_retarget_op
from . import fmr_scale_list_op
from . import fmr_files_ops
from . import fmr_settings_ops

from bpy.types import OperatorFileListElement
from bpy.props import BoolProperty, PointerProperty, CollectionProperty, IntProperty, StringProperty
from .fmr_retarget_pnl import ScaleList, update_source_rig, update_target_rig


def register():
    
    fmr_retarget_op.register()
    fmr_retarget_pnl.register()
    fmr_scale_list_op.register()
    fmr_files_ops.register()
    fmr_settings_ops.register()
    bpy.types.WindowManager.auto_scale_check = BoolProperty(name = "Auto Scale", default = True)
    bpy.types.WindowManager.source_rig_pointer = PointerProperty(name = "Source Armature", type = bpy.types.Object, update = update_source_rig)
    bpy.types.WindowManager.target_rig_pointer = PointerProperty(name = "Target Armature", type = bpy.types.Object, update = update_target_rig)
    bpy.types.WindowManager.scale_list = CollectionProperty(name = "Scale List", type=ScaleList)
    bpy.types.WindowManager.scale_list_index = IntProperty()
    bpy.types.WindowManager.bvh_files = CollectionProperty(name = "File Paths", type = fmr_files_ops.FileList)
    bpy.types.WindowManager.bvh_dir = StringProperty()

    
def unregister():
    fmr_settings_ops.unregister()
    fmr_files_ops.unregister()
    fmr_scale_list_op.unregister()
    fmr_retarget_pnl.unregister()
    fmr_retarget_op.unregister()

