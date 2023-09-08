from colour import Colour
from config import update_config

#turn off and on logger module.
def toggle_logger(config):
    global config
    if (config.logger_on):
        config.logger_on = False
        print (f"{Colour().red} Logger turned off.{Colour().default}")
    else:
        config.logger_on = True
        print (f"{Colour().green} logger turned on.{Colour().default}")
    update_config(config.__dict__)

#Toggle between logging all player traffic, and logging specified player traffic
def toggle_all_players():
    global config
    if (config.logall_on):
        config.logall_on = False
        currently_online_flush()
        print (f"{Colour().red} Log All Players Off.{Colour().default}")
    else:
        config.logall_on = True
        print (f"{Colour().green} Log All Players On.{Colour().default}")
    update_config(config.__dict__)