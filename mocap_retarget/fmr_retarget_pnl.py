import bpy
from bpy.props import PointerProperty, BoolProperty, FloatProperty, CollectionProperty, IntProperty
from bpy.types import PropertyGroup, UIList
from . import fmr_settings


class FMR_PT_Retarget_pnl(bpy.types.Panel):
    bl_label = "MoCap Retarget"
    bl_category = "FCHAR"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"DEFAULT_CLOSED"}

    
    

    def draw(self, context):
        
        settings = fmr_settings.Settings()

        


        scene = context.scene
        wm = context.window_manager
        layout = self.layout

        #if settings.get_setting("perforce_path") is "":
        #    layout.label(text="No Path")


        layout.prop_search(wm, "source_rig_pointer", scene, "objects", text="Source Armature")
        layout.prop_search(wm, "target_rig_pointer", scene, "objects", text="Target Armature")
        layout.prop(wm, "auto_scale_check")
        #layout.prop_search(scene, "source_rig", scene, "objects", text="Test: Source Rig ARP")
        #layout.prop_search(scene, "target_rig", scene, "objects", text="Test: Target Rig ARP")

        layout.operator("object.mocap_retarget")

        #layout.

class FMR_PT_ScaleList_pnl(bpy.types.Panel):
    bl_label = "Scale List"
    bl_category = "FCHAR"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_parent_id = "FMR_PT_Retarget_pnl"

    def draw(self, context):
        wm = context.window_manager
        layout = self.layout

        layout.template_list("FMR_UL_items", "", wm, "scale_list", wm, "scale_list_index", rows=2)
        row = layout.row()
        row.operator("file.import_scale_list")
#        split = layout.split(factor=0.5)
        row.operator("file.export_scale_list")

def ScaleUpdate(self, context):
    print("update")

class ScaleList(PropertyGroup):
    scale : FloatProperty(default=1, update=ScaleUpdate)

class FMR_UL_items(UIList):
    @classmethod
    def poll(cls, context):
        return True

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        split = layout.split(factor=1.0)
        split.prop(item, "name", text="", emboss=False, translate=False)
        split = layout.split(factor=1.0)
        split.prop(item, "scale", text="", emboss=False, translate=False)

    def invoke(self, context, event):
        pass



def NameUpdate(self, context):
    print("update")

def test_method(self, context):
        print("update")

def update_source_rig(self, context):
    wm = context.window_manager
    scene = context.scene
    print("update")
    if (wm.source_rig_pointer):
        print("setRig")
        scene.source_rig = wm.source_rig_pointer.name
    else:
        scene.source_rig = ""

def update_target_rig(self, context):
    wm = context.window_manager
    scene = context.scene

    if(wm.target_rig_pointer):
        scene.target_rig = wm.target_rig_pointer.name
    else:
        scene.target_rig = ""



def register():
    
    bpy.utils.register_class(FMR_PT_Retarget_pnl)
    bpy.utils.register_class(FMR_PT_ScaleList_pnl)
    bpy.utils.register_class(ScaleList)
    bpy.utils.register_class(FMR_UL_items)
    bpy.types.WindowManager.auto_scale_check = BoolProperty(name = "Auto Scale", default = True)
    bpy.types.WindowManager.source_rig_pointer = PointerProperty(name = "Source Armature", type = bpy.types.Object, update = update_source_rig)
    bpy.types.WindowManager.target_rig_pointer = PointerProperty(name = "Target Armature", type = bpy.types.Object, update = update_target_rig)
    bpy.types.WindowManager.scale_list = CollectionProperty(name = "Scale List", type=ScaleList)
    bpy.types.WindowManager.scale_list_index = IntProperty()

def unregister():
    bpy.utils.unregister_class(FMR_UL_items)
    bpy.utils.unregister_class(ScaleList)
    bpy.utils.unregister_class(FMR_PT_ScaleList_pnl)
    bpy.utils.unregister_class(FMR_PT_Retarget_pnl)


