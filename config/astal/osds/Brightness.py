from gi.repository import (
    Gtk,
    Gdk,
    GLib,
    GObject,
    Astal,
    AstalIO,
)

def get_device():
    return AstalIO.Process.exec("ls /sys/class/backlight")

def get_brightness(device):
    return round(int(AstalIO.read_file(f"/sys/class/backlight/{device}/brightness")) / 255 * 100)

SYNC = GObject.BindingFlags.SYNC_CREATE

class Icon(Astal.Icon):
    def __init__(self) -> None:
        super().__init__(
            visible=True,
        )

        Astal.widget_set_class_names(self, ["icon", "audio-icon"])

        self.set_icon("display-brightness-symbolic")

class Slider(Astal.Slider):
    def __init__(self) -> None:
        super().__init__(
            visible=True,
            vertical=False,
            min=0,
            max=101,
            sensitive=False,
        )

        Astal.widget_set_class_names(self, ["slider", "brightness-slider"])

class Label(Astal.Label):
    def __init__(self) -> None:
        super().__init__(
            visible=True,
        )

        Astal.widget_set_class_names(self, ["label", "brightness-label"])

class RootBox(Gtk.Box):
    def __init__(self) -> None:
        super().__init__(
            visible=True,
            spacing=8,
        )

        Astal.widget_set_class_names(self, ["container", "osd"])

        self.icon = Icon()
        self.label = Label()
        self.slider = Slider()

        self.pack_start(self.icon, False, False, 0)
        self.pack_end(self.label, False, False, 0)
        self.pack_end(self.slider, True, True, 0)

        AstalIO.monitor_file(f"/sys/class/backlight/{get_device()}/brightness", self.callback)

        self.callback()

    def callback(self, *_):
        self.slider.set_value(get_brightness(get_device()))
        self.label.set_label(f"{get_brightness(get_device())}%")

class BrightnessOSD(Astal.Window):
    def __init__(self, monitor: Gdk.Monitor) -> None:
        super().__init__(
            anchor=Astal.WindowAnchor.BOTTOM,
            gdkmonitor=monitor,
            exclusivity=Astal.Exclusivity.NORMAL,
            layer=Astal.Layer.OVERLAY,
            margin_bottom=16,
            name="brightness-osd"
        )

        self.timeout_id = None

        AstalIO.monitor_file(f"/sys/class/backlight/{get_device()}/brightness", self.callback)

        self.set_size_request(-1, -1)
        self.add(RootBox())
        self.hide()

    def callback(self, *_):
        if self.timeout_id is None:
            self.timeout_id = GLib.timeout_add(2000, self.hide)
        else:
            GLib.source_remove(self.timeout_id)
            self.timeout_id = None
            self.timeout_id = GLib.timeout_add(2000, self.hide)
        self.show_all()
