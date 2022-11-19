import json
import docker
import os
import random
import time
from config_game import *

passwords=json.load(open("passwords.json", "r")) # Load passwords for the registries
networks={}
client=docker.from_env()
print(client.images.build(path="../", dockerfile="Dockerfile", tag=f"kothbackend:latest")) # Build backend
next_round=0
if(not os.path.exists("./results/complete_rounds.json")): # Complete rounds is for the frontend to know which games are ready
    f=open("./results/complete_rounds.json", "w")
    f.write("[]")
    f.close()
else:
    data=json.load(open("./results/complete_rounds.json", "r"))
    if(len(data)>0):
        next_round=max(data)+1 #If it already exists, start from next game not complete to avoid overwriting!

if(not os.path.exists("./results/current_scoreboard.json")): # Current scoreboard is the unfrozen one
    f=open("./results/current_scoreboard.json", "w")
    data=[{"teamId":_, "score":0} for _ in range(PLAYERS)]
    f.write(json.dumps(data))
    f.close()

if(not os.path.exists("./results/user_scoreboard.json")): # User scoreboard is the frozen one
    f=open("./results/user_scoreboard.json", "w")
    data=[{"teamId":_, "score":0} for _ in range(PLAYERS)]
    f.write(json.dumps(data))
    f.close()


def recreate_networks(): # Delete and recreate all networks
    client.networks.prune()
    for x in range(1, PLAYERS+1):
        networks[x]=client.networks.create(f"koth-client{x}", driver="bridge", internal=True)

def update_images(): # Update the images from the registries
    for x in range(PLAYERS):
        print(client.images.pull(f"team{x+1}.koth.m0lecon.fans/bot/bot:latest", auth_config={"username":f"team{x+1}", "password":passwords[x]}))

def handle_game(players, history, scoreboard, prefix): # Handles a single game (or round? whatever, it makes bot play against each other for one time lol) 
    player_images={}
    print("Creating player containers")
    for player in players:
        player_images[player]=client.containers.run(f"team{player}.koth.m0lecon.fans/bot/bot:latest", name=f"{prefix}-bot-team{player}", environment=[f"name=team{player}"], hostname=f"player{player}", network=f"koth-client{player}", mem_limit="2g", nano_cpus=2000000000, detach=True) #TODO: limits
    print("Creating backend container")
    backend=client.containers.run("kothbackend:latest", name=f"{prefix}-kothbackend", environment=[f"PLAYERS={','.join([str(_) for _ in players])}", "HISTORY_PATH="+history, "SCOREBOARD_PATH="+scoreboard], volumes=[os.getcwd()+'/results:/results'], detach=True)
    for player in players:
        networks[player].connect(backend)
    return {"backend":backend, "players":player_images}

