import threading
from playsound import playsound
from requests import get
from bs4 import BeautifulSoup
from datetime import datetime
import json
from time import sleep

class Config:
    def __init__(self):
        self.players = []
        self.server = ""
        self.interval = 30

    #Prompts user to add values to config and creates config.json file with those values
    def initialize(self):
        self.add_player()
        self.change_server()
        self.change_interval()
        create_config()
        update_config(self.__dict__)

    #loads config.json values / Initializes a config.json file if one is not found
    def load_config(self):
        try:
            playerlist_file = open('config.json', 'r')
        except FileNotFoundError:
            print ("No config.json file found.")
            self.initialize()
        except Exception:
            print ("Other error occurred.")
        else:
            json_file = json.load(playerlist_file)
            self.players = json_file["players"]
            self.server = json_file["server"]
            self.interval = json_file["interval"]
            print (self.__dict__)
            playerlist_file.close()

    def print_values(self):
        lines = "------------------------------------"
        print (f"")
        print (f"Interval: {self.interval} Seconds\n", end=lines)
        print (f"Checking for players: {self.players} \n", end=lines)


    #append new players to players list
    def add_player(self):
        while True:
            new_player = input("Enter player name (enter 'x' when finished):    ")
            if (new_player == "x"):
                break
            self.players.append(new_player)

    #change server ip to be checked
    def change_server(self):
        self.server = input("Enter Server IP:    ")

    #change interval between each GET request
    def change_interval(self):
        while True:
            try:
                self.interval = int(input("Enter an interval in seconds between each fetch (must be at least 30 with no decimals"))
                raise ValueError if (self.interval < 30)
            except ValueError:
                print ("Input Error")



#create config.json file / no return variable
def create_config():
    print("Creating new config.json file.")
    new_file = open('config.json', 'x')
    new_file.close()

#update config.json file / takes dictionary argument from Config object instance
def update_config(dict_object):
    new_file = open('config.json', 'w')
    json_object = json.dumps(dict_object, indent=2)
    new_file.write(json_object)
    new_file.close()

#Returns InnerHTML string of given HTML elements/class
def get_innerHTML(element):
    return element.string


#return list object with currently online players / makes GET request to URL
def get_online_list():
    new_request = get("https://minecraftlist.com/servers/mc.craftymynes.com")
    if (new_request.ok == False): #Return None is HTTP response code is above 399
        print ("Error making HTTP request.")
        return None
    html_doc = BeautifulSoup(new_request.text, "html.parser")
    player_elements = html_doc.find_all("span", class_="truncate")
    player_list = list(map(get_innerHTML, player_elements))
    return player_list


def checker():
    online_list = get_online_list()
    for each_looked in config.players:
        for each_online in online_list:
            if (each_looked == each_online):
                print(f"{each_online} seen online at {datetime.now()}")
                playsound("ding.wav")
    print ("None on")
    return False


def looper():
    while True:
        checker()
        sleep(config.interval)

def print_manual():
    manual = open('help.txt', 'r')
    print (manual)
    manual.close()

def main():
    config = Config()
    config.load_config()
    command_dict = {
        "addplayer": config.add_player(),
        "delplayer": config.delete_player(),
        "changeint": config.change_interval(),
        "changeserver": config.change_server(),
        "checkconfig": config.print_values(),
        "help": print_manual()
    }
    while True:
        user_input = input()
        if (user_input == "exit"):
            print("Program exiting.")
            break
        if (user_input == "start" and threading.active_count() < 2):
            process = threading.Thread(target=looper)
            process.start()
        command_dict[user_input]

    return 0


if __name__ == '__main__':
    main()




