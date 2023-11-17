from threading import Thread, active_count
from datetime import datetime
from time import sleep
from utils import *
import logging

#flushes the online list of all players who are not listed in config.json
def currently_online_flush(config):
    for each_server in config.servers:
        state.currently_online_list[each_server["url"]] = list(filter(lambda player: player in config.players, state.currently_online_list[each_server["url"]]))

#log all players that log on to server
def login_check_all(online_list, server, config):
    login_list = []
    for each_player in online_list:
        if (each_player in state.currently_online_list[server]):
            continue
        state.append_current_list(server, each_player)
        if (each_player in config.players):
            play_sound("login.wav")
            login_list.append(f"{Colour().green} > {each_player} seen online at {datetime.now().strftime('%D  %H:%M:%S')} on Server: {server}{Colour().default}")
        else:
            login_list.append(f"{Colour().default} > {each_player} seen online at {datetime.now().strftime('%D  %H:%M:%S')} on Server: {server} {Colour().default}")
    return login_list


#log players in config who log on to server
def login_check(online_list, server, config):
    found_list = list(set(config.players).intersection(online_list))
    login_list = []
    for each_player in found_list:
        if (each_player in state.currently_online_list[server]):
            continue
        login_list.append(f"{Colour().green} > {each_player} seen online at {datetime.now().strftime('%D  %H:%M:%S')} on Server: {server}{Colour().default}")
        state.append_current_list(server, each_player)
        play_sound("login.wav")
    return login_list

#log players that log out
def logout_check(online_list, server, config):
    logout_list = []
    for each_player in state.currently_online_list[server]:
        if (each_player not in online_list):
            state.remove_current_list(server, each_player)
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

#check if server size has reached specified target number
def target_check(server, player_count):
    if (server['target'] == 0):
        return
    if (player_count >= server['target'] and state.target_reached[server["url"]] is False):
        state.target_reached[server["url"]] = True
        play_sound("chime.wav")
        print (f"{Colour().blue}[ {server['url']} ] has hit {server['target']} players at {datetime.now().strftime('%D  %H:%M:%S')} ")
    elif (player_count < server['target'] and state.target_reached[server["url"]] is True):
        state.target_reached[server["url"]] = False

#checks for newly joined players and players who have logged
def checker(config):
    log_list = []
    for each_server in config.servers:
        server_object = get_server_object(each_server["url"])
        online_list = get_online_list(server_object)
        if (online_list == None):
            return None
        if (config.logall_on):
            log_list.extend(login_check_all(online_list, each_server["url"], config))
        else:
            log_list.extend(login_check(online_list, each_server["url"], config))
        log_list.extend(logout_check(online_list, each_server["url"], config))
        player_count = get_player_count(server_object)
        target_check(each_server, player_count)
        return log_list

#looper thread sleeps for configured time
def wait(interval):
    for timer in range(interval):
        if state.continuing:
            sleep(1)
        else:
            break

#iterative function, continues if user has not stopped
def looper(config):
    state.error_count = 0
    while state.continuing:
        config.load_config()
        status_log = checker(config)
        state.error_handler(status_log, config.interval)
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
        if not(server_is_valid(each_server["url"])):
            return False
    return True

#start application
def start(config):
    config.load_config()
    if not (start_conditions_met(config)):
        return
    print (f"{Colour().green} Starting checker... {Colour().default}")
    state.toggle_continue()
    process = Thread(target=lambda: looper(config))
    process.start()
    print (f"{Colour().green} Checker started. {Colour().default}")

#stop application
def stop(config):
    if (active_count() == 1):
        print (f"{Colour().default} Checker not running.")
        return
    print (f"{Colour().red} Stopping checker...\n {Colour().default}")
    state.toggle_continue()
    for each_server in config.servers:
        state.reset_current_list(each_server)
    print(f"{Colour().red} Checker stopped.\n {Colour().default}")

#main user input command line interface for application
def main(config):
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
                if (added_server == None):
                    continue
                state.add_current_list(added_server)
            case "delserver":
                deleted_server = config.delete_server()
                if (deleted_server == None):
                    continue
                state.delete_current_list(deleted_server)
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
    print("Welcome to the Minecraft Java Edition Playerlist Pinger. Type 'help' to see list of commands.\n------------------------------------------- ")
    logging.basicConfig(level=logging.INFO, filename="errors.log", filemode="a", format="%(asctime)s - %(levelname)s - %(message)s")
    config = Config()
    config.load_config()
    config.print_values()
    state = ApplicationState()
    state.initialize()
    for each_server in config.servers:
        state.reset_current_list(each_server["url"])
        state.target_reached[each_server["url"]] = []
    main(config)
