import asyncio
import websockets
from bot import Bot
import pickle
import json
import time
from Hex import Hex
import copy
from hex_types import HEX_Type
import os

class RemotePlayerAdapter():
    def __init__(self, port):
        start_server = websockets.serve(self.handle_messages, '0.0.0.0', port)
        self.player=Bot()
        self.map=None
        self.seen_tiles=set()
        os.system(f"rm -rf /debug/{self.player.player_name}")
        os.system(f"mkdir /debug/{self.player.player_name}")
        print(f"Booting player {self.player.player_name} on port {port}")
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()


    def update_map(self, updates, tick):
        for update in updates:
            if(self.map[update[0]].get_point_type() in [HEX_Type.UNKNOWN_EMPTY, HEX_Type.UNKNOWN_OBJECT] and update[1] not in [HEX_Type.UNKNOWN_EMPTY, HEX_Type.UNKNOWN_OBJECT]):
                self.seen_tiles.add(update[0])
            elif (self.map[update[0]].get_point_type() not in [HEX_Type.UNKNOWN_EMPTY, HEX_Type.UNKNOWN_OBJECT] and update[1] in [HEX_Type.UNKNOWN_EMPTY, HEX_Type.UNKNOWN_OBJECT]):
                self.seen_tiles.discard(update[0])
            self.map[update[0]]=Hex(*update)
        for tile_tuple in self.seen_tiles:
            tile=self.map[tile_tuple]
            if(tile.get_owner_ID()!=None):
                if(tile.get_point_type() in [HEX_Type.FLAG, HEX_Type.FORT]):
                        tile.set_current_value(tile.get_current_value()+1)
                elif(tick%25==0):
                    tile.set_current_value(tile.get_current_value()+1)
        
    def set_map(self, map):
        self.seen_tiles=set()
        self.map=copy.deepcopy(map)
        for tile in map.hash_map.keys():
            if(map[tile].get_point_type() not in [HEX_Type.UNKNOWN_EMPTY, HEX_Type.UNKNOWN_OBJECT]):
                self.seen_tiles.add(tile)
    
    async def handle_messages(self, websocket, path): # TODO: handle game end properly without crashing, maybe send message
        try:
            conn_msg=await websocket.recv()
            print(f"Connection received, message: {conn_msg}") # TODO: verify it is the server connecting or avoid connections from other players
            await websocket.send(self.player.get_player_name())
            while(True):
                data=await websocket.recv()
                data=pickle.loads(data)
                if(data["type"]=="map"):
                    self.set_map(data["map"]) 
                else:
                    self.update_map(data["updates"], data["tick"])
                #json.dump(self.map.serializable(), open(f"/debug/{self.player.player_name}/{data['tick']}.json", 'w'))
                move=self.player.tick({"map":self.map, "ID":data["ID"], "tick":data["tick"]})
                await websocket.send(json.dumps({"start":[move[0][0],move[0][1], move[0][2]], "end":[move[1][0],move[1][1], move[1][2]]}))
        except websockets.exceptions.ConnectionClosedError:
            return

RemotePlayerAdapter(8765)