# To-do
# - Add reconnect and disconnect functionality to buttons for active connection
# - List available connections
# - Test ethernet
#

from gi.repository import (
    Gtk,
    Gdk,
    GLib,
    GObject,
    Astal,
    AstalIO,
    AstalNetwork as Network,
)

SYNC = GObject.BindingFlags.SYNC_CREATE

def internet_to_str(*_, internet: Network.Internet):
    match internet:
        case Network.Internet.CONNECTED:
            return "Connected"
        case Network.Internet.CONNECTING:
            return "Connecting..."
        case Network.Internet.DISCONNECTED:
            return "Disconnected"
        case _:
            return "Unknown"

def state_to_string(*_, state: Network.DeviceState):
    match state:
        case Network.DeviceState.UNKNOWN:
            return "Unknown"
        case Network.DeviceState.UNMANAGED:
            return "Unmanaged"
        case Network.DeviceState.UNAVAILABLE:
            return "Unavailable"
        case Network.DeviceState.DISCONNECTED:
            return "Disconnected"
        case Network.DeviceState.PREPARE:
            return "Preparing Connection..."
        case Network.DeviceState.CONFIG:
            return "Configuring Connection"
        case Network.DeviceState.NEED_AUTH:
            return "Awaiting Authentication..."
        case Network.DeviceState.IP_CONFIG:
            return "Configuring IP..."
        case Network.DeviceState.IP_CHECK:
            return "Checking IP..."
        case Network.DeviceState.SECONDARIES:
            return "Secondaries?"
        case Network.DeviceState.ACTIVATED:
            return "Connected"
        case Network.DeviceState.DEACTIVATING:
            return "Deactivating..."
        case Network.DeviceState.FAILED:
            return "Failed"
        case _:
            return "Unknown"

class NetworkButton(Gtk.Box):
    def __init__(self) -> None:
        super().__init__()

        self.icon = Astal.Icon(visible=True)
        self.label = Astal.Label(visible=True, xalign=0)
        nm = Network.get_default()

        if nm.get_primary() == Network.Primary.WIRED:
            wired = nm.get_wired()
            wired.bind_property("icon-name", self.icon, "icon", SYNC)
            wired.bind_property("state", self.label, "label", SYNC, state_to_string)

            self.add(self.icon)
            self.add(self.label)
            return

        wifi = nm.get_wifi()

        self.box = Gtk.Box(visible=True, orientation=Gtk.Orientation.VERTICAL)
        self.state_label = Astal.Label(visible=True, xalign=0)

        wifi.bind_property("icon-name", self.icon, "icon", SYNC)
        wifi.bind_property("state", self.state_label, "label", SYNC, state_to_string)
        wifi.bind_property("ssid", self.label, "label", SYNC)

        self.box.add(self.state_label)
        self.box.add(self.label)

        self.add(self.icon)
        self.add(self.box)

class TopLabel(Gtk.Box):
    def __init__(self) -> None:
        super().__init__(
            visible=True,
            hexpand=True,
            vexpand=False,
            spacing=8,
        )

        Astal.widget_set_class_names(self, ["top-label"])

        self.label = Astal.Label(
            visible=True,
            label="Network"
        )

        wifi = Network.get_default().get_wifi()

        # Scan button
        self.scan_button = Astal.Button(
            visible=True,
        )

        self.scan_button.connect("clicked", self.wifi_scan)

        self.scan_icon = Astal.Icon(
            visible=True,
            icon="system-reboot-symbolic"
        )

        self.scan_button.add(self.scan_icon)

        # Toggle checkbutton
        self.wifi_toggle_button = Gtk.CheckButton(
            visible=True,
            active=wifi.get_enabled()
        )

        self.wifi_toggle_button.connect("toggled", self.toggle_wifi)

        self.pack_start(self.label, False, False, 0)

        # pack_end goes right to left
        self.pack_end(self.wifi_toggle_button, False, False, 0)
        self.pack_end(self.scan_button, False, False, 0)

    def wifi_scan(self, widget, *args):
        wifi = Network.get_default().get_wifi()
        if not wifi.get_scanning():
            wifi.scan()

    def toggle_wifi(self, widget, *args):
        wifi = Network.get_default().get_wifi()
        self.wifi_toggle_button.set_active(not self.wifi_toggle_button.get_active())
        wifi.set_enabled(self.wifi_toggle_button.get_active())

