import json
import os


class Settings(object):

    _instance = None
    _settings_path = os.path.join(
                os.path.dirname(__file__),
                "fmr_settings.json")
    _settings = {}
    _default_settings = {
        "bone_map_path" : os.path.join(os.path.join(os.path.dirname(__file__),"BoneMap"),"IKlegFKarm.bmap"),
        "perforce_path" : ""
    }
    def __new__(cls):
        """Singleton initialization"""
        if cls._instance is None:
            print('Creating the object')
            cls._instance = super(Settings, cls).__new__(cls)
            cls._instance._load_settings()
        return cls._instance

    def _load_settings(self):

        try:
            if os.path.isfile(self._settings_path):
                f = open(self._settings_path, 'r')
                self._settings = json.load(f)
                f.close()
            else:
                
                self._settings = self._default_settings
                self._write_settings()

        except Exception:
            pass
            


    def _write_settings(self):
        
        try:
            with open(self._settings_path, 'w') as f:
                data_out = json.dump(self._settings, f, indent=4, sort_keys=True)
                f.write(data_out)
        except Exception:
            pass

    def get_setting(self, key):
        if key in self._settings:
           return self._settings[key]
        else:
            if key in self._default_settings:
                self._settings[key] = self._default_settings[key]
                self._write_settings()
                return self._settings[key]
            else:
                return None

    def set_setting(self, key, value):
        self._settings[key] = value
        self._write_settings()