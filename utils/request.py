from mcstatus import JavaServer
from datetime import datetime
from .colour import Colour

#seperate function to call for
def get_server_object(url):
    return JavaServer.lookup(url).status()

def server_is_valid(url):
    server_object = JavaServer.lookup(url)
    try:
        server_object.ping()
    except Exception:
        return False
    else:
        return True

def get_online_list(server_object):
    try:
        playerlist = server_object.players.sample
    except Exception:
        return None
    except IndexError:
        return None
    return_list = []
    for each_player in playerlist:
        return_list.append(each_player.name)
    return return_list

def get_player_count(server_object):
    return server_object.players.online


