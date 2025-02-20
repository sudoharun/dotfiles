from gi.repository import (
    Gtk,
    GLib,
    Astal,
    AstalIO,
    AstalWp as Wp
)

from .widgets.Audio import *
from .widgets.Backlight import BacklightGraphics

class SpeakerOSD(Gtk.Box):
    def __init__(self) -> None:
        super().__init__(
            orientation=Gtk.Orientation.VERTICAL
        )

        self.add_css_class('osd')
        self.add_css_class('speaker-osd')
        self.timeout_id = None

        self.description = SpeakerDescription()
        self.graphics = SpeakerGraphics()

        self.append(self.description)
        self.append(self.graphics)

class BacklightOSD(Gtk.Box):
    def __init__(self) -> None:
        super().__init__(
            orientation=Gtk.Orientation.VERTICAL
        )

        self.add_css_class('osd')
        self.add_css_class('backlight-osd')
        self.timeout_id = None

        self.label = Gtk.Label(
            label='Brightness',
            xalign=0
        )
        self.graphics = BacklightGraphics()

        self.append(self.label)
        self.append(self.graphics)

class OSDWindow(Astal.Window):
    def __init__(self, app: Astal.Application):
        super().__init__(
            anchor=Astal.WindowAnchor.BOTTOM,
            exclusivity=Astal.Exclusivity.IGNORE,
            layer=Astal.Layer.OVERLAY,
            keymode=Astal.Keymode.NONE,
            margin_bottom=56,
            application=app,
            name='osd'
        )

        self.add_css_class('osd-window')
        self.set_size_request(250, 0)
        self.set_default_size(1, 1)

        self.timeout_id = None
        self.box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
        )
        self.speaker = SpeakerOSD()
        self.backlight = BacklightOSD()

        AstalIO.monitor_file(f"/sys/class/backlight/{self.get_backlight_device()}/actual_brightness", self.callback)
        Wp.get_default().get_default_speaker().connect('notify::volume', self.callback)

        self.box.add_css_class('osd-box')
        self.set_child(self.box)
        self.present()

    def get_backlight_device(self, *_):
        return AstalIO.Process.exec("ls /sys/class/backlight")

    def callback(self, _what, _value):
        if type(_what) is str:
            context = self.backlight
            if _value == 1:
                return
        else:
            context = self.speaker

        if self.timeout_id is None:
            self.timeout_id = GLib.timeout_add(2100, self.hide)
        else:
            GLib.source_remove(self.timeout_id)
            self.timeout_id = None
            self.timeout_id = GLib.timeout_add(2100, self.hide)

        if context.timeout_id is None:
            context.timeout_id = GLib.timeout_add(2000, context.unparent)
        else:
            GLib.source_remove(context.timeout_id)
            context.timeout_id = None
            context.timeout_id = GLib.timeout_add(2000, context.unparent)

        if context.get_parent() is None:
            self.box.prepend(context)
        self.present()
