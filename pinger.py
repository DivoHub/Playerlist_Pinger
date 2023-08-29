from threading import Thread, active_count
from datetime import datetime
from time import sleep
from utils import *


#log all players that log on to server
def login_check_all(online_list, server):
    global currently_online_list
    login_list = []
    for each_player in online_list:
        if (each_player not in currently_online_list[server]):
            currently_online_list[server].append(each_player)
            if (each_player in config.players):
                play_sound("login.wav")
                login_list.append(f"{Colour().green} > {each_player} seen online at {datetime.now().strftime('%D  %H:%M:%S')} on Server: {server}{Colour().default}")
            else:
                login_list.append(f"{Colour().default} > {each_player} seen online at {datetime.now().strftime('%D  %H:%M:%S')} on Server: {server} {Colour().default}")
    return login_list

#flushes the online list of all players who are not listed in config.json
def currently_online_flush():
    global currently_online_list
    global config
    for each_server in config.servers:
        currently_online_list[each_server['url']] = list(filter(lambda player: player in config.players, currently_online_list[each_server['url']]))

#Toggle between logging all player traffic, and logging specified player traffic
def toggle_all_players():
    global config
    if (config.logall_on):
        config.logall_on = False
        currently_online_flush()
        print (f"{Colour().red} Log All Players Off.{Colour().default}")
    else:
        config.logall_on = True
        print (f"{Colour().green} Log All Players On.{Colour().default}")
    update_config(config.__dict__)

#Select between websites to scrape player list data
def website_selector():
    global config
    print (f"{Colour().default}__________________________________________")
    print (f"Choose from the 3 websites to retrieve player list data (Enter the corresponding number.")
    print ("1. https://minecraftlist.com/\n2. https://minecraft-statistic.net/ \n3. https://mcsrvstat.us/")
    print (f"{Colour().default}__________________________________________")
    while True:
        user_input = input()
        if (type(user_input) != int):
            print(f"{Colour().error}Input is not a number.{Colour().default}")
            continue
        elif (user_input > 3 and user_input < 1):
            print (f"{Colour().error}Input out of range.{Colour().default}")
            continue
        elif (user_input == 1):
            config.website = "https://minecraftlist.com/"
            break
        elif (user_input == 2):
            config.website = "https://minecraft-statistic.net/"
            break
        elif (user_input == 3):
            config.website = "https://mcsrvstat.us/"
            break
    print (f"Website changed to: {config.website}")
    update_config(config.__dict__)

#turn off and on logger module.
def toggle_logger():
    global config
    if (config.logger_on):
        config.logger_on = False
        print (f"{Colour().red} Logger turned off.{Colour().default}")
    else:
        config.logger_on = True
        print (f"{Colour().green} logger turned on.{Colour().default}")
    update_config(config.__dict__)

#check if server size has reached specified target number
def target_check(player_count, server):
    global config
    if (server['target'] == 0):
        return
    global target_reached
    if (player_count >= server['target'] and target_reached[server['url']] is False):
        target_reached[server['url']] = True
        play_sound("chime.wav")
        print (f"{Colour().blue} {server} has hit {config.target} players at {datetime.now().strftime('%D  %H:%M:%S')} ")
    elif (player_count < server['target'] and target_reached[server['url']] is True):
        target_reached[server['url']] = False

#log players in config who log on to server
def login_check(online_list, server):
    global config
    global currently_online_list
    found_list = list(set(config.players).intersection(online_list))
    login_list = []
    for each_player in found_list:
        if (each_player not in currently_online_list[server]):
            login_list.append(f"{Colour().green} > {each_player} seen online at {datetime.now().strftime('%D  %H:%M:%S')} on Server: {server}{Colour().default}")
            currently_online_list[server].append(each_player)
            play_sound("login.wav")
    return login_list

#log players that log out
def logout_check(online_list, server):
    global config
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

