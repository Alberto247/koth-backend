# Koth

## What is this game?

Koth is a king of the hill game where you control an army, trying to capture the enemy's flag.
It is played on a hexagonal map of side 15.
The game contains many features, described below.
Your objective is to write a bot able to play against other bots and capture their flags without getting killed!

## Scoring and game rules

The game is played in ticks, with no delay between them.
At every tick your bot should submit a move in less than 100 ms, failure to submit a move will result in no move being done.
Every game is composed of 4 rounds of 3 random players each. The 4 winners will play one final round against each other.
The scoring of each round is based on the death order. In case of multiple players alive at the time limit, the score is based first on number of troops,
then on the owned land's size, finally randomly.
The final score is calculated in this way:
First the final game scoreboard is used for the first 4 positions.
Then all seconds positions in the non-final games are set as 5th of equal merit.
And so on, with a final scoreboard of 6 different positions.

## Game features

The game is played on a hexagonal map, using cubic coordinates.
Each player is assigned a flag on the map. Capturing another player's flag kills him and makes all his army and land to become yours.
You can only see as far as your land extends, everything else is hidden under a fog of war. You can only see shadows where a mountain or fort is. Crystals stands over the fog, giving you vision of them.
The map contains impassable terrain, represented as mountains.
Forts are randomly placed on the map, controlled by a neutral entity. Capturing them costs a certain number of troops but allows to have some benefits described below.
Powerful magic crystals are placed on the map. They have some special vision property for who can conquer them.
All other tiles are grass.

At every tick your army increases, in particular:
 - Every tile in your control gets a soldier every 25 ticks.
 - Every fort and flag in your control gets a soldier every tick.

## Updating a bot

The bot provided is not very smart, it just moves randomly.
You can upgrade it by editing player_bot.py:
 - At every tick the function tick is called, with as data the map information. The map is a map object, as described in map.py
 - Your code should answer with a tuple of two tuples of three element each, representing start and end position, each represented as the three cubic coordinates.

You can test that your code works by running backend.py, which loads the config from config.py
Make sure that in config.py debug is set to true, to run the code in a testing environment. Note that you can't run it in a production environment.
The only difference between a testing and production environment is that the optimizations are removed and you have no timeout on the moves. 
Feel free to read the production code in all other files.
The result of backend.py is a history.json and a scoreboard.json file, you can upload them to the web app to see the game.

When your bot is ready, edit Dockerfile.bot to install the packages you need. Don't change the entrypoint, the adapter is required to run your code properly in the production environment!
You can now build, tag and push your image to the provided repository, you can see an example on how to do that in pushBot.sh.template
Keep in mind that remotely you are limited to 2 cpus and 2gb of ram!

By logging in on the web interface you can see the output of your bot for debugging remotely.

