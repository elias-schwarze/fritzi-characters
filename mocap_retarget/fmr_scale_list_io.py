import json
import os

class ScaleListDict(object):
    _instance = None
    _scale_list_path = os.path.join(os.path.dirname(__file__), "fmr_scale_list.json")
    _scale_list = {}
    _default_scale_list = {}
    _wm = None

    def __new__(cls, window_manager):
        """Singleton initialization"""
        if cls._instance is None:
            cls._instance = super(ScaleListDict, cls).__new__(cls)
            cls._instance._wm = window_manager
            cls._instance._load_scale_list()
        return cls._instance

    def _load_scale_list(self):

        try:
            if os.path.isfile(self._settings_path):
                f = open(self._scale_list_path, 'r')
                self._scale_list = json.load(f)
                f.close()

                #push scales to properties here
                
            else:
                self._scale_list = self._default_scale_list
                self._write_scale_list()
        
        except Exception:
            pass



    def _write_scale_list(self):

        try:
            with open(self._scale_list_path, 'w') as f:
                data_out = json.dump(self._scale_list, f, indent=4, sort_keys=True)
                f.write(data_out)
        except Exception:
            pass

    def _update_property(self, key, value):
        length = len(self._wm.scale_list)
        if length > 0:
            for i in range(length):
                #probably not needed
                return


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
        self._write_settings()