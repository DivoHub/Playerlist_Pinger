from threading import Thread, active_count
from datetime import datetime
from time import sleep
from utils import *

#flushes the online list of all players who are not listed in config.json
def currently_online_flush(config):
    global currently_online_list
    for each_server in config.servers:
        currently_online_list[each_server['url']] = list(filter(lambda player: player in config.players, currently_online_list[each_server['url']]))

#turn off and on logger module.
def toggle_logger(config):
    if (config.logger_on):
        config.logger_on = False
        print (f"{Colour().red} Logger turned off.{Colour().default}")
    else:
        config.logger_on = True
        print (f"{Colour().green} logger turned on.{Colour().default}")
    update_config(config.__dict__)

#Toggle between logging all player traffic, and logging specified player traffic
def toggle_all_players(config):
    if (config.logall_on):
        config.logall_on = False
        currently_online_flush()
        print (f"{Colour().red} Log All Players Off.{Colour().default}")
    else:
        config.logall_on = True
        print (f"{Colour().green} Log All Players On.{Colour().default}")
    update_config(config.__dict__)

#log all players that log on to server
def login_check_all(online_list, server, config):
    global currently_online_list
    login_list = []
    for each_player in online_list:
        if (each_player in currently_online_list[server]):
            continue
        currently_online_list[server].append(each_player)
        if (each_player in config.players):
            play_sound("login.wav")
            login_list.append(f"{Colour().green} > {each_player} seen online at {datetime.now().strftime('%D  %H:%M:%S')} on Server: {server}{Colour().default}")
        else:
            login_list.append(f"{Colour().default} > {each_player} seen online at {datetime.now().strftime('%D  %H:%M:%S')} on Server: {server} {Colour().default}")
    return login_list


#log players in config who log on to server
def login_check(online_list, server, config):
    global currently_online_list
    found_list = list(set(config.players).intersection(online_list))
    login_list = []
    for each_player in found_list:
        if (each_player in currently_online_list[server]):
            continue
        login_list.append(f"{Colour().green} > {each_player} seen online at {datetime.now().strftime('%D  %H:%M:%S')} on Server: {server}{Colour().default}")
        currently_online_list[server].append(each_player)
        play_sound("login.wav")
    return login_list

#log players that log out
def logout_check(online_list, server, config):
    global currently_online_list
    logout_list = []
    for each_player in currently_online_list[server]:
        if (each_player not in online_list):
            currently_online_list[server].remove(each_player)
            if (each_player in config.players):
                play_sound("logout.wav")
                logout_list.append(f"{Colour().red} > {each_player} logged off at {datetime.now().strftime('%D  %H:%M:%S')} on Server: {server}{Colour().default}")
            else:
                logout_list.append(f"{Colour().default} > {each_player} logged off at {datetime.now().strftime('%D  %H:%M:%S')} on Server: {server}")
    return logout_list

# quick command function that displays to users all online players in config servers
def quick_check(config):
    for each_server in config.servers:
        server_object = get_server_object(each_server["url"])
        online_list = get_online_list(server_object)
        if (online_list == None):
            return
        print(f"{Colour().blue}  [ {get_player_count(server_object)} ] Players online. {Colour().default}")
        for each_player in online_list:
            if (each_player in config.players):
                print(f"{Colour().green} > {each_player} seen online at {datetime.now().strftime('%D  %H:%M:%S')} on Server: {each_server['url']}{Colour().default}")
            else:
                print(f"{Colour().default} > {each_player} seen online at {datetime.now().strftime('%D  %H:%M:%S')} on Server: {each_server['url']}")
    play_sound(str("chime.wav"))

#check if server size has reached specified target number
def target_check(server, player_count, config):
    if (server['target'] == 0):
        return
    global target_reached
    if (player_count >= server['target'] and target_reached[server['url']] is False):
        target_reached[server['url']] = True
        play_sound("chime.wav")
        print (f"{Colour().blue} {server} has hit {config.target} players at {datetime.now().strftime('%D  %H:%M:%S')} ")
    elif (player_count < server['target'] and target_reached[server['url']] is True):
        target_reached[server['url']] = False

