from gi.repository import (
    Gtk,
    Gdk,
    GLib,
    GObject,
    Astal,
    AstalIO,
    AstalBattery as Battery,
    AstalPowerProfiles as PowerProfiles,
)

SYNC = GObject.BindingFlags.SYNC_CREATE

def get_display():
    return AstalIO.Process.exec("ls /sys/class/backlight")

def get_brightness(display):
    return round(int(AstalIO.read_file(f"/sys/class/backlight/{display}/brightness")) / 255 * 100)

class TopLabel(Gtk.Box):
    def __init__(self) -> None:
        super().__init__(
            visible=True,
            hexpand=True,
            vexpand=False,
            spacing=8
        )

        Astal.widget_set_class_names(self, ["top-label"])

        self.label = Astal.Label(
            visible=True,
            label="Power & Display"
        )

        self.lock_button = Astal.Button(visible=True)
        self.reboot_button = Astal.Button(visible=True)
        self.shutdown_button = Astal.Button(visible=True)

        self.lock_button.add(
            Astal.Icon(
                visible=True,
                icon="system-lock-screen-symbolic"
            )
        )
        self.reboot_button.add(
            Astal.Icon(
                visible=True,
                icon="system-reboot-symbolic"
            )
        )
        self.shutdown_button.add(
            Astal.Icon(
                visible=True,
                icon="system-shutdown-symbolic"
            )
        )

        self.lock_button.connect("clicked", self.on_lock_button_click)
        self.reboot_button.connect("clicked", self.on_reboot_button_click)
        self.shutdown_button.connect("clicked", self.on_shutdown_button_click)

        self.pack_start(self.label, False, False, 0)
        self.pack_end(self.shutdown_button, False, False, 0)
        self.pack_end(self.reboot_button, False, False, 0)
        self.pack_end(self.lock_button, False, False, 0)

    def on_lock_button_click(self, *_):
        AstalIO.Process.exec("hyprlock &")

    def on_reboot_button_click(self, *_):
        AstalIO.Process.exec("systemctl reboot")

    def on_shutdown_button_click(self, *_):
        AstalIO.Process.exec("systemctl poweroff")

class Brightness(Gtk.Box):
    def __init__(self) -> None:
        super().__init__(
            visible=True,
            spacing=8
        )
        Astal.widget_set_class_names(self, [""])

        self.icon = Astal.Icon(
            visible=True,
            icon="display-brightness-symbolic"
        )
        Astal.widget_set_class_names(self.icon, [""])

        self.slider = Astal.Slider(
            visible=True,
            hexpand=True,
            min=0.0,
            max=1.0,
            step=0.05,
        )
        Astal.widget_set_class_names(self.slider, [""])
        self.slider.connect("dragged", self.on_slider_dragged)

        self.percentage = Astal.Label(
            visible=True
        )
        Astal.widget_set_class_names(self.percentage, [""])

        AstalIO.monitor_file(f"/sys/class/backlight/{get_display()}/brightness", self.callback)
        self.callback()

        self.add(self.icon)
        self.add(self.slider)
        self.add(self.percentage)

    def on_slider_dragged(self, *_):
        AstalIO.Process.subprocess(f"brightnessctl s {str(round(self.slider.get_value() * 255))}")

    def callback(self, *_):
        self.slider.set_value(get_brightness(get_display()) / 100)
        self.percentage.set_label(f"{get_brightness(get_display())}%")

class MainWindow(Astal.Window):
    def __init__(self, monitor: Gdk.Monitor) -> None:
        super().__init__(
            anchor=Astal.WindowAnchor.BOTTOM
            | Astal.WindowAnchor.RIGHT,
            gdkmonitor=monitor,
            exclusivity=Astal.Exclusivity.NORMAL,
            layer=Astal.Layer.TOP,
            margin=4,
            name="battery"
        )

        self.eventbox = Astal.EventBox(
            visible=True,
            hexpand=True,
            vexpand=True
        )
        self.all_container = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            visible=True,
            spacing=0
        )
        self.box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            visible=True,
            spacing=16
        )

        self.eventbox.connect("key-press-event", self.on_escape)
        self.eventbox.connect("hover-lost", self.on_focus_out)

        self.all_container.add(TopLabel())
        self.box.add(Brightness())
        self.all_container.add(self.box)
        self.eventbox.add(self.all_container)

        Astal.widget_set_class_names(self.all_container, ["all-container"])
        Astal.widget_set_class_names(self.box, ["controls-container"])

        self.add(self.eventbox)
        self.set_size_request(375, -1)
        self.hide()

    def on_escape(self, widget, event, *args):
        if event.keyval == Gdk.KEY_Escape:
            AstalIO.Process.exec_async("astal -i battery -t battery")

    def on_focus_out(self, widget, event, *args):
        AstalIO.Process.exec_async("astal -i battery -t battery")
