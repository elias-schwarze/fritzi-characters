import bpy

class ANM_OT_AnimMover_OP(bpy.types.Operator):
    bl_idname = "object.move_animation"
    bl_label = "Move Animation"
    bl_description = "Move all animations in the file a given Amount forwards or backwards"
    bl_options = {"REGISTER", "UNDO"}

    move_type: None
    move_direction: None
    frame_in: None
    frame_out: None
    frame_amount: None

    problematic_keys = []

    def execute(self, context):

        wm = bpy.context.window_manager
        self.move_type = wm.move_type
        self.move_direction = wm.move_direction
        self.frame_in = wm.frame_in
        self.frame_out = wm.frame_out
        self.frame_amount = wm.frame_amount

        if self.check_keys():
            self.report({'WARNING'}, "Problem Keys")
            return {'CANCELLED'}

        #for ob in bpy.data.objects:
        #    print(ob.name)
        #    if wm.move_keys:
        #        self.move_keys_on_object(ob)
        #    
        #    if wm.move_NLA:
        #        self.move_NLA_strips_on_object(ob)
        #    
        #if wm.move_marker:
        #    for marker in context.scene.timeline_markers:
        #        if self.move_type == 'BEFORE':
        #            if marker.frame <= self.frame_in:
        #                self.move_marker(marker)
        #        elif self.move_type == 'AFTER':
        #            if marker.frame >= self.frame_in:
        #                self.move_marker(marker)
        #        elif self.move_type == 'BETWEEN':
        #            if marker.frame >= self.frame_in and marker.frame <= self.frame_out:
        #                self.move_marker(marker)

        self.report({'INFO'}, "No Problem Keys")
        return {'FINISHED'}

    def check_keys(self):

        problem = False

        for ob in bpy.data.objects:
            if (ob.animation_data and ob.animation_data.action and ob.animation_data.action.fcurves):
                for fCurve in ob.animation_data.action.fcurves:
                    for key in fCurve.keyframe_points:
                        if self.move_type == 'BEFORE':
                            if self.move_direction == 'FORWARD':
                                if key.co[0] > self.frame_in and key.co[0] <= self.frame_in + self.frame_amount:
                                    problem = True
                                    self.problematic_keys.append(ob.name +': ' + fCurve.data_path + ' ' +  str(fCurve.array_index) + ' Frame: ' + str(key.co[0]))
                                    print(ob.name +': ' + fCurve.data_path + ' ' +  str(fCurve.array_index) + ' Frame: ' + str(key.co[0]))
                            if self.move_direction == 'BACKWARD':
                                pass
                                #this can not have problematic keys
                        
                        if self.move_type == 'AFTER':
                            if self.move_direction == 'FORWARD':
                                pass
                                #this can not have problematic keys
                            if self.move_direction == 'BACKWARD':
                                if key.co[0] < self.frame_in and key.co[0] >= self.frame_in - self.frame_amount:
                                    problem = True
                                    self.problematic_keys.append(ob.name +': ' + fCurve.data_path + ' ' +  str(fCurve.array_index) + ' Frame: ' + str(key.co[0]))
                                    print(ob.name +': ' + fCurve.data_path + ' ' +  str(fCurve.array_index) + ' Frame: ' + str(key.co[0]))

                        if self.move_type == 'BETWEEN':
                            if self.move_direction == 'FORWARD':
                                if key.co[0] > self.frame_out and key.co[0] <= self.frame_out + self.frame_amount:
                                    problem = True
                                    self.problematic_keys.append(ob.name +': ' + fCurve.data_path + ' ' +  str(fCurve.array_index) + ' Frame: ' + str(key.co[0]))
                                    print(ob.name +': ' + fCurve.data_path + ' ' +  str(fCurve.array_index) + ' Frame: ' + str(key.co[0]))
                            if self.move_direction == 'BACKWARD':
                                if key.co[0] < self.frame_in and key.co[0] >= self.frame_in - self.frame_amount:
                                    problem = True
                                    self.problematic_keys.append(ob.name +': ' + fCurve.data_path + ' ' +  str(fCurve.array_index) + ' Frame: ' + str(key.co[0]))
                                    print(ob.name +': ' + fCurve.data_path + ' ' +  str(fCurve.array_index) + ' Frame: ' + str(key.co[0]))
        
        return problem


    def move_keys_on_object(self, ob):
        if (ob.animation_data and ob.animation_data.action and ob.animation_data.action.fcurves):
                for fCurve in ob.animation_data.action.fcurves:
                    print(fCurve.data_path)
                    print(fCurve.array_index)
                    for key in fCurve.keyframe_points:
                        print(ob.name +': ' + fCurve.data_path + ' ' +  str(fCurve.array_index) + ' Frame: ' + str(key.co[0]))
                        if self.move_type == 'BEFORE':
                            if key.co[0] <= self.frame_in:
                                self.move_key(key)
                        elif self.move_type == 'AFTER':
                            if key.co[0] >= self.frame_in:
                                self.move_key(key)
                        elif self.move_type == 'BETWEEN':
                            if key.co[0] >= self.frame_in and key.co[0]<=self.frame_out:
                                self.move_key(key)

                        print(key.co)
                        #key.co[0] = key.co[0] + 10

    def move_NLA_strips_on_object(self, ob):
        if (ob.animation_data and ob.animation_data.nla_tracks):
                for track in ob.animation_data.nla_tracks:
                    for strip in track.strips:
                        
                        if self.move_type == 'BEFORE':
                            if strip.frame_start <= self.frame_in and strip.frame_end >= self.frame_in:
                                print("IN BETWEEN")
                                pass
                                # Save strip, track and ob to later give ui feedback that it could not be moved
                            elif strip.frame_end <= self.frame_in:
                                self.move_strip(strip)

                        elif self.move_type == 'AFTER':
                            if strip.frame_start <= self.frame_in and strip.frame_end >= self.frame_in:
                                print("IN BETWEEN")
                                pass
                                # Save strip, track and ob to later give ui feedback that it could not be moved
                            elif strip.frame_start >= self.frame_in:
                                self.move_strip(strip)

                        elif self.move_type == 'BETWEEN':
                            if strip.frame_start >= self.frame_in and strip.frame_start <= self.frame_out and strip.frame_end >= self.frame_in and strip.frame_end <= self.frame_out:
                                self.move_strip(strip)
                            elif (strip.frame_start <= self.frame_in and strip.frame_end >= self.frame_in) or (strip.frame_end >= self.frame_out and strip.frame_start <= self.frame_out):
                                print("IN BETWEEN")
                                pass
                                #Save strip, track and ob to later give UI feedback why it could not be moved

    def move_key(self, key):
        if self.move_direction == 'FORWARD':
            key.co[0] = key.co[0] + self.frame_amount
        elif self.move_direction =='BACKWARD':
            key.co[0] = key.co[0] - self.frame_amount

    def move_marker(self, marker):
        if self.move_direction == 'FORWARD':
            marker.frame = marker.frame + self.frame_amount
        elif self.move_direction == 'BACKWARD':
            marker.frame = marker.frame - self.frame_amount

    def move_strip(self, strip):
        if self.move_direction == 'FORWARD':
            strip.frame_end = strip.frame_end + self.frame_amount
            strip.frame_start = strip.frame_start + self.frame_amount
            
        if self.move_direction == 'BACKWARD':
            strip.frame_start = strip.frame_start - self.frame_amount
            strip.frame_end = strip.frame_end - self.frame_amount

