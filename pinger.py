import threading
from playsound2 import playsound
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
        create_config()
        self.add_player()
        self.change_server()
        self.change_interval()
        update_config(self.__dict__)

    #reinitialize all values for config file
    def start_new(self):
        warning = input("This will erase your previous config file, are you sure? 'y' to continue.")
        if not (warning == 'y'):
            return
        self.players = []
        self.add_player()
        self.change_server()
        self.change_interval()

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
            playerlist_file.close()

    #remove specified player from checking list
    def delete_player(self):
        while True:
            del_player = input("Enter player name (case sensitive) enter 'x' when finished:    ")
            if (del_player == "x"):
                break
            if (del_player in self.players):
                self.players.remove(del_player)
            else:
                print ("Player is not in list")
        update_config(self.__dict__)

    #prints config values to console
    def print_values(self):
        print (f"Checking on Server IP: {self.server} \n")
        print (f"Interval: {self.interval} Seconds\n")
        print (f"Checking for players: {self.players} \n")


    #append new players to players list
    def add_player(self):
        while True:
            new_player = input("Enter player name (enter 'x' when finished):    ")
            if (new_player == "x"):
                break
            self.players.append(new_player)
        update_config(self.__dict__)

    #change server ip to be checked
    def change_server(self):
        self.server = input("Enter Server IP:    ")
        if (server_is_valid()):
            update_config(self.__dict__)

    #change interval between each GET request
    def change_interval(self):
        while True:
            try:
                self.interval = int(input("Enter an interval in seconds between each fetch (must be at least 30 with no decimals:   "))
                if (self.interval < 30): raise ValueError
            except ValueError:
                print ("Input Error")
            else:
                break
        update_config(self.__dict__)

#Prints help manual to console
def print_manual():
    manual = open('help.txt', 'r')
    print (manual.read())
    manual.close()

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

#checks validity of server IP / returns False if HTTP error code given or if blank
def server_is_valid():
    if (config.server == ""):
        print ("No Server IP given")
        return False
    try:
        get("https://minecraftlist.com/servers/" + config.server).ok
    except Exception:
        print ("Invalid server")
        stop()
        return False
    else:
        return True

#return list object with currently online players / makes GET request to URL
def get_online_list():
    if not (server_is_valid()): #Return None if HTTP response code is not valid
        print ("Error making HTTP request.")
        return None
    new_request = get("https://minecraftlist.com/servers/" + config.server)
    html_doc = BeautifulSoup(new_request.text, "html.parser")
    player_elements = html_doc.find_all("a", class_="block no-underline hover:bg-gray-200 px-2 py-1 flex items-center text-gray-800")
    player_list = []
    for each_element in player_elements:
        player = each_element.find("span", class_="truncate")
        player_list.append(player)
    online_list = list(map(get_innerHTML, player_list))
    return online_list


#play notification sound
def ding():
    while True:
        try:
            playsound("./ding.wav")
        except Exception:
            sleep(1)
        else:
            break

#checks for newly joined players and players who have logged
def checker():
    global currently_online_list
    online_list = get_online_list()
    found_list = list(set(config.players).intersection(online_list))
    for each_player in found_list:
        if (each_player not in currently_online_list):
            print(f"> {each_player} seen online at {datetime.now().strftime('%D  %H:%M:%S')}")
            currently_online_list.append(each_player)
            ding()
    for each_player in currently_online_list:
        if (each_player not in online_list):
            print (f"> {each_player} logged off at {datetime.now().strftime('%D  %H:%M:%S')}")
            currently_online_list.remove(each_player)
            ding()

    #print ("-----------------------------------")

#iterative function, continues if user has not stopped
def looper():
    global continue_condition
    while continue_condition:
        config.load_config()
        checker()
        for timer in range (config.interval):
            if continue_condition:
                sleep(1)
            else:
                break

#start application
def start():
    if (threading.active_count() < 2):
        print ("Starting checker \n")
        global continue_condition
        continue_condition = True
        process = threading.Thread(target=looper)
        process.start()
    else:
        print ("Checker already running. \n")

def stop():
    if (threading.active_count() == 1):
        print ("Checker not running.\n")
        return
    print ("Stopping checker.\n")
    global continue_condition
    global currently_online_list
    continue_condition = False
    currently_online_list = []

def main():
    command_dict = {"addplayer": config.add_player,
                    "delplayer": config.delete_player,
                    "changeint": config.change_interval,
                    "changeserver": config.change_server,
                    "checkconfig": config.print_values,
                    "fresh": config.start_new,
                    "start": start,
                    "stop": stop,
                    "help": print_manual}

    while True:
        print ("-------------------------")
        user_input = input()
        print ("-------------------------")
        if (user_input in command_dict.keys()):
            command_dict[user_input]()
        elif (user_input == "exit"):
            stop()
            print("Program exiting.")
            break
        elif (user_input == ""):
            print ("")
        else:
            print ("Unknown command.")

if __name__ == '__main__':
    print ("Welcome to the Minecraft Java Edition Playerlist Pinger. Type 'help' to see list of commands.\n-------------------------------------------")
    global continue_condition
    global currently_online_list
    currently_online_list = []
    config = Config()
    config.load_config()
    config.print_values()
    main()
