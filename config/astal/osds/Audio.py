from gi.repository import (
    Gtk,
    Gdk,
    GLib,
    GObject,
    Astal,
    AstalIO,
    AstalWp as Wp,
)

SYNC = GObject.BindingFlags.SYNC_CREATE

class Icon(Astal.Icon):
    def __init__(self) -> None:
        super().__init__(
            visible=True,
        )

        Astal.widget_set_class_names(self, ["icon", "audio-icon"])

        speaker = Wp.get_default().get_audio().get_default_speaker()
        speaker.bind_property("volume-icon", self, "icon", SYNC)

class Slider(Astal.Slider):
    def __init__(self) -> None:
        super().__init__(
            visible=True,
            vertical=False,
            min=0,
            max=101,
            sensitive=False,
        )

        Astal.widget_set_class_names(self, ["slider", "audio-slider"])

        speaker = Wp.get_default().get_audio().get_default_speaker()
        speaker.bind_property("volume", self, "value", SYNC, lambda _, value: round(value * 100))

class Label(Astal.Label):
    def __init__(self) -> None:
        super().__init__(
            visible=True,
        )

        Astal.widget_set_class_names(self, ["label", "audio-label"])

        speaker = Wp.get_default().get_audio().get_default_speaker()
        speaker.bind_property("mute", self, "label", SYNC, lambda _, value: "Muted" if value else f"{round(speaker.get_volume() * 100)}%")
        speaker.bind_property("volume", self, "label", SYNC, lambda _, value: f"{round(value * 100)}%" if not speaker.get_mute() else "Muted")

class RootBox(Gtk.Box):
    def __init__(self) -> None:
        super().__init__(
            visible=True,
            spacing=8,
        )

        Astal.widget_set_class_names(self, ["container", "osd"])

        self.pack_start(Icon(), False, False, 0)
        self.pack_end(Label(), False, False, 0)
        self.pack_end(Slider(), True, True, 0)

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
