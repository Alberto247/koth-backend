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


game = Game()
for x in range(PLAYERS):
    game.add_player(Player(x, "./random_bot.py"))

game.generate_all_players_maps()

""" game.tick()
plot(game.get_map())
input()
game.tick()
plot(game.get_map())
input()
game.tick()
plot(game.get_map())
input()
game.tick()
plot(game.get_map())
input()
game.tick()
plot(game.get_map())
input() """

os.system("RMDIR /Q/S global")
os.system("RMDIR /Q/S players")
os.mkdir("global")
os.mkdir("players")
for x in range(PLAYERS):
    os.mkdir(f"players/{x}")

filenames = []
print("Starting simulation")

start = time.time()
for i in range(SIMULATION_LENGTH):
    plot(game.get_map(), f"global/{i}.png")
    filenames.append(f"global/{i}.png")
    game.tick()
print(time.time()-start)

with imageio.get_writer('gifs/global.gif', mode='I') as writer:
    for filename in filenames:
        image = imageio.imread(filename)
        writer.append_data(image)

""" 
for x in range(PLAYERS):
    with imageio.get_writer(f'gifs/player{x}.gif', mode='I') as writer:
        filenames=[f"players/{x}/{_}.png" for _ in range(1, SIMULATION_LENGTH+1)]
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)

 """


game.json_serialize_history('frontend/history.json')
