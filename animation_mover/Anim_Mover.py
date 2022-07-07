import bpy

class Anim_Mover():

    move_type: None
    move_direction: None
    frame_in: None
    frame_out: None
    frame_amount: None
    wm: None
    context: None


    def __init__(self, window_manager, context):
        self.wm = window_manager
        self.context = context
        self.move_type = self.wm.move_type
        self.move_direction = self.wm.move_direction
        self.frame_in = self.wm.frame_in
        self.frame_out = self.wm.frame_out
        self.frame_amount = self.wm.frame_amount

    def move_anim(self):
        for ob in bpy.data.objects:
            print(ob.name)
            if self.wm.move_keys:
                self.move_keys_on_object(ob)
            
            if self.wm.move_NLA:
                self.move_NLA_strips_on_object(ob)
            
        if self.wm.move_marker:
            for marker in self.context.scene.timeline_markers:
                if self.move_type == 'BEFORE':
                    if marker.frame <= self.frame_in:
                        self.move_marker(marker)
                elif self.move_type == 'AFTER':
                    if marker.frame >= self.frame_in:
                        self.move_marker(marker)
                elif self.move_type == 'BETWEEN':
                    if marker.frame >= self.frame_in and marker.frame <= self.frame_out:
                        self.move_marker(marker)

        if self.wm.move_sounds:
            self.move_sound_sequences_in_file(self.context)

    def check_keys(self):

        problem = False
        key_list = bpy.context.window_manager.key_list
        key_list.clear()
        self.add_key_list_item("Object", "Curve", "Frame")
        for ob in bpy.data.objects:
            if (ob.animation_data and ob.animation_data.action and ob.animation_data.action.fcurves):
                for fCurve in ob.animation_data.action.fcurves:
                    for key in fCurve.keyframe_points:
                        if self.move_type == 'BEFORE':
                            if self.move_direction == 'FORWARD':
                                if key.co[0] > self.frame_in and key.co[0] <= self.frame_in + self.frame_amount:
                                    problem = True
                                    self.add_key_list_item(ob.name, fCurve.data_path + ': ' + str(fCurve.array_index), str(key.co[0]))
                                    
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
                                    self.add_key_list_item(ob.name, fCurve.data_path + ': ' + str(fCurve.array_index), str(key.co[0]))                                    
                                    
                                    print(ob.name +': ' + fCurve.data_path + ' ' +  str(fCurve.array_index) + ' Frame: ' + str(key.co[0]))

                        if self.move_type == 'BETWEEN':
                            if self.move_direction == 'FORWARD':
                                if key.co[0] > self.frame_out and key.co[0] <= self.frame_out + self.frame_amount:
                                    problem = True
                                    self.add_key_list_item(ob.name, fCurve.data_path + ': ' + str(fCurve.array_index), str(key.co[0]))                                    
                                    
                                    print(ob.name +': ' + fCurve.data_path + ' ' +  str(fCurve.array_index) + ' Frame: ' + str(key.co[0]))
                            if self.move_direction == 'BACKWARD':
                                if key.co[0] < self.frame_in and key.co[0] >= self.frame_in - self.frame_amount:
                                    problem = True
                                    self.add_key_list_item(ob.name, fCurve.data_path + ': ' + str(fCurve.array_index), str(key.co[0]))                                    
                                    
                                    print(ob.name +': ' + fCurve.data_path + ' ' +  str(fCurve.array_index) + ' Frame: ' + str(key.co[0]))
        
        return problem

    def add_key_list_item(self, ob, crv, frame):
        key_list = bpy.context.window_manager.key_list
        item = key_list.add()
        item.object = ob
        item.curve = crv
        item.frame = frame

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

    def move_sound_sequences_in_file(self, context):
        for sound_sequence in context.scene.sequence_editor.sequences_all:
            if self.move_type == 'BEFORE':
                if sound_sequence.frame_start <= self.frame_in and sound_sequence.frame_final_end >= self.frame_in:
                    print("IN BETWEEN")
                    pass
                    # Save strip, track and ob to later give ui feedback that it could not be moved
                elif sound_sequence.frame_final_end <= self.frame_in:
                    self.move_sound_sqeuence(sound_sequence)

            elif self.move_type == 'AFTER':
                if sound_sequence.frame_start <= self.frame_in and sound_sequence.frame_final_end >= self.frame_in:
                    print("IN BETWEEN")
                    pass
                    # Save strip, track and ob to later give ui feedback that it could not be moved
                elif sound_sequence.frame_start >= self.frame_in:
                    self.move_sound_sqeuence(sound_sequence)

            elif self.move_type == 'BETWEEN':
                if sound_sequence.frame_start >= self.frame_in and sound_sequence.frame_start <= self.frame_out and sound_sequence.frame_final_end >= self.frame_in and sound_sequence.frame_final_end <= self.frame_out:
                    self.move_sound_sqeuence(sound_sequence)
                elif (sound_sequence.frame_start <= self.frame_in and sound_sequence.frame_final_end >= self.frame_in) or (sound_sequence.frame_final_end >= self.frame_out and sound_sequence.frame_start <= self.frame_out):
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

    def move_sound_sqeuence(self, sound_sequence):
        if self.move_direction == 'FORWARD':
            #sound_sequence.frame_final_end = sound_sequence.frame_final_end + self.frame_amount
            sound_sequence.frame_start = sound_sequence.frame_start + self.frame_amount
            
        if self.move_direction == 'BACKWARD':
            sound_sequence.frame_start = sound_sequence.frame_start - self.frame_amount
            #sound_sequence.frame_final_end = sound_sequence.frame_final_end - self.frame_amount