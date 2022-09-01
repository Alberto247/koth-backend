import asyncio
import websockets
from bot import Bot
import pickle
import json

class RemotePlayerAdapter():
    def __init__(self, port):
        print(f"Booting player on port {port}")
        start_server = websockets.serve(self.handle_messages, 'localhost', port)
        self.player=Bot()
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
        
    
    async def handle_messages(self, websocket, path):
        conn_msg=await websocket.recv()
        print(f"Connection received, message: {conn_msg}") # TODO: verify it is the server connecting or avoid connections from other players
        await websocket.send(self.player.get_player_name())
        while(True):
            data=pickle.loads(await websocket.recv())
            move=self.player.tick(data)
            print(move)
            await websocket.send(json.dumps({"start":[move[0][0],move[0][1], move[0][2]], "end":[move[1][0],move[1][1], move[1][2]]}))

RemotePlayerAdapter(8765)