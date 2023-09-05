from mcstatus import JavaServer
from datetime import datetime
from .colour import Colour




def get_online_list(url):
    try:
        server = JavaServer.lookup(url)
        playerlist = server.status().players.sample
    except Exception:
        return False
    else:

