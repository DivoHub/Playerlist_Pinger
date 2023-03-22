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