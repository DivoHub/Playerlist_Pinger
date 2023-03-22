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