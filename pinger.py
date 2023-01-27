from threading import Thread, active_count
from simpleaudio import WaveObject
from requests import get
from bs4 import BeautifulSoup
from datetime import datetime
from json import dumps, load
from time import sleep

#Main configuration class
class Config:
    def __init__(self):
        self.players = []
        self.servers = []
        self.target = 0
        self.interval = 60
        self.alt_links = []

    #Prompts user to add values to config and creates config.json file with those values
    def initialize(self):
        create_config()
        self.add_player()
        self.add_server()
        update_config(self.__dict__)

    #reinitialize all values for config file
    def start_new(self):
        warning = input("This will erase your previous config file, are you sure? 'y' to continue.")
        if not (warning == 'y'):
            return
        self.players = []
        self.servers = []
        self.target = 0
        self.add_player()
        self.add_server()

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
            json_file = load(playerlist_file)
            self.players = json_file["players"]
            self.servers = json_file["servers"]
            self.target = json_file["target"]
            self.alt_links = json_file["alt_links"]
            playerlist_file.close()

    #remove specified player from checking list in config
    def delete_player(self):
        while True:
            del_player = input("Enter player name (case sensitive) enter 'x' when finished:    ")
            if (del_player == "x"):
                break
            elif (del_player in self.players):
                self.players.remove(del_player)
            else:
                print ("Player is not found in config")
        update_config(self.__dict__)

    def add_alt_links(self):
        while True:
            new_link = input("Enter alt link for server on minecraft-statistic.net. enter 'x' when finished:    ")
            if (new_link == "x"):
                break
            elif (new_link in self.alt_links):
                print("Alt link is already on list.")
            else:
                self.alt_links.append(new_link)
        update_config(self.__dict__)

    def del_alt_links(self):
        while True:
            del_link = input("Enter alt link to be removed. enter 'x' when finished:    ")
            if (del_link == "x"):
                break
            elif (del_link in self.alt_links):
                self.alt_links.remove(del_link)
            else:
                print ("Alt link not found in config.")
        update_config(self.__dict__)

    #prints config values to console
    def print_values(self):
        print (f"Number of Servers checking:  {len(self.servers)}")
        print (f"Checking on Server IP: {self.servers} \n")
        print(f"Number of Players checking: {len(self.players)}")
        print (f"Checking for players: {self.players} \n")
        print(f"Ping when server size reaches: {self.target} \n")

    #Change the number or size of playerlist to ping user for (Value 0 if setting is off, default is also 0)
    def change_target(self):
        try:
            self.target = int(input("Enter target size to ping user for:  "))
        except ValueError:
            print ("Invalid input given.")
        else:
            update_config(self.__dict__)

    #append new players to players list
    def add_player(self):
        while True:
            new_player = input("Enter player name (enter 'x' when finished):    ")
            if (new_player == "x"):
                break
            elif (new_player in self.players):
                print ("Player is already on list.")
            else:
                self.players.append(new_player)
        update_config(self.__dict__)

    #change server ip to be checked
    def add_server(self):
        while True:
            new_server = input("Enter Server IP (enter 'x' when finished):   ")
            if (new_server == "x"):
                break
            if (server_is_valid(new_server)):
                self.servers.append(new_server)
                update_config(self.__dict__)

    #delete specified player from checking list in config
    def delete_server(self):
        while True:
            del_server = input("Enter server name (case sensitive) enter 'x' when finished:    ")
            if (del_server == "x"):
                break
            if (del_server in self.servers):
                self.servers.remove(del_server)
            else:
                print ("Server is not in list")
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
    json_object = dumps(dict_object, indent=2)
    new_file.write(json_object)
    new_file.close()

#Returns InnerHTML string of given HTML elements/class
def get_innerHTML(element):
    return element.string

#checks validity of server IP / returns False if HTTP error code given or if blank
def server_is_valid():
    for server in config.servers:
        if (server == "" or len(config.servers) == 0):
            print ("No Server IP given")
            return False
        try:
            status_code = get("https://minecraftlist.com/servers/" + server).status_code
            if (status_code >= 200 and status_code <= 299):
                return True
            elif (status_code == 404):
                print("Invalid Server entered.")
                return False
            else:
                print("Connection error")
                return False
        except Exception:
            return False