def handle_round(round_ID): # handles a single round (or was it game? Makes bots play against each other multiple times and generates a scoreboard)
    print("Recreating networks")
    recreate_networks()
    print("Updating images")
    update_images()
    players=list(range(1, 13))
    random.shuffle(players) # Randomize players!
    game1=players[:3] # You'll need to change this to handle different number of players
    game2=players[3:6]
    game3=players[6:9]
    game4=players[9:]
    games=[game1, game2, game3, game4]
    games_containers=[]
    failed=False
    for game in range(4): # You may need more or less of theese, based on the number of games. If you change this the frontend may or may not break, idk
        print(f"Preparing game {game} for round {round_ID} with players {games[game]}")
        try:
            os.mkdir(f"results/{round_ID}")
            os.mkdir(f"results/{round_ID}/logs")
        except Exception:
            pass
        containers=handle_game(games[game], f"/results/{round_ID}/history_game_{game}.json", f"/results/{round_ID}/scoreboard_game_{game}.json", f"game-{game}")
        games_containers.append(containers)
    
    scoreboards=[]
    for game in range(4):
        containers=games_containers[game]
        containers["backend"].wait() # wait for the backend to finish
        print(f"Game {game} ended")
        f=open(f"./results/{round_ID}/logs/backend-game-{game}.logs", "w") # write logs for the backend
        f.write(containers["backend"].logs().decode())
        f.close()
        containers["backend"].remove()
        for team in containers["players"].keys(): 
            try:
                print(f"Killing team {team}")
                containers["players"][team].kill() # kill them all!
            except Exception as ex:
                print(ex)
            f=open(f"./results/{round_ID}/logs/team-{team}-game-{game}.logs", "w") # write logs for each bot
            f.write(containers["players"][team].logs(tail=1000).decode())
            f.close()
            containers["players"][team].remove()
        try:
            f=open(f"./results/{round_ID}/scoreboard_game_{game}.json", "r") # write scoreboard for game (round maybe?)
            scoreboards.append(json.load(f))
            f.close()
        except Exception:
            failed=True
    if(failed):
        return
    finalists=[]
    for scoreboard in scoreboards:
        finalists.append(scoreboard.pop(0)["real_ID"]) # get finalists
    print(f"Preparing game final for round {round_ID} with players {finalists}")
    containers=handle_game(finalists, f"/results/{round_ID}/history_game_final.json", f"/results/{round_ID}/scoreboard_game_final.json", f"game-final") # abd make them play!
    containers["backend"].wait() # again, wait for backend
    print(f"Game final ended")
    f=open(f"./results/{round_ID}/logs/backend-game-final.logs", "w") # save logs
    f.write(containers["backend"].logs().decode())
    f.close()
    containers["backend"].remove()
    for team in containers["players"].keys():
        try:
            containers["players"][team].kill() # kill them all
        except Exception:
            pass
        f=open(f"./results/{round_ID}/logs/team-{team}-game-final.logs", "w") # and save logs
        f.write(containers["players"][team].logs().decode())
        f.close()
        containers["players"][team].remove()
    try:
        f=open(f"./results/{round_ID}/scoreboard_game_final.json", "r") # and write results
        scoreboard_final=json.load(f)
        f.close()
    except Exception:
        failed=True
    if(failed):
        return
    final_scoreboard={1:[scoreboard_final[0]], 2:[scoreboard_final[1]], 3:[scoreboard_final[2]], 4:[scoreboard_final[3]]} # prepare final scoreboard
    final_scoreboard[5]=[scoreboard[0] for scoreboard in scoreboards]
    final_scoreboard[6]=[scoreboard[1] for scoreboard in scoreboards]
    f=open(f"./results/{round_ID}/scoreboard_final.json", "w") # save it
    f.write(json.dumps(final_scoreboard))
    f.close()
    f=open(f"./results/complete_rounds.json", "r") # let the frontend know we have new games
    data=json.loads(f.read())
    data.append(round_ID)
    f.close()
    f=open(f"./results/complete_rounds.json", "w")
    f.write(json.dumps(data))
    f.close()
    f=open(f"./results/current_scoreboard.json", "r") # update scoreboard
    data=json.loads(f.read())
    f.close()
    for position in final_scoreboard.keys():
        for player in final_scoreboard[position]:
            playerID=player["real_ID"]
            points=POSITIONS_POINTS[position]
            for _ in data:
                if(_["teamId"]==playerID%12):
                    _["score"]+=points
    f=open(f"./results/current_scoreboard.json", "w")
    f.write(json.dumps(data))
    f.close()
    if(FREEZE_ROUND>round_ID): # if not frozen
        f=open(f"./results/user_scoreboard.json", "r") # update user scoreboard
        data=json.loads(f.read())
        f.close()
        for position in final_scoreboard.keys():
            for player in final_scoreboard[position]:
                playerID=player["real_ID"]
                points=POSITIONS_POINTS[position]
                for _ in data:
                    if(_["teamId"]==playerID%12):
                        _["score"]+=points
        f=open(f"./results/user_scoreboard.json", "w")
        f.write(json.dumps(data))
        f.close()
    f=open(f"./results/{round_ID}/available_games.json", "w") # let the frontend know which games are available for this round (or rounds for this game, what the heck)
    f.write(json.dumps(["0", "1", "2", "3", "final"])) # Change this based on which games you have
    f.close() # Shouldn't this be saved before informing the scoreboard that the game is ready? IDK, it works apparently 
    print("Scoreboard written to file")

while(int(time.time())<START_TIME): # wait for start
    time.sleep(10)
x = next_round
while(int(time.time())<END_TIME): # wait until end
    try:
        handle_round(x) # handle round (game anyone?)
        while(int(time.time())%ROUND_LENGTH>10): # busy waiting is the best waiting
            time.sleep(5)
    except Exception as e:
        print(e)
        pass
    x=x+1
