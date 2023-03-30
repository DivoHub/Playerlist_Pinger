import .utils.alt_checker

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
