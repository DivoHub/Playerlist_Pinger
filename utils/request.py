from mcstatus import JavaServer
from .colour import Colour
from socket import create_connection

def internet_is_working():
    try:
        create_connection(("8.8.8.8", 53), timeout=5)
    except OSError:
        return False
    else:
        return True

#seperate function to fetch server object to avoid making extraneous calls
def get_server_object(url):
    try:
        server_object = JavaServer.lookup(url).status()
    except Exception:
        return None
    else:
        return server_object

#checks if ping returns a valid object returns True if so
def server_is_valid(url):
    try:
        server_object = JavaServer.lookup(url)
        server_object.ping()
    except Exception:
        print(f"{Colour().error} Invalid server error: {url} {Colour().default}")
        return False
    else:
        return True

#parses the server object to return a list of player names
def get_online_list(server_object):
    if (server_object == None):
        return None
    if (get_player_count(server_object) == 0):
        return []
    playerlist = server_object.players.sample
    return_list = []
    for each_player in playerlist:
        return_list.append(each_player.name)
    return return_list

#return an int with the number of players online on server
def get_player_count(server_object):
    return server_object.players.online