
import bpy

def start(elem):
        return elem.frame_start

class Anim_Mover():

    move_type: None
    move_direction: None
    frame_in: None
    frame_out: None
    frame_amount: None
    wm: None
    context: None
    min_key_frame: int
    max_key_frame: int


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
            # print(ob.name)
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

    def get_min_max_key_frames(self):
        self.min_key_frame = 10000000
        self.max_key_frame = -10000000

        for ob in bpy.data.objects:
            if (ob.animation_data and ob.animation_data.action and ob.animation_data.action.fcurves):
                
                for fCurve in ob.animation_data.action.fcurves:
                    for key in fCurve.keyframe_points:
                        if self.is_key_in_range(key): 
                            if self.min_key_frame is None:
                                
                                self.min_key_frame = key.co[0]
                                self.max_key_frame = key.co[0]

                            elif key.co[0] < self.min_key_frame:
                                self.min_key_frame = key.co[0]

                            elif key.co[0] > self.max_key_frame:
                                self.max_key_frame = key.co[0]
                        
                        
    def is_key_in_range(self, key):
        
        if self.move_type == 'BEFORE':
            if key.co[0] <= self.frame_in:
                return True
            
        if self.move_type == 'AFTER':
            if key.co[0] >= self.frame_in:
                return True
            
        if self.move_type == 'BETWEEN':
            if key.co[0] >= self.frame_in and key.co[0] <= self.frame_out:
                return True
        
        return False
    def get_fCurve_min_max_Frame_in_Range(self, fCurve):
        min_frame = 100000000
        max_frame = -100000000
        for key in fCurve.keyframe_points:
            if self.is_key_in_range(key):
                if key.co[0] < min_frame:
                    min_frame = key.co[0]
                if key.co[0] > max_frame:
                    max_frame = key.co[0]
        return min_frame, max_frame
        

    def check_keys(self):



        problem = False
        key_list = bpy.context.window_manager.key_list
        key_list.clear()
        self.add_key_list_item("Object", "Curve", "Frame")
        for ob in bpy.data.objects:
            if (ob.animation_data and ob.animation_data.action and ob.animation_data.action.fcurves):
                for fCurve in ob.animation_data.action.fcurves:
                    min_frame, max_frame = self.get_fCurve_min_max_Frame_in_Range(fCurve)
                    # print(ob.animation_data.action.name + ", " + ob.name)
                    for key in fCurve.keyframe_points:
                        if self.move_type == 'BEFORE':
                            if self.move_direction == 'FORWARD':
                                if key.co[0] > self.frame_in and key.co[0] <= max_frame + self.frame_amount:
                                    problem = True
                                    self.add_key_list_item(ob.name, fCurve.data_path + ': ' + str(fCurve.array_index), str(key.co[0]))
                                    
                                    # print(ob.name +': ' + fCurve.data_path + ' ' +  str(fCurve.array_index) + ' Frame: ' + str(key.co[0]))
                            if self.move_direction == 'BACKWARD':
                                pass
                                #this can not have problematic keys
                        
                        if self.move_type == 'AFTER':
                            if self.move_direction == 'FORWARD':
                                pass
                                #this can not have problematic keys
                            if self.move_direction == 'BACKWARD':
                                if key.co[0] < self.frame_in and key.co[0] >= min_frame - self.frame_amount:
                                    problem = True
                                    self.add_key_list_item(ob.name, fCurve.data_path + ': ' + str(fCurve.array_index), str(key.co[0]))                                    
                                    
                                    # print(ob.name +': ' + fCurve.data_path + ' ' +  str(fCurve.array_index) + ' Frame: ' + str(key.co[0]))

                        if self.move_type == 'BETWEEN':
                            if self.move_direction == 'FORWARD':
                                if key.co[0] > self.frame_out and key.co[0] <= max_frame + self.frame_amount:
                                    problem = True
                                    self.add_key_list_item(ob.name, fCurve.data_path + ': ' + str(fCurve.array_index), str(key.co[0]))                                    
                                    
                                    # print(ob.name +': ' + fCurve.data_path + ' ' +  str(fCurve.array_index) + ' Frame: ' + str(key.co[0]))
                            if self.move_direction == 'BACKWARD':
                                if key.co[0] < self.frame_in and key.co[0] >= min_frame - self.frame_amount:
                                    problem = True
                                    self.add_key_list_item(ob.name, fCurve.data_path + ': ' + str(fCurve.array_index), str(key.co[0]))                                    
                                    
                                    # print(ob.name +': ' + fCurve.data_path + ' ' +  str(fCurve.array_index) + ' Frame: ' + str(key.co[0]))
        
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
                    # print(fCurve.data_path)
                    # print(fCurve.array_index)
                    for key in fCurve.keyframe_points:
                        # print(ob.name +': ' + fCurve.data_path + ' ' +  str(fCurve.array_index) + ' Frame: ' + str(key.co[0]))
                        if self.move_type == 'BEFORE':
                            if key.co[0] <= self.frame_in:
                                self.move_key(key)
                        elif self.move_type == 'AFTER':
                            if key.co[0] >= self.frame_in:
                                self.move_key(key)
                        elif self.move_type == 'BETWEEN':
                            if key.co[0] >= self.frame_in and key.co[0]<=self.frame_out:
                                self.move_key(key)

                        # print(key.co)
                        #key.co[0] = key.co[0] + 10

    def add_intermediate_keys_on_object(self, ob):
        if (ob.animation_data and ob.animation_data.action and ob.animation_data.action.fcurves):
            for fCurve in ob.animation_data.action.fcurves:

                if self.move_type == 'AFTER' and self.move_direction == 'BACKWARD':
                    frame = self.frame_in
                    value = fCurve.evaluate(frame)
                    key_right = fCurve.keyframe_points.insert(frame, value)
                    key_right.handle_left_type = 'FREE'
                    key_right.handle_right_type = 'FREE'
                    


                    frame = self.frame_in - self.frame_amount - 1
                    value = fCurve.evaluate(frame)
                    key_left = fCurve.keyframe_points.insert(frame, value)
                    key_left.handle_right_type = 'FREE'
                    key_left.handle_left_type = 'FREE'
                    

    def delete_keys_in_move_range_on_object(self, ob):
        if (ob.animation_data and ob.animation_data.action and ob.animation_data.action.fcurves):
            for fCurve in ob.animation_data.action.fcurves:
                for key in fCurve.keyframe_points:
                    if self.is_key_in_move_range(key):
                        fCurve.keyframe_points.remove(key)


    def is_key_in_move_range(self, key):

        if self.move_type == 'AFTER' and self.move_direction == 'BACKWARD':
            if key.co[0] < self.frame_in and key.co[0] >= self.frame_in - self.frame_amount:
                return True
        else:
            return False
        
    def split_move_nla_strips_on_object(self, ob):
        if (ob.animation_data and ob.animation_data.nla_tracks):
            tracks = ob.animation_data.nla_tracks
            strips_to_splitmove = []
            strips_to_move = []
            for track in ob.animation_data.nla_tracks:
                strips_to_remove = []
                strips_to_clip_start = []
                strips_to_clip_end = []
                
                move_start_frame = self.frame_in
                move_dest_frame = self.frame_in - self.frame_amount
                for strip in sorted(track.strips, key=start, reverse=True):
                    if self.move_type == 'AFTER' and self.move_direction == 'BACKWARD':
                        move_start_frame = self.frame_in
                        move_dest_frame = self.frame_in - self.frame_amount


                        #Strips that are completely in the move range
                        if strip.frame_start < move_start_frame and strip.frame_start >= move_dest_frame and strip.frame_end <= move_start_frame and strip.frame_end > move_dest_frame:
                            strips_to_remove.append(strip)
                            

                        #Strips that begin before the move range and end in the move range
                        elif strip.frame_start < move_dest_frame and strip.frame_end > move_dest_frame and strip.frame_end <= move_start_frame:
                            strips_to_clip_end.append(strip)
                            

                        #Strips that begin in the move range and end after the move range
                        elif strip.frame_start >= move_dest_frame and strip.frame_start < move_start_frame and strip.frame_end > move_start_frame:
                            strips_to_clip_start.append(strip)
                            

                        #Strips that begin before the move range and end after the move range
                        elif strip.frame_start < move_dest_frame and strip.frame_end > move_start_frame:
                            strips_to_splitmove.append((strip, track))

                        #Strips that are fully outside the move range
                        elif strip.frame_start >= move_start_frame:
                            scale = strip.scale
            
                            strip.frame_end = strip.frame_end + 100000
                            strip.frame_start = strip.frame_start + 100000
                            strip.scale = scale
                            pass
                
                for strip in strips_to_remove:
                    track.strips.remove(strip)

                for strip in strips_to_clip_end:
                    strip.frame_end = move_dest_frame

                for strip in strips_to_clip_start:
                    start_overlap = move_start_frame - strip.frame_start
                    strip.frame_start = move_dest_frame
                    strip.action_frame_start = strip.action_frame_start + start_overlap
            
            

            for item in strips_to_splitmove:
                strip = item[0]
                track = item[1]
                start_overlap = move_start_frame - strip.frame_start
                end_overlap = strip.frame_end - move_dest_frame
                #new_track = tracks.new()
                #strip.frame_end = move_dest_frame
                scale = strip.scale
                strip.action_frame_end = strip.action_frame_end - end_overlap
                #strip.scale = scale
                new_strip = track.strips.new(strip.name + "copy", (int)(move_dest_frame), strip.action)
                #new_strip.frame_start = move_dest_frame
                #new_strip.frame_end = move_start_frame
                new_strip.action_frame_start = strip.action_frame_start + start_overlap
                new_strip.blend_type = strip.blend_type
                new_strip.extrapolation = strip.extrapolation
                new_strip.influence = strip.influence
                new_strip.mute = strip.mute

                
                
                print(new_strip.frame_start)
                print(new_strip.action_frame_start)

            for track in tracks:
                for strip in sorted(track.strips, key=start):
                    if strip.frame_start >= move_start_frame:
                        scale = strip.scale
        
            
                        
                        strip.frame_start = strip.frame_start - self.frame_amount - 100000
                        strip.frame_end = strip.frame_end - self.frame_amount - 100000

                        strip.scale = scale

             
        
                        
    def split_strips_on_object(self, ob, frame):
        if (ob.animation_data and ob.animation_data.nla_tracks):
            win = bpy.context.window
            scr = win.screen
            area = [area for area in scr.areas if area.type == 'NLA_EDITOR'][0]
            region = area.regions[0]
            override = {
                'window': win,
                'screen': scr,
                'area'  : area,
                'region': region,
                'scene' : bpy.context.scene
            }
            bpy.ops.nla.select_all(override, action='DESELECT')
            tracks = ob.animation_data.nla_tracks
            strips_to_split = []

            for track in tracks:
                for strip in track.strips:

                    if strip.frame_start < frame and strip.frame_end > frame:
                        strips_to_split.append(strip)
                        strip.select = True
                    else: 
                        strip.select = False
            
            bpy.context.scene.frame_set(frame)
            win = bpy.context.window
            scr = win.screen
            area = [area for area in scr.areas if area.type == 'NLA_EDITOR'][0]
            region = area.regions[0]
            override = {
                'window': win,
                'screen': scr,
                'area'  : area,
                'region': region,
                'scene' : bpy.context.scene
            }
            if strips_to_split:
                bpy.ops.nla.split(override)
            for strip in strips_to_split:
                strip.select = False
            bpy.ops.nla.select_all(override, action='DESELECT')

    def delete_strips_in_move_range(self, ob):
        if (ob.animation_data and ob.animation_data.nla_tracks):
            tracks = ob.animation_data.nla_tracks
            move_start_frame = self.frame_in
            move_dest_frame = self.frame_in - self.frame_amount

            for track in tracks:
                strips_to_remove = []
                
                
                for strip in track.strips:
                    if self.move_type == 'AFTER' and self.move_direction == 'BACKWARD':
                        
                        move_start_frame = self.frame_in
                        move_dest_frame = self.frame_in - self.frame_amount


                        #Strips that are completely in the move range
                        if strip.frame_start < move_start_frame and strip.frame_start >= move_dest_frame and strip.frame_end <= move_start_frame and strip.frame_end > move_dest_frame:
                            strips_to_remove.append(strip)
            
                for strip in strips_to_remove:
                        track.strips.remove(strip)



    def add_NLA_strip_list_item(self, ob, track, strip):
        
        NLA_strip_list = bpy.context.window_manager.NLA_strip_list
        item = NLA_strip_list.add()
        item.object = ob.name
        item.track = track.name
        item.strip = strip.name

    def move_NLA_strips_on_object(self, ob):
        
        if (ob.animation_data and ob.animation_data.nla_tracks):
                for track in ob.animation_data.nla_tracks:
                    for strip in self.sort_track(track):
                        
                        if self.move_type == 'BEFORE':
                            if strip.frame_start <= self.frame_in and strip.frame_end >= self.frame_in:
                                self.add_NLA_strip_list_item(ob, track, strip)
                                
                                pass
                                # Save strip, track and ob to later give ui feedback that it could not be moved
                            elif strip.frame_end <= self.frame_in:
                                self.move_strip(strip)

                        elif self.move_type == 'AFTER':
                            if strip.frame_start < self.frame_in and strip.frame_end >= self.frame_in:
                                self.add_NLA_strip_list_item(ob, track, strip)
                               
                                pass
                                # Save strip, track and ob to later give ui feedback that it could not be moved
                            elif strip.frame_start >= self.frame_in:
                                self.move_strip(strip)

                        elif self.move_type == 'BETWEEN':
                            if strip.frame_start >= self.frame_in and strip.frame_start <= self.frame_out and strip.frame_end >= self.frame_in and strip.frame_end <= self.frame_out:
                                self.move_strip(strip)
                            elif (strip.frame_start <= self.frame_in and strip.frame_end >= self.frame_in) or (strip.frame_end >= self.frame_out and strip.frame_start <= self.frame_out):
                                
                                self.add_NLA_strip_list_item(ob, track, strip)
                                pass
                                #Save strip, track and ob to later give UI feedback why it could not be moved
    
    def sort_track(self, track):
        
        if self.move_direction == 'FORWARD':
            strips = sorted(track.strips, key=start, reverse=True)
        else :
            strips = sorted(track.strips, key=start)
        
        return strips

    def add_sound_strip_list_item(self, strip):
        Sound_strip_list = bpy.context.window_manager.Sound_strip_list
        item = Sound_strip_list.add()
        
        item.track = str(strip.channel)
        item.strip = strip.name

    def move_sound_sequences_in_file(self, context):
       
        for sound_sequence in context.scene.sequence_editor.sequences_all:
            
            if self.move_type == 'BEFORE':
                if sound_sequence.frame_final_start <= self.frame_in and sound_sequence.frame_final_end >= self.frame_in:

                    # print("IN BETWEEN")
                    self.add_sound_strip_list_item(sound_sequence)
                    pass
                    # Save strip, track and ob to later give ui feedback that it could not be moved
                elif sound_sequence.frame_final_end <= self.frame_in:
                    self.move_sound_sqeuence(sound_sequence)

            elif self.move_type == 'AFTER':
                if sound_sequence.frame_final_start <= self.frame_in and sound_sequence.frame_final_end >= self.frame_in:
                    
                    self.add_sound_strip_list_item(sound_sequence)
                    pass
                    # Save strip, track and ob to later give ui feedback that it could not be moved
                elif sound_sequence.frame_final_start >= self.frame_in:
                    self.move_sound_sqeuence(sound_sequence)

            elif self.move_type == 'BETWEEN':
                if sound_sequence.frame_final_start >= self.frame_in and sound_sequence.frame_final_start <= self.frame_out and sound_sequence.frame_final_end >= self.frame_in and sound_sequence.frame_final_end <= self.frame_out:
                    self.move_sound_sqeuence(sound_sequence)
                elif (sound_sequence.frame_final_start <= self.frame_in and sound_sequence.frame_final_end >= self.frame_in) or (sound_sequence.frame_final_end >= self.frame_out and sound_sequence.frame_final_start <= self.frame_out):
                    # print("IN BETWEEN")
                    
                    pass
                    #Save strip, track and ob to later give UI feedback why it could not be moved

    def move_key(self, key):
        if self.move_direction == 'FORWARD':
            key.co[0] = key.co[0] + self.frame_amount
            key.handle_left[0] += self.frame_amount
            key.handle_right[0] += self.frame_amount
        elif self.move_direction =='BACKWARD':
            key.co[0] = key.co[0] - self.frame_amount
            key.handle_left[0] -= self.frame_amount
            key.handle_right[0] -= self.frame_amount

    def move_marker(self, marker):
        if self.move_direction == 'FORWARD':
            marker.frame = marker.frame + self.frame_amount
        elif self.move_direction == 'BACKWARD':
            marker.frame = marker.frame - self.frame_amount

    def remove_inbetween_markers(self):
        for marker in self.context.scene.timeline_markers:
            if self.move_type == 'AFTER' and self.move_direction == 'BACKWARD':
                if marker.frame < self.frame_in and marker.frame > self.frame_in - self.frame_amount:
                    self.context.scene.timeline_markers.remove(marker)

    def move_strip(self, strip):
        scale = strip.scale
        if self.move_direction == 'FORWARD':
            strip.frame_end = strip.frame_end + self.frame_amount
            strip.frame_start = strip.frame_start + self.frame_amount
            
        if self.move_direction == 'BACKWARD':
            strip.frame_start = strip.frame_start - self.frame_amount
            strip.frame_end = strip.frame_end - self.frame_amount

        strip.scale = scale

    def move_sound_sqeuence(self, sound_sequence):
        
        if sound_sequence.parent_meta():
            return

        if sound_sequence.type in {'SPEED', 'ADD', 'ALPHA_OVER', 'ALPHA_UNDER', 'SUBTRACT', 
                                    'Cross', 'GAMMA_CROSS', 'MULTIPLY', 'OVER_DROP',
                                    'WIPE', 'GLOW', 'TRANSFORM', 'COLOR', 'MULTICAM',
                                    'ADJUSTMENT', 'GAUSSIAN_BLUR', 'TEXT', 'COLORMIX'}:
            return

        if self.move_direction == 'FORWARD':
            #sound_sequence.frame_final_end = sound_sequence.frame_final_end + self.frame_amount
            sound_sequence.frame_start = sound_sequence.frame_start + self.frame_amount
            
        if self.move_direction == 'BACKWARD':
            sound_sequence.frame_start = sound_sequence.frame_start - self.frame_amount
            #sound_sequence.frame_final_end = sound_sequence.frame_final_end - self.frame_amount