#appends each status into log file in local folder. Creates log file if none exists
def logger(status_string):
    try:
        log_file = open('log.txt', 'a')
    except FileNotFoundError:
        log_file = open('log.txt', 'x')
    finally:
        log_file.write(status_string + "\n")
        log_file.close()

#reintiates another log file
def refresh_log():
    try:
        log_file = open('log.txt', 'w')
    except FileNotFoundError:
        log_file = open('log.txt', 'x')
    finally:
        log_file.write("")
        log_file.close()

def toggle_alt_checker():
    global use_alt_checker
    if (use_alt_checker):
        use_alt_checker = False
        print ("Alt Website checker turned off")
    else:
        use_alt_checker = True
        print ("Alt Website checker turned on")
    return

#turn off and on logger module.
def toggle_logger():
    global logger_is_on
    if (logger_is_on):
        logger_is_on = False
        print ("Logger turned off.")
    else:
        logger_is_on = True
        print ("logger turned on")
    return

def currently_online_flush():
    global currently_online_list
    for each_server in config.servers:
        currently_online_list[each_server] = list(filter(lambda player: player in config.players, currently_online_list[each_server]))
    return

def toggle_all_players():
    global log_all_players
    if (log_all_players):
        log_all_players = False
        currently_online_flush()
        print ("Log All Players Off.")
    else:
        log_all_players = True
        print ("Log All Players On.")
    return

#update time interval between each refresh (not in use, troubleshoot)
# def refresh_interval(string, server):
#     global interval_dict
#     if any(character.isdigit() for character in string):
#         string = string.replace("We last checked this server ", "")
#         string = string.replace(" minutes ago.", "")
#         interval_dict[server] = 920 - (int(string) * 60)
#     else:
#         interval_dict[server] = 0

#return list object with currently online players / makes GET request to URL

def get_online_list(server):
    try:
        new_request = get("https://minecraftlist.com/servers/" + server)
    except Exception:
        print (f"Error making HTTP request at {datetime.now().strftime('%D  %H:%M:%S')}")
        return False
    else:
        html_doc = BeautifulSoup(new_request.text, "html.parser")
        player_elements = html_doc.find_all("a", class_="block no-underline hover:bg-gray-200 px-2 py-1 flex items-center text-gray-800")
        #last_checked = html_doc.find("p", class_="text-center text-gray-500").text
        player_list = []
        for each_element in player_elements:
            player = each_element.find("span", class_="truncate")
            player_list.append(player)
        online_list = list(map(get_innerHTML, player_list))
        return online_list

#get online list from different website if minecraftlist.net is out of service
def get_online_list_alt(link):
    try:
        new_request = get(link)
    except Exception:
        print (f"Error making HTTP request at {datetime.now().strftime('%D  %H:%M:%S')}")
        return False
    else:
        html_doc = BeautifulSoup(new_request.text, "html.parser")
        player_elements = html_doc.find_all("a", class_="c-black")
        player_elements = list(map(get_innerHTML, player_elements))
        return player_elements

#play notification sound
def play_sound(sound_file):
        try:
            audio_object = WaveObject.from_wave_file(f"./sounds/{sound_file}")
            play = audio_object.play()
            play.wait_done()
            play.stop()
        except FileNotFoundError:
            print(f"{sound_file} file not found.")
        except Exception:
            print ("Error with playing notification audio.")
        finally:
            return

#check if server size has reached specified target number
def target_check(player_count, server):
    global target_reached
    if (player_count >= config.target and target_reached[server] is False):
        target_reached[server] = True
        print(f"{server} has hit {config.target} players at {datetime.now().strftime('%D  %H:%M:%S')}")
        play_sound("chime.wav")
    elif (player_count < config.target and target_reached[server] is True):
        target_reached[server] = False

#log all players that log on to server
def login_check_all(online_list, server):
    global currently_online_list
    login_list = []
    for each_player in online_list:
        if (each_player not in currently_online_list[server]):
            login_list.append(f"> {each_player} seen online at {datetime.now().strftime('%D  %H:%M:%S')} on Server: {server}")
            currently_online_list[server].append(each_player)
            if (each_player in config.players):
                play_sound("login.wav")
    return login_list

