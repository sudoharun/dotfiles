import json, subprocess

def main():
    monitors = list(json.loads(subprocess.run("hyprctl monitors -j", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode("utf-8")))
    workspaces = list(json.loads(subprocess.run("hyprctl workspaces -j", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode("utf-8")))
    monitors_list = list()
    monitor_groups = list()
    monitor_groups_id = list()
    ws_list = list()
    workspaces_list = list()

    for i in monitors:
        monitor_groups_id.append([])
        monitor_groups.append([])

    for i in workspaces:
        monitor_groups_id[i["monitorID"]].append(i["id"])
    for i in monitor_groups_id: i.sort()
    
    for i in range(len(monitor_groups_id)):
        for j in range(len(monitor_groups_id[i])):
            monitor_groups[i].append("occupied-ws")

    for i in monitors:
        if i["focused"]:
            for j in range(len(monitor_groups[i["id"]])):
                if monitor_groups_id[i["id"]][j] == i["activeWorkspace"]["id"]:
                    monitor_groups[i["id"]][j] = "active-monitor-ws"
        else:
            for j in range(len(monitor_groups[i["id"]])):
                if monitor_groups_id[i["id"]][j] == i["activeWorkspace"]["id"]:
                    monitor_groups[i["id"]][j] = "occupied-monitor-ws"

    widget_str = "(box :space-evenly false :spacing 0 :vexpand true :hexpand false "

    for i in range(len(monitor_groups_id)):
        for j in range(len(monitor_groups_id[i])):
            widget_str = widget_str + f"(eventbox :onclick \"hyprctl dispatch workspace {monitor_groups_id[i][j]}\" (label :class \"{monitor_groups[i][j]}\" :text \"{monitor_groups_id[i][j]}\"))"
        if i != len(monitor_groups_id)-1:
            widget_str = widget_str + f"(box :class \"ws-separator\")"
    widget_str = widget_str + ")"

    print(widget_str)

main()
