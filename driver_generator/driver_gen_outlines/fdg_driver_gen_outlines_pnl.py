from tokenize import String
import bpy
from bpy.types import PropertyGroup, UIList
from bpy.props import PointerProperty, IntProperty, StringProperty, FloatProperty, CollectionProperty, BoolProperty, EnumProperty

from ...fchar_settings import Settings
from..utility_functions.fdg_driver_utils import *

def load_defaults():
    """Loads the default settings for the L0, L1 and L2 thickness Drivers from the Settings class and stores theme in
    a window Manager Property"""
    settings = Settings()
    line_settings = settings.get_setting("line_settings")
    settings_prop = bpy.context.window_manager.gp_pass_defaults
    
    for key in line_settings:
        item = settings_prop.get(key)
        if not item:
            item = settings_prop.add()
        
        item["name"] = line_settings[key]["line_key"]
        item["line_key"] = line_settings[key]["line_key"]
        item["thick_dist_close"] = line_settings[key]["dist_close"]
        item["thick_dist_far"] = line_settings[key]["dist_far"]
        item["thick_close"] = line_settings[key]["thick_close"]
        item["thick_far"] = line_settings[key]["thick_far"]

        item["crv_max_dist"] = line_settings[key]["crv_max_dist"]
        item["crv_off_dist"] = line_settings[key]["crv_off_dist"]
        item["crv_mode"] = line_settings[key]["crv_mode"]
        item["crv_amount"] = line_settings[key]["crv_amount"]

def gp_enum_callback(scene, context):
    """Callback Method which returns a dynamic Enum filled with the modifier names of all individual PropertyGroups
    stored in the gp_settings CollectionProperty in the Scene."""
    items = []
    if context.scene.gp_settings:
        for setting in context.scene.gp_settings:
            if(setting.name):
                items.append((setting.name, setting.name, ""))
                
    
    return items

def gp_default_enum_callback(scene, context):
    """Callback Method which returns a dynamic Enum filled with the modifier names of all individual PropertyGroups
    stored in the gp_pass_defaults CollectionProperty in the windowmanager."""
    items = []
    if context.window_manager.gp_pass_defaults:
        for setting in context.window_manager.gp_pass_defaults:
            if(setting.line_key):
                items.append((setting.line_key, setting.line_key, ""))
                
    
    return items


def crv_mode_update(self, context):
    """Update Method which gets called, when the crv_mode property of a fritziGPPass PropertyGroup gets changed.
    It sets the crv_max_dist to 0.0 and the crv_off_dist to -1. This means, that the DriverExpression always takes
    the maximum Value in the interplation, since the distance from Cam to Character is always positive."""
    if self.crv_mode:
        self.crv_max_dist = 0.0
        self.crv_off_dist = -1.0

def clamp_mode_update(self, context):
    """Update method which gets called if the Clamp Booleans get changed.
    It searches the Driver associated with the currently selected fritziGPPass Propertygroup and changes its expression
    to either clamp or not clamp the Values at the min or max distance depending on which Booleans are toggled."""
    my_data_path = 'grease_pencil_modifiers["' + self.thick_modifier + '"].thickness_factor'
    for fcurve in self.gp_object.animation_data.drivers:
        #print(fcurve.data_path)
        #print(my_data_path)
        if fcurve.data_path == my_data_path:
            #print("here")
            if self.clamp_close and self.clamp_far:
                #print("both")
                fcurve.driver.expression = "max(close_thick, min(far_thick, ((close_thick * (1 - (dist - close_dist) / (far_dist - close_dist))) + (far_thick * (dist - close_dist) / (far_dist - close_dist)))))/crv_value"
            elif self.clamp_close and not self.clamp_far:
                #print("close")
                fcurve.driver.expression = "max(close_thick, ((close_thick * (1 - (dist - close_dist) / (far_dist - close_dist))) + (far_thick * (dist - close_dist) / (far_dist - close_dist))))/crv_value"
            elif not self.clamp_close and self.clamp_far:
                #print("far")
                fcurve.driver.expression = "min(far_thick, ((close_thick * (1 - (dist - close_dist) / (far_dist - close_dist))) + (far_thick * (dist - close_dist) / (far_dist - close_dist))))/crv_value"
            elif not self.clamp_close and not self.clamp_far:
                #print("none")
                fcurve.driver.expression = "((close_thick * (1 - (dist - close_dist) / (far_dist - close_dist))) + (far_thick * (dist - close_dist) / (far_dist - close_dist)))/crv_value"

