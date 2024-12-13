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

class Audio(Gtk.Box):
    def __init__(self) -> None:
        super().__init__(orientation=Gtk.Orientation.VERTICAL, visible=True)

        wp = Wp.get_default()
        speaker = wp.get_default_speaker()
        mic = wp.get_default_microphone()

        speaker_box = Gtk.Box(visible=True)
        speaker_icon = Astal.Icon(visible=True)
        speaker_slider = Astal.Slider(min=0.00, max=1.00, step=0.05, hexpand=True, visible=True)
        speaker_label = Astal.Label(visible=True)

        speaker_slider.connect("dragged", self.speaker_on_dragged)

        speaker_box.add(speaker_icon)
        speaker_box.add(speaker_slider)
        speaker_box.add(speaker_label)

        speaker.bind_property("volume-icon", speaker_icon, "icon", SYNC)
        speaker.bind_property("volume", speaker_label, "label", SYNC, lambda _, value: f"{round(value * 100)}%")
        speaker.bind_property("volume", speaker_slider, "value", SYNC)

        self.add(speaker_box)

        mic_box = Gtk.Box(visible=True)
        mic_icon = Astal.Icon(visible=True)
        mic_slider = Astal.Slider(min=0.00, max=1.00, step=0.05, hexpand=True, visible=True)
        mic_label = Astal.Label(visible=True)

        mic_slider.connect("dragged", self.mic_on_dragged)

        mic_box.add(mic_icon)
        mic_box.add(mic_slider)
        mic_box.add(mic_label)

        mic.bind_property("volume-icon", mic_icon, "icon", SYNC)
        mic.bind_property("volume", mic_label, "label", SYNC, lambda _, value: f"{round(value * 100)}%")
        mic.bind_property("volume", mic_slider, "value", SYNC)

        self.add(mic_box)

    def speaker_on_dragged(self, widget, *args):
        speaker = Wp.get_default().get_default_speaker()
        speaker.set_volume(widget.get_value())

    def mic_on_dragged(self, widget, *args):
        mic = Wp.get_default().get_default_microphone()
        mic.set_volume(widget.get_value())

class Speakers(Gtk.Box):
    pass

class Mics(Gtk.Box):
    pass
