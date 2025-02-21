from gi.repository import (
    Astal,
    AstalIO,
    Gtk,
    GLib,
    GObject,
    AstalBattery as Battery,
    AstalWp as Wp,
    AstalTray as Tray,
    AstalNetwork as Network,
    AstalHyprland as Hyprland,
    AstalNotifd as Notifd
)
from .NotificationCenter import NotificationCenter
from .AppLauncher import AppLauncher
from .AudioPopover import AudioPopover
from .NotificationPopups import NotificationPopups
from .PowerDisplayPopover import PowerDisplayWidget as PDPopover

SYNC = GObject.BindingFlags.SYNC_CREATE

class EmptyBox(Gtk.Box):
    def __init__(self) -> None:
        super().__init__()

class Separator(Gtk.Label):
    def __init__(self) -> None:
        super().__init__()
        self.add_css_class('separator')
        self.set_label("|")

class SearchButton(Gtk.Button):
    def __init__(self, app: Astal.Application) -> None:
        super().__init__()

        self.app_launcher = AppLauncher(app)

        self.add_css_class('search-button')

        self.set_tooltip_text('Search applications...')
        self.set_child(Gtk.Image.new_from_icon_name('system-search-symbolic'))

        self.connect('clicked', self.on_clicked)

    def on_clicked(self, *_):
        self.app_launcher.set_visible(not self.app_launcher.get_visible())

class Workspaces(Astal.Box):
    def __init__(self) -> None:
        super().__init__(
            spacing=4
        )

        self.add_css_class('workspaces')

        self.workspaces = []
        for i in range(10):
            btn = self.button(i+1)
            self.append(btn)
            self.workspaces.append(btn)

        hypr = Hyprland.get_default()
        hypr.connect("notify::workspaces", self.sync)
        hypr.connect("notify::focused-workspace", self.sync)

        self.sync()

    def sync(self, *_):
        for child in self.get_children():
            child.set_visible(False)

        hypr = Hyprland.get_default()

        for workspace in hypr.get_workspaces():
            self.workspaces[workspace.get_id()-1].set_visible(True)
            self.workspaces[workspace.get_id()-1].add_css_class('workspace')
            if hypr.get_focused_workspace() == workspace:
                self.workspaces[workspace.get_id()-1].add_css_class('focused-workspace')
            else:
                self.workspaces[workspace.get_id()-1].remove_css_class('focused-workspace')

    def button(self, workspace: int):
        hypr = Hyprland.get_default()
        btn = Gtk.Button(
            label=str(workspace),
            visible=False
        )
        btn.set_tooltip_text(f'Switch to workspace {workspace}')

        btn.connect('clicked', lambda *_: hypr.get_workspace(workspace).focus())
        return btn

class Systray(Gtk.Box):
    def __init__(self) -> None:
        super().__init__()

        self.add_css_class('systray')

        self.items = dict()

        tray = Tray.get_default()
        tray.connect("item_added", self.add_item)
        tray.connect("item_removed", self.remove_item)

    def add_item(self, _: Tray.Tray, id: str):
        if id in self.items:
            return

        item = Tray.get_default().get_item(id)
        btn = Gtk.MenuButton()
        icon = Gtk.Image()

        item.bind_property("tooltip-markup", btn, "tooltip-markup", SYNC)
        item.bind_property("gicon", icon, "gicon", SYNC)
        item.bind_property("menu-model", btn, "menu-model", SYNC)
        btn.insert_action_group("dbusmenu", item.get_action_group())

        def on_action_group(*args):
            btn.insert_action_group("dbusmenu", item.get_action_group())

        item.connect("notify::action-group", on_action_group)

        btn.set_child(icon)
        self.prepend(btn)
        self.items[id] = btn

    def remove_item(self, _: Tray.Tray, id: str):
        if id in self.items:
            self.remove(self.items[id])
            del self.items[id]

class EmojiButton(Gtk.MenuButton):
    def __init__(self) -> None:
        super().__init__()

        self.set_tooltip_text('Emoji Picker')

        self.popover = Gtk.EmojiChooser.new()
        self.popover.set_size_request(350, 350)
        self.popover.connect('emoji-picked', self.on_emoji_picked)
        self.set_popover(self.popover)

        self.icon = Gtk.Image.new_from_icon_name('emoji-symbols-symbolic')
        self.set_child(self.icon)

    def on_emoji_picked(self, _, emoji):
        AstalIO.Process.subprocess(f'wl-copy {emoji}')
        AstalIO.Process.subprocess(f'notify-send -a "Emoji Picker" "Emoji copied to clipboard!" "{emoji} was copied to your clipboard"')

class NetworkButton(Gtk.Button):
    def __init__(self) -> None:
        super().__init__()

        self.add_css_class('control-button')

        self.wifi_icon = Gtk.Image()
        self.wired_icon = Gtk.Image()

        network = Network.get_default()
        network.connect('notify::primary', self.set_network_icon)
        network.bind_property('state', self, 'tooltip-text', SYNC, self.state_to_string)
        network.get_wired().bind_property('icon-name', self.wired_icon, 'icon-name', SYNC)
        network.get_wifi().bind_property('icon-name', self.wifi_icon, 'icon-name', SYNC)

        self.connect('clicked', self.on_clicked)

        self.set_network_icon()

    def set_network_icon(self, *_):
        network = Network.get_default()
        if network.get_primary() == Network.Primary.WIRED:
            self.set_child(self.wired_icon)
        else:
            self.set_child(self.wifi_icon)

    def state_to_string(self, _, value):
        match value:
            case Network.State.CONNECTED_GLOBAL:
                return "Connected (global)"
            case Network.State.CONNECTED_SITE:
                return "Connected (site)"
            case Network.State.CONNECTED_LOCAL:
                return "Connected (local)"
            case Network.State.CONNECTING:
                return "Connecting..."
            case Network.State.DISCONNECTING:
                return "Disconnecting..."
            case Network.State.DISCONNECTED:
                return "Disconnected"
            case Network.State.ASLEEP:
                return "Asleep"
            case _:
                return "Unknown"
        return ""

    def on_clicked(self, *_):
        AstalIO.Process.subprocess("foot sh -c 'sleep 0.1 && nmtui'")

