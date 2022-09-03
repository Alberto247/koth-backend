from map import Map
from config import *
from lloyd import *
from Hex import *
from hex_types import *
import random
from math import floor
import copy
import asyncio
import time
from player import Player
from debug import timer_func
import json
import os

class Game:

    def __init__(self):
        self.map=Map()
        self.player_spawns=[]
        self.player_controllers=[]
        self.crystal_spots=[]
        self.player_crystals=[]
        self.current_tick=0
        self.history = []
        self.last_tick_deads=False

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
    

    def update_players_maps(self, moves):
        players_edits=[]
        for player in range(PLAYERS):
            single_player_edits=[]
            player_map=self.player_controllers[player].get_map()
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
                        single_player_edits.append(player_tile.serializable())
                        self.player_controllers[player].seen_tiles.discard(tile_tuple)
                    else:
                        player_map[tile_tuple]=copy.deepcopy(map_tile)
                        single_player_edits.append(map_tile.serializable())
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
                            single_player_edits.append(player_tile.serializable())
                            self.player_controllers[player].seen_tiles.discard(tile_tuple)
                        else:
                            player_map[neighbour_tile]=copy.deepcopy(map_neighbour_tile)
                            single_player_edits.append(map_neighbour_tile.serializable())
                            self.player_controllers[player].seen_tiles.add(tile_tuple)
            for crystal in self.crystal_spots:
                if(crystal.get_point_type() in self.player_crystals[player]):
                    player_map[crystal]=copy.deepcopy(self.map[crystal])
                    single_player_edits.append(self.map[crystal].serializable())
                    self.player_controllers[player].seen_tiles.add(crystal)
                    for x in crystal.get_neighbors():
                        player_map[x]=copy.deepcopy(self.map[x])
                        single_player_edits.append(self.map[x].serializable())
                        self.player_controllers[player].seen_tiles.add(x)
                        for y in player_map[x].get_neighbors():
                            player_map[y]=copy.deepcopy(self.map[y])
                            single_player_edits.append(self.map[y].serializable())
                            self.player_controllers[player].seen_tiles.add(y)
            for tile in self.player_controllers[player].seen_tiles:
                tile=player_map[tile]
                if(tile.get_owner_ID()!=None):
                    if(tile.get_point_type() in [HEX_Type.FLAG, HEX_Type.FORT]):
                        tile.set_current_value(tile.get_current_value()+1)
                    elif(self.current_tick%25==0):
                        tile.set_current_value(tile.get_current_value()+1)
            players_edits.append(single_player_edits)
        return players_edits
            
    async def async_tick(self):
        start=time.time()
        print(self.current_tick)
        moves=[]
        edited_hex = set() # This is for the web map
        ts=[]
        if(self.last_tick_deads):
            self.generate_all_players_maps() # If someone died it is easier to regenerate all maps
        for player in range(PLAYERS):
            json.dump(self.player_controllers[player].player_map.serializable(), open(f"/debug/backend/{player}/{self.current_tick}.json", 'w')) # Save map for testing
        for player in range(PLAYERS):
            asyncio.get_event_loop()
            if(self.current_tick==0 or self.last_tick_deads): # At first tick, send whole map, or when someone died
                ts.append(self.player_controllers[player].tick_map(self.current_tick)) # Send map to every player
            else:
                ts.append(self.player_controllers[player].tick(self.current_tick)) # Send updates to every player
        if(self.last_tick_deads):
            self.last_tick_deads=False
        moves=await asyncio.gather(*ts) # Wait for all moves
        moves_gathered=time.time()
        for player_move in moves:
            edited_hex.add(player_move[0]) # This is for the web app
            edited_hex.add(player_move[1])
        for player in range(PLAYERS):
            edited_hex |= self.do_move(player, moves[player]) # Do all moves
        updates=self.update_players_maps(moves) # Update every map and return updated tiles
        for player in range(PLAYERS):
            if(self.player_controllers[player].dead==False): # TODO: this is not consistent in case the dead player conquered something during this tick
                self.player_controllers[player].set_update(updates[player]) # Set update to be sent to players at next tick
        edited_hex |= self.update_map() # Update global map count on every tile
        update_maps=time.time()
        self.history.append(self.map.serializable_partial(edited_hex)) # Add to web map history
        self.current_tick+=1 # Next tick
        #print(f"tick: Time to gather moves: {moves_gathered-start}, time to update maps: {update_maps-moves_gathered}, total time: {time.time()-start}")

    def tick(self):
        self.current_tick+=1
        print(self.current_tick)
        moves=[]
        edited_hex = set()
        if(self.last_tick_deads):
            self.last_tick_deads=False
            self.generate_all_players_maps()
        for player in range(PLAYERS):
            player_move=self.player_controllers[player].tick(self.current_tick) 
            moves.append(player_move)
            edited_hex.add(player_move[0])
            edited_hex.add(player_move[1])
        for player in range(PLAYERS):
            edited_hex |= self.do_move(player, moves[player])
        self.update_players_maps(moves)
        edited_hex |= self.update_map()
        self.history.append(self.map.serializable_partial(edited_hex))

    def run(self):
        for x in range(PLAYERS): # Use this for local testing
            self.add_player(Player(x, "./random_bot.py"))
        print("Starting simulation")
        self.generate_all_players_maps()

        start=time.time()
        for i in range(SIMULATION_LENGTH):
            self.tick()
        print(time.time()-start)
        self.json_serialize_history('./frontend/history.json')
    
    async def run_async(self):
        for x in range(PLAYERS): # Use this for websocket testing
            self.add_player(Player(x, f"ws://player{x+1}:8765/"))
        for x in range(PLAYERS):
            await self.player_controllers[x].connect() # Connect to players
        self.generate_all_players_maps() # Generate every map
        os.system("rm -r /debug/backend")
        os.system("mkdir /debug/backend")
        for x in range(PLAYERS):
            os.system(f"mkdir /debug/backend/{x}")
        print("Starting simulation")
        start=time.time()
        for i in range(SIMULATION_LENGTH):
            await self.async_tick()
        print(time.time()-start)
        self.json_serialize_history('./frontend/history.json')

    def do_move(self, player, move): #TODO: handle crystals
        edited_hex=set()
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
                        if(hex_end.get_point_type()==HEX_Type.FLAG):
                                self.last_tick_deads=True
                                print(f"Player {hex_end.get_owner_ID()} has been killed by {player} at tick {self.current_tick}!")
                                self.player_controllers[hex_end.get_owner_ID()].dead=True
                                new_owner=hex_end.get_owner_ID()
                                for tile in self.player_controllers[new_owner].seen_tiles:
                                    if(self.map[tile].get_owner_ID()==new_owner):
                                        self.map[tile].set_owner_ID(player)
                                        edited_hex.add(tile)
                                hex_end.set_point_type(HEX_Type.FORT)
                        hex_end.set_owner_ID(player)
                        hex_end.set_current_value(abs(hex_end.get_current_value()))
                        
            if(hex_end.get_point_type() in [HEX_Type.CRYPTO_CRYSTAL, HEX_Type.REV_CRYSTAL, HEX_Type.WEB_CRYSTAL, HEX_Type.MISC_CRYSTAL, HEX_Type.PWN_CRYSTAL] and hex_end.get_point_type() not in self.player_crystals[player]):
                self.player_crystals[player].append(hex_end.get_point_type())
        return edited_hex

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
