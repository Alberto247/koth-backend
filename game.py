'''
    This file handles every game. At initialization it creates the map.
'''

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
import json
import os


class Game:

    def __init__(self):
        self.map = Map()
        # FIXME use dicts instead of lists to avoid errors due to non consecutive player ids
        self.player_spawns = []
        self.player_controllers = []
        self.crystal_spots = []
        self.player_crystals = []
        self.current_tick = 0
        self.history = []
        self.last_tick_deads = False
        self.dead_order = []

        # Create an empty map
        for q in range(-SIDE, SIDE+1):
            for r in range(-SIDE, SIDE+1):
                s = -(q+r)
                if(-SIDE <= s <= SIDE):
                    self.map[(q, r, s)] = Hex((q, r, s), HEX_Type.GRASS)

        print("Generating spawn points...")

        for x in range(PLAYERS):  # generate players spawn points
            s = -100
            q = 0
            r = 0
            while(not (-SIDE <= s <= SIDE) or not self.map[(q, r, s)].get_point_type() == HEX_Type.GRASS):
                q = random.randint(-SIDE, SIDE)
                r = random.randint(-SIDE, SIDE)
                s = -(q+r)
            self.map[(q, r, s)].set_point_type(HEX_Type.FLAG)
            self.map[(q, r, s)].set_owner_ID(x)
            self.map[(q, r, s)].set_current_value(1)
            self.player_spawns.append(Hex((q, r, s), HEX_Type.FLAG))

        print("Applying some distance...")

        # force players to have at least some distance in between one eachother
        for x in range(PLAYER_DISTANCE):
            compute_voronoi(self.map, self.player_spawns)

            self.player_spawns = relax(self.map, self.player_spawns)
            for q in range(-SIDE, SIDE+1):
                for r in range(-SIDE, SIDE+1):
                    s = -(q+r)
                    if(-SIDE <= s <= SIDE):
                        self.map[(q, r, s)] = Hex((q, r, s))
            for x in range(PLAYERS):
                self.map[self.player_spawns[x]].set_point_type(HEX_Type.FLAG)
                self.map[self.player_spawns[x]].set_owner_ID(x)
                self.map[self.player_spawns[x]].set_current_value(1)

        print("Generating the undecipherable crypto crystal...")
        s = -100
        q = 0
        r = 0
        while(not (-SIDE <= s <= SIDE) or not self.map[(q, r, s)].get_point_type() == HEX_Type.GRASS):
            q = random.randint(-SIDE, SIDE)
            r = random.randint(-SIDE, SIDE)
            s = -(q+r)
        self.map[(q, r, s)].set_point_type(HEX_Type.CRYPTO_CRYSTAL)
        self.crystal_spots.append(Hex((q, r, s), HEX_Type.CRYPTO_CRYSTAL))

        print("Generating the sticky web crystal...")
        s = -100
        q = 0
        r = 0
        while(not (-SIDE <= s <= SIDE) or not self.map[(q, r, s)].get_point_type() == HEX_Type.GRASS):
            q = random.randint(-SIDE, SIDE)
            r = random.randint(-SIDE, SIDE)
            s = -(q+r)
        self.map[(q, r, s)].set_point_type(HEX_Type.WEB_CRYSTAL)
        self.crystal_spots.append(Hex((q, r, s), HEX_Type.WEB_CRYSTAL))

        print("...latsyrc ver driew eht gnitareneG")
        s = -100
        q = 0
        r = 0
        while(not (-SIDE <= s <= SIDE) or not self.map[(q, r, s)].get_point_type() == HEX_Type.GRASS):
            q = random.randint(-SIDE, SIDE)
            r = random.randint(-SIDE, SIDE)
            s = -(q+r)
        self.map[(q, r, s)].set_point_type(HEX_Type.REV_CRYSTAL)
        self.crystal_spots.append(Hex((q, r, s), HEX_Type.REV_CRYSTAL))

        print("Generating the powerful pwn crystal...")
        s = -100
        q = 0
        r = 0
        while(not (-SIDE <= s <= SIDE) or not self.map[(q, r, s)].get_point_type() == HEX_Type.GRASS):
            q = random.randint(-SIDE, SIDE)
            r = random.randint(-SIDE, SIDE)
            s = -(q+r)
        self.map[(q, r, s)].set_point_type(HEX_Type.PWN_CRYSTAL)
        self.crystal_spots.append(Hex((q, r, s), HEX_Type.PWN_CRYSTAL))

        print("Generating the all-knowning misc crystal...")
        s = -100
        q = 0
        r = 0
        while(not (-SIDE <= s <= SIDE) or not self.map[(q, r, s)].get_point_type() == HEX_Type.GRASS):
            q = random.randint(-SIDE, SIDE)
            r = random.randint(-SIDE, SIDE)
            s = -(q+r)
        self.map[(q, r, s)].set_point_type(HEX_Type.MISC_CRYSTAL)
        self.crystal_spots.append(Hex((q, r, s), HEX_Type.MISC_CRYSTAL))

        print("Generating mountain ranges...")
        # Now generate mountains
        total_tiles = SIDE*(SIDE-1)*3+1
        assert 0 < MOUNTAIN_DENSITY and MOUNTAIN_DENSITY < 1, "Mountain density must be between 0 and 1 excluded"
        tot_mountains = floor(total_tiles*MOUNTAIN_DENSITY)
        n_mountains = 0

        while(n_mountains < tot_mountains):
            s = -100
            q = 0
            r = 0
            while(not (-SIDE <= s <= SIDE) or not self.map[(q, r, s)].get_point_type() == HEX_Type.GRASS):
                q = random.randint(-SIDE, SIDE)
                r = random.randint(-SIDE, SIDE)
                s = -(q+r)
            start = Hex((q, r, s))
            number = random.randint(1, MOUNTAIN_LINKAGE) # Generate mountain range of at most MOUNTAIN_LINKAGE
            for x in range(number):
                if(self.map[start].get_point_type() not in [HEX_Type.FLAG, HEX_Type.CRYPTO_CRYSTAL, HEX_Type.REV_CRYSTAL, HEX_Type.WEB_CRYSTAL, HEX_Type.MISC_CRYSTAL, HEX_Type.PWN_CRYSTAL]):
                    self.map[start].set_point_type(HEX_Type.WALL)
                    n_mountains += 1
                start = Hex(random.choice(self.map[start].get_neighbors()))

        print("Running reachability fix...")

        # verify everyone can reach everyone and every important point
        reachable_spots = self.player_spawns+self.crystal_spots

        self.reachability_fix(reachable_spots)

        #Fill unreachable spots in map with mountains
        print("Running mountain fix...")

        self.mountain_fix()

        # Sanity checks, this should always pass if you did not modify the above code
        assert self.reachability_test(
            reachable_spots) == True, f"Some places are not reachable?"

        for x in self.player_spawns:
            assert self.map[x].get_point_type(
            ) == HEX_Type.FLAG, f"Sanity check failed, a spawn is now {self.map[x].get_point_type()}"

        for x in self.crystal_spots:
            assert self.map[x].get_point_type() in [HEX_Type.CRYPTO_CRYSTAL, HEX_Type.REV_CRYSTAL, HEX_Type.WEB_CRYSTAL,
                                                    HEX_Type.MISC_CRYSTAL, HEX_Type.PWN_CRYSTAL], f"Sanity check failed, a crystal is now {self.map[x].get_point_type()}"

        # Now place forts randomly
        print("Placing forts...")

        tot_forts = floor(total_tiles*FORT_DENSITY)
        n_forts = 0
        while(n_forts < tot_forts):
            s = -100
            q = 0
            r = 0
            while(not (-SIDE <= s <= SIDE) or not self.map[(q, r, s)].get_point_type() == HEX_Type.GRASS):
                q = random.randint(-SIDE, SIDE)
                r = random.randint(-SIDE, SIDE)
                s = -(q+r)
            self.map[(q, r, s)].set_point_type(HEX_Type.FORT)
            number = random.randint(MIN_FORT_COST, MAX_FORT_COST)
            self.map[(q, r, s)].set_current_value(number)
            n_forts += 1

        # Save map to history
        self.history.append(self.map.serializable())

    # Simple bfs from player 0 to check that he can reach everyone
    def reachability_test(self, reachable_spots):
        mapcopy = copy.deepcopy(self.map)
        start = self.player_spawns[0]
        self.bfs(mapcopy, start)
        for x in reachable_spots:
            if(mapcopy[x].get_owner_ID() != 0):
                return False
        return True

    # Bfs to find unreachable spots and fill them with mountains
    def mountain_fix(self):
        mapcopy = copy.deepcopy(self.map)
        start = self.player_spawns[0]
        self.bfs(mapcopy, start)
        for hex in mapcopy.hash_map.values():
            if hex.get_owner_ID() != 0:
                self.map[hex.get_position_tuple()].set_point_type(
                    HEX_Type.WALL)

    # Fix reachability using bfs and lines
    def reachability_fix(self, reachable_spots):
        mapcopy = copy.deepcopy(self.map)
        start = self.player_spawns[0]
        self.bfs(mapcopy, start)  # bfs to color all map of color 0
        for x in reachable_spots:
            if(mapcopy[x].get_owner_ID() != 0):  # if we find something not connected
                # choose a random point until it is a connected point
                start = random.choice(list(mapcopy.hash_map.values()))
                line = []
                # and nothing is in the path
                while(mapcopy[start].get_owner_ID() != 0 or line == []):
                    start = random.choice(list(mapcopy.hash_map.values()))
                    line = hex_linedraw(start, x)
                for _ in line:  # FIXME this for does not update mapcopy and does not call bfs on the updated map, this might result in multiple unnecessary lines been drawn and slowness
                    if(self.map[_].get_point_type() == HEX_Type.WALL):
                        self.map[_].set_point_type(
                            HEX_Type.GRASS)  # and color!

    def bfs(self, map, start):
        to_visit = [start]
        visited = []
        while(len(to_visit) != 0):
            start = to_visit.pop(0)
            for neighbour in map[start].get_neighbors():
                if(map[neighbour].get_point_type() != HEX_Type.WALL):
                    map[neighbour].set_owner_ID(0)
                    if(neighbour not in visited):
                        to_visit.append(neighbour)
                        visited.append(neighbour)  # FIXME use set for better performance
                        # FIXME to visit and visited appends might be in the wrong place

    def add_player(self, controller):
        self.player_controllers.append(controller)  # FIXME use a dictionary to avoid errors due to non consecutive player ids
        self.player_crystals.append([])  # FIXME use a dictionary to avoid errors due to non consecutive player ids

    # This function generates the map the player is supposed to see.
    def generate_player_map(self, player):
        player_map = copy.deepcopy(self.map) # Make a copy of the full map
        # self.player_controllers[player].seen_tiles = set(
        #     player_map.hash_map.keys()) # And set all tiles to seen
        self.player_controllers[player].seen_tiles = set() # Set tiles as not seen
        for tile in player_map.hash_map.values(): # For every tile
            if(tile.get_owner_ID() != player and not any([self.map[_].get_owner_ID() == player for _ in tile.get_neighbors()])): # If not seen
                if(tile.get_point_type() in [HEX_Type.GRASS, HEX_Type.FLAG]):
                    tile.set_point_type(HEX_Type.UNKNOWN_EMPTY) # Hide it
                else:
                    tile.set_point_type(HEX_Type.UNKNOWN_OBJECT)
                tile.set_current_value(0)
                tile.set_owner_ID(None)
                # self.player_controllers[player].seen_tiles.remove(  # FIXME adding tiles might be faster since at the start only 6 tiles should be visible
                #     tile.get_position_tuple()) # And remove from seen set
            else:
                self.player_controllers[player].seen_tiles.add(tile.get_position_tuple()) # Add seen tile

        for crystal in self.crystal_spots:
            if(crystal.get_point_type() in self.player_crystals[player]):  # FIXME just add the tiles in self.player_crystals[player] on cristalcapture and loop them
                player_map[crystal] = copy.deepcopy(self.map[crystal])  # FIXME using references might be helpfull here instead of copy or might be a vuln
                self.player_controllers[player].seen_tiles.add(
                    crystal.get_position_tuple())
                for x in crystal.get_neighbors():
                    player_map[x] = copy.deepcopy(self.map[x])  # FIXME same here
                    self.player_controllers[player].seen_tiles.add(x)
                    for y in player_map[x].get_neighbors():  # FIXME not skipping already seen tiles, mabe use coordinates instead of nested neighbours loop
                        player_map[y] = copy.deepcopy(self.map[y])  # FIXME same here
                        self.player_controllers[player].seen_tiles.add(y)
        return player_map

    def generate_all_players_maps(self):
        for player in range(PLAYERS):
            self.player_controllers[player].set_map(
                self.generate_player_map(player))

    # Takes all updates in the map and applies them to the players' maps
    def update_players_maps(self, moves):
        players_edits = []  # FIXME change to set to randomize order and coherence with the rest of edits logs
        for player in range(PLAYERS):  # for each player, apply all moves
            single_player_edits = []  # All tiles edited for this player, so we can send them over
            player_map = self.player_controllers[player].get_map()
            for move in moves:
                for tile_tuple in move:  # For each start and end of move
                    map_tile = self.map[tile_tuple]  # FIXME nothing catched potentially non existent tile if tuple is outside map bounds
                    player_tile = player_map[tile_tuple]  # FIXME nothing catched potentially non existent tile if tuple is outside map bounds
                    # If player does not see that move
                    if(map_tile.get_owner_ID() != player and not any([self.map[_].get_owner_ID() == player for _ in map_tile.get_neighbors()])):  # FIXME this does not check for crystal tiles   # FIXME maybe just check if one of the two move tiles are in the seen tiles set but i don'tknow it
                        if(map_tile.get_point_type() in [HEX_Type.GRASS, HEX_Type.FLAG]):  # FIXME why is this done? if the player does not see the move should it already be unknown type?
                            player_tile.set_point_type(HEX_Type.UNKNOWN_EMPTY)
                        else:
                            player_tile.set_point_type(HEX_Type.UNKNOWN_OBJECT)
                        # Make it empty and unknown
                        player_tile.set_current_value(0)
                        player_tile.set_owner_ID(None)
                        # Add to the edited tiles the serialized version of the tile
                        single_player_edits.append(player_tile.serializable())  # FIXME maybe check if the tile was visible before to avoid sending invisible moves and leaking map events
                        self.player_controllers[player].seen_tiles.discard(  # FIXME maybe this is redundant
                            tile_tuple)  # Remove the tuple from the seen tiles
                    else:
                        # If player sees the tile, copy it from the map
                        player_map[tile_tuple] = copy.deepcopy(map_tile)
                        # add the tile from the map to the edits
                        single_player_edits.append(map_tile.serializable())
                        self.player_controllers[player].seen_tiles.add(  # FIXME maybe this is redundant, also might add visible tiles if someone manages to get here since this method does not check if move is valid
                            tile_tuple)  # add the tuple to the seen tiles
                    for neighbour_tile in map_tile.get_neighbors():  # Now for each neighbour  # FIXME this does not check if tile is already updated in the other move tile
                        map_neighbour_tile = self.map[neighbour_tile]
                        player_tile = player_map[neighbour_tile]
                        # if not seen
                        if(map_neighbour_tile.get_owner_ID() != player and not any([self.map[_].get_owner_ID() == player for _ in map_neighbour_tile.get_neighbors()])):  # FIXME mostly fame fixes as before
                            if(map_neighbour_tile.get_point_type() in [HEX_Type.GRASS, HEX_Type.FLAG]):
                                player_tile.set_point_type(
                                    HEX_Type.UNKNOWN_EMPTY)
                            else:
                                player_tile.set_point_type(
                                    HEX_Type.UNKNOWN_OBJECT)
                            player_tile.set_current_value(0)
                            player_tile.set_owner_ID(None)
                            # Add player tile to edits
                            single_player_edits.append(
                                player_tile.serializable())
                            self.player_controllers[player].seen_tiles.discard(
                                neighbour_tile)  # remove the tuple from the seen tiles
                        else:
                            player_map[neighbour_tile] = copy.deepcopy(
                                map_neighbour_tile)  # copy the new tile to the player map
                            single_player_edits.append(
                                map_neighbour_tile.serializable())  # add tile to edits
                            self.player_controllers[player].seen_tiles.add(
                                neighbour_tile)  # add tile tuple to seen tiles
            for crystal in self.crystal_spots: # For every crystal  # FIXME same as in do_move also all updates do not check if already sent and if the cell actually changed
                if(crystal.get_point_type() in self.player_crystals[player]): # If player has conquered that crystal in the past
                    player_map[crystal.get_position_tuple()] = copy.deepcopy( # Make it visible
                        self.map[crystal.get_position_tuple()])
                    single_player_edits.append(
                        self.map[crystal.get_position_tuple()].serializable())
                    self.player_controllers[player].seen_tiles.add(
                        crystal.get_position_tuple())
                    for x in crystal.get_neighbors(): # Do it for the crystal's neighbours
                        player_map[x] = copy.deepcopy(self.map[x])
                        single_player_edits.append(self.map[x].serializable())
                        self.player_controllers[player].seen_tiles.add(x)
                        for y in player_map[x].get_neighbors(): # Do it for the crystal's neighbours' neighbours
                            player_map[y] = copy.deepcopy(self.map[y])
                            single_player_edits.append(
                                self.map[y].serializable())
                            self.player_controllers[player].seen_tiles.add(y)
            for tile_tuple in self.player_controllers[player].seen_tiles: # For every seen tiles, update the value on it  # FIXME this is already done later in update_map, consider moving this in that function and calculating apdates after that
                tile = player_map[tile_tuple]
                # if(tile.get_owner_ID() != None):  # FIXME use is not None
                if(tile.get_owner_ID() is not None):
                    if(tile.get_point_type() in [HEX_Type.FLAG, HEX_Type.FORT]):
                        tile.set_current_value(tile.get_current_value()+1)
                    elif(self.current_tick % 25 == 0):
                        tile.set_current_value(tile.get_current_value()+1)
            players_edits.append(single_player_edits)
        return players_edits # Returns a list of list of updates to be sent to players

    '''
      This function handles a single tick in production environment, it contains a lot of tricks to reduce the data sent, in an effort to increase performances
      Notice that it may be hard to understand as the tick is updated during the function. Here is a better description of the inner working of the function
      tick 0
        generate players map if needed
        send map/updates to players
        get players moves
      tick 1
        apply moves to main map
        set map updates to be sent to each player at next call
        update players maps around moves and values of seen tile
        update main map values of all tiles
      repeat

      updating the main map with only the moves, then the whole player map, and only then the values in the main map
      allows to copy from the main map only the tiles around the moves, while updating all others. This considerably speeds up the code.
    '''
    async def async_tick(self):
        moves = []
        edited_hex = set()  # This is for the web map
        ts = []
        if(self.last_tick_deads):
            # If someone died it is easier to regenerate all maps
            self.generate_all_players_maps()
        for player in range(PLAYERS):
            # At first tick, send whole map, or when someone died
            if(self.current_tick == 0 or self.last_tick_deads):
                ts.append(self.player_controllers[player].tick_map(
                    self.current_tick))  # Send whole map to every player
            else:
                ts.append(self.player_controllers[player].tick(
                    self.current_tick))  # Send only updates to every player
        if(self.last_tick_deads):
            self.last_tick_deads = False  # FIXME if this is used in the coroutines stored in ts this will lead to a race condition, maybe move after await
        moves = await asyncio.gather(*ts)  # Wait for all moves  # FIXME coroutine errors are not catched, consider return_exceptions=False
        self.current_tick += 1  # Next tick
        for player_move in moves:
            edited_hex.add(player_move[0])  # This is for the web app
            edited_hex.add(player_move[1])
        for player in range(PLAYERS):
            if(self.player_controllers[player].dead == False):  # FIXME maybe do not call tick_map and tick to avoid waiting untill timeout if dead players stop responding, since thelist of awaitables can't have holes because of the player id logic consider making a dummy call like lambda: [] that returns empty moves and ends instantly
                edited_hex |= self.do_move(
                    player, moves[player])  # Do all moves
        # Update every player's map and return updated tiles
        updates = self.update_players_maps(moves)  # FIXME sending updates to all players will leak start and end tiles for all moves in not visible tiles
        for player in range(PLAYERS):
            if(self.player_controllers[player].dead == False):
                # Set update to be sent to players at next tick
                self.player_controllers[player].set_update(updates[player])
        edited_hex |= self.update_map()  # Update global map count on every tile
        # FIXME consider updating the actualmap completely before any of the player maps:
        # FIXME do_move should filter the moves, calculate edited_hex
        # FIXME update_map should then be run and calculate its edited_hex and be called at the end but inside do_move (maybe rename do_move to update_map) so that updates already include new troups
        # FIXME after that for each edited_hex calculate the players that actually own a tile near or at the edited tile and add or remove visible tiles accordingly taking crystals into account
        # FIXME while doing this in a list of lists (alist per player) record visibility changes when a visible tile was in a player's visible_tiles_set and was actually removed
        # FIXME at this point visible_tiles_sets are correctly updated
        # FIXME update_players_maps shoulditerate for all players then should iterate over edited_hex and not moves,
        # FIXME if edited tile is in player's visible_tiles_set then add this tile to the updates
        # FIXME since both edited_hex and visible_tiles_set are sets something like edited_hex && visible_tiles_set could be done
        # FIXME include the recorded player visibility deletion previously recorded and sent custom updates to each player
        # FIXME this should simplify somewhat the logic and make it faster iterating only when needed
        self.history.append(self.map.serializable_partial(
            edited_hex))  # Add to web map history
    '''
      This function does the same as the above function, except that it is used only for local testing and does not require all optimizations.
      You can see a description of the inner working

      tick 0
        generate players maps
        send map to players
        get players moves
      tick 1
        apply moves to main map
        update players maps around moves and values of seen tile
        update main map values of all tiles
      repeat
    '''
    def tick(self):  # This is simple to test the bot, it sends the whole map at each tick and the moves are done sequentially
        self.current_tick += 1
        print(self.current_tick)
        moves = []
        edited_hex = set()
        if(self.last_tick_deads):  # TODO verify this can only be true
            self.last_tick_deads = False
            self.generate_all_players_maps()
        for player in range(PLAYERS):
            player_move = self.player_controllers[player].tick(
                self.current_tick)
            moves.append(player_move)
            edited_hex.add(player_move[0])
            edited_hex.add(player_move[1])
        for player in range(PLAYERS):
            if(self.player_controllers[player].dead == False):
                edited_hex |= self.do_move(player, moves[player])
        self.update_players_maps(moves)
        edited_hex |= self.update_map()
        self.history.append(self.map.serializable_partial(edited_hex))

    def run(self): # Use this for local testing
        for x in range(PLAYERS):
            self.add_player(Player(x, "./bot.py")) # Load all bots, they are all equal, feel free to change this if you want to experiment with different types of bots
        print("Starting simulation")
        self.generate_all_players_maps() # Generate initial maps
        start = time.time()
        for i in range(SIMULATION_LENGTH): # Play until everyone but one is dead, or time limit is reached
            if(len(self.dead_order) >= PLAYERS-1):
                break
            self.tick()
        print(f"Simulation ended in {time.time()-start}")
        self.json_serialize_history('./history.json') # Write results
        self.generate_results("./scoreboard.json")

    async def run_async(self, players): # This is for production enviroment
        for x in range(PLAYERS):  # Load all players remotely
            self.add_player(
                Player(x, f"ws://player{players[x]}:8765/", ID_MAP[players[x]], players[x]))
        for x in range(PLAYERS):
            try:
                # Connect to players
                await asyncio.wait_for(self.player_controllers[x].connect(), timeout=5.0)  # FIXME not parallel, will wait up to 5s * player count
            except Exception:
                print(f"Player {x} failed to connect!")
                self.player_controllers[x].dead = True # Sorry buddy
                self.dead_order.append(x)
        self.generate_all_players_maps()  # Generate every map
        print("Starting simulation")
        start = time.time()
        for i in range(SIMULATION_LENGTH): # Play until everyone but one is dead or time is up
            if(len(self.dead_order) >= PLAYERS-1):
                break
            await self.async_tick()
        print(f"Simulation ended in {time.time()-start}")
        path = os.environ.get("HISTORY_PATH") # Write results for web app to load
        if(path == None):
            path = './frontend/history.json'
        self.json_serialize_history(path)
        scoreboard = os.environ.get("SCOREBOARD_PATH")
        if(scoreboard == None):
            scoreboard = "./frontend/scoreboard.json"
        self.generate_results(scoreboard)

    def generate_results(self, path):
        scoreboard = []
        for x in self.dead_order:
            scoreboard.append({"ID": x, "real_ID": self.player_controllers[x].real_ID, "name": self.player_controllers[
                              x].name, "preferred_name": self.player_controllers[x].preferred_name, "land": 0, "power": 0})
        players_score = {}
        for x in range(PLAYERS):
            tot_land = sum(
                [1 if y.get_owner_ID() == x else 0 for y in self.map.hash_map.values()])
            tot_power = sum([y.get_current_value() if y.get_owner_ID() == x else 0 for y in self.map.hash_map.values()])
            players_score[x] = {"land": tot_land, "power": tot_power}
        players = range(PLAYERS)
        players = sorted(players, key=lambda x: (
            self.player_controllers[x].dead == False, players_score[x]["power"], players_score[x]["land"]))
        for player in players:
            if(self.player_controllers[player].dead == False):
                scoreboard.append({"ID": player, "real_ID": self.player_controllers[player].real_ID, "name": self.player_controllers[player].name,
                                  "preferred_name": self.player_controllers[player].preferred_name, "land": players_score[player]["land"], "power": players_score[player]["power"]})
        scoreboard = scoreboard[::-1]
        print(scoreboard)
        f = open(path, "w")
        scoreboard = json.dumps(scoreboard)
        f.write(scoreboard)
        f.close()

    # This applies all moves in sequence. It leads to some inconsistencies in some very specific cases, but who cares?
    def do_move(self, player, move):
        edited_hex = set()
        try:
            hex_start = self.map[move[0]]
            hex_end = self.map[move[1]]
        except Exception:
            return edited_hex
        if(hex_start.get_owner_ID() == player and hex_start.get_current_value() > 1 and hex_end.get_point_type() != HEX_Type.WALL and move[1] in hex_start.get_neighbors()):
            amount = hex_start.get_current_value()-1
            hex_start.set_current_value(1)
            if(hex_end.get_owner_ID() == None):
                if(hex_end.get_point_type() != HEX_Type.FORT):  # FIXME this will not support trups in non owned tiles myabe just check values alwais. generalizing this checks
                    hex_end.set_owner_ID(player)
                    hex_end.set_current_value(amount)
                else:
                    hex_end.set_current_value(
                        hex_end.get_current_value()-amount)
                    if(hex_end.get_current_value() < 0):
                        hex_end.set_owner_ID(player)
                        hex_end.set_current_value(
                            abs(hex_end.get_current_value()))
            else:
                if(hex_end.get_owner_ID() == player):
                    hex_end.set_current_value(
                        hex_end.get_current_value()+amount)
                else:
                    hex_end.set_current_value(
                        hex_end.get_current_value()-amount)
                    if(hex_end.get_current_value() < 0):
                        if(hex_end.get_point_type() == HEX_Type.FLAG):
                            self.last_tick_deads = True
                            print(
                                f"Player {hex_end.get_owner_ID()} has been killed by {player} at tick {self.current_tick}!")
                            self.dead_order.append(hex_end.get_owner_ID())
                            self.player_controllers[hex_end.get_owner_ID(
                            )].dead = True
                            old_owner = hex_end.get_owner_ID()
                            for tile in self.player_controllers[old_owner].seen_tiles:
                                if(self.map[tile].get_owner_ID() == old_owner):
                                    self.map[tile].set_owner_ID(player)
                                    edited_hex.add(tile)
                            hex_end.set_point_type(HEX_Type.FORT)
                        hex_end.set_owner_ID(player)
                        hex_end.set_current_value(
                            abs(hex_end.get_current_value()))

            # if(hex_end.get_owner_ID() == player and (not hex_end.get_point_type() in self.player_crystals[player]) and hex_end.get_point_type() in [HEX_Type.CRYPTO_CRYSTAL, HEX_Type.REV_CRYSTAL, HEX_Type.WEB_CRYSTAL, HEX_Type.MISC_CRYSTAL, HEX_Type.PWN_CRYSTAL] and hex_end.get_point_type() not in self.player_crystals[player]):  # FIXME duplicate not already owned player ristal check
            if(hex_end.get_owner_ID() == player and hex_end.get_point_type() not in self.player_crystals[player] and hex_end.get_point_type() in [HEX_Type.CRYPTO_CRYSTAL, HEX_Type.REV_CRYSTAL, HEX_Type.WEB_CRYSTAL, HEX_Type.MISC_CRYSTAL, HEX_Type.PWN_CRYSTAL]):
                self.player_crystals[player].append(hex_end.get_point_type())
        return edited_hex

    # Updates global map's values
    def update_map(self):
        edited_hex = set()
        for tile in self.map.hash_map.values():
            # if(tile.get_owner_ID() != None):  # FIXME use is not None
            if(tile.get_owner_ID() is not None):
                if(tile.get_point_type() in [HEX_Type.FLAG, HEX_Type.FORT]):
                    tile.set_current_value(tile.get_current_value()+1)
                    edited_hex.add(tile.get_position_tuple())
                elif(self.current_tick % 25 == 0):
                    tile.set_current_value(tile.get_current_value()+1)
                    edited_hex.add(tile.get_position_tuple())
        return edited_hex

    def get_map(self):
        return self.map

    def get_player_spawns(self):
        return self.player_spawns

    def json_serialize_history(self, filename):
        # json.dump(self.history, open(filename, 'w'))  # FIXME: this file is never closed
        with open(filename, 'w') as f:
            json.dump(self.history, f)
