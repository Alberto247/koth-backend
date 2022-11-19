import time
PLAYERS=12
ROUND_LENGTH=5*60 # Length of a round, this needs to be grater than the time needed for a round to run or else it won't be respected
FREEZE_TIME=60*60*7 # Time to freeze the scoreboard (in seconds after the start)
START_TIME=1668765600 # Set this correctly
END_TIME=START_TIME+60*60*10
FREEZE_ROUND=FREEZE_TIME//ROUND_LENGTH
POSITIONS_POINTS={1:10, 2:5, 3:3, 4:2, 5:1, 6:0, 7:0}