class ActiveConnection(Gtk.Box):
    def __init__(self) -> None:
        super().__init__(
            visible=True,
            orientation=Gtk.Orientation.VERTICAL,
            hexpand=True,
            vexpand=False,
            spacing=0,
        )

        Astal.widget_set_class_names(self, ["active-connection"])

        # Container for label

        self.main_container = Gtk.Box(
            visible=True,
            spacing=8,
        )

        self.connectivity_icon = Astal.Icon(
            visible=True
        )

        self.wifi_name = Astal.Label(
            visible=True,
            xalign=0
        )

        self.connectivity_label = Astal.Label(
            visible=True,
            xalign=0
        )

        self.labels_container = Gtk.Box(
            visible=True,
            orientation=Gtk.Orientation.VERTICAL
        )

        # Revealer

        self.revealer = Gtk.Revealer(
            visible=True,
            reveal_child=False
        )

        self.revealer_button = Astal.Button(
            visible=True
        )

        self.revealer_button_icon = Astal.Icon(
            visible=True,
            icon="pan-down-symbolic"
        )

        self.revealer_button.add(self.revealer_button_icon)
        self.revealer_button.connect("clicked", self.revealer_toggle)

        # What will be revealed

        self.revealer_child = Gtk.Box(
            visible=True,
            orientation=Gtk.Orientation.VERTICAL
        )

        self.speed_label = Astal.Label(
            visible=True
        )

        self.connection_buttons_container = Gtk.Box(
            visible=True
        )

        # Buttons inside revealer for reconnecting and disconnecting

        # Functionality not yet available in Astal
        # self.reconnect_button = Astal.Button(
        #     visible=True,
        #     label="Reconnect"
        # )

        # self.reconnect_button.connect("clicked", self.reconnect)
        # self.connection_buttons_container.add(self.reconnect_button)

        # self.disconnect_button = Astal.Button(
        #     visible=True,
        #     label="Disconnect"
        # )

        # self.disconnect_button.connect("clicked", self.disconnect)
        # self.connection_buttons_container.add(self.disconnect_button)

        # Adding all the boxes to make the complete product

        self.labels_container.add(self.wifi_name)
        self.labels_container.add(self.connectivity_label)

        self.revealer_child.add(self.speed_label)
        self.revealer_child.add(self.connection_buttons_container)
        self.revealer.add(self.revealer_child)

        self.main_container.add(self.connectivity_icon)
        self.main_container.add(self.labels_container)
        self.main_container.pack_end(self.revealer_button, False, False, 0)
        self.add(self.main_container)
        self.add(self.revealer)

        nm = Network.get_default()
        nm.connect("notify::state", self.sync)
        nm.connect("notify::connectivity", self.sync)

        self.sync()

    def sync(self, *_):
        nm = Network.get_default()

        if nm.get_wifi().get_device() is None:
            wired = nm.get_wired()

            self.connectivity_icon.set_icon(wired.get_icon_name())
            self.wifi_name.set_visible(False)
            self.connectivity_label.set_label(internet_to_str(internet=wired.get_internet()))
            self.speed_label.set_label(f"Speed: {str(wired.get_speed())}")
        else:
            wifi = nm.get_wifi()

            self.connectivity_icon.set_icon(wifi.get_icon_name())
            self.wifi_name.set_label(wifi.get_ssid())
            self.connectivity_label.set_label(internet_to_str(internet=wifi.get_internet()))
            self.speed_label.set_label(f"Strength: {str(wifi.get_strength())}%")

    def revealer_toggle(self, widget, *_):
        self.revealer.set_reveal_child(not self.revealer.get_reveal_child())

    # Functionality not yet available in Astal
    # def reconnect(self, widget, *_):
    #     wifi = Network.get_default().get_wifi()

    # def disconnect(self, widget, *_):
    #     wifi = Network.get_default().get_wifi()

class RootBox(Gtk.Box):
    def __init__(self) -> None:
        super().__init__(
            visible=True,
        )

        self.eventbox = Astal.EventBox(
            visible=True
        )

        self.box = Gtk.Box(
            visible=True,
            orientation=Gtk.Orientation.VERTICAL
        )

        Astal.widget_set_class_names(self, ['container'])

        self.eventbox.connect("key-press-event", self.on_escape)
        self.eventbox.connect("hover-lost", self.on_focus_out)

        self.box.add(TopLabel())
        self.box.add(ActiveConnection())
        self.eventbox.add(self.box)
        self.add(self.eventbox)

    def on_escape(self, widget, event, *args):
        if event.keyval == Gdk.KEY_Escape:
            AstalIO.Process.exec_async("astal -i network -t network")

    def on_focus_out(self, widget, event, *args):
        AstalIO.Process.exec_async("astal -i network -t network")

class MainWindow(Astal.Window):
    def __init__(self, monitor: Gdk.Monitor) -> None:
        super().__init__(
            anchor=Astal.WindowAnchor.BOTTOM
            | Astal.WindowAnchor.RIGHT,
            gdkmonitor=monitor,
            exclusivity=Astal.Exclusivity.NORMAL,
            layer=Astal.Layer.TOP,
            margin=4,
            name="network"
        )

        self.add(RootBox())
        self.set_size_request(375, -1)
        self.hide()
