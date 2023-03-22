
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

#Returns InnerHTML string of given HTML elements/class
def get_innerHTML(element):
    return element.string
