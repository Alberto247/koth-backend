from map import Map
from config import *
from lloyd import *
from Hex import *
from hex_types import *
import random
from math import floor
import copy
from debug import plot


class Game:

    def __init__(self):
        self.map=Map()
        self.player_spawns=[]
        self.player_controllers=[]
        self.crystal_spots=[]


        for q in range(-SIDE, SIDE+1):
            for r in range(-SIDE, SIDE+1):
                s=-(q+r)
                if(-SIDE<=s<=SIDE):
                    self.map[(q, r, s)]=Hex((q, r, s))

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
            self.player_spawns.append(Hex((q, r, s) , HEX_Type.FLAG))

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
        print(self.player_spawns)

        # verify everyone can reach everyone
        '''
         TODO: this currently does a bfs from player 0, then checks if any player is not reachable.
               In that case it picks a random point and draws a line to the unreachable player, making sure not to destroy anything important in its path
        '''
        rechable_spots=self.player_spawns+self.crystal_spots

        self.reachability_fix(rechable_spots)

        for x in self.player_spawns:
            assert self.map[x].get_point_type()==HEX_Type.FLAG, f"Sanity check failed, a spawn is now {self.map[x].get_point_type()}"
        
        for x in self.crystal_spots:
            assert self.map[x].get_point_type() in [HEX_Type.CRYPTO_CRYSTAL, HEX_Type.REV_CRYSTAL, HEX_Type.WEB_CRYSTAL, HEX_Type.MISC_CRYSTAL, HEX_Type.PWN_CRYSTAL], f"Sanity check failed, a crystal is now {self.map[x].get_point_type()}"



    
    def reachability_fix(self, reachable_spots):
        mapcopy=copy.deepcopy(self.map) #TODO: maybe we can avoid copy if later on we reset all the map owning, this is not too slow however
        start=self.player_spawns[0]
        self.bfs(mapcopy, start) # color all map of color 0
        for x in reachable_spots:
            if(mapcopy[x].get_owner_ID()!=0): #if we find something not connected
                start=random.choice(list(mapcopy.hash_map.values())) #choose a random point until it is a connected point
                line=[]
                while(mapcopy[start].get_owner_ID()!=0 and all((mapcopy[_].get_point_type() in [HEX_Type.WALL, HEX_Type.GRASS] for _ in line[:-1]))): # and nothing is in the path
                    start=random.choice(list(mapcopy.hash_map.values()))
                    line=hex_linedraw(start, x)
                print(line)
                for _ in line[:-1]:
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
            

    def get_map(self):
        return self.map
    
    def get_player_spawns(self):
        return self.player_spawns
    
