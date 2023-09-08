from mcstatus import JavaServer

#seperate function to fetch server object to avoid making extraneous calls
def get_server_object(url):
    return JavaServer.lookup(url).status()

#checks if ping returns a valid object returns True if so
def server_is_valid(url):
    server_object = JavaServer.lookup(url)
    try:
        server_object.ping()
    except Exception:
        return False
    else:
        return True

#parses the server object to return a list of player names
def get_online_list(server_object):
    try:
        playerlist = server_object.players.sample
    except Exception:
        return None
    except IndexError:
        return None
    if (len(playerlist) == 0):
        return []
    return_list = []
    for each_player in playerlist:
        return_list.append(each_player.name)
    return return_list


#return an int with the number of players online on server
def get_player_count(server_object):
    return server_object.players.online