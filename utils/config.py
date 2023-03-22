from server import Server

class Config:
    def __init__(self):
        self.players = []
        self.servers = []
        self.interval = 120

    #Prompts user to add values to config and creates config.json file with those values
    def initialize(self):
        create_config()
        self.add_player()
        self.add_server()

    #reinitialize all values for config file
    def start_new(self):
        warning = input(f"{colour.warning}This will erase your previous config file, are you sure? 'y' to continue.{colour.default}")
        if not (warning == 'y'):
            return
        self.players = []
        self.servers = []
        self.add_player()
        self.add_server()

    # checks if config file given is valid
    def config_validator(self):
        json_object = self.config_handler()
        if not(type(json_object['players']) is list and type(json_object['servers']) is list and type(json_object['interval']) is int):
            print (f"{colour.error}Issue with config file compatibility. Please reinitialize, or fix config file before starting checker.{colour.default}")
            return
        if (len(json_object['players']) + len(json_object['servers']) == 0):
            print (f"{colour.error}No players or servers given from config.json file.{colour.default}")
            return
        if not(all(type(each_element) is dict for each_element in json_object['servers'])):
            self.config_conversion(json_object)
            return

    # Convert old json config files to be compatible with new version
    def config_conversion(self, json_object):
        self.players = json_object['players']
        self.interval = json_object['interval']
        converted_server_list = []
        for index in range (len(json_object['servers'])):
            server_dict = dict()
            server_dict['url'] = json_object['servers'][index]
            server_dict['target'] = json_object['target']
            server_dict['alt_link'] = json_object['alt_links'][index]
            converted_server_list.append(server_dict)
        self.servers = converted_server_list
        update_config(self.__dict__)

    #loader for config.json file
    def config_handler(self):
        try:
            playerlist_file = open('config.json', 'r')
            json_file = load(playerlist_file)
        except FileNotFoundError:
            print (f"{colour.error} No config.json file found. {colour.default}")
            self.initialize()
        except Exception:
            print (f"{colour.error} Other error occurred. {colour.default}")
        else:
            playerlist_file.close()
            return json_file

    #loads config.json values / Initializes a config.json file if one is not found
    def load_config(self):
        json_file = self.config_handler()
        self.players = json_file["players"]
        self.servers = json_file["servers"]
        self.interval = json_file["interval"]

    #remove specified player from checking list in config
    def delete_player(self):
        if (len(self.players) == 0):
            print (f"{colour.error}No players to delete{colour.default}")
            return
        elif (len(self.players) == 1):
            self.players.pop()
            update_config(self.__dict__)
            return
        while True:
            del_player = input(f"{colour.default} Enter player name (case sensitive) enter 'x' when finished:    ")
            if (del_player == "x"):
                break
            elif (del_player in self.players):
                self.players.remove(del_player)
                update_config(self.__dict__)
            else:
                print (f"{colour.error} Player is not found in config {colour.default}")

    #append new players to players list
    def add_player(self):
        while True:
            new_player = input(f"{colour.default} Enter player name (enter 'x' when finished):    ")
            if (new_player == "x"):
                break
            elif (new_player in self.players):
                print (f"{colour.error} Player is already on list. {colour.default}")
            else:
                self.players.append(new_player)
                update_config(self.__dict__)

    #prints all servers and corresponding indexes
    def server_index_printer(self):
        print("--------------------------------")
        for index in range(len(self.servers)):
            print(f"{index}: {self.servers[index]['url']} \n")
        print("--------------------------------")

    #if main web scrape is not working, use alt_link of each server
    def add_alt_links(self):
        self.server_index_printer()
        try:
            server_index = int(input(f"{colour.default} Enter index (number) of server to add/change alt link to:     "))
            new_alt_link = input(f"{colour.default} Enter alt link for server on minecraft-statistic.net: ")
            self.servers[server_index]['alt_link'] = new_alt_link
        except ValueError:
            print(f"{colour.error} Invalid Input Given.{colour.default}")
        except IndexError:
            print(f"{colour.error} Index does not match a given server.{colour.default}")
        else:
            update_config(self.__dict__)

    #delete alt link for given server index
    def del_alt_links(self):
        self.server_index_printer()
        try:
            deletion_index = int(input(f"{colour.default} Enter index (number) of server to delete alt link to:    {colour.default}"))
            if self.servers[deletion_index]['alt_link'] is None: raise KeyError
            self.servers[deletion_index]['alt_link'] = None
        except ValueError:
            print(f"{colour.error} Invalid Input Given. {colour.default}")
        except IndexError:
            print(f"{colour.error} Index does not match a given server.{colour.default}")
        except KeyError:
            print(f"{colour.error} Server does not have an alt link to delete.{colour.default}")
        else:
            update_config(self.__dict__)

    #prints config values to console
    def print_values(self):
        self.load_config()
        print (f"{colour.default}Number of Servers checking:  {len(self.servers)}")
        print(f"{colour.default}Number of Players checking: {len(self.players)}")
        print (f"{colour.default}Checking for players: {self.players} \n")
        for each_server in self.servers:
            print (f"{colour.default}IP: {each_server['url']} ")
            print (f"{colour.default}Target: {each_server['target']}" )
            print ("-------------------------------")

    #Change the number or size of playerlist to ping user for (Value 0 if setting is off, default is also 0)
    def change_target(self):
        self.server_index_printer()
        try:
            server_index = int(input(f"{colour.default} Enter index (number) of server to change target for:    "))
            self.servers[server_index]['target'] = int(input(f"{colour.default}Enter number target for {self.servers[server_index]['url']}:    "))
        except ValueError:
            print(f"{colour.error} Invalid input given. {colour.default}")
        else:
            update_config(self.__dict__)

    #change server ip to be checked
    def add_server(self):
        new_server = Server()
        user_input = input(f"{colour.default} Enter Server IP (enter 'x' to cancel):   ")
        if (user_input == 'x'):
            return
        new_server.url = user_input
        user_input = input(f"{colour.default}  Add an alt link? 'y' if yes, enter to skip. ")
        if (user_input == "y".casefold()):
            new_server.alt_link = input(f"{colour.default} Enter alt link for server:  ")
        self.servers.append(new_server.__dict__)
        update_config(self.__dict__)

    #delete specified player from checking list in config
    def delete_server(self):
        if (len(self.servers) == 0):
            print (f"{colour.error}No servers to delete.{colour.default}")
            return
        elif (len(self.servers) == 1):
            self.servers.pop()
            return
        self.server_index_printer()
        deletion_index = input(f"{colour.default} Enter index (number) of server to delete (enter 'x' to cancel):")
        if (deletion_index== "x"):
            return
        try:
            deletion_index = int(deletion_index)
            self.servers.pop(deletion_index)
        except ValueError:
            print (f"{colour.error}Invalid Entry.{colour.default}")
        except IndexError:
            print (f"{colour.error}Input does not correspond to a server index.{colour.default}")
        else:
            update_config(self.__dict__)

    #change interval between each GET request
    def change_interval(self):
            try:
                self.interval = int(input(f"{colour.default} Enter an interval in seconds between each fetch (Anything over 30 is ill-advised.)")) #default all
            except ValueError:
                print (f"{colour.error} Input Error {colour.default}")
            else:
                update_config(self.__dict__)