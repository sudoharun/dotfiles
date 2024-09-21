import json
from os import getcwd
from sys import argv as args

cwd = getcwd()

def deleteNotification(notificationId):
	with open(f"{cwd}/files/notifications.json", "r") as f:
		notifs = json.load(f)
	try:
		del notifs[notificationId]
	except:
		print(f"Couldn't delete notification {notificationId} (doesn't exist)")
		raise SystemExit
	with open(f"{cwd}/files/notifications.json", "w") as f:
		json.dump(notifs, f)

def deleteAllNotifications():
	with open(f"{cwd}/files/notifications.json", "r") as f:
		notifs = json.load(f)
	notifs.clear()
	with open(f"{cwd}/files/notifications.json", "w") as f:
		json.dump(notifs, f)

if args[-2] == "-d":
	try:
		int(args[-1])
	except:
		if args[-1] == "-a":
			deleteAllNotifications()
			raise SystemExit
		else:
			print("Syntax: `python handle_notifs.py -d <int:notification ID>`")
			raise SystemExit
	deleteNotification(args[-1])
