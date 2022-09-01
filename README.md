# File content:

 - backend.py : handles multiple games, loads the Game class, instantiates the players, runs ticks
 - bot.py : class for the remote Bot, it loads the proper file as the Bot
 - config.py : global game config
 - debug.py : plotting and logging in debug
 - game.py : handles map generation and ticks
 - hex_types.py : enum for tile types
 - Hex.py : single tile class
 - lloyd.py : handles lloyd's algorithm for distance
 - map.py : collection and handling of Hex objects
 - player.py : allows choosing between TestPlayer (local) and RemotePlayer(remote)
 - random_bot.py : bot example doing random movements
 - remote_player_adapter.py : code running remotely handling the websocket

