import json
import os


class Settings(object):
    """A Singleton class which stores all the custom settings for the FCHAR MoCap retarget AddOn and keeps them synced with a json."""
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
        """Loads the Settings. If no settings JSON is found, uses the default settings and writes them to disk as JSON."""
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
        """Writes the SettingsDict to disk as JSON"""
        
        try:
            with open(self._settings_path, 'w') as f:
                data_out = json.dump(self._settings, f, indent=4, sort_keys=True)
                
        except Exception:
            pass

    def get_setting(self, key):
        """Gets a Setting from the Dict. If the Setting is not in the Dict, it tries to find it in the default settings.
        If it is not in either retuns None."""
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
        """Sets a Setting in the dict and updates the Json afterwards."""
        self._settings[key] = value
        self._write_settings()