def poll_gp_object(self, object):
        if object.type == 'GPENCIL':
            return True

        return False

class fritziGPSettings(PropertyGroup):
    """A Property Group which stores the general settings for the Grease Pencil Setup"""

    default_view_layer : StringProperty(name="3D Layer")
    gp_object : PointerProperty(name="Grease_Pencil", type=bpy.types.Object, poll=poll_gp_object)
    outline_collection : PointerProperty(name="Outline Collection", type=bpy.types.Collection)
    objects_collection : PointerProperty(name="Objects Collection", type=bpy.types.Collection)
    environment_collection : PointerProperty(name="Environment Collection", type=bpy.types.Collection)
    environment_L0_collection: PointerProperty(name="Environment L0 Collection", type=bpy.types.Collection)
    environment_L1_collection: PointerProperty(name="Environment L1 Collection", type=bpy.types.Collection)
    environment_L2_collection: PointerProperty(name="Environment L2 Collection", type=bpy.types.Collection)
    character_collection : PointerProperty(name="Character Collection", type=bpy.types.Collection)
    excluded_collection : PointerProperty(name="Excluded Collection", type=bpy.types.Collection)
    forceintersection_collection : PointerProperty(name="ForceIntersection Collection", type=bpy.types.Collection)
    nointersection_collection : PointerProperty(name="NoIntersection Collection", type= bpy.types.Collection)
    extraobjects_collection : PointerProperty(name= "Extra Objects Collection", type=bpy.types.Collection)
    gp_material : StringProperty(name="GP Material") # Change all materials if changed!
    environment_layer_L0 : StringProperty(name="Environment Layer L0")
    environment_layer_L1 : StringProperty(name="Environment Layer L1")
    environment_layer_L2 : StringProperty(name="Environment Layer L2")
    environment_L0_lineart : StringProperty(name="Environment L0 Lineart")
    environment_L0_thickness : StringProperty(name="Environment L0 Thickness Modifier")
    environment_L1_lineart : StringProperty(name="Environment L1 Lineart")
    environment_L1_thickness : StringProperty(name="Environment L1 Thickness Modifier")
    environment_L2_lineart : StringProperty(name="Environment L2 Lineart")
    environment_L2_thickness : StringProperty(name="Environment L2 Thickness Modifier")
    environment_view_layer : StringProperty(name="Environment View Layer")
    character_view_layer : StringProperty(name="Character View Layer")
    extra_view_layer : StringProperty(name="Extra View Layer")


class fritziGPPass(PropertyGroup):
    """A Property Group which stores the setup of one GP Pass"""

    gp_object : PointerProperty(name="Grease Pencil", type = bpy.types.Object, poll=poll_gp_object)
    view_layer : StringProperty(name="View_Layer")

    pass_name : StringProperty(name="Pass Name")
    pass_nr : IntProperty(name="Pass Nr.")

    collection : PointerProperty(name="Collection", type=bpy.types.Collection)
    lineart : StringProperty(name="Line Art Modifier")
    thick_modifier : StringProperty(name="Thickness Modifier")
    crv_modifier : StringProperty(name="Curve Modifier")
    GP_layer : StringProperty(name= "GP_Layer")
    
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

def default_value_update(self, context):
    """Update method which gets called if the user updates the default value of a gp_setting"""

    settings = Settings()
    wm = context.window_manager
    line_settings = {}
    for item in wm.gp_pass_defaults:
        setting = {}

        setting["line_key"] = item["line_key"]
        setting["dist_close"] = item["thick_dist_close"]
        setting["dist_far"] = item["thick_dist_far"]
        setting["thick_close"] = item["thick_close"]
        setting["thick_far"] = item["thick_far"]

        setting["crv_max_dist"] = item["crv_max_dist"]
        setting["crv_off_dist"] = item["crv_off_dist"]
        setting["crv_mode"] = item["crv_mode"]
        setting["crv_amount"] = item["crv_amount"]



        line_settings[item.name] = setting

    settings.set_setting("line_settings", line_settings)
    
