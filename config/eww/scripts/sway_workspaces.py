import json, subprocess

def main():
    swaymsg = list(json.loads(subprocess.run("swaymsg -r -t get_workspaces", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode("utf-8")))
    workspaces = list()

    for i in swaymsg:
        workspaces.append({"id": i["num"], "output": i["output"], "focused": i["focused"]})
    
    widget_str = "(box :space-evenly false :spacing 0 :vexpand true :hexpand false "

    for i in workspaces:
        if i['focused']:
            ws = "active-monitor-ws"
        else:
            ws = "occupied-ws"
        widget_str = widget_str + f"(label :class \"{ws}\" :text \"{i['id']}\")"

    widget_str = widget_str + ")"

    print(widget_str)

main()
