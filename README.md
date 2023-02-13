# Info

This is a project developed for m0lecon 2023, a cybersecurity competition organized by pwnthem0le (pwnthem0le.polito.it)
It is a king of the hill game, where players are supposed to upload a bot, which will play against the other bots every N minutes.
It contains the frontend to replay games and the backend to handle them.
The code was open source to all the teams (stripped of comments) and included two intended vulnerabilities:
 - The random was breakable by knowing the location of some landmarks
 - The players moves were anonymized but wrongly sent to all players instead of only the ones intended to see them, leading to a leak of information, which however was pretty hard to use properly.

The code is free to use and modify, but be aware of the intended vulnerabilities (and, possibly, of unintended ones, altough none were found in the 12 hours of competition). :)

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

# File structure

 - dist directory contains all files to distribute to teams
 - bots directory contains some example bots
 - deploy directory contains all files to deploy the game
 - deploy/results is the result directory
 - deploy/webbackend is the backend serving the results directory
 - deploy/webfrontend is the react frontend
 - deploy/scoreboard-server exposes the scoreboard to be used by other services
 - debug directory contains a verifier to check that the code is behaving properly and all bots see what they are expected to see

# How to deploy

You will need an https certificate to deploy the registries, you can configure it in nginx.conf
 
   1. cd deploy/webfrontend && npm i && npm run build && cd .. 
   2. rm rf passwords.json auth/team*
   3. python3 setup_all.py
   4. copy content of passwords.json into deploy/webbackend/index.js
   5. docker-compose up --build -d
   6. python3 setup_all.py
   7. Setup correctly in config_game.py
   8. python3 game_handler.py

# Changing player names

Players name (in accordance with the best programming practices, which we always follow here at pwnthem0le) are stored in a number of different places and all needs to be updated for everything to be synced.
Here is a list of files where the names must be set correctly
 - ./config.py
 - ./dist/config.py
 - ./deploy/webbackend/index.js
 - ./deploy/webfrontend/src/config.js

# Changing the number of players

Changing the number of players currently is not trivial.
This is a short description of the procedure, but it may need some inventive on your side as the round structure (semi-finals and final) is tied to the current number of 12 teams.

 1. Change player names in all files above
 2. Change number of players in ./config.py ./dist/config.py ./deploy/config_game.py
 3. Change number of registries in docker-compose.yml
 4. In game hander, rows 155 and 169, change 12 to the new number (for the nop team to be mapped to 0, you can ignore this if you don't need it)
 5. Change ./deploy/game_handler.py to handle games differently based on your schema

# Game vs round

As usual, with respect to good programming practices, game and round have different meaning in different files, to give a better headache to anyone trying to set-up everything, don't trust anything you read on this subject :)