class fritziGPPassDefaults(PropertyGroup):
    """A Property Group which stores the default Settings for GP Pass"""   
    
    line_key : StringProperty(name="Pass", update=default_value_update)
    thick_dist_close : FloatProperty(name="Distance Close", update=default_value_update)
    thick_dist_far : FloatProperty(name="Distance Far", update=default_value_update)
    thick_close : FloatProperty(name="Thickness Close", update=default_value_update)
    thick_far : FloatProperty(name="Thickness Far", update=default_value_update)
    clamp_close : BoolProperty(name="Clamp Close", default=False, update=default_value_update)
    clamp_far : BoolProperty(name="Clamp Far", default=True, update=default_value_update)
    crv_mode : BoolProperty(name="Always Dynamic Line", default=True, update=default_value_update)
    crv_max_dist : FloatProperty(name="Curve Max Distance", description="The Distance at which the Dynamic Line is in full effect", update=default_value_update)
    crv_off_dist : FloatProperty(name="Curve Off Distance", description="The distance at which the Dynamic Line gets turned off", update=default_value_update)
    crv_amount : FloatProperty(name="Dynamic Line Amount", description="The amount of the Dynamic Line", min=0.0, update=default_value_update)




class FDG_PT_Outlines_pnl(bpy.types.Panel):
    bl_label = "Outlines"
    bl_category = "FCHAR"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        pass

class FDG_PT_DriverGenOutlines_pnl(bpy.types.Panel):
    bl_label = "Outline Driver Generator"
    bl_category = "FCHAR"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"DEFAULT_CLOSED"}
    bl_parent_id = "FDG_PT_Outlines_pnl"
    
    
    
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
    bpy.types.WindowManager.lineart_collection = PointerProperty(name="Line Art Collection", type=bpy.types.Collection)
    bpy.types.WindowManager.gp_defaults_enum = EnumProperty(name = "", items=gp_default_enum_callback)
    bpy.types.WindowManager.chk_old_collection = BoolProperty(name="Check for _old Collections", default=True)

    def draw(self, context):
        wm = context.window_manager
        scene = context.scene
        settings = scene.gp_defaults
        layout = self.layout

        layout.operator("fdg.gen_view_layers")

        layout.prop_search(settings, "default_view_layer", scene, "view_layers")
        layout.prop_search(settings, "environment_view_layer", scene, "view_layers")
        layout.prop_search(settings, "character_view_layer", scene, "view_layers")
        layout.prop_search(settings, "extra_view_layer", scene, "view_layers")
        
        layout.operator("fdg.gen_lineart_collections")
        
        layout.prop(wm, "Pass_Name")

        layout.prop_search(wm, "character_rig", bpy.data, "objects", text="Character Rig")
        rig = wm.character_rig
        if rig:
            if rig.type == 'ARMATURE':
                layout.prop_search(wm, "character_rig_bone", rig.data, "bones")
                if 'c_head.x' in rig.data.bones:
                    wm.character_rig_bone = 'c_head.x'
       
        layout.prop_search(wm, "camera", bpy.data, "objects", text="Camera")

        layout.prop(wm, "chk_old_collection")

        layout.operator("fdg.gen_lineart_pass")

        pass





"""Following are all Panels containing Settings for the Outline Driver Setup.
General Settings, Pass Settings, Default Settings, and Debug Settings"""


class FDG_PT_DriverGenOutlinesSettings_pnl(bpy.types.Panel):
    bl_label = "Outline Settings"
    bl_category = "FCHAR"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"DEFAULT_CLOSED"}
    bl_parent_id = "FDG_PT_DriverGenOutlines_pnl"

    def draw(self, context):
        pass

