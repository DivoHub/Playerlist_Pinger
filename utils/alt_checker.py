from requests import get
from bs4 import BeautifulSoup
from datetime import datetime
from get_innerhtml import get_innerHTML

#get online list from minecraft-statistic.net if minecraftlist.net is out of service
def get_online_list_alt(alt_link, url):
    if (alt_link == None):
        raise RuntimeError
    try:
        new_request = get(alt_link)
        new_request = BeautifulSoup(new_request.text, "html.parser")
        if ("hours" in new_request.find("time").string or "days" in new_request.find("time").string):
                raise RuntimeError
    except RuntimeError:
        return get_online_list_last_resort(url)
    except Exception:
        print (f"{colour.error} Error making HTTP request at {datetime.now().strftime('%D  %H:%M:%S')} {colour.default}")
        return False
    else:
        player_list = new_request.find_all("a", class_="c-black")
        player_list = list(map(get_innerHTML, player_list))
        return player_list

def get_online_list_last_resort(url):
    try:
        new_request = get(f"mcsrvstat.us/server/{url}")
        new_request = BeautifulSoup(new_request.text, "html.parser")
        new_request = new_request.find("tr", id="players").find_all('img',alt=True)
    except Exception:
        print (f"{colour.error} Error making HTTP request at {datetime.now().strftime('%D  %H:%M:%S')} {colour.default}")
        return False
    else:
        player_list = []
        for each_player in new_request:
            player_list.append(each_player['alt'])
        return player_list

def toggle_alt_checker():
    global use_alt_checker
    if (use_alt_checker):
        use_alt_checker = False
        print (f"{colour.red} Alt Website checker turned off.{colour.default}")
    else:
        use_alt_checker = True
        print (f"{colour.green} Alt Website checker turned on.{colour.default}")
    return


