from config import *
import json

for tick in range(SIMULATION_LENGTH):
    print(tick)
    for bot in range(PLAYERS):
        backend=json.load(open(f"./debug/backend/{bot}/{tick}.json", "r"))
        bot_json=json.load(open(f"./debug/bot{bot+1}/{tick}.json", "r"))
        if(backend!=bot_json):
            print(f"Difference at tick {tick} for player {bot}!")
            for x in range(len(backend)):
                if(backend[x]!=bot_json[x]):
                    print(backend[x], bot_json[x])
            