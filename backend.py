from Hex import Hex
from config import *
from player import Player
from map import Map
from game import Game
from hex_types import *
from debug import plot
from lloyd import *
import imageio
import os
import time

# os.system("RMDIR /Q/S global")
# os.system("RMDIR /Q/S players")
# os.mkdir("global")
# os.mkdir("players")
# for x in range(PLAYERS):
#     os.mkdir(f"players/{x}")

# filenames = []




game = Game()
# for x in range(PLAYERS):
#     game.add_player(Player(x, "./random_bot.py"))

for x in range(PLAYERS):
    game.add_player(Player(x, "ws://localhost:8765/"))

game.generate_all_players_maps()


print("Starting simulation")

start=time.time()
for i in range(SIMULATION_LENGTH):
    game.tick()
print(time.time()-start)
#plot(game.get_map(), "global/map.png")
# for player in range(PLAYERS):
#     plot(game.player_controllers[player].get_map(), f"players/{player}/{SIMULATION_LENGTH}.png")
game.json_serialize_history('frontend/history.json')


""" 
for x in range(PLAYERS):
    with imageio.get_writer(f'gifs/player{x}.gif', mode='I') as writer:
        filenames=[f"players/{x}/{_}.png" for _ in range(1, SIMULATION_LENGTH+1)]
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)

 """


