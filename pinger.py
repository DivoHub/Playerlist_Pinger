from bs4 import BeautifulSoup
from datetime import datetime
from json import dumps, load
from requests import get
from simpleaudio import WaveObject
from threading import Thread, active_count
from time import sleep

from utils import colour, config, server


#Prints help manual to console
def print_manual():
    manual = open('help.txt', 'r')
    print (manual.read())
    manual.close()

#create config.json file / no return variable
def create_config():
    print(f"{colour.default} Creating new config.json file.")
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
def servers_are_valid():
    for each_server in config.servers:
        if (len(each_server['url']) == 0):
            print (f"{colour.error} No Server IP given {colour.default}")
            return False
        status_code = get("https://minecraftlist.com/servers/" + each_server['url']).status_code
        if (status_code >= 200 and status_code <= 299):
            return True
        elif (status_code == 404):
            print(f"{colour.error} Invalid Server entered. {colour.default}")
            return False
        else:
            print(f"{colour.error} Connection error {colour.default}")
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

def currently_online_flush():
    global currently_online_list
    for each_server in config.servers:
        currently_online_list[each_server]['url'] = list(filter(lambda player: player in config.players, currently_online_list[each_server]))
    return

def toggle_alt_checker():
    global use_alt_checker
    if (use_alt_checker):
        use_alt_checker = False
        print (f"{colour.red} Alt Website checker turned off.{colour.default}")
    else:
        use_alt_checker = True
        print (f"{colour.green} Alt Website checker turned on.{colour.default}")
    return

#turn off and on logger module.
def toggle_logger():
    global logger_is_on
    if (logger_is_on):
        logger_is_on = False
        print (f"{colour.red} Logger turned off.{colour.default}")
    else:
        logger_is_on = True
        print (f"{colour.green} logger turned on.{colour.default}")
    return

def toggle_all_players():
    global log_all_players
    if (log_all_players):
        log_all_players = False
        currently_online_flush()
        print (f"{colour.red} Log All Players Off.{colour.default}")
    else:
        log_all_players = True
        print (f"{colour.green} Log All Players On.{colour.default}")
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
        print (f"{colour.error} Error making HTTP request at {datetime.now().strftime('%D  %H:%M:%S')} {colour.default}")
        return False
    else:
        new_request = BeautifulSoup(new_request.text, "html.parser")
        player_elements = new_request.find_all("a", class_="block no-underline hover:bg-gray-200 px-2 py-1 flex items-center text-gray-800")
        #last_checked = html_doc.find("p", class_="text-center text-gray-500").text
        player_list = []
        for each_element in player_elements:
            player = each_element.find("span", class_="truncate")
            player_list.append(player)
        online_list = list(map(get_innerHTML, player_list))
        return online_list

#get online list from different website if minecraftlist.net is out of service
def get_online_list_alt(alt_link):
    if (alt_link == None):
        return False
    try:
        new_request = get(alt_link)
        new_request = BeautifulSoup(new_request.text, "html.parser")
        player_list = new_request.find_all("a", class_="c-black")
    except Exception:
        print (f"{colour.error} Error making HTTP request at {datetime.now().strftime('%D  %H:%M:%S')} {colour.default}")
        return False
    else:
        player_list = list(map(get_innerHTML, player_list))
        return player_list

#play notification sound
def play_sound(sound_file):
        try:
            audio_object = WaveObject.from_wave_file(f"./sounds/{sound_file}")
            play = audio_object.play()
            play.wait_done()
            play.stop()
        except FileNotFoundError:
            print(f"{colour.error} {sound_file} file not found. {colour.default}")
        except Exception:
            print (f"{colour.error} Error with playing notification audio. {colour.default}")
        finally:
            return

#check if server size has reached specified target number
def target_check(player_count, server):
    if (server['target'] == 0):
        return
    global target_reached
    if (player_count >= server['target'] and target_reached[server['url']] is False):
        target_reached[server['url']] = True
        play_sound("chime.wav")
        print (f"{colour.blue} {server} has hit {config.target} players at {datetime.now().strftime('%D  %H:%M:%S')} ")
    elif (player_count < server['target'] and target_reached[server['url']] is True):
        target_reached[server['url']] = False

#log all players that log on to server
def login_check_all(online_list, server):
    global currently_online_list
    login_list = []
    for each_player in online_list:
        if (each_player not in currently_online_list[server]):
            currently_online_list[server].append(each_player)
            if (each_player in config.players):
                play_sound("login.wav")
                login_list.append(f"{colour.green} > {each_player} seen online at {datetime.now().strftime('%D  %H:%M:%S')} on Server: {server}{colour.default}")
            else:
                login_list.append(f"{colour.default} > {each_player} seen online at {datetime.now().strftime('%D  %H:%M:%S')} on Server: {server} {colour.default}")
    return login_list

