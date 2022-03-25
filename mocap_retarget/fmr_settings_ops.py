from ast import Return
import bpy
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper
from .fmr_settings import Settings
import os
import time


class FMR_OT_ChoosePerforcePath_OP(Operator, ImportHelper):
    bl_idname = "settings.choose_perforce_path"
    bl_label = "Select Perforce DIR"
    bl_description = "Select the Main Directory of the Fritzi Perforce on your Computer"

    def execute(self, context):
        settings = Settings()
        settings.set_setting("perforce_path", self.filepath)
        if not (os.path.isdir(self.filepath) and os.path.isdir(os.path.join(self.filepath, "080_scenes")) and os.path.isdir(os.path.join(self.filepath, "075_capture"))):
            self.report({'WARNING'}, "NO VALID PERFORCE DIRECTORY FOUND!")
            bpy.ops.settings.choose_perforce_path('INVOKE_DEFAULT')
        else:
            self.report({'INFO'}, "Perforce Directory set!")
            

        return {'FINISHED'}

class FMR_OT_Test_OP(Operator):
    bl_idname = "settings.test"
    bl_label = "Test Choosing"

    def execute(self,context):
        settings = Settings()
        filepath = settings.get_setting("perforce_path")

        if not (os.path.isdir(filepath) and os.path.isdir(os.path.join(filepath, "080_scenes")) and os.path.isdir(os.path.join(filepath, "075_capture"))):
            
            
            bpy.ops.settings.choose_perforce_path('INVOKE_DEFAULT')
            self.report({'WARNING'}, "Set Perforce Path first!")
            return {'FINISHED'}
        else:
            #Select BVHS and then create filestructure and retarget

            #check if bvhs are already loaded otherwise exec selection and at the end of loading exec this operator again
            bpy.ops.retarget.select_bvhs('INVOKE_DEFAULT')
            #after each retargeted bvh delete it from the bvh list (Maybe show bvh list in UI)
            #
        

        
        return {'FINISHED'}


def register():
    bpy.utils.register_class(FMR_OT_ChoosePerforcePath_OP)
    bpy.utils.register_class(FMR_OT_Test_OP)

def unregister():
    bpy.utils.unregister_class(FMR_OT_Test_OP)
    bpy.utils.unregister_class(FMR_OT_ChoosePerforcePath_OP)
