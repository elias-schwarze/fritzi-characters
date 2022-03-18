import json
import os
import bpy

class ScaleListDict(object):
    _instance = None
    _scale_list_path = os.path.join(os.path.dirname(__file__), "fmr_scale_list.json")
    _scale_list = {}
    _default_scale_list = {
        "Fritzi" : 0.4,
        "Hanno" : 0.3,
        "Kai" : 0.35
    }
    _wm = None
    loading = True

    def __new__(cls, window_manager):
        """Singleton initialization"""
        if cls._instance is None:
            cls._instance = super(ScaleListDict, cls).__new__(cls)
            cls._instance._wm = window_manager
            #cls._instance.initializin = True
            cls._instance._load_scale_list(cls._instance._scale_list_path)
            #cls._instance.initializin = False
        return cls._instance

    def _load_scale_list(self, path):
        self.loading = True
        try:
            if os.path.isfile(path):
                f = open(path, 'r')
                self._scale_list = json.load(f)
                f.close()


            else:
                self._scale_list = self._default_scale_list
                self._write_scale_list()

            self._push_to_properties()
            
        
        except Exception:
            
            pass
        finally:
            self.loading = False



    def _write_scale_list(self):
        print("writing")
        try:
            with open(self._scale_list_path, 'w') as f:
                data_out = json.dump(self._scale_list, f, indent=4, sort_keys=True)
                #f.write(data_out)
                print("written")
        except Exception as e:
            print("exception")
            print(e)
            pass

    def _update_property(self, key, value):
        length = len(self._wm.scale_list)
        if length > 0:
            for i in range(length):
                #probably not needed
                return

    def _push_to_properties(self):
        self.loading = True
        scale_list_prop = self._wm.scale_list
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
        if key in self._scale_list:
            return self._scale_list[key]
        else:
            if key in self._default_scale_list:
                self._scale_list[key] = self._default_scale_list[key]
                self._write_scale_list()
                return self._scale_list[key]
            else:
                return None

    def set_scale(self, key, value):
        self._scale_list[key] = value
        if not self.loading:
           self._push_to_properties()
        self._write_scale_list()

    def remove_scale(self, key):
        if key in self._scale_list:
            del self._scale_list[key]

            if not self.loading:
                self._push_to_properties()
            self._write_scale_list()


    def change_key(self, key, new_key):
        return

    def fetch_properties(self):
        print(self.loading)
        if not self.loading:
            self._scale_list.clear()
            scale_props = self._wm.scale_list
            length = len(scale_props)
            if length > 0:
                for i in range(length):
                    self._scale_list[scale_props[i].character] = scale_props[i].scale
            self._write_scale_list()
