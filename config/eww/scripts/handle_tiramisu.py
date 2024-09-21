import json, subprocess
from playsound import playsound
from datetime import datetime
from os import getcwd

cwd = getcwd()

subprocess.run(["killall", "mako", "&&", "killall", "tiramisu"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

with subprocess.Popen(["tiramisu", "-j"], stdout=subprocess.PIPE, text=True) as proc:
	for line in proc.stdout:
		notification = json.loads(line.strip())
		with open(f'{cwd}/files/notifications.json', "r") as f:
			notifs = json.load(f)
			f.close()
		if len(notifs) > 0:
			notif_id = int(list(notifs.keys())[-1])+1
		else:
			notif_id = 1
		notifs[notif_id] = notification

		notif_time = datetime.now().strftime('%I:%M%p').lower()

		source_text = notifs[notif_id]["source"]
		if len(source_text) == 0:
			# source = f"(box :class \"nm-text nm-source\" :halign \"start\" (label :text \"No Source(?)\")) "
			source = ""
		elif len(source_text) < 35:
			source = f"(box :class \"nm-text nm-source\" :hexpand true (label :halign \"start\" :text \"{source_text} ({notif_time})\")) "
		else:
			source = f"(box :class \"nm-text nm-source\" :hexpand true \"start\" (label :halign \"start\" :text \"{source_text[:35]}... ({notif_time})\")) "

		summary_text = notifs[notif_id]["summary"]
		if len(summary_text) == 0:
			# summary = f"(box :class \"nm-text nm-summary\" :halign \"start\" (label :text \"No Summary(?)\")) "
			summary = ""
		elif len(summary_text) < 35:
			summary = f"(box :class \"nm-text nm-summary\" :halign \"start\" (label :halign \"start\" :text \"{summary_text}\")) "
		else:
			summary = f"(box :class \"nm-text nm-summary\" :halign \"start\" (label :halign \"start\" :text \"{summary_text[:35]}...\")) "

		body_text = notifs[notif_id]["body"]
		if len(body_text) == 0:
			# body = f"(box :class \"nm-text nm-body\" :halign \"start\" (label :text \"No Body(?)\")) "
			body = ""
		elif len(body_text) < 35:
			body = f"(box :class \"nm-text nm-body\" :halign \"start\" (label :halign \"start\" :text \"{body_text}\")) "
		elif len(body_text) < 70:
			body = f"(box :class \"nm-text nm-body\" :orientation \"v\" :halign \"start\" (label :halign \"start\" :text \"{body_text[:35]}\") (label :halign \"start\" :text \"{body_text[36:]}\")) "
		else:
			body = f"(box :class \"nm-text nm-body\" :orientation \"v\" :halign \"start\" (label :halign \"start\" :text \"{body_text[:35]}\") (label :halign \"start\" :text \"{body_text[36:70]}...\")) "

		widget = f"(box :class \"nm-child nm-text-parent\" :orientation \"v\" :vexpand true :hexpand true :halign \"start\" :valign \"center\" :space-evenly false :spacing 0 {source} {summary} {body} )"
		parent_widget = f"(box :class \"nm-parent\" :orientation \"h\" :space-evenly false :spacing 10 {widget} (box :class \"nm-action\" :hexpand false :vexpand true :valign \"center\" :halign \"center\" (button :onclick \"python {cwd}/scripts/edit_notifs.py -d {notif_id}\" (image :path \"images/close.svg\" :image-height \"20\"))))"
		notifs[notif_id]["widget"] = parent_widget

		with open(f'{cwd}/files/notifications.json', 'w') as f:
			json.dump(notifs, f)
			f.close()

		playsound(f"{cwd}/files/notification.wav")
