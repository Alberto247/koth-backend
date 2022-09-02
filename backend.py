from config import *

from game import Game
from hex_types import *
from lloyd import *
import time
import asyncio

game = Game()




if(DEBUG):
    game.run()
else:
    time.sleep(10)
    asyncio.run(game.run_async())



