import json, os
from sys import argv as args
from subprocess import run, PIPE
from configparser import RawConfigParser as configparser

def cacheDesktops():
    base = dict()
    base["apps"] = list()
    base["list_indexes"] = list()
    base["prev_term"] = str()
    desktops_dir = ["/usr/share/applications", f"{os.path.expanduser('~')}/.local/share/applications", f"{os.path.expanduser('~')}/Desktop"]
    desktops_list = list()
    desktops_file = "desktops.json"
    
    with open(desktops_file,"w") as f:
        f.write("{}")
        f.close()
    
    for dir in desktops_dir:
        for desktop in os.listdir(dir):
            desktops_list.append(f"{dir}/{desktop}")
    
    for desktop in desktops_list:
        config = configparser()
        do_not_add = False
        config.read(desktop)
        if "Desktop Entry" in config:
            if "NoDisplay" in config["Desktop Entry"]:
                if config["Desktop Entry"].getboolean("NoDisplay"): do_not_add = True
            if not do_not_add:
                to_add = dict({"name":f"{config['Desktop Entry'].get('Name',desktop)}","exec":f"{config['Desktop Entry'].get('Exec').strip()}","icon":f"{config['Desktop Entry'].get('Icon','None')}"})
                if to_add not in base["apps"]:
                    base["apps"].append(to_add)

    # Sort them now
    for i in range(len(base["apps"])):
        i_copy = i
        try:
            while base["apps"][i_copy]['name'].lower() < base["apps"][i_copy-1]['name'].lower():
                temp = base["apps"][i_copy-1]
                base["apps"][i_copy-1] = base["apps"][i_copy]
                base["apps"][i_copy] = temp
                i_copy-=1
        except:
            pass

    with open("desktops.json","w") as f:
        json.dump(base, f)

def searchForDesktop(search_term: str):
    temp_list = list()

    with open("desktops.json","r") as f:
        desktops = json.load(f)

    if len(desktops) == 0:
        cacheDesktops()
        searchForDesktop(search_term)

    prev = False
    add = True

    if len(search_term) == 0:
        print("search term is empty")
        list_to_search = desktops["apps"]
    elif search_term == desktops["prev_term"]:
        if len(desktops["list_indexes"]) > 0:
            list_to_search = desktops["apps"][desktops["list_indexes"][-1][0]:desktops["list_indexes"][-1][1]]
            raise SystemExit
        else:
            print("curr_list doesn't exist, using apps list")
            list_to_search = desktops["apps"]
    elif search_term[:-1] == desktops["prev_term"]:
        print(f"{search_term[:-1]} is equal to {desktops['prev_term']}")
        list_to_search = desktops["apps"][desktops["list_indexes"][-1][0]:desktops["list_indexes"][-1][1]]
    elif search_term == desktops["prev_term"][:-1]:
        desktops["list_indexes"].pop(-1)
        list_to_search = desktops["apps"][desktops["list_indexes"][-1][0]:desktops["list_indexes"][-1][1]]
        add = False
        prev = True
    else:
        print(f"{search_term[:-1]} is not equal to {desktops['prev_term']}")
        list_to_search = desktops["apps"]
        desktops["list_indexes"].clear()

    first_val = 0
    last_val = len(list_to_search)
    start_pt = 0
    while first_val != last_val:
        mid_val = (first_val+last_val)//2
        if search_term == list_to_search[mid_val]['name'][:len(search_term)].lower():
            start_pt = int(mid_val)
            break
        elif search_term < list_to_search[mid_val]['name'][:len(search_term)].lower():
            last_val = mid_val
        elif search_term > list_to_search[mid_val]['name'][:len(search_term)].lower():
            first_val = mid_val

    if add:
        end_pt = start_pt
        try:
            while start_pt != 0 and start_pt != len(list_to_search) and search_term in list_to_search[start_pt-1]['name'].lower():
                start_pt-=1
            while end_pt != 0 and end_pt != len(list_to_search) and search_term in list_to_search[end_pt+1]['name'].lower():
                end_pt+=1
        except:
            print("some error")

        if len(desktops["list_indexes"]) > 0:
            start_pt+=desktops["list_indexes"][-1][0]
            end_pt+=desktops["list_indexes"][-1][0]

        desktops["list_indexes"].append([start_pt, end_pt+1])

    print(desktops["list_indexes"])
    print(len(desktops["list_indexes"]))

    if len(desktops["list_indexes"]) > 0:
        one = desktops["list_indexes"][-1][0]
        two = desktops["list_indexes"][-1][1]
    else:
        one = 0
        two = -1

    print(one)
    print(two)

    for desktop in desktops["apps"][one:two]:
        print(desktop)

    desktops["prev_term"] = search_term

    with open("desktops.json","w") as f:
        json.dump(desktops, f)

def clearLists():
    with open("desktops.json","r") as f:
        desktops = json.load(f)

    desktops["list_indexes"].clear()

    with open("desktops.json","w") as f:
        json.dump(desktops, f)

if len(args) > 1:
    if args[-1] == "--cache":
        cacheDesktops()
    elif args[-2] == "--search":
        searchForDesktop(args[-1].lower().replace("\"",""))
    elif args[-1] == "--clear":
        clearLists()
    elif args[-1] in ["--help", "-h", "help"]:
        print("Usage:")
        print(" --cache                    -->   cache .desktops into file")
        print(" --search \"<search term>\"   -->   search for an application")
        print(" --clear                    -->   clear cached lists (not apps)")
    else:
        print("Invalid args. Doing nothing. Run with --help, -h or help for help.")
else:
    print("Invalid args. Doing nothing. Run with --help, -h or help for help.")
