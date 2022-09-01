from debug import *
import importlib.util
import sys

import websockets
import asyncio
import json
import pickle

# suppongo di essere sempre il tizio 0 
# innanzitutto non supponi un cazzo te
class TestingPlayer():
    def __init__(self, controller):
        self.player_id = ID
        self.player_map=None
        self.seen_tiles=set()
        self.dead=False
        spec = importlib.util.spec_from_file_location("module.name", controller)
        bot_controller = importlib.util.module_from_spec(spec)
        sys.modules["module.name"] = bot_controller
        spec.loader.exec_module(bot_controller)
        self.controller=bot_controller.Bot()
    
    def tick(self, tick):
        if(self.dead):
            return ((0,0,0), (0,0,0))
        return self.controller.tick({"map":self.player_map, "ID":self.player_id, "tick":tick})
    
    def set_map(self, map):
        self.player_map=map
    
    def get_map(self):
        return self.player_map

class RemotePlayer():
    def __init__(self, ID, uri):
        self.player_id = ID
        self.player_map=None
        self.seen_tiles=set()
        self.dead=False
        self.websocket=None
        self.name=asyncio.get_event_loop().run_until_complete(self.connect(uri))

    async def connect(self, uri):
        self.websocket=await websockets.connect(uri)
        await self.websocket.send("HELO")
        name=await self.websocket.recv()
        print(f"Player {name} connected!")
        return name
    
    def tick(self, tick):
        if(self.dead):
            return ((0,0,0), (0,0,0))
        return asyncio.get_event_loop().run_until_complete(self.send_tick({"map":self.player_map, "ID":self.player_id, "tick":tick}))
    
    async def send_tick(self, tick):
        await self.websocket.send(pickle.dumps(tick))
        move=json.loads(await self.websocket.recv()) # TODO: timeout
        return ((move["start"][0], move["start"][1], move["start"][2]), (move["end"][0], move["end"][1], move["end"][2]))

    
    def set_map(self, map):
        self.player_map=map
    
    def get_map(self):
        return self.player_map

Player=RemotePlayer