import importlib.util
import sys
from config import *

import websockets
import asyncio
import json
import pickle
import time
from map import Map

# suppongo di essere sempre il tizio 0 
# innanzitutto non supponi un cazzo te
class TestingPlayer():
    def __init__(self, ID, controller):
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
        self.name=None
        self.uri=uri
        self.update=[]

    async def connect(self):
        self.websocket=await websockets.connect(self.uri)
        await self.websocket.send("HELO")
        self.name=await self.websocket.recv()
        print(f"Player {self.name} connected!")
    
    async def tick_map(self, tick):
        if(self.dead):
            return ((0,0,0), (0,0,0))
        move=await self.send_tick({"map":self.player_map, "ID":self.player_id, "tick":tick, "type":"map"})
        return move
    
    async def tick(self, tick):
        if(self.dead):
            return ((0,0,0), (0,0,0))
        move=await self.send_tick({"updates":self.update, "ID":self.player_id, "tick":tick, "type":"update"})
        return move
    
    async def send_tick(self, tick):
        start=time.time()
        data=pickle.dumps(tick)
        unpickle=time.time()
        await self.websocket.send(data)
        try:
            move=json.loads(await asyncio.wait_for(self.websocket.recv()), timeout=0.1) 
            #print(f"send_tick: Time to pickle {unpickle-start}, time to receive response: {time.time()-unpickle}")
            return ((move["start"][0], move["start"][1], move["start"][2]), (move["end"][0], move["end"][1], move["end"][2]))
        except asyncio.TimeoutError:
            return ((0,0,0),(0,0,0))

    def set_map(self, map):
        self.player_map=map
    
    def get_map(self):
        return self.player_map
    
    def set_update(self, update):
        self.update=update

Player=RemotePlayer
if(DEBUG):
    Player=TestingPlayer
