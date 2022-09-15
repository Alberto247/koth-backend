import json
import docker
import os
import random
PLAYERS=16

passwords=json.load(open("passwords.json", "r"))
networks={}
client=docker.from_env()
print(client.images.build(path="../", dockerfile="Dockerfile", tag=f"kothbackend:latest"))
next_round=0
if(not os.path.exists("./results/complete_rounds.json")):
    f=open("./results/complete_rounds.json", "w")
    f.write("[]")
    f.close()
else:
    data=json.load(open("./results/complete_rounds.json", "r"))
    if(len(data)>0):
        next_round=max(data)+1


def recreate_networks():
    client.networks.prune()
    for x in range(1, PLAYERS+1):
        networks[x]=client.networks.create(f"koth-client{x}", driver="bridge")

def update_images():
    for x in range(PLAYERS):
        print(client.images.pull(f"team{x+1}.registry.alberto247.xyz:7394/bot/bot:latest", auth_config={"username":f"team{x+1}", "password":passwords[x]}))

def handle_game(players, history, scoreboard, prefix):
    player_images={}
    print("Creating player containers")
    for player in players:
        player_images[player]=client.containers.run(f"team{player}.registry.alberto247.xyz:7394/bot/bot:latest", name=f"{prefix}-bot-team{player}", environment=[f"name=team{player}"], hostname=f"player{player}", network=f"koth-client{player}", mem_limit="2g", nano_cpus=2000000000, detach=True) #TODO: limits
    print("Creating backend container")
    backend=client.containers.run("kothbackend:latest", name=f"{prefix}-kothbackend", environment=[f"PLAYERS={','.join([str(_) for _ in players])}", "HISTORY_PATH="+history, "SCOREBOARD_PATH="+scoreboard], volumes=[os.getcwd()+'/results:/results'], detach=True)
    for player in players:
        networks[player].connect(backend)
    return {"backend":backend, "players":player_images}

def handle_round(round_ID):
    print("Recreating networks")
    recreate_networks()
    print("Updating images")
    update_images()
    players=list(range(1, 17))
    random.shuffle(players)
    game1=players[:4]
    game2=players[4:8]
    game3=players[8:12]
    game4=players[12:]
    games=[game1, game2, game3, game4]
    games_containers=[]
    for game in range(4):
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
        containers["backend"].wait()
        print(f"Game {game} ended")
        f=open(f"./results/{round_ID}/logs/backend-game-{game}.logs", "w")
        f.write(containers["backend"].logs().decode())
        f.close()
        containers["backend"].remove()
        for team in containers["players"].keys():
            try:
                containers["players"][team].kill()
            except Exception:
                pass
            f=open(f"./results/{round_ID}/logs/team-{team}-game-{game}.logs", "w")
            f.write(containers["players"][team].logs().decode())
            f.close()
            containers["players"][team].remove()
        f=open(f"./results/{round_ID}/scoreboard_game_{game}.json", "r")
        scoreboards.append(json.load(f))
        f.close()
    finalists=[]
    for scoreboard in scoreboards:
        finalists.append(scoreboard.pop(0)["real_ID"])
    print(f"Preparing game final for round {round_ID} with players {finalists}")
    containers=handle_game(finalists, f"/results/{round_ID}/history_game_final.json", f"/results/{round_ID}/scoreboard_game_final.json", f"game-final")
    containers["backend"].wait()
    print(f"Game final ended")
    f=open(f"./results/{round_ID}/logs/backend-game-final.logs", "w")
    f.write(containers["backend"].logs().decode())
    f.close()
    containers["backend"].remove()
    for team in containers["players"].keys():
        try:
            containers["players"][team].kill()
        except Exception:
            pass
        f=open(f"./results/{round_ID}/logs/team-{team}-game-final.logs", "w")
        f.write(containers["players"][team].logs().decode())
        f.close()
        containers["players"][team].remove()
    f=open(f"./results/{round_ID}/scoreboard_game_final.json", "r")
    scoreboard_final=json.load(f)
    f.close()
    final_scoreboard={1:[scoreboard_final[0]], 2:[scoreboard_final[1]], 3:[scoreboard_final[2]], 4:[scoreboard_final[3]]}
    final_scoreboard[5]=[scoreboard[0] for scoreboard in scoreboards]
    final_scoreboard[6]=[scoreboard[1] for scoreboard in scoreboards]
    final_scoreboard[7]=[scoreboard[2] for scoreboard in scoreboards]
    f=open(f"./results/{round_ID}/scoreboard_final.json", "w")
    f.write(json.dumps(final_scoreboard))
    f.close()
    print("Scoreboard written to file")
    f=open(f"./results/complete_rounds.json", "r")
    data=json.loads(f.read())
    data.append(round_ID)
    f.close()
    f=open(f"./results/complete_rounds.json", "w")
    f.write(json.dumps(data))
    f.close()
    f=open(f"./results/{round_ID}/available_games.json", "w")
    f.write(json.dumps(["0", "1", "2", "3", "final"]))
    f.close()


for x in range(next_round, 100):
    try:
        handle_round(x)
    except Exception as e:
        print(e)
        pass