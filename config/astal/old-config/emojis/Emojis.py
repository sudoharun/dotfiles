from gi.repository import (
    Gtk,
    Gdk,
    GLib,
    GObject,
    Astal,
    AstalIO,
    AstalApps as Apps
)
import json
from pathlib import Path

emojis_json = str(Path(__file__).parent.resolve() / "emojis.json")

def extract_emojis_from_json():
    with open(emojis_json) as f:
        emojis_dict = json.load(f)
    return emojis_dict

class EmojiButton(Astal.Button):
    def __init__(self, emoji: str, name: str) -> None:
        super().__init__(
            visible=True,
            hexpand=True
        )

        self.set_label(emoji)
        self.set_name(name)

class EmojisList(Astal.Scrollable):
    def __init__(self) -> None:
        super().__init__(
            visible=True,
            hexpand=True,
            vexpand=True
        )

        self.box = Gtk.Box(
            visible=True,
            orientation=Gtk.Orientation.VERTICAL,
            hexpand=True,
            vexpand=True,
        )

        for emoji in extract_emojis_from_json()["emojis"]:
            btn = EmojiButton(emoji["emoji"], emoji["name"])
            self.box.add(btn)

        self.add(self.box)

class MainWindow(Astal.Window):
    def __init__(self, monitor: Gdk.Monitor) -> None:
        super().__init__(
            anchor=Astal.WindowAnchor.BOTTOM
            | Astal.WindowAnchor.RIGHT,
            gdkmonitor=monitor,
            exclusivity=Astal.Exclusivity.NORMAL,
            keymode=Astal.Keymode.NONE,
            layer=Astal.Layer.TOP,
            margin=4,
            name="emojis"
        )

        self.set_size_request(350, 350)
        self.add(EmojisList())
        self.show_all()
