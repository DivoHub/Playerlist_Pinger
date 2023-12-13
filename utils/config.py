from json import load
from utils.server import Server
from .files import create_config, update_config
from .colour import Colour
import logging

class Config:
    def __init__(self):
        self.players = []
        self.servers = []
        self.interval = 120
        self.logger_on = False
        self.logall_on = False

    #Prompts user to add values to config and creates config.json file with those values
    def initialize(self):
        self.__init__()
        update_config(self.__dict__)

    #reinitialize all values for config file
    def start_new(self):
        warning = input(f"{Colour().warning}Start a new config file? any pre-existing config.json file will be deleted. Enter 'y' to continue.{Colour().default}")
        if not (warning.casefold() == 'y'):
            return
        self.initialize()
        logging.info("Config file overwritten.")

    # checks if config file given is valid
    def config_is_valid(self, json_object):
        condition_list = []
        try:
            condition_list.append(type(json_object["logger_on"]) == bool)
            condition_list.append(type(json_object["logall_on"]) == bool)
            condition_list.append(type(json_object["servers"]) == list)
            condition_list.append(type(json_object["interval"]) == int)
            condition_list.append(type(json_object["players"]) == list)
        except KeyError:
            logging.error(f"{Colour().error} Error loading keys from config.json file. \nCheck config.json file for validity issues {Colour().default}")
            return False
        except Exception:
            logging.error(f"{Colour().error} Error occurred checking for config.json validity. {Colour().default}")
            return False
        if (json_object["servers"]):
            condition_list.append(type(json_object["servers"][0]) == dict)
        if (json_object["players"]):
            condition_list.append(type(json_object["players"][0]) == str)
        return all(condition_list)

    #loader for config.json file
    def config_fetcher(self):
        try:
            playerlist_file = open('./config.json', 'r')
            json_object = load(playerlist_file)
        except FileNotFoundError:
            logging.warning(f"{Colour().error} No config.json file found. {Colour().default}")
            create_config()
            self.initialize()
            return None
        except Exception:
            logging.error(f"{Colour().error} Error loading config.json file\nPlease fix any issues with config file before starting checker.{Colour().default}")
            self.__init__()
            return None
        else:
            playerlist_file.close()
            return json_object

    #loads config.json values / Initializes a config.json file if one is not found
    def load_config(self):
        json_object = self.config_fetcher()
        if (json_object == None):
            return
        if not (self.config_is_valid(json_object)):
            return
        self.players = json_object["players"]
        self.servers = json_object["servers"]
        self.interval = json_object["interval"]
        self.logger_on = bool(json_object["logger_on"])
        self.logall_on = bool(json_object["logall_on"])

    #remove specified player from checking list in config
    def delete_player(self):
        if (len(self.players) == 0):
            print (f"{Colour().error}No players to delete{Colour().default}")
            return
        elif (len(self.players) == 1):
            self.players.pop()
            update_config(self.__dict__)
            return
        while True:
            del_player = input(f"{Colour().default} Enter player name (case sensitive) Leave blank and press enter when finished:    ")
            if (del_player.casefold() == ""):
                break
            elif (del_player in self.players):
                self.players.remove(del_player)
                update_config(self.__dict__)
            else:
                logging.info(f"{Colour().error} Player is not found in config {Colour().default}")

    #append new players to players list
    def add_player(self):
        while True:
            new_player = input(f"{Colour().default} Enter player name (Leave blank and press enter when finished):    ")
            if (new_player.casefold() == ""):
                break
            elif (new_player in self.players):
                logging.info(f"{Colour().warning} Player is already on list. {Colour().default}")
            else:
                self.players.append(new_player)
                update_config(self.__dict__)

    #prints all servers and corresponding indexes
    def server_index_printer(self):
        print("--------------------------------")
        for index in range(len(self.servers)):
            print(f"{index}: {self.servers[index]['url']} \n")
        print("--------------------------------")

    #prints config values to console
    def print_values(self):
        on_or_off = {True: f"{Colour().green}On{Colour().default}", False: f"{Colour().red}Off{Colour().default}"}
        print (f"{Colour().default}Number of Servers checking:  {len(self.servers)}")
        print(f"{Colour().default}Number of Players checking: {len(self.players)}")
        print (f"{Colour().default}Checking for players: {self.players} \n")
        print (f"Logger: {on_or_off[self.logger_on]}")
        print (f"Log all player traffic: {on_or_off[self.logall_on]}")
        for each_server in self.servers:
            print (f"{Colour().default}IP: {each_server['url']} ")
            print (f"{Colour().default}Target: {each_server['target']}" )
            print ("-------------------------------")

    #Change the number or size of playerlist to ping user for (Value 0 if setting is off, default is also 0)
    def change_target(self):
        self.server_index_printer()
        try:
            server_index = int(input(f"{Colour().default} Enter index (number) of server to change target for:    "))
            self.servers[server_index]['target'] = int(input(f"{Colour().default}Enter number target for {self.servers[server_index]['url']}:    "))
        except ValueError:
            logging.info(f"{Colour().error} Invalid input given. {Colour().default}")
        except IndexError:
            logging.info(f"{Colour().error} Index is out of range. {Colour().default}")
        else:
            update_config(self.__dict__)

    #change server ip to be checked
    def add_server(self):
        user_input = input(f"{Colour().default} Enter Server IP (Leave blank and press enter to cancel):   ")
        if (user_input.casefold() == ''):
            return None
        new_server = Server()
        new_server.url = user_input
        self.servers.append(new_server.__dict__)
        update_config(self.__dict__)
        return new_server.url

    #delete specified player from checking list in config
    def delete_server(self):
        if (len(self.servers) == 0):
            logging.info(f"{Colour().error}No servers to delete.{Colour().default}")
            return None
        elif (len(self.servers) == 1):
            deleted_server = self.servers.pop()
            update_config(self.__dict__)
            return deleted_server['url']
        self.server_index_printer()
        deletion_index = input(f"{Colour().default} Enter index (number) of server to delete (enter 'x' to cancel):")
        if (deletion_index== "x"):
            return None
        try:
            deleted_server = self.servers.pop(int(deletion_index))['url']
        except ValueError:
            logging.info(f"{Colour().error}Invalid Entry.{Colour().default}")
        except IndexError:
            logging.info(f"{Colour().error}Input does not correspond to a server index.{Colour().default}")
        else:
            update_config(self.__dict__)
            return deleted_server

    #change interval between each GET request
    def change_interval(self):
            try:
                self.interval = int(input(f"{Colour().default} Enter an interval in seconds between each fetch (Anything lower than 10 seconds is not recommended):  "))
            except ValueError:
                logging.info(f"{Colour().error} Input Error {Colour().default}")
            else:
                update_config(self.__dict__)