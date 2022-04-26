from playsound import playsound
from requests import get
from bs4 import BeautifulSoup

URL = 'https://minecraftlist.com/servers/mc.craftymynes.com'


#Returns InnerHTML string of given HTML elements/class
def get_innerHTML(element):
    return element.string

def get_players():
    try:
        with open ('playerlist.txt', 'r') as playerlist_file:
            playerlist = playerlist_file.splitlines()
            close()
        return playerlist
    except FileNotFoundError as NoFile:
        with open ('playerlist.txt', 'x') as new_file:
            close()

#return list object with currently online players / makes GET request to URL
def get_online_list():
    new_request = get(URL).text
    html_doc = BeautifulSoup(new_request, "html.parser")
    player_elements = html_doc.find_all("span", class_="truncate")
    player_list = list(map(get_innerHTML, player_elements))
    return player_list


#print (new_request.ok)
#print(get_players())
print(get_online_list())
playsound('./ding.wav')