# quick command function that displays to users all online players in config servers (refactor because ugly)
def quick_check():
    global config
    for each_server in config.servers:
        if (config.alt_checker_on):
            online_list = get_online_list_alt(each_server['alt_link'], each_server['url'])
        else:
            online_list = get_online_list(each_server['url'])
        if (online_list == None or type(online_list) == bool):
            return
        elif (len(online_list) == 0):
            print(f"{Colour().blue} 0 players found on Server: {each_server['url']}{Colour().default}")
        else:
            for each_player in online_list:
                if (each_player in config.players):
                    print(f"{Colour().green} > {each_player} seen online at {datetime.now().strftime('%D  %H:%M:%S')} on Server: {each_server['url']}{Colour().default}")
                else:
                    print(f"{Colour().default} > {each_player} seen online at {datetime.now().strftime('%D  %H:%M:%S')} on Server: {each_server['url']}")
    play_sound(str("chime.wav"))

#checks for newly joined players and players who have logged
def checker():
    global config
    log_list = []
    for each_server in config.servers:
        if (config.alt_checker_on):
            online_list = get_online_list_alt(each_server['alt_link'], each_server['url'])
        else:
            online_list = get_online_list(each_server['url'])
        if (online_list == False):
            break
        if (config.logall_on):
            log_list.extend(login_check_all(online_list, each_server['url']))
        else:
            log_list.extend(login_check(online_list, each_server['url']))
        log_list.extend(logout_check(online_list, each_server['url']))
        target_check(len(online_list), each_server)
    return log_list

def wait():
    global config
    global continue_condition
    for timer in range(config.interval):
        if continue_condition:
            sleep(1)
        else:
            break

# iterative function, continues if user has not stopped
def looper():
    global config
    global continue_condition
    while continue_condition:
        config.load_config()
        status_log = checker()
        for each_status in status_log:
            print(each_status)
            if (config.logger_on):
                logger(each_status)
        wait()


def start_conditions_met():
    global config
    if (active_count() > 1):
        print(f"{Colour().default} Checker already running.")
        return False
    if (len(config.players) == 0):
        print (f"{Colour().error} Checker cannot start if there are no players to look for. \nCheck configurations or add players and try again. ")
        return False
    if (len(config.servers) == 0):
        print (f"{Colour().error} Checker cannot start if there are no servers to check. \nCheck configurations or add servers and try again. ")
        return False
    if not(servers_are_valid(config)):
        print (f"{Colour().error} Invalid server error...\n check configurations or connection, and try again.{Colour().default}")
        return False
    return True


#start application
def start():
    if not (start_conditions_met()):
        return
    print (f"{Colour().green} Starting checker... {Colour().default}")
    global continue_condition
    continue_condition = True
    process = Thread(target=looper)
    process.start()
    print (f"{Colour().green} Checker started. {Colour().default}")


#stop application
def stop():
    global config
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


def init():
    global config
    global continue_condition
    global currently_online_list
    global target_reached
    config = Config()
    config.config_handler()
    continue_condition = True
    currently_online_list = {}
    target_reached = {}
    for each_server in config.servers:
        currently_online_list[each_server['url']] = []
        target_reached[each_server['url']] = False

#main user input command line interface for application
def main():
    global currently_online_list
    print(f"Welcome to the Minecraft Java Edition Playerlist Pinger. Type 'help' to see list of commands.\n------------------------------------------- ")
    while True:
        print (f"{Colour().default} -------------------------")
        user_input = input()
        print (f"{Colour().default} -------------------------")
        match user_input:
            case "":
                print(f"{Colour().default}\n")
            case "exit":
                stop()
                print(f"{Colour().red} Program exiting. {Colour().default}")
                break
            case "addplayer":
                config.add_player()
            case "delplayer":
                config.delete_player()
            case "addserver":
                added_server = config.add_server()
                if (added_server != None):
                    currently_online_list[added_server] = []
            case "delserver":
                deleted_server = config.delete_server()
                if (deleted_server != None):
                    del currently_online_list[deleted_server]
            case "interval":
                config.change_interval()
            case "online":
                quick_check()
            case "target":
                config.change_target()
            case "config":
                config.print_values()
            case "logger":
                toggle_logger()
            case "logall":
                toggle_all_players()
            case "web":
                website_selector()
            case "addalt":
                config.add_alt_links()
            case "delalt":
                config.del_alt_links()
            case "newlog":
                refresh_log()
            case "fresh":
                config.start_new()
            case "start":
                start()
            case "stop":
                stop()
            case "help":
                print_manual()
            case _:
                print (f"{Colour().error} Unknown command. {Colour().default}")

if __name__ == '__main__':
    init()
    main()
