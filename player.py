import importlib.util
import sys
from config import *

import websockets
import asyncio
import json
import pickle
import time

class TestingPlayer():
    def __init__(self, ID, controller):
        self.player_id = ID
        self.player_map=None
        self.seen_tiles=set()
        self.dead=False
        self.name=str(ID)
        self.real_ID=ID
        self.preferred_name=self.name
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
    def __init__(self, ID, uri, name, real_ID):
        self.player_id = ID
        self.player_map=None
        self.seen_tiles=set()
        self.dead=False
        self.websocket=None
        self.name=name
        self.uri=uri
        self.update=[]
        self.preferred_name=name
        self.real_ID=real_ID

    async def connect(self):
        print(f"Connecting to {self.uri}")
        self.websocket=await websockets.connect(self.uri)
        await self.websocket.send("HELO")
        self.preferred_name=await self.websocket.recv()
        print(f"Player {self.name} connected as {self.preferred_name}!")
    
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
        data=pickle.dumps(tick)
        await self.websocket.send(data)
        try:
            move=json.loads(await asyncio.wait_for(self.websocket.recv(), timeout=0.1)) 
            if("start" in move and len(move["start"])==3 and "end" in move and len(move["end"])==3):
                return ((move["start"][0], move["start"][1], move["start"][2]), (move["end"][0], move["end"][1], move["end"][2]))
            return ((0,0,0), (0,0,0))
        except Exception:
            return ((0,0,0), (0,0,0))

    def set_map(self, map):
        self.player_map=map
    
    def get_map(self):
        return self.player_map
    
    def set_update(self, update):
        self.update=update

Player=RemotePlayer
if(DEBUG):
    Player=TestingPlayer
