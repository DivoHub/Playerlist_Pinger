from threading import Thread, active_count
from .colour import Colour
from .request import servers_are_valid

#start application
def start():
    global config
    if (active_count() > 1):
        print(f"{Colour().default} Checker already running.")
        return
    if (len(config.players) == 0):
        print (f"{Colour().error} Checker cannot start if there are no players to look for. \nCheck configurations or add players and try again. ")
        return
    if (len(config.servers) == 0):
        print (f"{Colour().error} Checker cannot start if there are no servers to check. \nCheck configurations or add servers and try again. ")
        return
    if not(servers_are_valid()):
        print (f"{Colour().error} Invalid server error...\n check configurations or connection, and try again.{Colour().default}")
        return
    print (f"{Colour().green} Starting checker... {Colour().default}")
    global continue_condition
    continue_condition = True
    process = Thread(target=looper)
    process.start()