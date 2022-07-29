import bpy
from bpy.types import PropertyGroup
from bpy.props import PointerProperty, IntProperty, StringProperty, FloatProperty, CollectionProperty, BoolProperty

class fritziGpSetup(PropertyGroup):
    """A Property Group which stores the setup of one GP Pass"""
    GP_layer : StringProperty(name= "GP_Layer")
    view_layer : StringProperty(name="View_Layer")
    thick_modifier : StringProperty(name="Thickness Modifier")
    thick_crv_start : FloatProperty(name="Curve Start")
    thick_crv_end : FloatProperty(name="Curve End")
    thick_crv_min : FloatProperty(name="Min Thickness")
    thick_crv_max : FloatProperty(name="Max Thickness")

class FDG_PT_DriverGenOutlines_pnl(bpy.types.Panel):
    bl_label = "Outline Driver Generator"
    bl_category = "FCHAR"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"DEFAULT_CLOSED"}
    bl_parent_id = "FDG_PT_DriverGenerator_pnl"
    
    def poll_gp_object(self, object):
        if object.type == 'GPENCIL':
            return True

        return False
    
    bpy.types.WindowManager.gp_object = PointerProperty(name="Grease Pencil", type = bpy.types.Object, poll=poll_gp_object)
    bpy.types.WindowManager.Pass_Name = StringProperty(name="Pass Name")
    bpy.types.WindowManager.Pass_Number = IntProperty(name="Pass Number", min=0, max=100)
    bpy.types.WindowManager.modifier = StringProperty(name= "ThickMod")
    bpy.types.WindowManager.do_create_view_layer = BoolProperty(name= "Create a new View Layer", default=True)
    bpy.types.WindowManager.do_create_gp_layer = BoolProperty(name="Create a new Grease Pencil Layer", default=True)
    bpy.types.WindowManager.gp_layer = StringProperty(name="GP Layer")
    bpy.types.WindowManager.view_layer = StringProperty(name="View Layer")
    bpy.types.WindowManager.new_view_layer_name = StringProperty(name="New View Layer Name")

    

    def draw(self, context):
        wm = context.window_manager
        layout = self.layout

        layout.prop(wm, "Pass_Number")
        layout.prop(wm, "Pass_Name")

        box = layout.box()
        box.prop_search(wm, "gp_object", bpy.data, "objects", text="Grease Pencil")
        if wm.gp_object:
            box.prop(wm, "do_create_gp_layer")
            if not wm.do_create_gp_layer:
                box.prop_search(wm, "gp_layer", wm.gp_object.data, "layers")

        box = layout.box()
        box.prop(wm, "do_create_view_layer")
        if not wm.do_create_view_layer:
            box.prop_search(wm, "view_layer", context.scene, "view_layers")
        else:
            box.prop(wm, "new_view_layer_name")
        


        layout.prop_search(wm, "character_rig", bpy.data, "objects", text="Character Rig")
        rig = wm.character_rig
        if rig:
            if rig.type == 'ARMATURE':
                layout.prop_search(wm, "character_rig_bone", rig.data, "bones")
                if 'c_root_master.x' in rig.data.bones:
                    wm.character_rig_bone = 'c_root_master.x'

        
        


        layout.prop_search(wm, "camera", bpy.data, "objects", text="Camera")

        layout.operator("fdg.gen_outline_driver")
        

        pass



def register():
    bpy.utils.register_class(fritziGpSetup)
    bpy.types.WindowManager.gp_settings = CollectionProperty(type=fritziGpSetup)
    
    bpy.utils.register_class(FDG_PT_DriverGenOutlines_pnl)
    

def unregister():
    bpy.utils.unregister_class(FDG_PT_DriverGenOutlines_pnl)
    bpy.utils.unregister_class(fritziGpSetup)