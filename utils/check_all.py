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

#flushes the online list of all players who are not listed in config.json
def currently_online_flush():
    global currently_online_list
    for each_server in config.servers:
        currently_online_list[each_server]['url'] = list(filter(lambda player: player in config.players, currently_online_list[each_server]))
    return
