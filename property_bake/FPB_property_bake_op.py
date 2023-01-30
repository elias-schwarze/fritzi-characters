import bpy
from bpy.types import Operator
from bpy.props import IntProperty

class FPB_OT_PropertyBake_OP(Operator):
    bl_idname = "fpb.bake_properties"
    bl_label = "Bake Ik/Fk Properties"
    bl_description = "Bakes all the Ik/Fk switches on a character into the current action"
    bl_options = {"REGISTER", "UNDO"}

    frame_start: IntProperty(name= 'Start')
    frame_end: IntProperty(name= 'End')
    
    @classmethod
    def poll(cls, context):
        wm = context.window_manager
        if not wm.character_rig:
            return False
        return True

    def invoke(self, context, event):
        self.frame_start = context.scene.frame_start
        self.frame_end = context.scene.frame_end
        return context.window_manager.invoke_props_dialog(self, width = 400)

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop(self, "frame_start")
        row.prop(self, "frame_end")

    def execute(self, context):
        self.bake_easy_but_slow()

        return {'FINISHED'}
    
    def bake_easy_but_slow(self):
        wm = bpy.context.window_manager
        rig = wm.character_rig
        anim_data = rig.animation_data
        action = rig.animation_data.action
        influence = anim_data.action_influence
        anim_data.action_influence = 0.0
        bone_hand_l = rig.pose.bones["c_hand_ik.l"]
        hand_l_switch_curve = action.fcurves.find('pose.bones["c_hand_ik.l"]["ik_fk_switch"]')
        if not hand_l_switch_curve:
            hand_l_switch_curve = action.fcurves.new('pose.bones["c_hand_ik.l"]["ik_fk_switch"]')
        
        bone_hand_r = rig.pose.bones["c_hand_ik.r"]
        hand_r_switch_curve = action.fcurves.find('pose.bones["c_hand_ik.r"]["ik_fk_switch"]')
        if not hand_r_switch_curve:
            hand_r_switch_curve = action.fcurves.new('pose.bones["c_hand_ik.r"]["ik_fk_switch"]')

        bone_foot_l = rig.pose.bones["c_foot_ik.l"]
        foot_l_switch_curve = action.fcurves.find('pose.bones["c_foot_ik.l"]["ik_fk_switch"]')
        if not foot_l_switch_curve:
            foot_l_switch_curve = action.fcurves.new('pose.bones["c_foot_ik.l"]["ik_fk_switch"]')

        bone_foot_r = rig.pose.bones["c_foot_ik.r"]
        foot_r_switch_curve = action.fcurves.find('pose.bones["c_foot_ik.r"]["ik_fk_switch"]')
        if not foot_r_switch_curve:
            foot_r_switch_curve = action.fcurves.new('pose.bones["c_foot_ik.r"]["ik_fk_switch"]')

        for i in range(self.frame_start, self.frame_end):
            bpy.context.scene.frame_set(i)
            #print(bone_hand_l["ik_fk_switch"])
            #print(rig.pose.bones["c_hand_ik.l"]["ik_fk_switch"])
            hand_l_switch_curve.keyframe_points.insert(i, bone_hand_l["ik_fk_switch"], options={'FAST'})
            hand_r_switch_curve.keyframe_points.insert(i, bone_hand_r["ik_fk_switch"], options={'FAST'})
            foot_l_switch_curve.keyframe_points.insert(i, bone_foot_l["ik_fk_switch"], options={'FAST'})
            foot_r_switch_curve.keyframe_points.insert(i, bone_foot_r["ik_fk_switch"], options={'FAST'})
        
        anim_data.action_influence = influence
        
    
    def bake_complicated_but_fast(self):
        wm = bpy.context.window_manager
        rig = wm.character_rig

        #I cant think of a better name, I am sorry
        #This list holds Fcurve_Datas with unique data_paths and array_indices
        datas_list = Fcurve_Datas_List()

        for track in rig.animation_data.nla_tracks:
            for strip in track.strips:
                for fcurve in strip.action.fcurves:
                    if 'ik_fk_switch' in fcurve.data_path:
                        data = Fcurve_Data(track, strip, fcurve)
                        datas_list.add_with_unique_path(data)

        for datas in datas_list.datas_list:
            print("----------------")
            print("Unique Path List")
            print("Path: " + datas.data_path + ": " + str(datas.array_index))
            for i in range(160, 310):
                print(datas.evaluate(i))
            for data in datas.Fcurve_List:
                print("----------------")
                print("Data:")
                print("Path: " + data.data_path)
                print("Index: " + str(data.array_index))
                print("fcurve: " + str(data.fcurve))
                print("Blending: " + str(data.blend_mode))
                print("Extrapolation: " + str(data.hold_mode))
                print("Active: " + str(data.active))

class Fcurve_Data:
    
    def __init__(self, track, strip, fcurve):
        self.track = track
        self.strip = strip
        self.data_path = fcurve.data_path
        self.array_index = fcurve.array_index
        self.fcurve = fcurve
        self.postition = 0
        self.blend_mode = strip.blend_mode
        self.hold_mode = strip.extrapolation
        self.active = strip.active

class Fcurve_Datas:

    def __init__(self, data_path, array_index):
        self.data_path = data_path
        self.array_index = array_index
        self.Fcurve_List = []

    def add_fcurve_data(self, fcurve_data: Fcurve_Data):
        if fcurve_data.data_path == self.data_path and fcurve_data.array_index == self.array_index:
            self.Fcurve_List.append(fcurve_data)
    
    def evaluate(self, frame):
        for data in self.Fcurve_List:
            pass

class Fcurve_Datas_List:
    
    def __init__(self):
        self.datas_list = []

    def add_with_unique_path(self, fcurve_data: Fcurve_Data):
        if len(self.datas_list) == 0:
            datas = Fcurve_Datas(fcurve_data.data_path, fcurve_data.array_index)
            self.datas_list.append(datas)
            datas.add_fcurve_data(fcurve_data)
        else:
            for datas in self.datas_list:
                if fcurve_data.data_path == datas.data_path and fcurve_data.array_index == datas.array_index:
                    datas.add_fcurve_data(fcurve_data)
                    return
            datas = Fcurve_Datas(fcurve_data.data_path, fcurve_data.array_index)
            self.datas_list.append(datas)
            datas.add_fcurve_data(fcurve_data)



    

def register():
    bpy.utils.register_class(FPB_OT_PropertyBake_OP)

def unregister():
    bpy.utils.unregister_class(FPB_OT_PropertyBake_OP)