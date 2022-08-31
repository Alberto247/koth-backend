from map import Map
from config import *
from lloyd import *
from Hex import *
from hex_types import *
import random
from math import floor
import copy
from debug import plot, timer_func
import time

class Game:

    def __init__(self):
        self.map=Map()
        self.player_spawns=[]
        self.player_controllers=[]
        self.crystal_spots=[]
        self.player_crystals=[]
        self.current_tick=0
        self.history = []



        for q in range(-SIDE, SIDE+1):
            for r in range(-SIDE, SIDE+1):
                s=-(q+r)
                if(-SIDE<=s<=SIDE):
                    self.map[(q, r, s)]=Hex((q, r, s), HEX_Type.GRASS)

        print("Generating spawn points...")

        for x in range(PLAYERS): # generate players spawn points
            s=-100
            q=0
            r=0
            while(not (-SIDE<=s<=SIDE) or not self.map[(q, r, s)].get_point_type()==HEX_Type.GRASS):
                q=random.randint(-SIDE, SIDE)
                r=random.randint(-SIDE, SIDE)
                s=-(q+r)
            self.map[(q, r, s)].set_point_type(HEX_Type.FLAG)
            self.map[(q, r, s)].set_owner_ID(x)
            self.map[(q, r, s)].set_current_value(1)
            self.player_spawns.append(Hex((q, r, s), HEX_Type.FLAG))

        print("Applying some distance...")

        for x in range(PLAYER_DISTANCE): # force players to have at least some distance in between one eachother TODO: This is slow but probably ok
            compute_voronoi(self.map, self.player_spawns)

            self.player_spawns=relax(self.map, self.player_spawns)
            for q in range(-SIDE, SIDE+1):
                for r in range(-SIDE, SIDE+1):
                    s=-(q+r)
                    if(-SIDE<=s<=SIDE):
                        self.map[(q, r, s)]=Hex((q, r, s))
            for x in range(PLAYERS):
                self.map[self.player_spawns[x]].set_point_type(HEX_Type.FLAG)
                self.map[self.player_spawns[x]].set_owner_ID(x)
                self.map[self.player_spawns[x]].set_current_value(1)
        
        print("Generating the undecipherable crypto crystal...")
        s=-100
        q=0
        r=0
        while(not (-SIDE<=s<=SIDE) or not self.map[(q, r, s)].get_point_type()==HEX_Type.GRASS):
            q=random.randint(-SIDE, SIDE)
            r=random.randint(-SIDE, SIDE)
            s=-(q+r)
        self.map[(q, r, s)].set_point_type(HEX_Type.CRYPTO_CRYSTAL)
        self.crystal_spots.append(Hex((q, r, s), HEX_Type.CRYPTO_CRYSTAL))

        print("Generating the sticky web crystal...")
        s=-100
        q=0
        r=0
        while(not (-SIDE<=s<=SIDE) or not self.map[(q, r, s)].get_point_type()==HEX_Type.GRASS):
            q=random.randint(-SIDE, SIDE)
            r=random.randint(-SIDE, SIDE)
            s=-(q+r)
        self.map[(q, r, s)].set_point_type(HEX_Type.WEB_CRYSTAL)
        self.crystal_spots.append(Hex((q, r, s), HEX_Type.WEB_CRYSTAL))

        print("...latsyrc ver driew eht gnitareneG")
        s=-100
        q=0
        r=0
        while(not (-SIDE<=s<=SIDE) or not self.map[(q, r, s)].get_point_type()==HEX_Type.GRASS):
            q=random.randint(-SIDE, SIDE)
            r=random.randint(-SIDE, SIDE)
            s=-(q+r)
        self.map[(q, r, s)].set_point_type(HEX_Type.REV_CRYSTAL)
        self.crystal_spots.append(Hex((q, r, s), HEX_Type.REV_CRYSTAL))

        print("Generating the powerful pwn crystal...")
        s=-100
        q=0
        r=0
        while(not (-SIDE<=s<=SIDE) or not self.map[(q, r, s)].get_point_type()==HEX_Type.GRASS):
            q=random.randint(-SIDE, SIDE)
            r=random.randint(-SIDE, SIDE)
            s=-(q+r)
        self.map[(q, r, s)].set_point_type(HEX_Type.PWN_CRYSTAL)
        self.crystal_spots.append(Hex((q, r, s), HEX_Type.PWN_CRYSTAL))

        print("Generating the all-knowning misc crystal...")
        s=-100
        q=0
        r=0
        while(not (-SIDE<=s<=SIDE) or not self.map[(q, r, s)].get_point_type()==HEX_Type.GRASS):
            q=random.randint(-SIDE, SIDE)
            r=random.randint(-SIDE, SIDE)
            s=-(q+r)
        self.map[(q, r, s)].set_point_type(HEX_Type.MISC_CRYSTAL)
        self.crystal_spots.append(Hex((q, r, s), HEX_Type.MISC_CRYSTAL))
        
        print("Generating mountain ranges...")
        # Now generate mountains
        total_tiles=SIDE*(SIDE-1)*3+1
        assert 0<MOUNTAIN_DENSITY and MOUNTAIN_DENSITY<1, "Mountain density must be between 0 and 1 excluded"
        tot_mountains=floor(total_tiles*MOUNTAIN_DENSITY)
        n_mountains=0

        while(n_mountains<tot_mountains):
            s=-100
            q=0
            r=0
            while(not (-SIDE<=s<=SIDE) or not self.map[(q, r, s)].get_point_type()==HEX_Type.GRASS):
                q=random.randint(-SIDE, SIDE)
                r=random.randint(-SIDE, SIDE)
                s=-(q+r)
            start=Hex((q, r, s))
            number=random.randint(1, MOUNTAIN_LINKAGE)
            for x in range(number):
                if(self.map[start].get_point_type() not in [HEX_Type.FLAG, HEX_Type.CRYPTO_CRYSTAL, HEX_Type.REV_CRYSTAL, HEX_Type.WEB_CRYSTAL, HEX_Type.MISC_CRYSTAL, HEX_Type.PWN_CRYSTAL]):
                    self.map[start].set_point_type(HEX_Type.WALL)
                    n_mountains+=1
                start=Hex(random.choice(self.map[start].get_neighbors()))
        
        print("Running reachability fix...")

        # verify everyone can reach everyone
        '''
         TODO: this currently does a bfs from player 0, then checks if any player is not reachable.
               In that case it picks a random point and draws a line to the unreachable player, making sure not to destroy anything important in its path
        '''
        reachable_spots=self.player_spawns+self.crystal_spots

        self.reachability_fix(reachable_spots)

        print("Running mountain fix...")

        self.mountain_fix()

        assert self.reachability_test(reachable_spots)==True, f"Some places are not reachable?"

        for x in self.player_spawns:
            assert self.map[x].get_point_type()==HEX_Type.FLAG, f"Sanity check failed, a spawn is now {self.map[x].get_point_type()}"
        
        for x in self.crystal_spots:
            assert self.map[x].get_point_type() in [HEX_Type.CRYPTO_CRYSTAL, HEX_Type.REV_CRYSTAL, HEX_Type.WEB_CRYSTAL, HEX_Type.MISC_CRYSTAL, HEX_Type.PWN_CRYSTAL], f"Sanity check failed, a crystal is now {self.map[x].get_point_type()}"

        print("Placing forts...")

        tot_forts=floor(total_tiles*FORT_DENSITY)
        n_forts=0
        while(n_forts<tot_forts):
            s=-100
            q=0
            r=0
            while(not (-SIDE<=s<=SIDE) or not self.map[(q, r, s)].get_point_type()==HEX_Type.GRASS):
                q=random.randint(-SIDE, SIDE)
                r=random.randint(-SIDE, SIDE)
                s=-(q+r)
            self.map[(q, r, s)].set_point_type(HEX_Type.FORT)
            number=random.randint(MIN_FORT_COST, MAX_FORT_COST)
            self.map[(q, r, s)].set_current_value(number)
            n_forts+=1
        
        self.history.append(self.map.serializable())

        

    def reachability_test(self, reachable_spots):
        mapcopy=copy.deepcopy(self.map)
        start=self.player_spawns[0]
        self.bfs(mapcopy, start)
        for x in reachable_spots:
            if(mapcopy[x].get_owner_ID()!=0):
                return False
        return True
    
    def mountain_fix(self):
        mapcopy=copy.deepcopy(self.map)
        start=self.player_spawns[0]
        self.bfs(mapcopy, start)
        for hex in mapcopy.hash_map.values():
            if hex.get_owner_ID()!=0:
                self.map[hex.get_position_tuple()].set_point_type(HEX_Type.WALL)
        

    
    def reachability_fix(self, reachable_spots):
        mapcopy=copy.deepcopy(self.map) #TODO: maybe we can avoid copy if later on we reset all the map owning, this is not too slow however
        start=self.player_spawns[0]
        self.bfs(mapcopy, start) # color all map of color 0
        for x in reachable_spots:
            if(mapcopy[x].get_owner_ID()!=0): #if we find something not connected
                start=random.choice(list(mapcopy.hash_map.values())) #choose a random point until it is a connected point
                line=[]
                while(mapcopy[start].get_owner_ID()!=0 or line==[]): # and nothing is in the path
                    start=random.choice(list(mapcopy.hash_map.values()))
                    line=hex_linedraw(start, x)
                for _ in line:
                    if(self.map[_].get_point_type()==HEX_Type.WALL):
                        self.map[_].set_point_type(HEX_Type.GRASS) # and color!
    
    def bfs(self, map, start):
        to_visit=[start]
        visited=[]
        while(len(to_visit)!=0):
            start=to_visit.pop(0)
            for neighbour in map[start].get_neighbors():
                if(map[neighbour].get_point_type()!=HEX_Type.WALL):
                    map[neighbour].set_owner_ID(0)
                    if(neighbour not in visited):
                        to_visit.append(neighbour)
                        visited.append(neighbour)
    
    def add_player(self, controller):
        self.player_controllers.append(controller)
        self.player_crystals.append([])
    
    def generate_player_map(self, player):
        player_map=copy.deepcopy(self.map)
        self.player_controllers[player].seen_tiles=set(player_map.hash_map.keys())
        for tile in player_map.hash_map.values():
            if(tile.get_owner_ID()!=player and not any([self.map[_].get_owner_ID()==player for _ in tile.get_neighbors()])):
                if(tile.get_point_type() in [HEX_Type.GRASS, HEX_Type.FLAG]):
                    tile.set_point_type(HEX_Type.UNKNOWN_EMPTY)
                else:
                    tile.set_point_type(HEX_Type.UNKNOWN_OBJECT)
                tile.set_current_value(0)
                tile.set_owner_ID(None)
                self.player_controllers[player].seen_tiles.remove(tile.get_position_tuple())
        for crystal in self.crystal_spots:
            if(crystal.get_point_type() in self.player_crystals[player]):
                player_map[crystal]=copy.deepcopy(self.map[crystal])
                for x in crystal.get_neighbors():
                    player_map[x]=copy.deepcopy(self.map[x])
                    for y in player_map[x].get_neighbors():
                        player_map[y]=copy.deepcopy(self.map[y])
        return player_map
    
    def generate_all_players_maps(self):
        for player in range(PLAYERS):
            self.player_controllers[player].set_map(self.generate_player_map(player))
    
    @timer_func
    def update_players_maps(self, moves):
        for player in range(PLAYERS):
            player_map=self.player_controllers[player].get_map()
            start=time.time()
            for move in moves:
                for tile_tuple in move:
                    map_tile=self.map[tile_tuple]
                    player_tile=player_map[tile_tuple]
                    if(map_tile.get_owner_ID()!=player and not any([self.map[_].get_owner_ID()==player for _ in map_tile.get_neighbors()])):
                        if(map_tile.get_point_type() in [HEX_Type.GRASS, HEX_Type.FLAG]):
                            player_tile.set_point_type(HEX_Type.UNKNOWN_EMPTY)
                        else:
                            player_tile.set_point_type(HEX_Type.UNKNOWN_OBJECT)
                        player_tile.set_current_value(0)
                        player_tile.set_owner_ID(None)
                        self.player_controllers[player].seen_tiles.discard(tile_tuple)
                    else:
                        player_map[tile_tuple]=copy.deepcopy(map_tile)
                        self.player_controllers[player].seen_tiles.add(tile_tuple)
                    for neighbour_tile in map_tile.get_neighbors():
                        map_neighbour_tile=self.map[neighbour_tile]
                        player_tile=player_map[neighbour_tile]
                        if(map_neighbour_tile.get_owner_ID()!=player and not any([self.map[_].get_owner_ID()==player for _ in map_neighbour_tile.get_neighbors()])):
                            if(map_neighbour_tile.get_point_type() in [HEX_Type.GRASS, HEX_Type.FLAG]):
                                player_tile.set_point_type(HEX_Type.UNKNOWN_EMPTY)
                            else:
                                player_tile.set_point_type(HEX_Type.UNKNOWN_OBJECT)
                            player_tile.set_current_value(0)
                            player_tile.set_owner_ID(None)
                            self.player_controllers[player].seen_tiles.discard(tile_tuple)
                        else:
                            player_map[neighbour_tile]=copy.deepcopy(map_neighbour_tile)
                            self.player_controllers[player].seen_tiles.add(tile_tuple)
            #print(f"Step 1: {time.time()-start}")
            for crystal in self.crystal_spots:
                if(crystal.get_point_type() in self.player_crystals[player]):
                    player_map[crystal]=copy.deepcopy(self.map[crystal])
                    for x in crystal.get_neighbors():
                        player_map[x]=copy.deepcopy(self.map[x])
                        for y in player_map[x].get_neighbors():
                            player_map[y]=copy.deepcopy(self.map[y])
            for tile in self.player_controllers[player].seen_tiles:
                tile=player_map[tile]
                if(tile.get_owner_ID()!=None):
                    if(tile.get_point_type() in [HEX_Type.FLAG, HEX_Type.FORT]):
                        tile.set_current_value(tile.get_current_value()+1)
                    elif(self.current_tick%25==0):
                        tile.set_current_value(tile.get_current_value()+1)
            

    def tick(self):
        self.current_tick+=1
        #print(self.current_tick)
        moves=[]
        edited_hex = set()

        for player in range(PLAYERS):
            player_move=self.player_controllers[player].tick(self.current_tick)
            moves.append(player_move)
            edited_hex.add(player_move[0])
            edited_hex.add(player_move[1])
        for player in range(PLAYERS):
            self.do_move(player, moves[player])
        edited_hex |= self.update_map()
        self.update_players_maps(moves)
        self.history.append(self.map.serializable_partial(edited_hex))

    def do_move(self, player, move): #TODO: handle crystals
        hex_start=self.map[move[0]]
        hex_end=self.map[move[1]]
        if(hex_start.get_owner_ID()==player and hex_start.get_current_value()>1 and hex_end.get_point_type()!=HEX_Type.WALL):
            amount=hex_start.get_current_value()-1
            hex_start.set_current_value(1)
            if(hex_end.get_owner_ID()==None):
                if(hex_end.get_point_type()!=HEX_Type.FORT):
                    hex_end.set_owner_ID(player)
                    hex_end.set_current_value(amount)
                else:
                    hex_end.set_current_value(hex_end.get_current_value()-amount)
                    if(hex_end.get_current_value()<0):
                        hex_end.set_owner_ID(player)
                        hex_end.set_current_value(abs(hex_end.get_current_value()))
            else:
                if(hex_end.get_owner_ID()==player):
                    hex_end.set_current_value(hex_end.get_current_value()+amount)
                else:
                    hex_end.set_current_value(hex_end.get_current_value()-amount)
                    if(hex_end.get_current_value()<0):
                        hex_end.set_owner_ID(player)
                        hex_end.set_current_value(abs(hex_end.get_current_value()))
                        if(hex_end.get_point_type()==HEX_Type.FLAG):
                            pass # TODO: Player is killed
            if(hex_end.get_point_type() in [HEX_Type.CRYPTO_CRYSTAL, HEX_Type.REV_CRYSTAL, HEX_Type.WEB_CRYSTAL, HEX_Type.MISC_CRYSTAL, HEX_Type.PWN_CRYSTAL] and hex_end.get_point_type() not in self.player_crystals[player]):
                self.player_crystals[player].append(hex_end.get_point_type())

    def update_map(self): # TODO: a bit slow (3ms), but not too slow
        edited_hex = set()
        for tile in self.map.hash_map.values():
            if(tile.get_owner_ID()!=None):
                if(tile.get_point_type() in [HEX_Type.FLAG, HEX_Type.FORT]):
                    tile.set_current_value(tile.get_current_value()+1)
                    edited_hex.add(tile.get_position_tuple())
                elif(self.current_tick%25==0):
                    tile.set_current_value(tile.get_current_value()+1)
                    edited_hex.add(tile.get_position_tuple())
        return edited_hex

    def get_map(self):
        return self.map
    
    def get_player_spawns(self):
        return self.player_spawns

    def json_serialize_history(self, filename):
        import json
        json.dump(self.history, open(filename, 'w'))
