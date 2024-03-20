import discord
import os
from re import search
from dotenv import load_dotenv, set_key
from threading import Thread, active_count
from datetime import datetime
from time import sleep
from utils import *


#flushes the online list of all players who are not listed in config.json
def currently_online_flush(config):
    for each_server in config.servers:
        state.currently_online_list[each_server["url"]] = list(filter(lambda player: player in config.players, state.currently_online_list[each_server["url"]]))

#log all players that log on to server
def login_check_all(online_list, server, config):
    for each_player in online_list:
        if each_player not in state.currently_online_list[server]:
            state.append_current_list(server, each_player)
            if each_player in config.players:
                play_sound("login.wav")
                yield (f"> {each_player} seen online at {datetime.now().strftime('%D  %H:%M:%S')} on Server: {server}")
            else:
                yield (f"> {each_player} seen online at {datetime.now().strftime('%D  %H:%M:%S')} on Server: {server}")

#log players in config who log on to server
def login_check(online_list, server, config):
    found_list = list(set(config.players).intersection(online_list))
    for each_player in found_list:
        if (each_player in state.currently_online_list[server]):
            continue
        yield (f"> {each_player} seen online at {datetime.now().strftime('%D  %H:%M:%S')} on Server: {server}")
        state.append_current_list(server, each_player)
        play_sound("login.wav")

#log players that log out
def logout_check(online_list, server, config):
    for each_player in state.currently_online_list[server]:
        if (each_player not in online_list):
            state.remove_current_list(server, each_player)
            if (each_player in config.players):
                play_sound("logout.wav")
                yield (f"> {each_player} logged off at {datetime.now().strftime('%D  %H:%M:%S')} on Server: {server}")
            else:
                yield (f"> {each_player} logged off at {datetime.now().strftime('%D  %H:%M:%S')} on Server: {server}")

# quick command function that displays to users all online players in config servers
def quick_check(config):
    print_list = []
    for each_server in config.servers:
        server_object = get_server_object(each_server["url"])
        online_list = get_online_list(server_object)
        if (online_list == None):
            return
        print_list.append(f"[ {get_player_count(server_object)} ] Players online.")
        for each_player in online_list:
            if (each_player in config.players):
                print_list.append(f"> {each_player} seen online at {datetime.now().strftime('%D  %H:%M:%S')} on Server: {each_server['url']}")
            else:
                print_list.append(f"> {each_player} seen online at {datetime.now().strftime('%D  %H:%M:%S')} on Server: {each_server['url']}")
    return print_list

#check if server size has reached specified target number
def target_check(server, player_count):
    if (server['target'] == 0):
        return
    if (player_count >= server['target'] and state.target_reached[server["url"]] is False):
        state.target_reached[server["url"]] = True
        play_sound("chime.wav")
        print (f"[ {server['url']} ] has hit {server['target']} players at {datetime.now().strftime('%D  %H:%M:%S')} ")
    elif (player_count < server['target'] and state.target_reached[server["url"]] is True):
        state.target_reached[server["url"]] = False

#checks for newly joined players and players who have logged
def checker(config):
    for each_server in config.servers:
        server_object = get_server_object(each_server["url"])
        online_list = get_online_list(server_object)
        if (online_list is None):
            return
        if (config.logall_on):
            yield from login_check_all(online_list, each_server["url"], config)
        else:
            yield from login_check(online_list, each_server["url"], config)
        yield from logout_check(online_list, each_server["url"], config)
        player_count = get_player_count(server_object)
        if (player_count > 11 and state.limit_exceeded == False) or (player_count < 11 and state.limit_exceeded == True):
            state.toggle_limit_exceeded(config.limit_warning_on)
            state.exceed_warning(config.limit_warning_on, player_count)
        target_check(each_server, player_count)

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
        print("Checker already running.")
        return False
    if (len(config.players) == 0):
        print (" Checker cannot start if there are no players to look for. \nCheck configurations or add players and try again.")
        return False
    if (len(config.servers) == 0):
        print (" Checker cannot start if there are no servers to check. \nCheck configurations or add servers and try again.")
        return False
    if not (internet_is_working()):
        print (" No internet connection. Check connection before starting.")
        return False
    for each_server in config.servers:
        if not(server_is_valid(each_server["url"])):
            return False
    return True

