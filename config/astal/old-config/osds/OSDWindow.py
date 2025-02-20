from gi.repository import (
    Gtk,
    Gdk,
    GLib,
    GObject,
    Astal,
    AstalIO,
    AstalWp as Wp
)
from Audio import RootBox as AudioBox
from Brightness import RootBox as BrightnessBox

class AudioOSD(Astal.Window):
    def __init__(self, monitor: Gdk.Monitor) -> None:
        super().__init__(
            anchor=Astal.WindowAnchor.BOTTOM,
            gdkmonitor=monitor,
            exclusivity=Astal.Exclusivity.NORMAL,
            layer=Astal.Layer.OVERLAY,
            margin_bottom=16,
            name="audio-osd"
        )

        self.timeout_id = None
        speaker = Wp.get_default().get_audio().get_default_speaker()
        speaker.connect("notify::volume", self.on_request_show)
        speaker.connect("notify::mute", self.on_request_show)

        self.set_size_request(-1, -1)
        self.add(RootBox())
        self.hide()

    def on_request_show(self, *_):
        if self.timeout_id is None:
            self.timeout_id = GLib.timeout_add(2000, self.hide)
        else:
            GLib.source_remove(self.timeout_id)
            self.timeout_id = None
            self.timeout_id = GLib.timeout_add(2000, self.hide)
        self.show_all()
