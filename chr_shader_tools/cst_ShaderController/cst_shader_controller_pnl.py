import bpy
from bpy.props import PointerProperty, StringProperty


class CST_PT_ShaderController_pnl(bpy.types.Panel):
    bl_label = "Shader Controller"
    bl_category = "FCHAR"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_idname = "CST_PT_ShaderController_pnl"
    bl_options = {"DEFAULT_CLOSED"}

    bpy.types.WindowManager.character_name = StringProperty(name="Character Name")
    bpy.types.WindowManager.controller_empty = PointerProperty(
        name="Shader Controller", type=bpy.types.Object)
    bpy.types.WindowManager.character_collection = PointerProperty(
        name="Character Collection", type=bpy.types.Collection)
    bpy.types.WindowManager.light_empty = PointerProperty(
        name="Light Empty", type=bpy.types.Object)
    bpy.types.WindowManager.character_rig = PointerProperty(name = "Character Rig", type=bpy.types.Object)
    bpy.types.WindowManager.character_rig_bone = StringProperty(name = "Character Rig Bone")

    def draw(self, context):
        
        wm = context.window_manager
        layout = self.layout

        layout.prop(wm, "character_name")
        layout.operator("object.create_shader_controller")
        layout.operator("object.create_light_empty")

        layout.prop_search(wm, "controller_empty",
                           context.scene, "objects", text="Shader Controller")
        layout.prop_search(wm, "light_empty",
                            context.scene, "objects", text="Light Empty")
        layout.prop_search(wm, "character_collection",
                           bpy.data, "collections", text="Character Collection")
        layout.prop_search(wm, "character_rig", bpy.data, "objects", text="Character Rig")
        rig = wm.character_rig
        if rig:
            if rig.type == 'ARMATURE':
                layout.prop_search(wm, "character_rig_bone", rig.data, "bones")
                if 'c_root_master.x' in rig.data.bones:
                    wm.character_rig_bone = 'c_root_master.x'
        
        layout.operator("object.select_shader_controller")
        layout.operator("object.select_light_empty")

class CST_PT_ShaderControllerAdvanced_PNL(bpy.types.Panel):
    bl_label = "Advanced"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "FCHAR"
    bl_parent_id = "CST_PT_ShaderController_pnl"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):

        wm = context.window_manager
        layout = self.layout

        layout.label(text = 'Cleanup')
        layout.operator("object.remove_props")

        layout.separator()
        layout.operator("object.update_shader_controller")

        


def register():
    bpy.utils.register_class(CST_PT_ShaderController_pnl)
    bpy.utils.register_class(CST_PT_ShaderControllerAdvanced_PNL)

def unregister():
    bpy.utils.unregister_class(CST_PT_ShaderControllerAdvanced_PNL)
    bpy.utils.unregister_class(CST_PT_ShaderController_pnl)