#start application
def start(config):
    config.load_config()
    if not (start_conditions_met(config)):
        return False
    print ("Starting checker...")
    state.toggle_continue()
    process = Thread(target=lambda: looper(config))
    process.start()
    print (" Checker started. ")
    return True

#stop application
def stop(config):
    if (active_count() == 1):
        print ("Checker not running.")
        return False
    print ("Stopping checker...\n ")
    state.toggle_continue()
    for each_server in config.servers:
        state.reset_current_list(each_server["url"])
    print("Checker stopped.\n ")
    return True

def load_key():
    try:
        key_file = open(".env","r")
    except FileNotFoundError:
        print ("No .env API key file given.")
        user_input = str(input("Please enter an API Key. For help or more information please refer to Documentation: \n"))
        new_key_file = open(".env","x")
        new_key_file.write(f"API_KEY={user_input}\nPREFIX=+")
        new_key_file.close()
    finally:
        load_dotenv()

def change_channel(channel):
    try:
        os.environ["CHANNEL_ID"] = str(channel)
        set_key(".env", "CHANNEL_ID", os.environ["CHANNEL_ID"])
    except Exception:
        print ("Error occurred changing Channel_ID for logs.")
        return False
    else:
        return True

def change_prefix(new_prefix):
    if (len(new_prefix) > 1):
        return ("Prefix must be 1 character")
    os.environ["PREFIX"] = new_prefix
    set_key(".env", "PREFIX", os.environ["PREFIX"])
    return (f"Prefix changed to {os.environ['PREFIX']}")

def set_channel():
    try:
        channel_id = os.getenv("CHANNEL_ID")
    except Exception:
        print ("Channel ID is not set in .env file. Type ")

def set_prefix():
    prefix = os.getenv("PREFIX")
    if (len(prefix) > 1):
        print ("Prefix must be 1 character. Check .env file before starting.")
        return False
    return True

intents = discord.Intents.all()
intents.members = True
client = discord.Client(intents=intents)
#client = discord.commands.Bot(command_prefix="+", intents=intents)
global prefix
global channel_id
load_key()
set_prefix()
set_channel()
config = Config()
config.load_config()
state = ApplicationState()
state.initialize()
for each_server in config.servers:
    state.reset_current_list(each_server["url"])
    state.target_reached[each_server["url"]] = []

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    print('Ready!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    msg = message.content.lower()
    if (msg.startswith(f'{os.getenv("PREFIX")}ping')):
        await message.channel.send('Pong.')

    elif (msg.startswith(f'{os.getenv("PREFIX")}online')):
        print_list = quick_check(config)
        for each_print in print_list:
            await message.channel.send(each_print)
    elif (msg.startswith(f'{os.getenv("PREFIX")}start')):
        if (start(config)):
            await message.channel.send('Checker started.')
        else:
            await message.channel.send('Checker already started.')
    elif (msg.startswith(f'{os.getenv("PREFIX")}stop')):
        if (stop(config)):
            await message.channel.send('Checker stopped.')
        else:
            await message.channel.send('Checker is not on.')
    elif (msg.startswith(f'{os.getenv("PREFIX")}config')):

        await message.channel.send('')
    elif (msg.startswith(f'{os.getenv("PREFIX")}setchannel')):
        change_channel(message.channel.id)
        await message.channel.send(f"{message.channel} is now set for logs.")
    elif (msg.startswith(f'{os.getenv("PREFIX")}logall')):
        toggle_all_players(config)
        await message.channel.send('')
    elif (msg.startswith(f'{os.getenv("PREFIX")}prefix')):
        if (len(msg) != 8 and " " not in msg[-2:] and not bool(search("[*&^%$#@!+_=|?><.:;~]", msg[-1:]))):
            await message.channel.send("Prefix must be 1 character from selection: *&^%$#@!+_=|?><.:;~")
            return
        await message.channel.send(change_prefix(msg[-1:]))

client.run(os.getenv("API_KEY"))