import bpy
from bpy.props import FloatProperty, StringProperty, PointerProperty
from bpy.types import PropertyGroup, UIList
from . import fmr_settings
from . import fmr_scale_list_io
import os


class FMR_PT_Retarget_pnl(bpy.types.Panel):
    """Main Panel for the retarget Operators. Only is a container for subpanels"""
    bl_label = "MoCap Retarget"
    bl_category = "FCHAR"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"DEFAULT_CLOSED"}

    
    

    def draw(self, context):
        
        pass

class FMR_PT_SingleRetarget_pnl(bpy.types.Panel):
    bl_label = "Single Retarget"
    bl_category = "FCHAR"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_parent_id = "FMR_PT_Retarget_pnl"

    def draw(self, context):
        
        settings = fmr_settings.Settings()

        perforce_path = settings.get_setting("perforce_path")
        


        scene = context.scene
        wm = context.window_manager
        layout = self.layout

        scale_list = fmr_scale_list_io.ScaleListDict()
        
        

        layout.prop_search(wm, "source_rig_pointer", scene, "objects", text="Source Armature")
        layout.prop_search(wm, "target_rig_pointer", scene, "objects", text="Target Armature")
        layout.prop(wm, "auto_scale_check")
        

        layout.operator("object.mocap_retarget")

        

class FMR_PT_BatchRetarget_pnl(bpy.types.Panel):
    bl_label = "Batch Retarget"
    bl_category = "FCHAR"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_parent_id = "FMR_PT_Retarget_pnl"

    def draw(self, context):
        wm = context.window_manager
        scene = context.scene
        layout = self.layout
        settings = fmr_settings.Settings()

        perforce_path = settings.get_setting("perforce_path")

        # checks if the perforce directory is correctly set: If it is, the retarget Operators are displayed.
        # If not, an Operator to select the Perforce directory is displayed.
        if not (os.path.isdir(perforce_path) and os.path.isdir(os.path.join(perforce_path, "080_scenes")) and os.path.isdir(os.path.join(perforce_path, "075_capture"))):
            layout.label(text="No vaild Perforce Path set.")
            layout.label(text="Please set the Perforce Path")
            layout.operator("settings.choose_perforce_path")
        else:
            op = layout.operator("retarget.select_char_file")
            op.filepath = perforce_path
            op = layout.operator("retarget.select_bvhs")
            op.filepath = perforce_path
            

            if wm.bvh_files:
                row = layout.row()
                row.template_list("FMR_UL_BVHList_items", "", wm, "bvh_files", wm, "bvh_files_index", rows = 3)

                column = row.column(align=True)
                column.operator("object.add_bvh", icon='ADD', text="")
                column.operator("retarget.remove_bvh", icon='REMOVE', text="")
            
            layout.prop_search(wm, "target_rig_pointer", scene, "objects", text="Target Armature")

            layout.operator("retarget.mocap_batch_retarget")


class FMR_PT_ScaleList_pnl(bpy.types.Panel):
    bl_label = "Scale List"
    bl_category = "FCHAR"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_parent_id = "FMR_PT_Retarget_pnl"

    def draw(self, context):
        wm = context.window_manager
        layout = self.layout

        row = layout.row()
        row.template_list("FMR_UL_ScaleList_items", "", wm, "scale_list", wm, "scale_list_index", rows=3)
        
        # Fetches the newest Scales every update.
        scale_list = fmr_scale_list_io.ScaleListDict()
        scale_list.push_to_properties()

        column = row.column(align=True)
        
        
        column.operator("object.add_character_scale", icon='ADD', text="")
        column.operator("object.remove_character_scale", icon='REMOVE', text="")

        row = layout.row(align=True)
        row.operator("file.import_scale_list")
        row.operator("file.export_scale_list")



def ScaleUpdate(self, context):
    """This Method gets triggered if a Scaleproperty gets updated (Either by the User or through the API.
    The new property value gets set in the Scale List Dict."""
    scale_list = fmr_scale_list_io.ScaleListDict()
    
    #print("scaleupdate")
    #print(self.name)
    #print(self.scale)
    scale_list.set_scale(self.name, self.scale)
    

def NameUpdate(self, context):
    """ This Method gets triggered if the Name Property gets updated (Either by the User or through the API.
    Triggers the Scale List Dict to fetch all new Properties from the UI"""
    scale_list = fmr_scale_list_io.ScaleListDict()
    #print("Name")
    #print(self.character)

    scale_list.fetch_properties()

class ScaleList(PropertyGroup):
    """ A PropertyGroup which can Store the Name and Scale of characters"""
    scale : FloatProperty(default=1.0, update=ScaleUpdate)
    character : StringProperty(default="", update=NameUpdate)

class FMR_UL_ScaleList_items(UIList):
    @classmethod
    def poll(cls, context):
        return True

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        
        split = layout.split(factor=1.0)
        split.prop(item, "character", text="", emboss=False, translate=False)
        split = layout.split(factor=1.0)
        split.prop(item, "scale", text="", emboss=False, translate=False)

        
    def invoke(self, context, event):
        
        pass


class FMR_UL_BVHList_items(UIList):
    @classmethod
    def poll(cls, context):
        return True

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        row = layout.row()
        row.prop(item, "name", text="", emboss=False, translate=False)
        row.enabled = False


def update_source_rig(self, context):
    """Updates the Source Rig Property of ARP if a new Source Rig is selected in FCHAR"""
    wm = context.window_manager
    scene = context.scene
    print("update")
    if (wm.source_rig_pointer):
        print("setRig")
        scene.source_rig = wm.source_rig_pointer.name
    else:
        scene.source_rig = ""

def update_target_rig(self, context):
    """Updates the Target Rig Property of ARP if a new Target Rig is selected in FCHAR"""
    wm = context.window_manager
    scene = context.scene

    if(wm.target_rig_pointer):
        scene.target_rig = wm.target_rig_pointer.name
    else:
        scene.target_rig = ""



def register():
    
    
    bpy.utils.register_class(FMR_PT_Retarget_pnl)
    bpy.utils.register_class(FMR_PT_SingleRetarget_pnl)
    bpy.utils.register_class(FMR_PT_BatchRetarget_pnl)
    bpy.utils.register_class(FMR_UL_BVHList_items)
    bpy.utils.register_class(FMR_PT_ScaleList_pnl)
    bpy.utils.register_class(ScaleList)
    bpy.utils.register_class(FMR_UL_ScaleList_items)
    

def unregister():
    bpy.utils.unregister_class(FMR_UL_ScaleList_items)
    bpy.utils.unregister_class(ScaleList)
    bpy.utils.unregister_class(FMR_PT_ScaleList_pnl)
    bpy.utils.unregister_class(FMR_UL_BVHList_items)
    bpy.utils.unregister_class(FMR_PT_BatchRetarget_pnl)
    bpy.utils.unregister_class(FMR_PT_SingleRetarget_pnl)
    bpy.utils.unregister_class(FMR_PT_Retarget_pnl)
    