class FDG_PT_DriverGenOutlinesGeneralSettings_pnl(bpy.types.Panel):
    bl_label = "General Settings"
    bl_category = "FCHAR"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"DEFAULT_CLOSED"}
    bl_parent_id = "FDG_PT_DriverGenOutlinesSettings_pnl"

    def draw(self, context):
        scene = context.scene

        layout = self.layout
        settings = scene.gp_defaults
        layout.prop_search(settings, "gp_object", bpy.data, "objects", text="Grease Pencil")
        layout.prop_search(settings, "outline_collection", bpy.data, "collections")
        layout.prop_search(settings, "character_collection", bpy.data, "collections")

class FDG_PT_DriverGenOutlinesPassSettings_pnl(bpy.types.Panel):
    bl_label = "Outline Driver Settings"
    bl_category = "FCHAR"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"DEFAULT_CLOSED"}
    bl_parent_id = "FDG_PT_DriverGenOutlinesSettings_pnl"

    def draw(self, context):
        wm = context.window_manager
        scene = context.scene
        layout = self.layout
        

        layout.prop(wm, "gp_auto_enum")
        if scene.gp_settings:
            settings = scene.gp_settings.get(wm.gp_auto_enum)

            layout.prop_search(settings, "gp_object", bpy.data, "objects", text="Grease Pencil")

            layout.separator()

            layout.prop_search(settings, "collection", bpy.data, "collections", text="Collection")
            layout.prop_search(settings, "GP_layer", settings.gp_object.data, "layers", text="Grease Pencil Layer")
            layout.prop_search(settings, "lineart", settings.gp_object, "grease_pencil_modifiers", text="Line Art Modifier")
            layout.prop_search(settings, "thick_modifier", settings.gp_object, "grease_pencil_modifiers", text="Thickness Modifier")
            layout.prop_search(settings, "crv_modifier", settings.gp_object, "grease_pencil_modifiers", text="Curve Modifier")

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
            
            layout.separator()

            layout.operator("fdg.remove_lineart_pass")


class FDG_PT_DriverGenOutlinesDefaults_pnl(bpy.types.Panel):
    bl_label = "Defaults"
    bl_category = "FCHAR"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"DEFAULT_CLOSED"}
    bl_parent_id = "FDG_PT_DriverGenOutlinesSettings_pnl"

    def draw(self, context):
        wm = context.window_manager
        layout = self.layout
        load_defaults()
        layout.prop(wm, "gp_defaults_enum")

        if wm.gp_pass_defaults:
            settings = wm.gp_pass_defaults.get(wm.gp_defaults_enum)

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
           
            column = layout.column(align=True)
            column.prop(settings, "crv_max_dist")
            column.prop(settings, "crv_off_dist")


