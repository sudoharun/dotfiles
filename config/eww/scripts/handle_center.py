import subprocess, json
from os import getcwd

cwd = getcwd()

with subprocess.Popen(["watchexec", "-q", "-w", f"{cwd}/files/notifications.json", "echo", "0"], stdout=subprocess.PIPE, text=True) as proc:
	for line in proc.stdout:
		with open(f"{cwd}/files/notifications.json", "r") as f:
			json_file = json.load(f)
			f.close()
		nc_widget = "(box :orientation \"v\" :space-evenly false :spacing 16"
		if len(json_file.keys()) > 0:
			for n in json_file.keys():
				nc_widget = nc_widget + json_file[n]["widget"]
		nc_widget = nc_widget + ")"
		print(nc_widget, flush=True)