class AudioButton(Gtk.MenuButton):
    def __init__(self) -> None:
        super().__init__()

        self.add_css_class('control-button')

        popover = AudioPopover()
        self.set_popover(popover)

        self.icon = Gtk.Image()
        self.set_child(self.icon)

        speaker = Wp.get_default().get_audio().get_default_speaker()
        speaker.bind_property("volume-icon", self.icon, "icon-name", SYNC)
        speaker.bind_property("volume", self.icon, "tooltip-text", SYNC, lambda _, value: f"{round(value*100)}%")

class BatteryButton(Gtk.MenuButton):
    def __init__(self) -> None:
        super().__init__()

        self.add_css_class('control-button')

        self.popover = PDPopover()
        self.set_popover(self.popover)

        self.icon = Gtk.Image()
        self.set_child(self.icon)

        battery = Battery.get_default()
        battery.bind_property('is-present', self, 'visible', SYNC)

        if battery.get_is_present():
            battery.bind_property('percentage', self, 'tooltip-text', SYNC, lambda _, value: f"{round(value*100)}%")
            battery.bind_property('icon-name', self.icon, 'icon-name', SYNC)

class NotificationButton(Gtk.Button):
    def __init__(self, app: Astal.Application) -> None:
        super().__init__()

        self.add_css_class('control-button')

        self.notification_center = NotificationCenter(app)
        self.notification_popups = NotificationPopups(app)

        self.icon = Gtk.Image()
        self.set_child(self.icon)

        notifd = Notifd.get_default()
        notifd.connect('notify::notifications', self.set_label_visibility)
        notifd.connect('notify::notifications', self.set_notification_icon)

        self.notification_center.connect('notify::visible', self.on_notification_center_visible)

        self.connect('clicked', self.on_clicked)

        self.set_label_visibility()
        self.set_notification_icon()

    def set_label_visibility(self, *_):
        notifications = Notifd.get_default().get_notifications()
        if notifications is not None:
            if len(notifications) > 0:
                self.set_tooltip_text(f"{len(notifications)} new notification(s)!")
                return

        self.set_tooltip_text("All caught up!")

    def set_notification_icon(self, *_):
        notifications = Notifd.get_default().get_notifications()
        if notifications is not None:
            if len(notifications) > 0:
                self.icon.set_from_icon_name("notification-active-symbolic")
                return

        self.icon.set_from_icon_name("notification-inactive-symbolic")

    def on_notification_center_visible(self, *_):
        if not Notifd.get_default().get_dont_disturb() and not self.notification_center.get_visible():
            self.notification_popups.set_visible(True)
        else:
            self.notification_popups.set_visible(False)

    def on_clicked(self, *_):
        self.notification_center.set_visible(not self.notification_center.get_visible())

class Time(Gtk.Label):
    def __init__(
        self,
        time_format="%I:%M%P",
        date_format="%a %d %b, %Y"
    ) -> None:
        super().__init__()

        self.time_format = time_format
        self.date_format = date_format
        self.interval = AstalIO.Time.interval(1000, self.sync)
        self.connect("destroy", self.interval.cancel)

        self.set_justify(Gtk.Justification.RIGHT)

    def sync(self):
        self.set_label(GLib.DateTime.new_now_local().format(self.time_format))
        self.set_tooltip_text(GLib.DateTime.new_now_local().format(self.date_format))

class Controls(Gtk.Box):
    def __init__(self, app: Astal.Application) -> None:
        super().__init__()

        network_button = NetworkButton()
        audio_button = AudioButton()
        battery_button = BatteryButton()
        notification_button = NotificationButton(app)
        self.append(network_button)
        self.append(audio_button)
        self.append(battery_button)
        self.append(notification_button)

class Left(Astal.Box):
    def __init__(self, app: Astal.Application) -> None:
        super().__init__(
            spacing=8
        )

        search_button = SearchButton(app)
        separator = Separator()
        workspaces = Workspaces()

        self.append(search_button)
        self.append(separator)
        self.append(workspaces)

class Center(Gtk.Box):
    def __init__(self) -> None:
        super().__init__()

        empty_box = EmptyBox()
        self.append(empty_box)

class Right(Gtk.Box):
    def __init__(self, app: Astal.Application) -> None:
        super().__init__(
            spacing=8
        )

        emoji_button = EmojiButton()
        systray = Systray()
        controls = Controls(app)
        separator = Separator()
        time = Time()

        self.append(emoji_button)
        self.append(systray)
        self.append(controls)
        self.append(separator)
        self.append(time)

class Bar(Astal.Window):
    def __init__(self, app: Astal.Application, **kwargs) -> None:
        super().__init__(
            anchor=Astal.WindowAnchor.LEFT
            | Astal.WindowAnchor.BOTTOM
            | Astal.WindowAnchor.RIGHT,
            exclusivity=Astal.Exclusivity.EXCLUSIVE,
            layer=Astal.Layer.BOTTOM,
            application=app,
            name="bar",
            **kwargs
        )

        self.add_css_class('bar')

        self.box = Gtk.CenterBox(
            start_widget=Left(app),
            center_widget=Center(),
            end_widget=Right(app)
        )

        self.set_child(self.box)
        self.set_visible(True)
