from requests import get
from bs4 import BeautifulSoup
from datetime import datetime
from .get_innerhtml import get_innerHTML
from .colour import Colour


def last_resort_condition(new_request):
    if ("hours" in new_request.find("time").string or "days" in new_request.find("time").string):
        return True
    elif (new_request.find("span", class_="label label-big label-success").string == "offline"):
        return True
    else:
        return False

#get online list from minecraft-statistic.net if minecraftlist.net is out of service
def get_online_list_alt(alt_link, url):
    if (alt_link == None):
        raise RuntimeError
    try:
        new_request = get(alt_link)
        new_request = BeautifulSoup(new_request.text, "html.parser")
        if (last_resort_condition(new_request)):
                raise RuntimeError
    except RuntimeError:
        return get_online_list_last_resort(url)
    except Exception:
        return False
    else:
        player_list = new_request.find_all("a", class_="c-black")
        player_list = list(map(get_innerHTML, player_list))
        return player_list

def get_online_list_last_resort(url):
    try:
        new_request = get(f"https://mcsrvstat.us/server/{url}")
        new_request = BeautifulSoup(new_request.text, "html.parser")
        new_request = new_request.find_all("div", id="players")
        new_request = new_request[0].find_all("a")
    except AttributeError:
        return []
    except Exception:
        return False
    else:
        player_list = []
        for each_player in new_request:
            player_list.append(each_player.find('img')['title'])
        return player_list