#log players in config who log on to server
def login_check(online_list, server):
    global currently_online_list
    found_list = list(set(config.players).intersection(online_list))
    login_list = []
    for each_player in found_list:
        if (each_player not in currently_online_list[server]):
            login_list.append(f"{colour.green} > {each_player} seen online at {datetime.now().strftime('%D  %H:%M:%S')} on Server: {server}{colour.default}")
            currently_online_list[server].append(each_player)
            play_sound("login.wav")
    return login_list

#log players that log out
def logout_check(online_list, server):
    global currently_online_list
    logout_list = []
    for each_player in currently_online_list[server]:
        if (each_player not in online_list):
            currently_online_list[server].remove(each_player)
            if (each_player in config.players):
                play_sound("logout.wav")
                logout_list.append(f"{colour.red} > {each_player} logged off at {datetime.now().strftime('%D  %H:%M:%S')} on Server: {server}{colour.default}")
            else:
                logout_list.append(f"{colour.default} > {each_player} logged off at {datetime.now().strftime('%D  %H:%M:%S')} on Server: {server}")
    return logout_list

# quick command function that displays to users all online players in config servers (refactor because ugly)
def quick_check():
    global use_alt_checker
    for each_server in config.servers:
        if (use_alt_checker):
            online_list = get_online_list_alt(each_server['alt_link'])
        else:
            online_list = get_online_list(each_server['url'])
        if (online_list == None):
            return
        elif (len(online_list) == 0):
            print(f"{colour.blue} 0 players found on Server: {each_server['url']}{colour.default}")
        else:
            for each_player in online_list:
                if (each_player in config.players):
                    print(f"{colour.green} > {each_player} seen online at {datetime.now().strftime('%D  %H:%M:%S')} on Server: {each_server['url']}{colour.default}")
                else:
                    print(f"{colour.default} > {each_player} seen online at {datetime.now().strftime('%D  %H:%M:%S')} on Server: {each_server['url']}")
    play_sound(str("chime.wav"))

#checks for newly joined players and players who have logged
def checker():
    global log_all_players
    global use_alt_checker
    log_list = []
    for each_server in config.servers:
        if (use_alt_checker):
            online_list = get_online_list_alt(each_server['alt_link'])
        else:
            online_list = get_online_list(each_server['url'])
        if (online_list == False):
            break
        if (log_all_players):
            log_list.extend(login_check_all(online_list, each_server['url']))
        else:
            log_list.extend(login_check(online_list, each_server['url']))
        log_list.extend(logout_check(online_list, each_server['url']))
        target_check(len(online_list), each_server)
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
    global logger_is_on
    while continue_condition:
        config.load_config()
        status_log = checker()
        for each_status in status_log:
            print (each_status)
            if (logger_is_on):
                logger(each_status)
        wait()

#start application
def start():
    if (active_count() > 1):
        print(f"{colour.default} Checker already running.")
        return
    if (len(config.players) == 0):
        print (f"{colour.error} Checker cannot start if there are no players to look for. \nCheck configurations or add players and try again. ")
        return
    if (len(config.servers) == 0):
        print (f"{colour.error} Checker cannot start if there are no servers to check. \nCheck configurations or add servers and try again. ")
        return
    if not(servers_are_valid()):
        print (f"{colour.error} Invalid server error...\n check configurations or connection, and try again.{colour.default}")
        return
    print (f"{colour.green} Starting checker... {colour.default}")
    global continue_condition
    continue_condition = True
    process = Thread(target=looper)
    process.start()

#stop application
def stop():
    if (active_count() == 1):
        print (f"{colour.default} Checker not running.")
        return
    print (f"{colour.red} Stopping checker.\n {colour.default}")
    global continue_condition
    global currently_online_list
    continue_condition = False
    for each_server in config.servers:
        currently_online_list[each_server['url']] = []

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
        print (f"{colour.default} -------------------------")
        user_input = input()
        print (f"{colour.default} -------------------------")
        if (user_input in command_dict.keys()):
            command_dict[user_input]()
        elif (user_input == "exit"):
            stop()
            print(f"{colour.red} Program exiting. {colour.default}")
            break
        elif (user_input == ""):
            print (f"{colour.default}\n")
        else:
            print (f"{colour.error} Unknown command. {colour.default}")


if __name__ == '__main__':
    print(f"Welcome to the Minecraft Java Edition Playerlist Pinger. Type 'help' to see list of commands.\n------------------------------------------- ")
    global continue_condition
    global currently_online_list
    global target_reached
    global logger_is_on
    global log_all_players
    global use_alt_checker
    colour = Colour()
    config = Config()
    config.config_validator()
    config.load_config()
    config.print_values()
    currently_online_list = dict()
    target_reached = dict()
    logger_is_on = False
    log_all_players = False
    use_alt_checker = False
    for each_server in config.servers:
        currently_online_list[each_server['url']] = []
        target_reached[each_server['url']] = False
    main()
