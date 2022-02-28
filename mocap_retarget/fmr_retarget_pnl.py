import bpy
from bpy.props import StringProperty, PointerProperty


class FMR_PT_Retarget_pnl(bpy.types.Panel):
    bl_label = "MoCap Retarget"
    bl_category = "FCHAR"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"DEFAULT_CLOSED"}

    
    

    def draw(self, context):



        scene = context.scene
        wm = context.window_manager
        layout = self.layout
        layout.prop_search(wm, "source_rig_pointer", scene, "objects", text="Source Armature")
        layout.prop_search(wm, "target_rig_pointer", scene, "objects", text="Target Armature")
        layout.prop_search(scene, "source_rig", scene, "objects", text="Test: Source Rig ARP")
        layout.prop_search(scene, "target_rig", scene, "objects", text="Test: Target Rig ARP")

        layout.operator("object.mocap_retarget")


    

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
    bpy.types.Scene.test_prop = StringProperty(name = "test", default="", description="", update=test_method)
    #bpy.types.Scene.source_rig = StringProperty(name = "Source Rig", default = "", description = "Source Rig Armature to take action from")
    bpy.types.WindowManager.source_rig_pointer = PointerProperty(name = "Source Armature", type = bpy.types.Object, update = update_source_rig)
    bpy.types.WindowManager.target_rig_pointer = PointerProperty(name = "Target Armature", type = bpy.types.Object, update = update_target_rig)

def unregister():
    del bpy.types.Scene.test_prop
    bpy.utils.unregister_class(FMR_PT_Retarget_pnl)


