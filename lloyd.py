from Hex import *
from config import *


def compute_voronoi(map, players_positions):
    for q in range(-SIDE, SIDE+1):
        for r in range(-SIDE, SIDE+1):
            s = -(q+r)
            if(-SIDE <= s <= SIDE):
                hex = map[(q, r, s)]
                min_distance = SIDE*2
                min_distance_player = -1
                for x in range(len(players_positions)):
                    tmp = hex_distance(hex, map[players_positions[x]])
                    if(tmp < min_distance):
                        min_distance = tmp
                        min_distance_player = x
                hex.set_owner_ID(min_distance_player)

def relax(map, player_spawns):
    centers = {}
    counts = {}

    for q in range(-SIDE, SIDE+1):
        for r in range(-SIDE, SIDE+1):
            s = -(q+r)
            if(-SIDE <= s <= SIDE):
                hex = map[(q, r, s)]
                if(hex.get_owner_ID() not in centers.keys()):
                    centers[hex.get_owner_ID()] = hex
                    counts[hex.get_owner_ID()] = 1
                else:
                    centers[hex.get_owner_ID()] = hex_add(
                        centers[hex.get_owner_ID()], hex)
                    counts[hex.get_owner_ID()] += 1

    for x in range(len(player_spawns)):
        centers[x] = hex_round(centers[x].q/counts[x],
                               centers[x].r/counts[x], centers[x].s/counts[x])

    for x in range(PLAYERS):  
        dist_q = player_spawns[x].q-centers[x].q
        dist_r = player_spawns[x].r-centers[x].r
        dist_s = player_spawns[x].s-centers[x].s
        dist_q_abs = abs(dist_q)
        dist_r_abs = abs(dist_r)
        dist_s_abs = abs(dist_s)
        if(dist_q_abs != 0 or dist_r_abs != 0 or dist_s_abs != 0):
            m = min(dist_q_abs, dist_r_abs, dist_s_abs)
            if(m == dist_q_abs):
                if(dist_r >= dist_s):
                    player_spawns[x].r -= 1
                    player_spawns[x].s += 1
                else:
                    player_spawns[x].r += 1
                    player_spawns[x].s -= 1
            elif(m == dist_r_abs):
                if(dist_q >= dist_s):
                    player_spawns[x].q -= 1
                    player_spawns[x].s += 1
                else:
                    player_spawns[x].q += 1
                    player_spawns[x].s -= 1
            elif(m == dist_s_abs):
                if(dist_r >= dist_q):
                    player_spawns[x].r -= 1
                    player_spawns[x].q += 1
                else:
                    player_spawns[x].r += 1
                    player_spawns[x].q -= 1
    return player_spawns

