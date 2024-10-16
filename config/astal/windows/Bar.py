import versions
import subprocess
from gi.repository import (
    Astal,
    Gtk,
    Gdk,
    GLib,
    GObject,
    AstalBattery as Battery,
    AstalWp as Wp,
    AstalTray as Tray,
    AstalNetwork as Network,
    AstalMpris as Mpris,
    AstalHyprland as Hyprland
)

SYNC = GObject.BindingFlags.SYNC_CREATE

class Runner(Gtk.Button):
    def __init__(self) -> None:
        super().__init__()
        self.connect("clicked", self.search)
        Astal.widget_set_class_names(self, ["Runner"])

        self.add(Astal.Icon(icon="search-symbolic"))
        # self.set_label("Applications")

    def search(self, *_):
        if len(subprocess.run(["pidof", "wofi"], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout) < 1:
            subprocess.Popen(["wofi"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

class Workspaces(Gtk.Box):
    def __init__(self) -> None:
        super().__init__(spacing=4)
        Astal.widget_set_class_names(self, ["Workspaces"])
        hypr = Hyprland.get_default()
        hypr.connect("notify::workspaces", self.sync)
        hypr.connect("notify::focused-workspace", self.sync)
        self.sync()

    def sync(self, *_):
        hypr = Hyprland.get_default()
        for child in self.get_children():
            child.destroy()

        workspaces = []
        for ws in hypr.get_workspaces():
            workspaces.append(ws)

        count = 1
        while count != 0:
            count = 0
            for i in range(len(workspaces)):
                if i+1 < len(workspaces):
                    if workspaces[i].get_id() > workspaces[i+1].get_id():
                        count+=1
                        temp = workspaces[i+1]
                        workspaces.insert(i, temp)
                        workspaces.pop(i+2)

        for ws in workspaces:
            self.add(self.button(ws))

    def button(self, ws):
        hypr = Hyprland.get_default()
        btn = Gtk.Button(visible=True)
        btn.add(Gtk.Label(visible=True, label=ws.get_id()))

        if hypr.get_focused_workspace() == ws:
            Astal.widget_set_class_names(btn, ["focused"])

        btn.connect("clicked", lambda *_: ws.focus())
        return btn

class Time(Astal.Label):
    def __init__(self, format="%I:%M%P%n%a %d %b, %Y") -> None:
        super().__init__()
        self.format = format
        self.interval = Astal.Time.interval(1000, self.sync)
        self.connect("destroy", self.interval.cancel)
        Astal.widget_set_class_names(self, ["Time"])
        self.set_justify(Gtk.Justification.CENTER)

    def sync(self):
        self.set_label(GLib.DateTime.new_now_local().format(self.format))

class Wifi(Astal.Icon):
    def __init__(self) -> None:
        super().__init__()
        Astal.widget_set_class_names(self, ["Wifi"])
        wifi = Network.get_default().get_wifi()
        wifi.bind_property("ssid", self, "tooltip-text", SYNC)
        wifi.bind_property("icon-name", self, "icon", SYNC)

class Audio(Astal.Icon):
    def __init__(self) -> None:
        super().__init__()
        Astal.widget_set_class_names(self, ["Audio"])
        speaker = Wp.get_default().get_audio().get_default_speaker()
        speaker.bind_property("volume-icon", self, "icon", SYNC)
        speaker.bind_property("volume", self, "tooltip-text", SYNC, lambda _, value: f"{round(value * 100)}%")

class BatteryIcon(Astal.Icon):
    def __init__(self) -> None:
        super().__init__()
        Astal.widget_set_class_names(self, ["Battery"])
        battery = Battery.get_default()
        battery.bind_property("is-present", self, "visible", SYNC)
        battery.bind_property("battery-icon-name", self, "icon", SYNC)
        battery.bind_property("percentage", self, "tooltip-text", SYNC, lambda _, value: f"{round(value * 100)}%")

class SysTray(Gtk.Box):
    def __init__(self) -> None:
        super().__init__(spacing=12)
        self.items = {}
        Astal.widget_set_class_names(self, ["Tray"])
        tray = Tray.get_default()
        tray.connect("item_added", self.add_item)
        tray.connect("item_removed", self.remove_item)

    def add_item(self, _: Tray.Tray, id: str):
        if id in self.items:
            return

        item = Tray.get_default().get_item(id)
        theme = item.get_icon_theme_path()

        if theme is not None:
            from bar import app

            app.add_icons(theme)

        menu = item.create_menu()
        btn = Astal.Button()
        icon = Astal.Icon()

        def on_clicked(btn):
            if menu:
                menu.popup_at_widget(btn, Gdk.Gravity.SOUTH, Gdk.Gravity.NORTH, None)

        def on_destroy(btn):
            if menu:
                menu.destroy()

        btn.connect("clicked", on_clicked)
        btn.connect("destroy", on_destroy)

        item.bind_property("tooltip-markup", btn, "tooltip-markup", SYNC)

        if item.get_property("gicon") is not None:
            item.bind_property("gicon", icon, "g-icon", SYNC)
            Astal.widget_set_class_names(icon, ["tray-g-icon"])
        else:
            item.bind_property("icon-name", icon, "icon", SYNC)
            Astal.widget_set_class_names(icon, ["tray-icon"])

        btn.add(icon)
        btn.set_name(id)
        Astal.widget_set_class_names(btn, ["tray-item"])
        self.add(btn)
        self.items[id] = btn
        self.show_all()

    def remove_item(self, _: Tray.Tray, id: str):
        if id in self.items:
            del self.items[id]
        for child in self.get_children():
            if child.get_name() == id:
                child.destroy()
                return

class Left(Gtk.Box):
    def __init__(self) -> None:
        super().__init__(halign=Gtk.Align.START, hexpand=True, spacing=12)
        self.add(Runner())
        self.add(Astal.Label(label="|"))
        self.add(Workspaces())

class Middle(Gtk.Box):
    def __init__(self) -> None:
        super().__init__()
        self.add(Time())

class Right(Gtk.Box):
    def __init__(self) -> None:
        super().__init__(hexpand=True, halign=Gtk.Align.END, spacing=12)
        self.add(Wifi())
        self.add(Audio())
        self.add(BatteryIcon())
        self.add(SysTray())

class Bar(Astal.Window):
    def __init__(self, monitor: Gdk.Monitor):
        super().__init__(
            anchor=Astal.WindowAnchor.LEFT
            | Astal.WindowAnchor.RIGHT
            | Astal.WindowAnchor.BOTTOM,
            gdkmonitor=monitor,
            exclusivity=Astal.Exclusivity.EXCLUSIVE,
        )

        Astal.widget_set_class_names(self, ["Bar"])

        self.add(Astal.CenterBox(
            start_widget=Left(),
            center_widget=Middle(),
            end_widget=Right()
        ))

        self.show_all()
