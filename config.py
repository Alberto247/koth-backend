'''
    The map generation configs you see here are equal to the ones in the backend. Feel free to change them if you want to.
'''
import os
SIDE = 15  # Map size, if you change this expect many things to break in the frontend when you upload your replay
PLAYERS = 4 if os.environ.get("PLAYERS") is None else len(os.environ.get("PLAYERS").split(","))  # Number of players
PLAYER_DISTANCE = 15 # Number of iterations of lloyd's algorithm
MOUNTAIN_DENSITY = 0.30 # Density of mountains, between 0 and 1 excluded
MOUNTAIN_LINKAGE = 5 # How often the mountains will form mountain ranges
FORT_DENSITY = 0.05 # Density of forts, between 0 and 1 excluded
MIN_FORT_COST = 40 # Minimum cost to capture a fort
MAX_FORT_COST = 50 # Maximum cost to capture a fort
SIMULATION_LENGTH = 1000 # Maximum length of the game
DEBUG = False  # True loads bots from their classes files, without timeout on the moves. False works with the websockets as in the infrastructure. To test please use Debug=True
ID_MAP = {1: "Alberto247", # Used only to map colors
          2: "mr96",
          3: "matpro",
          4: "0000matteo0000",
          5: "hdesk",
          6: "Matte23",
          7: "SolidCinder7914",
          8: "Xato",
          9: "Drago_1729",
          10: "Ravn",
          11: "Giotino",
          12: "team12"
          }
