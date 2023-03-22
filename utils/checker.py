
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