import json
import os
import bpy

class ScaleListDict(object):
    """A Singleton class which stores all the custom scalings for characters and keeps them synced with a json."""
    _instance = None
    _scale_list_path = os.path.join(os.path.dirname(__file__), "fmr_scale_list.json")
    _scale_list = {}
    _default_scale_list = {
        "hanno" : 0.52,
        "sophie" : 0.86
    }
    _wm = None
    loading = True

    def __new__(cls):
        """Singleton initialization"""
        if cls._instance is None:
            cls._instance = super(ScaleListDict, cls).__new__(cls)
            if not cls._instance._wm:
                cls._instance._wm = bpy.context.window_manager
            #cls._instance._wm = window_manager
            #cls._instance.initializin = True
            cls._instance.load_scale_list(cls._instance._scale_list_path)
            #cls._instance.initializin = False
        
        if not cls._instance._wm:
            cls._instance._wm = bpy.context.window_manager
        
        return cls._instance

    def load_scale_list(self, path):
        """Loads the Scale List JSON and pushes it to the UI.
        Sets the loading flag, so UI updates do not trigger infinite recursion.
        If no Scale List JSON is found, the default scale list gets used and written to disk."""
        self.loading = True
        try:
            if os.path.isfile(path):
                f = open(path, 'r')
                self._scale_list = json.load(f)
                f.close()
                if not self._scale_list:
                    self._scale_list = self._default_scale_list
                    self.write_scale_list(self._scale_list_path)

            else:
                self._scale_list = self._default_scale_list
                self.write_scale_list(self._scale_list_path)

            
            
        
        except Exception:
            self._scale_list = self._default_scale_list
            self.write_scale_list(self._scale_list_path)
            
        finally:
            self.push_to_properties()
            self.loading = False



    def write_scale_list(self, path):
        """ Writes the Scale List to disk as JSON."""
        # print("writing")
        try:
            with open(path, 'w') as f:
                data_out = json.dump(self._scale_list, f, indent=4, sort_keys=True)
                
                # print("written")
        except Exception as e:
            print("exception")
            print(e)
            pass

    

    def push_to_properties(self):
        """ Pushes all scales and character Names to the UI. Sets the Loading flag while doing it, so UI Updates do not cause infinite recursion."""
        self.loading = True
        scale_list_prop = bpy.context.window_manager.scale_list
        scale_list_prop.clear()
        for key in self._scale_list:
            item = scale_list_prop.add()
            item.name = key
            item.character = key
            item.scale = self._scale_list[key]
        
        for area in bpy.context.screen.areas:
            area.tag_redraw()
        self.loading = False


    def get_scale(self, key):
        """Returns the scale of a given character. If the Character is not in the scale list dict, searches for it in the default values.
        If it is not in there either, returns None"""
        
        if key in self._scale_list:
            return self._scale_list[key]
        else:
            if key in self._default_scale_list:
                self._scale_list[key] = self._default_scale_list[key]
                self.write_scale_list(self._scale_list_path)
                return self._scale_list[key]
            else:
                return None

    def set_scale(self, key, value):
        """Sets a scale in the scale List Dict."""
        if not self.loading:
            key = key.lower()
            self._scale_list[key] = value
        
            self.push_to_properties()
            self.write_scale_list(self._scale_list_path)

    def remove_scale(self, key):
        """Removes a Character Scaling from the scale list dict if it exists."""
        if key in self._scale_list:
            del self._scale_list[key]

            if not self.loading:
                self.push_to_properties()
            self.write_scale_list(self._scale_list_path)



    def fetch_properties(self):
        """ Gets the Scale List Properties from the UI and puts them in the scale list dict, if the Loading flag is not set.
        Whis prevents infinite recursion, since the update methods in the ui also get triggered on API calls."""
        if not self.loading:
            self._scale_list.clear()
            scale_props = bpy.context.window_manager.scale_list
            length = len(scale_props)
            if length > 0:
                for i in range(length):
                    self._scale_list[scale_props[i].character.lower()] = scale_props[i].scale
            self.write_scale_list(self._scale_list_path)
            self.push_to_properties()
