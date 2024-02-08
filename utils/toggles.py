from .colour import Colour
from .config import update_config

#turn off and on logger module.
def toggle_logger(config):
    if (config.logger_on):
        config.logger_on = False
        print (f"{Colour().red} Logger turned off.{Colour().default}")
    else:
        config.logger_on = True
        print (f"{Colour().green} logger turned on.{Colour().default}")
    update_config(config.__dict__)

#Toggle between logging all player traffic, and logging specified player traffic
def toggle_all_players(config):
    if (config.logall_on):
        config.logall_on = False
        currently_online_flush()
        print (f"{Colour().red} Log All Players Off.{Colour().default}")
    else:
        config.logall_on = True
        print (f"{Colour().green} Log All Players On.{Colour().default}")
    update_config(config.__dict__)

#Toggle warning prompt to user if server player count exceeds 11 players
def toggle_limit_warning(config):
    if (config.limit_warning_on):
        config.limit_warning_on = False
        print (f"{Colour().red} Player count limit warning Off.{Colour().default}")
    else:
        config.logall_on = True
        print (f"{Colour().green} Player count limit warning On.{Colour().default}")
    update_config(config.__dict__)