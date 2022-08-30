from debug import *
import importlib.util
import sys



# suppongo di essere sempre il tizio 0 
# innanzitutto non supponi un cazzo te
class Player():
    def __init__(self, ID, controller):
        self.player_id = ID
        self.player_map=None
        spec = importlib.util.spec_from_file_location("module.name", controller)
        bot_controller = importlib.util.module_from_spec(spec)
        sys.modules["module.name"] = bot_controller
        spec.loader.exec_module(bot_controller)
        self.controller=bot_controller.Bot(self.player_id)
    
    def tick(self, tick):
        return self.controller.tick({"map":self.player_map, "ID":self.player_id, "tick":tick})
    
    def set_map(self, map):
        self.player_map=map
    
    def get_map(self):
        return self.player_map

