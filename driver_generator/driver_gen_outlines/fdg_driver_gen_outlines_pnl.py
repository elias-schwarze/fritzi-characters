from multiprocessing import context
import bpy
from bpy.types import PropertyGroup
from bpy.props import PointerProperty, IntProperty, StringProperty, FloatProperty, CollectionProperty, BoolProperty, EnumProperty

class fritziGpSetup(PropertyGroup):
    """A Property Group which stores the setup of one GP Pass"""
    GP_layer : StringProperty(name= "GP_Layer")
    view_layer : StringProperty(name="View_Layer")
    pass_name : StringProperty(name="Pass Name")
    pass_nr : IntProperty(name="Pass Nr.")
    thick_modifier : StringProperty(name="Thickness Modifier")
    crv_modifier : StringProperty(name="Curve Modifier")
    thick_dist_close : FloatProperty(name="Distance Close")
    thick_dist_far : FloatProperty(name="Distance Far")
    thick_close : FloatProperty(name="Thickness Close")
    thick_far : FloatProperty(name="Thickness Far")
    clamp_close : BoolProperty(name="Clamp Close", default=False)
    clamp_far : BoolProperty(name="Clamp Far", default=True)

def gp_enum_callback(scene, context):
    items = []
    if context.scene.gp_settings:
        for setting in context.scene.gp_settings:
            if(setting.name):
                items.append((setting.name, setting.name, ""))
                
    
    return items

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
    bpy.types.WindowManager.modifier_thick = StringProperty(name= "ThickMod")
    bpy.types.WindowManager.modifier_crv = StringProperty(name= "CrvMod")
    bpy.types.WindowManager.do_create_view_layer = BoolProperty(name= "Create a new View Layer", default=True)
    bpy.types.WindowManager.do_create_gp_layer = BoolProperty(name="Create a new Grease Pencil Layer", default=False)
    bpy.types.WindowManager.gp_layer = StringProperty(name="GP Layer")
    bpy.types.WindowManager.view_layer = StringProperty(name="View Layer")
    bpy.types.WindowManager.new_view_layer_name = StringProperty(name="New View Layer Name")
    bpy.types.WindowManager.gp_auto_enum = EnumProperty(name = "",items=gp_enum_callback)
    

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

        layout.prop(wm, "gp_auto_enum")
        

        pass

class FDG_PT_DriverGenOutlinesSettings_pnl(bpy.types.Panel):
    bl_label = "Outline Driver Settings"
    bl_category = "FCHAR"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"DEFAULT_CLOSED"}
    bl_parent_id = "FDG_PT_DriverGenOutlines_pnl"

    def draw(self, context):
        wm = context.window_manager
        scene = context.scene
        layout = self.layout
        gp_settings = scene.gp_settings

        layout.prop(wm, "gp_auto_enum")
        if scene.gp_settings:
            settings = scene.gp_settings.get(wm.gp_auto_enum)
            layout.label(text=settings.GP_layer)



            layout.prop(settings, "GP_layer")
            layout.prop(settings, "view_layer")
            
            layout.prop_search(settings, "thick_modifier", wm.gp_object, "grease_pencil_modifiers", text = "Thickness Modifier")
            layout.prop_search(settings, "crv_modifier", wm.gp_object, "grease_pencil_modifiers", text = "Curve Modifier")
            layout.separator()
            column = layout.column(align=True)
            column.prop(settings, "thick_dist_close")
            column.prop(settings, "thick_close")
            layout.prop(settings, "clamp_close")
            layout.separator()
            column = layout.column(align=True)
            column.prop(settings, "thick_dist_far")
            column.prop(settings, "thick_far")
            layout.prop(settings, "clamp_far")


def register():
    bpy.utils.register_class(fritziGpSetup)
    bpy.types.Scene.gp_settings = CollectionProperty(type=fritziGpSetup)
    bpy.types.Scene.gp = PointerProperty(type=fritziGpSetup)
    
    bpy.utils.register_class(FDG_PT_DriverGenOutlines_pnl)
    bpy.utils.register_class(FDG_PT_DriverGenOutlinesSettings_pnl)
    

def unregister():
    bpy.utils.unregister_class(FDG_PT_DriverGenOutlinesSettings_pnl)
    bpy.utils.unregister_class(FDG_PT_DriverGenOutlines_pnl)
    bpy.utils.unregister_class(fritziGpSetup)