#log players in config who log on to server
def login_check(online_list, server):
    global currently_online_list
    found_list = list(set(config.players).intersection(online_list))
    login_list = []
    for each_player in found_list:
        if (each_player not in currently_online_list[server]):
            login_list.append(f"> {each_player} seen online at {datetime.now().strftime('%D  %H:%M:%S')} on Server: {server}")
            currently_online_list[server].append(each_player)
            play_sound("login.wav")
    return login_list

#log players that log out
def logout_check(online_list, server):
    global currently_online_list
    logout_list = []
    for each_player in currently_online_list[server]:
        if (each_player not in online_list):
            logout_list.append(f"> {each_player} logged off at {datetime.now().strftime('%D  %H:%M:%S')} on Server: {server}")
            currently_online_list[server].remove(each_player)
            if (each_player in config.players):
                play_sound("logout.wav")
    return logout_list

# quick command function that displays to users all online players in config servers
def quick_check():
    global use_alt_checker
    for each_server in config.servers:
        online_list = get_online_list(each_server)
        if (online_list == None):
            return
        elif (len(online_list) == 0):
            print(f"0 players found on Server: {each_server}")
        else:
            for each_player in online_list:
                print(
                    f"> {each_player} seen online at {datetime.now().strftime('%D  %H:%M:%S')} on Server: {each_server}")
    play_sound(str("chime.wav"))

#checks for newly joined players and players who have logged
def checker():
    global log_all_players
    global use_alt_checker
    log_list = []
    for index in range (len(config.servers)):
        if (use_alt_checker):
            online_list = get_online_list_alt(config.alt_links[index])
        else:
            online_list = get_online_list(config.servers[index])
        if (online_list == False):
            return []
        if (log_all_players):
            log_list.extend(login_check_all(online_list, config.servers[index]))
        else:
            log_list.extend(login_check(online_list, config.servers[index]))
        log_list.extend(logout_check(online_list, config.servers[index]))
        target_check(len(online_list), config.servers[index])
    return log_list

#Halts program for configured time before making another request
def wait():
    global continue_condition
    for timer in range(config.interval):
        if continue_condition:
            sleep(1)
        else:
            break

#iterative function, continues if user has not stopped
def looper():
    global continue_condition
    global interval_dict
    global log_all_players
    while continue_condition:
        config.load_config()
        status_log = checker()
        for each_status in status_log:
            print (each_status)
            if logger_is_on:
                logger(each_status)
        wait()

#start application
def start():
    if (active_count() > 1):
        print("Checker already running. \n")
        return
    if not(server_is_valid()):
        print ("Invalid server error...\n check configurations or connection, and try again")
        return
    print ("Starting checker \n")
    global continue_condition
    continue_condition = True
    process = Thread(target=looper)
    process.start()

#stop application
def stop():
    if (active_count() == 1):
        print ("Checker not running.\n")
        return
    print ("Stopping checker.\n")
    global continue_condition
    global currently_online_list
    continue_condition = False
    for each_server in config.servers:
        currently_online_list[each_server] = []

#main user input command line interface for application
def main():
    command_dict = {"addplayer": config.add_player,
                    "delplayer": config.delete_player,
                    "addserver": config.add_server,
                    "delserver": config.delete_server,
                    "online": quick_check,
                    "target": config.change_target,
                    "config": config.print_values,
                    "logger": toggle_logger,
                    "logall": toggle_all_players,
                    "alt": toggle_alt_checker,
                    "addalt": config.add_alt_links,
                    "delalt": config.del_alt_links,
                    "newlog": refresh_log,
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
    print("Welcome to the Minecraft Java Edition Playerlist Pinger. Type 'help' to see list of commands.\n-------------------------------------------")
    global continue_condition
    global currently_online_list
    global interval_dict
    global target_reached
    global logger_is_on
    global log_all_players
    global use_alt_checker
    config = Config()
    config.load_config()
    config.print_values()
    currently_online_list = dict()
    interval_dict = dict()
    target_reached = dict()
    logger_is_on = False
    log_all_players = False
    use_alt_checker = False
    for each_server in config.servers:
        currently_online_list[each_server] = []
        interval_dict[each_server] = 0
        target_reached[each_server] = False
    main()
