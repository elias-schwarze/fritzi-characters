import bpy
from bpy.props import EnumProperty, IntProperty, BoolProperty


class ANM_PT_KeyframeMover_pnl(bpy.types.Panel):
    bl_label = "Animation Mover"
    bl_category = "FCHAR"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"DEFAULT_CLOSED"}

    bpy.types.WindowManager.move_type = EnumProperty(name='move_type', 
                            description='Shows which Type of Frame Range should be used for the animation move (Before, After, Between',
                            items={('BEFORE', 'before', 'Move all before'),
                            ('AFTER', 'after', 'Move all after'),
                            ('BETWEEN', 'between', 'move all between')},
                            default = 'AFTER')

    bpy.types.WindowManager.move_direction = EnumProperty(name='move_direction',
                            description='Which direction to move the keyframes',
                            items={('FORWARD', 'forward', 'Move Keyframes forwards'),
                            ('BACKWARD', 'backwards', 'Move Keyframes backwards')},
                            default= 'FORWARD')
    bpy.types.WindowManager.frame_in = IntProperty(name= 'Frame In')
    bpy.types.WindowManager.frame_out = IntProperty(name= 'Frame Out')
    bpy.types.WindowManager.frame_amount = IntProperty(name= 'Frames', min = 0, soft_min = 0)

    bpy.types.WindowManager.move_keys = BoolProperty(name='Move Keyframes', description='Should the Move Operator Move Keyframes', default=True)
    bpy.types.WindowManager.move_NLA = BoolProperty(name='Move NLA Strips', description='Should the Move Operator Move NLA Strips', default=True)
    bpy.types.WindowManager.move_marker = BoolProperty(name='Move Camera Marker', description='Should the Move Operator Move Camera Markers', default=True)
    bpy.types.WindowManager.move_sounds = BoolProperty(name= 'Move Sounds', description= 'Should the Move Operator move Sound Strips', default=True)
    def draw(self, context):
        wm = context.window_manager
        layout = self.layout
        layout.label(text="Move all Keyframes")
        row = layout.row(align=True)
        
        
        if wm.move_type == 'BEFORE':
            row.operator("object.move_animation_before", depress=True)
            row.operator("object.move_animation_after", depress=False)
            row.operator("object.move_animation_between", depress=False)
            layout.label(text= 'Frame')
            layout.prop(wm, "frame_in", text="")
        elif wm.move_type == 'AFTER':
            
            row.operator("object.move_animation_before", depress=False)
            row.operator("object.move_animation_after", depress=True)
            row.operator("object.move_animation_between", depress=False)
            layout.label(text= 'Frame')
            layout.prop(wm, "frame_in", text="")
        elif wm.move_type == 'BETWEEN':
            row.operator("object.move_animation_before", depress=False)
            row.operator("object.move_animation_after", depress=False)
            row.operator("object.move_animation_between", depress=True)
            layout.label(text= 'Frames')
            row = layout.row()
            row.prop(wm, "frame_in",text="")
            row.alignment = 'CENTER'
            row.label(text="and")
            row.alignment = 'EXPAND'
            row.prop(wm, "frame_out",text="")
        
        layout.prop(wm, 'frame_amount')
        row = layout.row(align=True)

        if wm.move_direction == 'FORWARD':
            row.operator("object.move_animation_backward", depress=False)
            row.operator("object.move_animation_forward", depress=True)
        elif wm.move_direction == 'BACKWARD':
            row.operator("object.move_animation_backward", depress=True)
            row.operator("object.move_animation_forward", depress=False)

        layout.operator("object.move_animation")

        layout.separator()
        layout.operator("animation.move_test")

class ANM_PT_MoveOptions_pnl(bpy.types.Panel):
    bl_label = "Options"
    bl_category = "FCHAR"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_parent_id = "ANM_PT_KeyframeMover_pnl"

    def draw(self, context):

        wm = context.window_manager
        layout = self.layout

        layout.prop(wm, 'move_keys')
        layout.prop(wm, 'move_NLA')
        layout.prop(wm, 'move_marker')
        layout.prop(wm, 'move_sounds')

class ANM_PT_SyncLength_pnl(bpy.types.Panel):
    bl_label = "Sync Length"
    bl_category = "FCHAR"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_parent_id = "ANM_PT_KeyframeMover_pnl"

    def draw(self, context):
        wm = context.window_manager
        layout = self.layout

        layout.label(text="For all NLA Strips:")

        row = layout.row(align=True)
        row.operator("object.sync_length_on")
        row.operator("object.sync_length_off")

def draw_copy_animation_menu(self, context):

    layout = self.layout
    layout.separator()
    layout.operator("anm.copy_anim_data") 

def register():
    bpy.types.VIEW3D_MT_make_links.append(draw_copy_animation_menu)
    bpy.utils.register_class(ANM_PT_KeyframeMover_pnl)
    bpy.utils.register_class(ANM_PT_MoveOptions_pnl)
    bpy.utils.register_class(ANM_PT_SyncLength_pnl)

def unregister():
    bpy.utils.unregister_class(ANM_PT_SyncLength_pnl)
    bpy.utils.unregister_class(ANM_PT_MoveOptions_pnl)
    bpy.utils.unregister_class(ANM_PT_KeyframeMover_pnl)
    bpy.types.VIEW3D_MT_make_links.remove(draw_copy_animation_menu)