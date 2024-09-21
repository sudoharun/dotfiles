import subprocess, json
from os import getcwd

cwd = getcwd()

with subprocess.Popen(["watchexec", "-q", "-w", f"{cwd}/files/notifications.json", "echo", "0"], stdout=subprocess.PIPE, text=True) as proc:
    for line in proc.stdout:
        with open(f"{cwd}/files/notifications.json", "r") as f:
            json_file = json.load(f)
            f.close()
        if len(json_file.keys()) > 0:
            nm_num = len(json_file.keys())
        else:
            nm_num = 0

        print(nm_num, flush=True)