class FDG_PT_DriverGenOutlinesDebug_pnl(bpy.types.Panel):
    bl_label = "Debug"
    bl_category = "FCHAR"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"DEFAULT_CLOSED"}
    bl_parent_id = "FDG_PT_DriverGenOutlinesSettings_pnl"

    def draw(self, context):
        wm = context.window_manager
        scene = context.scene

        layout = self.layout
        settings = scene.gp_defaults
        layout.operator("fdg.update_cam_empties")
        layout.operator("fdg.fix_driver_targets")

        layout.separator()

        layout.prop(wm, "Pass_Name")

        layout.prop_search(wm, "character_rig", bpy.data, "objects", text="Character Rig")
        rig = wm.character_rig
        if rig:
            if rig.type == 'ARMATURE':
                layout.prop_search(wm, "character_rig_bone", rig.data, "bones")
                if 'c_head.x' in rig.data.bones:
                    wm.character_rig_bone = 'c_head.x'

        layout.operator("fdg.update_character_rig")
        
        layout.separator()
        
        layout.prop_search(settings, "gp_object", bpy.data, "objects", text="Grease Pencil")
        layout.prop_search(settings, "outline_collection", bpy.data, "collections")
        layout.prop_search(settings, "objects_collection", bpy.data, "collections")
        layout.prop_search(settings, "environment_collection", bpy.data, "collections")
        layout.prop_search(settings, "environment_L0_collection", bpy.data, "collections")
        layout.prop_search(settings, "environment_L1_collection", bpy.data, "collections")
        layout.prop_search(settings, "environment_L2_collection", bpy.data, "collections")
        layout.prop_search(settings, "character_collection", bpy.data, "collections")
        layout.prop_search(settings, "excluded_collection", bpy.data, "collections")
        layout.prop_search(settings, "nointersection_collection", bpy.data, "collections")
        layout.prop_search(settings, "forceintersection_collection", bpy.data, "collections")
        layout.prop_search(settings, "extraobjects_collection", bpy.data, "collections")
        layout.prop_search(settings, "gp_material", bpy.data, "materials")
        if settings.gp_object:
            layout.prop_search(settings, "environment_layer_L0", settings.gp_object.data, "layers", text="Environment Layer L0", icon='GREASEPENCIL')
            layout.prop_search(settings, "environment_layer_L1", settings.gp_object.data, "layers", text="Environment Layer L1", icon='GREASEPENCIL')
            layout.prop_search(settings, "environment_layer_L2", settings.gp_object.data, "layers", text="Environment Layer L2", icon='GREASEPENCIL')
            layout.prop_search(settings, "environment_L0_lineart", settings.gp_object, "grease_pencil_modifiers", text="Environment Line Art L0", icon='MOD_LINEART')
            layout.prop_search(settings, "environment_L1_lineart", settings.gp_object, "grease_pencil_modifiers", text="Environment Line Art L1", icon='MOD_LINEART')
            layout.prop_search(settings, "environment_L2_lineart", settings.gp_object, "grease_pencil_modifiers", text="Environment Line Art L2", icon='MOD_LINEART')
            layout.prop_search(settings, "environment_L0_thickness", settings.gp_object, "grease_pencil_modifiers", text="Environment Thickness Modifier L0", icon='MOD_THICKNESS')
            layout.prop_search(settings, "environment_L1_thickness", settings.gp_object, "grease_pencil_modifiers", text="Environment Thickness Modifier L1", icon='MOD_THICKNESS')
            layout.prop_search(settings, "environment_L2_thickness", settings.gp_object, "grease_pencil_modifiers", text="Environment Thickness Modifier L2", icon='MOD_THICKNESS')
        layout.prop_search(settings, "default_view_layer", scene, "view_layers")
        layout.prop_search(settings, "environment_view_layer", scene, "view_layers")
        layout.prop_search(settings, "character_view_layer", scene, "view_layers")
        layout.prop_search(settings, "extra_view_layer", scene, "view_layers")

        if is_handler_in_file():
            layout.label(text="Handler in File")
        else:
            layout.label(text="Handler NOT in File")




"""Following are Methods and Classes for the Preview Outline Generation"""

def draw_fritzi_outliner_menu(self, context):

    layout = self.layout
    layout.separator()
    layout.operator("fdg.add_collections", text="Add Selected Collections to Preview Outlines")

class FDG_UL_CollectionList_items(UIList):

    @classmethod
    def poll(cls, context):
        return True

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.prop_search(item, "character_collection", bpy.data, "collections", text = "Collection")

class CharacterProp(PropertyGroup):
    character_collection : PointerProperty(type=bpy.types.Collection)
    outline_object : PointerProperty(type=bpy.types.Object)

