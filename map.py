from config import *
from Hex import Hex
import json

class Map:

    def __init__(self):
        self.hash_map={}

    def __setitem__(self, key, value):
        if(type(key) is Hex):
            self.hash_map[key.get_position_tuple()]=value
        else:
            self.hash_map[key]=value
    
    def __getitem__(self, key) -> Hex:
        if(type(key) is Hex):
            return self.hash_map[key.get_position_tuple()]
        return self.hash_map[key]
    
    def serializable(self):
        return self.serializable_partial(self.hash_map.keys())

    def serializable_partial(self, keys):
        d = []
        for k in keys:
            i = self.hash_map[k]
            d.append((k, i.get_point_type(),
                     i.get_owner_ID(), i.get_current_value()))
        return d
