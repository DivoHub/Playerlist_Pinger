from requests import get
from bs4 import BeautifulSoup
from datetime import datetime
from .get_innerhtml import get_innerHTML
from .colour import Colour



#checks validity of server IP / returns False if HTTP error code given or if blank
def servers_are_valid(config):
    for each_server in config.servers:
        if (len(each_server['url']) == 0):
            print (f"{Colour().error} No Server IP given {Colour().default}")
            return False
        status_code = get("https://minecraftlist.com/servers/" + each_server['url']).status_code
        if (status_code >= 200 and status_code <= 299):
            return True
        elif (status_code == 404):
            print(f"{Colour().error} Invalid Server entered. {Colour().default}")
            return False
        else:
            print(f"{Colour().error} Connection error {Colour().default}")
            return False


#return list object with currently online players / makes GET request to URL
def get_online_list(server):
    try:
        new_request = get("https://minecraftlist.com/servers/" + server)
    except Exception:
        return False
    else:
        new_request = BeautifulSoup(new_request.text, "html.parser")
        if (updated_recently(new_request)):

        player_elements = new_request.find_all("a", class_="block no-underline hover:bg-gray-200 px-2 py-1 flex items-center text-gray-800")
        #last_checked = html_doc.find("p", class_="text-center text-gray-500").text
        player_list = []
        for each_element in player_elements:
            player = each_element.find("span", class_="truncate")
            player_list.append(player)
        online_list = list(map(get_innerHTML, player_list))
        return online_list


def updated_recently(request):
    request = str(request.find("p", class_="text-center text-gray-500"))
    if ("month" in request or "week" in request or "day" in request or "hour" in request):
        return False
    else:
        return True

def last_resort_condition(new_request):
    if ("hours" in new_request.find("time").string or "days" in new_request.find("time").string):
        return True
    elif (new_request.find("span", class_="label label-big label-success").string == "offline"):
        return True
    else:
        return False

# get online list from minecraft-statistic.net if minecraftlist.net is out of service
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
        new_request = new_request.find("tr", id="players").find_all('img', alt=True)
    except AttributeError:
        return []
    except Exception:
        return False
    else:
        player_list = []
        for each_player in new_request:
            player_list.append(each_player['alt'])
        return player_list


