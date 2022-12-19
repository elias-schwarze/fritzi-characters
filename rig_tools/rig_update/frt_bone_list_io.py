import json
import os
import bpy
from . import bone_list

class BoneList(object):

    _bone_list_path = os.path.join(os.path.dirname(__file__), "frt_bone_list.json")
    _bone_list = {}
    _default_bone_list = bone_list.bone_list


    def __init__(self):
        self.load_list(self._bone_list_path)

    def load_list(self, path):
        try:
            if os.path.isfile(path):
                f = open(path, 'r')
                self._bone_list = json.load(f)
                f.close()
                if not self._bone_list:
                    self._bone_list = self._default_bone_list
                    self.write_list(self._bone_list_path)
            else:
                self._bone_list = self._default_bone_list
                self.write_list(self._bone_list_path)

        except:
            self._bone_list = self._default_bone_list
            self.write_list(self._bone_list_path)

        return

    def write_list(self, path):
        try:
            with open(path, 'w') as f:
                data_out = json.dump(self._bone_list, f, indent=4, sort_keys=False)
        
        except Exception as e:
            print("exception")
            print(e)
            pass

        return

    def get_bone_list(self):
        if "bone_list" in self._bone_list:
            return self._bone_list["bone_list"]
        
        else:
            self._bone_list["bone_list"] = self._default_bone_list["bone_list"]
            self.write_list(self._bone_list_path)
            return self._bone_list["bone_list"]

    def get_constraint_update_list(self):
        if "constraint_update_list" in self._bone_list:
            return self._bone_list["constraint_update_list"]
        
        else:
            self._bone_list["constraint_update_list"] = self._default_bone_list["constraint_update_list"]
            self.write_list(self._bone_list_path)
            return self._bone_list["constraint_update_list"]

    def get_constraint_add_list(self):
        if "constraint_add_list" in self._bone_list:
            return self._bone_list["constraint_add_list"]
        
        else:
            self._bone_list["constraint_add_list"] = self._default_bone_list["constraint_add_list"]
            self.write_list(self._bone_list_path)
            return self._bone_list["constraint_add_list"]