from enum import Enum

class HEX_Type(int, Enum):
    UNKNOWN_OBJECT = -2
    UNKNOWN_EMPTY = -1
    GRASS = 0
    WALL = 1
    FORT = 2
    CRYPTO_CRYSTAL = 3
    WEB_CRYSTAL = 4
    REV_CRYSTAL = 5
    PWN_CRYSTAL = 6
    MISC_CRYSTAL = 7
    FLAG=100