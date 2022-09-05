import random
import os
from hex_types import HEX_Type

class Bot():
    def __init__(self):
        self.player_id=None
        self.map=None
        self.player_name=os.environ.get("name")
        if(self.player_name==None):
            self.player_name="UnknownBot"
    
    def find_my_land(self):
        if self.map == None:
            return []
        lands = []
        for tile in self.map.hash_map.values():
            if tile.get_owner_ID() == self.player_id:
                lands.append(tile)
        return lands

    def tick(self, data):
        self.map = data["map"]
        self.player_id = data["ID"]
        myland = self.find_my_land()
        assert len(myland) != 0
        tries = 0
        while tries < 100:
            startpos = random.choice(myland)
            candidate_end = random.choice(self.map[startpos].get_neighbors())
            if self.map[candidate_end].get_point_type() != HEX_Type.WALL and self.map[startpos].get_current_value()>1:
                return (self.map[startpos].get_position_tuple(), self.map[candidate_end].get_position_tuple())
            tries += 1
        return ((0,0,0), (0,0,0))
    
    def get_player_name(self):
        return self.player_name