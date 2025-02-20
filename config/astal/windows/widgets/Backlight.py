from gi.repository import (
    Gtk,
    Astal,
    AstalIO
)

class BacklightGraphics(Gtk.Box):
    def __init__(self) -> None:
        super().__init__(
            valign=Gtk.Align.END,
            spacing=2
        )

        self.icon = Gtk.Image.new_from_icon_name('display-brightness-symbolic')
        self.icon.set_pixel_size(24)
        self.slider = Astal.Slider(
            hexpand=True,
            min=0.0,
            max=self.get_max_brightness(),
        )
        self.percentage = Gtk.Label()

        self.append(self.icon)
        self.append(self.slider)
        self.append(self.percentage)

        self.icon.set_size_request(20, -1)
        self.percentage.set_size_request(40, -1)

        self.slider.connect('change-value', self.on_dragged)

        if len(self.get_device()) > 0:
            self.set_visible(True)
            AstalIO.monitor_file(f"/sys/class/backlight/{self.get_device()}/brightness", self.callback)
            self.callback()
        else:
            self.set_visible(False)

    def get_device(self, *_):
        return AstalIO.Process.exec("ls /sys/class/backlight")

    def get_max_brightness(self, *_):
        return int(AstalIO.read_file(f"/sys/class/backlight/{self.get_device()}/max_brightness"))

    def get_brightness(self, *_):
        return int(AstalIO.read_file(f"/sys/class/backlight/{self.get_device()}/actual_brightness"))

    def callback(self, *_):
        self.slider.set_value(self.get_brightness())
        self.percentage.set_label(f'{round(self.get_brightness() / self.get_max_brightness() * 100)}%')

    def on_dragged(self, *_):
        AstalIO.Process.subprocess(f'brightnessctl s {str(self.slider.get_value())}')
