from config import *

from game import Game
from hex_types import *
from lloyd import *
import time
import asyncio
import os


game = Game()

if(DEBUG):
    game.run()
else:
    players=os.environ.get("PLAYERS")
    if(players==None):
        players=range(PLAYERS)
    else:
        players=[int(_) for _ in players.split(",")]
    print(f"Starting game for players {players}")
    time.sleep(10)
    asyncio.run(game.run_async(players))



