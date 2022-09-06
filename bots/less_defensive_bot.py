import json
import random
import os
from hex_types import HEX_Type

DEBUG = False

class Bot():
    def __init__(self):
        self.player_id=None
        self.map=None
        self.player_name=os.environ.get("name")
        self.last_cell_from_attack = None
        if(self.player_name==None):
            self.player_name="UnknownBot"
        # self.flag = None
    
    def find_my_land(self):
        if self.map == None:
            return []
        lands = []
        for tile in self.map.hash_map.values():
            if tile.get_owner_ID() == self.player_id:
                lands.append(tile)
                # if tile.get_point_type == HEX_Type.FLAG:
                #     self.flag = tile
        return lands

    def tick(self, data):
        self.map = data["map"]
        self.player_id = data["ID"]
        # if self.player_id > 0:
        #     return ((0,0,0), (0,0,0))

        myland = self.find_my_land()
        assert len(myland) != 0
        # tries = 0
        # while tries < 100:
        #     startpos = random.choice(myland)
        #     candidate_end = random.choice(self.map[startpos].get_neighbors())
        #     if self.map[candidate_end].get_point_type() != HEX_Type.WALL and self.map[startpos].get_current_value()>1:
        #         return (self.map[startpos].get_position_tuple(), self.map[candidate_end].get_position_tuple())
        #     tries += 1

        target = None

        # Try to attack, if possible
        for startpos in myland:
            alternative = None
            for candidate_end in self.map[startpos].get_neighbors():
                if (self.map[candidate_end].get_point_type() != HEX_Type.WALL and
                self.map[candidate_end].get_owner_ID() != None and
                self.map[candidate_end].get_owner_ID() != self.player_id):
                    if target == None:
                        target = candidate_end
                    if self.map[candidate_end].get_point_type == HEX_Type.FLAG:
                        target = candidate_end
                        if self.map[startpos].get_current_value() > self.map[candidate_end].get_current_value()*1.5:
                            last_cell_from_attack = startpos
                            return (self.map[startpos].get_position_tuple(), self.map[candidate_end].get_position_tuple())
        #                 found_flag = True
        #             if self.map[startpos].get_current_value() > self.map[candidate_end].get_current_value()+1:
        #                 if alternative == None:
        #                     alternative = candidate_end
        #             else:
        #                 if not found_flag:
        #                     target = candidate_end
        # if alternative != None and not found_flag:
        #     if DEBUG: print(f"bot {self.player_id}:\tattack {self.map[alternative].get_owner_ID()} ----- {self.map[startpos].get_position_tuple()} -> {self.map[alternative].get_position_tuple()}")
        #     return (self.map[startpos].get_position_tuple(), self.map[alternative].get_position_tuple())
        if target != None:
            if DEBUG: print(f"bot {self.player_id}:\t {target = }")
        
        if target == None:
            # Try to expand (towards the center), if possible
            best_val = 9999
            best_start = None
            best_end = None
            for startpos in myland:
                for candidate_end in self.map[startpos].get_neighbors():
                    curr_val = sum([_**2 for _ in self.map[candidate_end].get_position_tuple()])

                    if (self.map[candidate_end].get_point_type() != HEX_Type.WALL and
                    self.map[candidate_end].get_owner_ID() != self.player_id and
                    self.map[startpos].get_current_value() > 1 and
                    curr_val < best_val):
                        best_val = curr_val
                        best_start = startpos
                        best_end = candidate_end
            if best_end != None:
                if DEBUG: print(f"bot {self.player_id}:\texpand ----- {self.map[best_start].get_position_tuple()}[{self.map[best_start].get_current_value()}] -> {self.map[best_end].get_position_tuple()}")
                return (self.map[best_start].get_position_tuple(), self.map[best_end].get_position_tuple())

        # Try to accumulate troops
        best_val = 9999
        best_start = None
        best_end = None
        for startpos in myland:
            for candidate_end in self.map[startpos].get_neighbors():
                if target == None:
                    if (self.map[candidate_end].get_point_type() == HEX_Type.FLAG and
                    self.map[startpos].get_current_value() > 1):
                        if DEBUG: print(f"bot {self.player_id}:\taccumulate ----- {self.map[startpos].get_position_tuple()} -> {self.map[candidate_end].get_position_tuple()}")
                        return (self.map[startpos].get_position_tuple(), self.map[candidate_end].get_position_tuple())
                else:
                    if self.map[startpos].get_current_value() > 1:
                        curr_val = sum([(xx-yy)**2 for (xx, yy) in zip(self.map[candidate_end].get_position_tuple(), self.map[target].get_position_tuple())])-0.9*self.map[startpos].get_current_value()
                        if (self.map[candidate_end].get_point_type() != HEX_Type.WALL and
                        candidate_end != self.last_cell_from_attack and
                        self.map[startpos].get_current_value() > 1 and
                        curr_val < best_val):
                            best_val = curr_val
                            best_start = startpos
                            best_end = candidate_end
        if target != None and best_end != None:
            if DEBUG: print(f"bot {self.player_id}:\tmove ----- {self.map[best_start].get_position_tuple()} -> {self.map[best_end].get_position_tuple()}")
            self.last_cell_from_attack = best_start
            return (self.map[best_start].get_position_tuple(), self.map[best_end].get_position_tuple())

        if DEBUG: print(f"bot {self.player_id}:\tpass")
        return ((0,0,0), (0,0,0))
    
    def get_player_name(self):
        return self.player_name