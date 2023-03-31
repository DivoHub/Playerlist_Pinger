from threading import active_count
from .colour import Colour

#stop application
def stop():
    global config
    if (active_count() == 1):
        print (f"{Colour().default} Checker not running.")
        return
    print (f"{Colour().red} Stopping checker.\n {Colour().default}")
    global continue_condition
    global currently_online_list
    continue_condition = False
    for each_server in config.servers:
        currently_online_list[each_server['url']] = []