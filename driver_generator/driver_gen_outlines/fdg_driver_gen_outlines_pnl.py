from multiprocessing import context
import bpy
from bpy.types import PropertyGroup
from bpy.props import PointerProperty, IntProperty, StringProperty, FloatProperty, CollectionProperty, BoolProperty, EnumProperty

def crv_mode_update(self, context):
    """Update Method which gets called, when the crv_mode property of a fritziGPSetup PropertyGroup gets changed.
    It sets the crv_max_dist to 0.0 and the crv_off_dist to -1. This means, that the DriverExpression always takes
    the maximum Value in the interplation, since the distance from Cam to Character is always positive."""
    if self.crv_mode:
        self.crv_max_dist = 0.0
        self.crv_off_dist = -1.0

def clamp_mode_update(self, context):
    """Update method which gets called if the Clamp Booleans get changed.
    It searches the Driver associated with the currently selected fritziGPSetup Propertygroup and changes its expression
    to either clamp or not clamp the Values at the min or max distance depending on which Booleans are toggled."""
    my_data_path = 'grease_pencil_modifiers["' + self.thick_modifier + '"].thickness_factor'
    for fcurve in self.gp_object.animation_data.drivers:
        print(fcurve.data_path)
        print(my_data_path)
        if fcurve.data_path == my_data_path:
            print("here")
            if self.clamp_close and self.clamp_far:
                print("both")
                fcurve.driver.expression = "max(close_thick, min(far_thick, ((close_thick * (1 - (dist - close_dist) / (far_dist - close_dist))) + (far_thick * (dist - close_dist) / (far_dist - close_dist)))))/crv_value"
            elif self.clamp_close and not self.clamp_far:
                print("close")
                fcurve.driver.expression = "max(close_thick, ((close_thick * (1 - (dist - close_dist) / (far_dist - close_dist))) + (far_thick * (dist - close_dist) / (far_dist - close_dist))))/crv_value"
            elif not self.clamp_close and self.clamp_far:
                print("far")
                fcurve.driver.expression = "min(far_thick, ((close_thick * (1 - (dist - close_dist) / (far_dist - close_dist))) + (far_thick * (dist - close_dist) / (far_dist - close_dist))))/crv_value"
            elif not self.clamp_close and not self.clamp_far:
                print("none")
                fcurve.driver.expression = "((close_thick * (1 - (dist - close_dist) / (far_dist - close_dist))) + (far_thick * (dist - close_dist) / (far_dist - close_dist)))/crv_value"

def poll_gp_object(self, object):
        if object.type == 'GPENCIL':
            return True

        return False

class fritziGpSetup(PropertyGroup):
    """A Property Group which stores the setup of one GP Pass"""
    gp_object : PointerProperty(name="Grease Pencil", type = bpy.types.Object, poll=poll_gp_object)
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
    clamp_close : BoolProperty(name="Clamp Close", default=False, update=clamp_mode_update)
    clamp_far : BoolProperty(name="Clamp Far", default=True, update=clamp_mode_update)
    crv_mode : BoolProperty(name="Always Dynamic Line", default=True, update=crv_mode_update)
    crv_max_dist : FloatProperty(name="Curve Max Distance", description="The Distance at which the Dynamic Line is in full effect")
    crv_off_dist : FloatProperty(name="Curve Off Distance", description="The distance at which the Dynamic Line gets turned off")
    crv_amount : FloatProperty(name="Dynamic Line Amount", description="The amount of the Dynamic Line", min=0.0)

def gp_enum_callback(scene, context):
    """Callback Method which returns a dynamic Enum filled with the modifier names of all individual PropertyGroups
    stored in the gp_settings CollectionProperty in the Scene."""
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
    bpy.types.WindowManager.gp_auto_advanced_toggle = BoolProperty(name = "Advanced", default=False)
    

    def draw(self, context):
        wm = context.window_manager
        layout = self.layout

        layout.prop(wm, "Pass_Number")
        layout.prop(wm, "Pass_Name")

        
        layout.prop_search(wm, "gp_object", bpy.data, "objects", text="Grease Pencil")


        layout.prop_search(wm, "character_rig", bpy.data, "objects", text="Character Rig")
        rig = wm.character_rig
        if rig:
            if rig.type == 'ARMATURE':
                layout.prop_search(wm, "character_rig_bone", rig.data, "bones")
                if 'c_head.x' in rig.data.bones:
                    wm.character_rig_bone = 'c_head.x'

        
        


        layout.prop_search(wm, "camera", bpy.data, "objects", text="Camera")

        layout.operator("fdg.gen_outline_driver")


        #This will be implemented in the future
        #layout.prop(wm, "gp_auto_advanced_toggle")

        
        
        #if (wm.gp_auto_advanced_toggle):
        #    box = layout.box()
        #    if wm.gp_object:
        #        box.prop(wm, "do_create_gp_layer")
        #        if not wm.do_create_gp_layer:
        #            box.prop_search(wm, "gp_layer", wm.gp_object.data, "layers")
#
        #    box = layout.box()
        #    box.prop(wm, "do_create_view_layer")
        #    if not wm.do_create_view_layer:
        #        box.prop_search(wm, "view_layer", context.scene, "view_layers")
        #    else:
        #        box.prop(wm, "new_view_layer_name")
        

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
        

        layout.prop(wm, "gp_auto_enum")
        if scene.gp_settings:
            settings = scene.gp_settings.get(wm.gp_auto_enum)
            #layout.label(text=settings.GP_layer)



            #layout.prop(settings, "GP_layer")
            #layout.prop(settings, "view_layer")
            layout.prop_search(settings, "gp_object", bpy.data, "objects", text="Grease Pencil")
            layout.prop_search(settings, "thick_modifier", settings.gp_object, "grease_pencil_modifiers", text = "Thickness Modifier")
            layout.prop_search(settings, "crv_modifier", settings.gp_object, "grease_pencil_modifiers", text = "Curve Modifier")
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

            layout.separator()

            layout.prop(settings, "crv_amount")
            layout.prop(settings, "crv_mode")
            if not settings.crv_mode:
                column = layout.column(align=True)
                column.prop(settings, "crv_max_dist")
                column.prop(settings, "crv_off_dist")



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