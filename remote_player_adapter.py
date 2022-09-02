import asyncio
import websockets
from bot import Bot
import pickle
import json

class RemotePlayerAdapter():
    def __init__(self, port):
        start_server = websockets.serve(self.handle_messages, '0.0.0.0', port)
        self.player=Bot()
        print(f"Booting player {self.player.player_name} on port {port}")
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
        
    
    async def handle_messages(self, websocket, path): # TODO: handle game end properly without crashing, maybe send message
        try:
            conn_msg=await websocket.recv()
            print(f"Connection received, message: {conn_msg}") # TODO: verify it is the server connecting or avoid connections from other players
            await websocket.send(self.player.get_player_name())
            while(True):
                data=pickle.loads(await websocket.recv())
                move=self.player.tick(data)
                await websocket.send(json.dumps({"start":[move[0][0],move[0][1], move[0][2]], "end":[move[1][0],move[1][1], move[1][2]]}))
        except websockets.exceptions.ConnectionClosedError:
            return

RemotePlayerAdapter(8765)