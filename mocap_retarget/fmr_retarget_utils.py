import bpy
import json
import os

settings_path = os.path.join(
            os.path.dirname(__file__),
            "fmr_settings.json")
settings = {}


def load_settings():
    
    try:
        
        f = open(settings_path, 'r')
        settings = json.load(f)
    except Exception:
        pass
    finally:
        f.close()
        

def write_settings( new_settings):
    settings = new_settings
    try:
        with open(settings_path, 'w') as f:
            json.dump(settings, f, indent=4, sort_keys=True)
    except Exception:
        pass
    finally:
        f.close()

def get_settings():
    return settings