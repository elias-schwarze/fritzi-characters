import bpy
from bpy.types import Operator

class CST_OT_CopyControllerData_OP(Operator):
    bl_idname = "object.copy_controller_data"
    bl_label = "Copy Settings to selected"
    bl_description = "Copies all Controller settings from the active controller to all selected controllers."#
    bl_options = {"REGISTER", "UNDO"}

    props = ['vector_diffuse_mix', 'highlight_amount', 'highlight_color', 'rimlight_amount',
                'rimlight_color', 'advanced_mix_switch', 'advanced_mix_light_amount',
                'advanced_mix_light_color', 'advanced_mix_shadow_amount', 'advanced_mix_shadow_tint',
                'main_color_tint', 'main_color_tint_amount', 'shadow_color_tint', 'shadow_color_tint_amount']

    @classmethod
    def poll(cls, context):
        
        if not bpy.context.active_object:
            return False

        for prop in cls.props:
            if prop not in bpy.context.active_object:
                return False

        for controller in context.selected_objects:
            for prop in cls.props:
                if prop not in controller:
                    
                    return False

        return True
    
    def execute(self, context):

        active_controller = context.active_object
        selected_controllers = context.selected_objects

        for controller in selected_controllers:
            if controller == active_controller:
                continue

            for prop in self.props:
                controller[prop] = active_controller[prop]

        return {'FINISHED'}

def register():
    bpy.utils.register_class(CST_OT_CopyControllerData_OP)

def unregister():
    bpy.utils.unregister_class(CST_OT_CopyControllerData_OP)