#checks for newly joined players and players who have logged
def checker(config):
    log_list = []
    for each_server in config.servers:
        server_object = get_server_object(each_server["url"])
        online_list = get_online_list(server_object)
        if (online_list == None):
            return None
        if (config.logall_on):
            log_list.extend(login_check_all(online_list, each_server['url'], config))
        else:
            log_list.extend(login_check(online_list, each_server['url'], config))
        log_list.extend(logout_check(online_list, each_server['url'], config))
        player_count = get_player_count(server_object)
        target_check(each_server, player_count, config)
        return log_list

#looper thread sleeps for configured time
def wait(interval):
    global continue_condition
    for timer in range(interval):
        if continue_condition:
            sleep(1)
        else:
            break

#iterative function, continues if user has not stopped
def looper(config):
    global continue_condition
    error_count = 0
    while continue_condition:
        config.load_config()
        status_log = checker(config)
        error_count = error_handler(error_count, status_log, config.interval)
        if (status_log == None):
            wait(config.interval)
            continue
        for each_status in status_log:
            print(each_status)
            if (config.logger_on):
                logger(each_status)
        wait(config.interval)

#checks if checker is already running, and verifies the validity of config.json file
def start_conditions_met(config):
    if (active_count() > 1):
        print(f"{Colour().error} Checker already running.{Colour().default}")
        return False
    if (len(config.players) == 0):
        print (f"{Colour().error} Checker cannot start if there are no players to look for. \nCheck configurations or add players and try again. {Colour().default}")
        return False
    if (len(config.servers) == 0):
        print (f"{Colour().error} Checker cannot start if there are no servers to check. \nCheck configurations or add servers and try again. {Colour().default}")
        return False
    if not (internet_is_working()):
        print (f"{Colour().error} No internet connection. Check connection before starting.{Colour().default}")
        return False
    for each_server in config.servers:
        if not(server_is_valid(each_server['url'])):
            return False
    return True

#start application
def start(config):
    config.load_config()
    if not (start_conditions_met(config)):
        return
    print (f"{Colour().green} Starting checker... {Colour().default}")
    global continue_condition
    continue_condition = True
    process = Thread(target=lambda: looper(config))
    process.start()
    print (f"{Colour().green} Checker started. {Colour().default}")

#stop application
def stop(config):
    if (active_count() == 1):
        print (f"{Colour().default} Checker not running.")
        return
    print (f"{Colour().red} Stopping checker...\n {Colour().default}")
    global continue_condition
    global currently_online_list
    continue_condition = False
    for each_server in config.servers:
        currently_online_list[each_server['url']] = []
    print(f"{Colour().red} Checker stopped.\n {Colour().default}")

#initializes variables before application runs
def init():
    print("Welcome to the Minecraft Java Edition Playerlist Pinger. Type 'help' to see list of commands.\n------------------------------------------- ")
    global continue_condition
    global currently_online_list
    global target_reached
    config = Config()
    config.load_config()
    config.print_values()
    continue_condition = True
    currently_online_list = {}
    target_reached = {}
    for each_server in config.servers:
        currently_online_list[each_server['url']] = []
        target_reached[each_server['url']] = False
    return config


#main user input command line interface for application
def main(config):
    global currently_online_list
    while True:
        print (f"{Colour().default} -------------------------")
        user_input = input()
        print (f"{Colour().default} -------------------------")
        match user_input:
            case "":
                print(f"{Colour().default}\n")
            case "exit":
                stop(config)
                print(f"{Colour().red} Program exiting. {Colour().default}")
                break
            case "addplayer":
                config.add_player()
            case "delplayer":
                config.delete_player()
            case "addserver":
                added_server = config.add_server()
                if (added_server != None and server_is_valid(added_server)):
                    currently_online_list[added_server] = []
            case "delserver":
                deleted_server = config.delete_server()
                if (deleted_server != None):
                    del currently_online_list[deleted_server]
            case "interval":
                config.change_interval()
            case "online":
                quick_check(config)
            case "target":
                config.change_target()
            case "config":
                config.print_values()
            case "logger":
                toggle_logger(config)
            case "logall":
                toggle_all_players(config)
            case "reload":
                config.load_config()
                config.print_values()
            case "newlog":
                refresh_log()
            case "newconfig":
                config.start_new()
            case "start":
                start(config)
            case "stop":
                stop(config)
            case "help":
                print_manual()
            case _:
                print (f"{Colour().error} Unknown command. {Colour().default}")

if __name__ == '__main__':
    config = init()
    main(config)
