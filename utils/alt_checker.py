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

def toggle_alt_checker():
    global use_alt_checker
    if (use_alt_checker):
        use_alt_checker = False
        print (f"{colour.red} Alt Website checker turned off.{colour.default}")
    else:
        use_alt_checker = True
        print (f"{colour.green} Alt Website checker turned on.{colour.default}")
    return