class FDG_PT_PreviewOutlines_pnl(bpy.types.Panel):
    bl_label = "Preview Outlines"
    bl_category = "FCHAR"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"DEFAULT_CLOSED"}
    bl_parent_id = "FDG_PT_Outlines_pnl"

    
    bpy.types.WindowManager.output_path = StringProperty(name="Output Path", subtype='DIR_PATH')
    bpy.types.WindowManager.file_name = StringProperty(name="File Name", subtype='FILE_NAME')
    

    def draw(self, context):
        wm = context.window_manager
        scene = context.scene
        layout = self.layout

        row = layout.row()
        row.template_list("FDG_UL_CollectionList_items", "", scene, "collection_list", scene, "collection_list_index")
        column = row.column(align=True)
        column.operator("fdg.add_collection", icon='ADD', text="")
        column.operator("fdg.remove_collection", icon='REMOVE', text="")
        
        layout.label(text= "Output Directory:")
        layout.prop(wm, "output_path", text="")
        layout.label(text="File Name:")
        layout.prop(wm, "file_name", text="")  
        layout.operator("fdg.gen_preview_outlines")
        layout.separator()

        layout.operator("fdg.create_preview_lines")
        layout.operator("fdg.activate_booleans")
        layout.operator("fdg.deactivate_booleans")
        layout.operator("fdg.prepare_scene")
        layout.operator("fdg.conform_visibilities")
        layout.operator("fdg.save_line_file")
        layout.separator()
        

        row = layout.row()
        row.prop(scene, "frame_start", text="Start")
        row.prop(scene, "frame_end", text="End")
        layout.operator("fdg.render_preview")
        
    

def register():
    bpy.utils.register_class(fritziGPPassDefaults)
    bpy.types.WindowManager.gp_pass_defaults = CollectionProperty(type=fritziGPPassDefaults)
    load_defaults()
    bpy.utils.register_class(fritziGPPass)
    bpy.types.Scene.gp_settings = CollectionProperty(type=fritziGPPass)
    bpy.utils.register_class(fritziGPSettings)
    bpy.types.Scene.gp_defaults = PointerProperty(type=fritziGPSettings)
    bpy.utils.register_class(CharacterProp)
    bpy.types.Scene.collection_list = CollectionProperty(name = "Character Collections", type=CharacterProp)
    bpy.types.Scene.collection_list_index = IntProperty()
    bpy.utils.register_class(FDG_PT_Outlines_pnl)
    bpy.utils.register_class(FDG_PT_PreviewOutlines_pnl)
    bpy.utils.register_class(FDG_PT_DriverGenOutlines_pnl)
    bpy.utils.register_class(FDG_PT_DriverGenOutlinesSettings_pnl)
    bpy.utils.register_class(FDG_PT_DriverGenOutlinesGeneralSettings_pnl)
    bpy.utils.register_class(FDG_PT_DriverGenOutlinesPassSettings_pnl)
    bpy.utils.register_class(FDG_PT_DriverGenOutlinesDefaults_pnl)
    bpy.utils.register_class(FDG_PT_DriverGenOutlinesDebug_pnl)
    
    bpy.utils.register_class(FDG_UL_CollectionList_items)
    bpy.types.OUTLINER_MT_context_menu.append(draw_fritzi_outliner_menu)
    bpy.types.OUTLINER_MT_collection.append(draw_fritzi_outliner_menu)
    

def unregister():
    bpy.types.OUTLINER_MT_context_menu.remove(draw_fritzi_outliner_menu)
    bpy.types.OUTLINER_MT_collection.remove(draw_fritzi_outliner_menu)
    bpy.utils.unregister_class(FDG_UL_CollectionList_items)
    
    bpy.utils.unregister_class(FDG_PT_DriverGenOutlinesDebug_pnl)
    bpy.utils.unregister_class(FDG_PT_DriverGenOutlinesDefaults_pnl)
    bpy.utils.unregister_class(FDG_PT_DriverGenOutlinesPassSettings_pnl)
    bpy.utils.unregister_class(FDG_PT_DriverGenOutlinesGeneralSettings_pnl)
    bpy.utils.unregister_class(FDG_PT_DriverGenOutlinesSettings_pnl)
    bpy.utils.unregister_class(FDG_PT_DriverGenOutlines_pnl)
    bpy.utils.unregister_class(FDG_PT_PreviewOutlines_pnl)
    bpy.utils.unregister_class(FDG_PT_Outlines_pnl)
    del bpy.types.Scene.collection_list_index
    del bpy.types.Scene.collection_list
    bpy.utils.unregister_class(CharacterProp)

    bpy.utils.unregister_class(fritziGPSettings)
    
    bpy.utils.unregister_class(fritziGPPass)

    bpy.utils.unregister_class(fritziGPPassDefaults)