from config import *
from Hex import Hex


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
    
    
    