class ANM_OT_AnimMoverBefore_OP(bpy.types.Operator):
    bl_idname = "object.move_animation_before"
    bl_label = "Before"
    bl_description = "Only move all Keyframes before a given Frame"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        wm = context.window_manager
        wm.move_type = 'BEFORE'
        

        return {'FINISHED'}

class ANM_OT_AnimMoverAfter_OP(bpy.types.Operator):
    bl_idname = "object.move_animation_after"
    bl_label = "After"
    bl_description = "Only move all Keyframes after a given Frame"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        wm = context.window_manager
        wm.move_type = 'AFTER'
        

        return {'FINISHED'}

class ANM_OT_AnimMoverBetween_OP(bpy.types.Operator):
    bl_idname = "object.move_animation_between"
    bl_label = "Between"
    bl_description = "Only move all Keyframes in a given Frame Range"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        wm = context.window_manager
        wm.move_type = 'BETWEEN'
        

        return {'FINISHED'}

class ANM_OT_AnimMoverBackward_OP(bpy.types.Operator):
    bl_idname = "object.move_animation_backward"
    bl_label = "Backwards"
    bl_description = "Move the Frames Backwards"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        wm = context.window_manager
        wm.move_direction = 'BACKWARD'
        

        return {'FINISHED'}

class ANM_OT_AnimMoverForward_OP(bpy.types.Operator):
    bl_idname = "object.move_animation_forward"
    bl_label = "Forwards"
    bl_description = "Move the Frames Forwards"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        wm = context.window_manager
        wm.move_direction = 'FORWARD'
        

        return {'FINISHED'}



def register():
    bpy.utils.register_class(ANM_OT_AnimMover_OP)
    bpy.utils.register_class(ANM_OT_AnimMoverBefore_OP)
    bpy.utils.register_class(ANM_OT_AnimMoverAfter_OP)
    bpy.utils.register_class(ANM_OT_AnimMoverBetween_OP)
    bpy.utils.register_class(ANM_OT_AnimMoverForward_OP)
    bpy.utils.register_class(ANM_OT_AnimMoverBackward_OP)

def unregister():
    bpy.utils.unregister_class(ANM_OT_AnimMoverBackward_OP)
    bpy.utils.unregister_class(ANM_OT_AnimMoverForward_OP)
    bpy.utils.unregister_class(ANM_OT_AnimMoverBetween_OP)
    bpy.utils.unregister_class(ANM_OT_AnimMoverAfter_OP)
    bpy.utils.unregister_class(ANM_OT_AnimMoverBefore_OP)
    bpy.utils.unregister_class(ANM_OT_AnimMover_OP)