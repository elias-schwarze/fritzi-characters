import json
import os


class Settings(object):

    _instance = None
    settings_path = os.path.join(
                os.path.dirname(__file__),
                "fmr_settings.json")
    settings = {}

    def __new__(cls):
        """Singleton initialization"""
        if cls._instance is None:
            print('Creating the object')
            cls._instance = super(Settings, cls).__new__(cls)
            cls._instance._load_settings()
        return cls._instance

    def _load_settings(self):

        try:

            f = open(self.settings_path, 'r')
            self.settings = json.load(f)
        except Exception:
            pass
        finally:
            f.close()


    def _write_settings(self):
        
        try:
            with open(self.settings_path, 'w') as f:
                json.dump(self.settings, f, indent=4, sort_keys=True)
        except Exception:
            pass
        finally:
            f.close()

    def get_setting(self, key):
        return self.settings[key]

    def set_setting(self, key, value):
        self.settings[key] = value
        self._write_settings()