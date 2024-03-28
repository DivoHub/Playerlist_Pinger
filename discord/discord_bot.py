import discord
from discord.ext import tasks
import os
from re import search
from dotenv import load_dotenv, set_key
from datetime import datetime
from utils import *


#flushes the online list of all players who are not listed in config.json
def currently_online_flush(config):
    for each_server in config.servers:
        state.currently_online_list[each_server["url"]] = list(filter(lambda player: player in config.players, state.currently_online_list[each_server["url"]]))

#log all players that log on to server
def login_check_all(online_list, server, config):
    print_list = []
    for each_player in online_list:
        if each_player not in state.currently_online_list[server]:
            state.append_current_list(server, each_player)
            if each_player in config.players:
                print_list.append(f"> {each_player} seen online at {datetime.now().strftime('%D  %H:%M:%S')} on Server: {server}")
            else:
                print_list.append(f"> {each_player} seen online at {datetime.now().strftime('%D  %H:%M:%S')} on Server: {server}")
    return print_list

#log players in config who log on to server
def login_check(online_list, server, config):
    print_list = []
    found_list = list(set(config.players).intersection(online_list))
    for each_player in found_list:
        if (each_player in state.currently_online_list[server]):
            continue
        print_list.append(f"> {each_player} seen online at {datetime.now().strftime('%D  %H:%M:%S')} on Server: {server}")
        state.append_current_list(server, each_player)
    return print_list

#log players that log out
def logout_check(online_list, server, config):
    print_list = []
    for each_player in state.currently_online_list[server]:
        if (each_player not in online_list):
            state.remove_current_list(server, each_player)
            if (each_player in config.players):
                print_list.append(f"> {each_player} logged off at {datetime.now().strftime('%D  %H:%M:%S')} on Server: {server}")
            else:
                print_list.append(f"> {each_player} logged off at {datetime.now().strftime('%D  %H:%M:%S')} on Server: {server}")
    return print_list

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
        return (f"[ {server['url']} ] reached {server['target']} players at {datetime.now().strftime('%D  %H:%M:%S')} ")
    elif (player_count < server['target'] and state.target_reached[server["url"]] is True):
        state.target_reached[server["url"]] = False

#checks for newly joined players and players who have logged
def checker(config):
    for each_server in config.servers:
        server_object = get_server_object(each_server["url"])
        online_list = get_online_list(server_object)
        print_list = []
        if (online_list is None):
            return
        if (config.logall_on):
            print_list.extend(login_check_all(online_list, each_server["url"], config))
        else:
            print_list.extend(login_check(online_list, each_server["url"], config))
        print_list.extend(logout_check(online_list, each_server["url"], config))
        player_count = get_player_count(server_object)
        if (player_count > 11 and state.limit_exceeded == False) or (player_count < 11 and state.limit_exceeded == True):
            state.toggle_limit_exceeded(config.limit_warning_on)
            state.exceed_warning(config.limit_warning_on, player_count)
        target_check_string = target_check(each_server, player_count)
        if (target_check_string):
            print_list.append(target_check_string)
        return print_list

#checks if checker is already running, and verifies the validity of config.json file
def start_conditions_met(config):
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

def load_env():
    try:
        open(".env","r")
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

def delete_server(server_list, ip):
    for each_server in server_list:
        if (each_server["url"] == ip):
            server_list.remove(each_server)
            return True
    return Exception ValueError

intents = discord.Intents.all()
intents.members = True
client = discord.Client(intents=intents)
#client = discord.commands.Bot(command_prefix="+", intents=intents)
load_env()
config = Config()
config.load_config()
state = ApplicationState()
state.initialize()
for each_server in config.servers:
    state.reset_current_list(each_server["url"])
    state.target_reached[each_server["url"]] = []


@tasks.loop(seconds=config.interval)
async def looper():
    state.error_count = 0
    channel = client.get_channel(int(os.environ["CHANNEL_ID"]))
    if not channel:
        print ("No channel set for logging.")
        return
    config.load_config()
    status_log = checker(config)
    state.error_handler(status_log, config.interval)
    if (status_log == None):
        return
    for each_status in status_log:
        await channel.send(each_status)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    print('Checker starting...')
    looper.start()
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
        try:
            looper.start()
        except RuntimeError:
            await message.channel.send('Checker is already running')
        else:
            await message.channel.send('Checker started.')
    elif (msg.startswith(f'{os.getenv("PREFIX")}stop')):
        try:
            looper.stop()
        except RuntimeError:
            await message.channel.send('Checker is not running.')
        else:
            await message.channel.send('Checker stopped.')
    elif (msg.startswith(f'{os.getenv("PREFIX")}config')):
        await message.channel.send((f"Searching for {len(config.players)} players: {str(config.players)}"))
        await message.channel.send((f"On {len(config.servers)} Servers: "))
        for each_server in config.servers:
            await message.channel.send((f"{each_server['url']}"))
    elif (msg.startswith(f'{os.getenv("PREFIX")}setchannel')):
        change_channel(message.channel.id)
        await message.channel.send(f"{message.channel} is now set for logs.")
    elif (msg.startswith(f'{os.getenv("PREFIX")}logall')):
        toggle_all_players(config)
        if config.logall_on:
            currently_online_flush(config)
            await message.channel.send('Logging all Player Traffic')
        else:
            currently_online_flush(config)
            await message.channel.send('Logging only specified players')
    elif (msg.startswith(f'{os.getenv("PREFIX")}prefix')):
        if (len(msg) != 8 and " " not in msg[-2:] and not bool(search("[*&^%$#@!+_=|?><.:;~]", msg[-1:]))):
            await message.channel.send("Prefix must be 1 character from selection: *&^%$#@!+_=|?><.:;~")
            return
    elif (msg.startswith(f'{os.getenv("PREFIX")}addplayer ')):
        player = msg.split()[-1]
        config.players.append(player)
        config.update_config(config.__dict__)
        await message.channel.send(f"{player} has been added to the config.")
    elif (msg.startswith(f'{os.getenv("PREFIX")}addserver ')):
        server = msg.split()[-1]
        config.servers.append{"url": server, "target": 10}
        config.update_config(config.__dict__)
        await message.channel.send(f"{server} has been added to the config.")
    elif (msg.startswith(f'{os.getenv("PREFIX")}delplayer ')):
        player = msg.split()[-1]
        try:
            config.players.remove(player)
        except ValueError:
            await message.channel.send(f"{player} is not found in the config.")
        else:
            config.update_config(config.__dict__)
            await message.channel.send(f"{player} has been added to the config.")
    elif (msg.startswith(f'{os.getenv("PREFIX")}delserver ')):
        server = msg.split()[-1]
        try:
            delete_server(config.servers, server)
        except ValueError:
            await message.channel.send(f"{server} was not found in the config.")
        else:
            config.update_config(config.__dict__)
            await message.channel.send(f"{server} has been added to the config.")

client.run(os.getenv("API_KEY"))