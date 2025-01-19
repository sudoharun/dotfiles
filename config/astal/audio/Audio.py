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

class TopLabel(Gtk.Box):
    def __init__(self) -> None:
        super().__init__(
            visible=True,
            hexpand=True,
            vexpand=False,
        )

        Astal.widget_set_class_names(self, ["top-label"])

        self.label = Astal.Label(
            visible=True,
            label="Audio"
        )

        self.pack_start(self.label, False, False, 0)

class DefaultSpeaker(Gtk.Box):
    def __init__(self) -> None:
        super().__init__(
            visible=True,
            orientation=Gtk.Orientation.VERTICAL,
            spacing=8
        )

        Astal.widget_set_class_names(self, ["default-speaker"])

        speaker = Wp.get_default().get_default_speaker()
        description = Astal.Label(
            visible=True
        )
        box = Gtk.Box(
            visible=True,
            spacing=8
        )
        icon = Astal.Icon(
            visible=True
        )
        slider = Astal.Slider(
            visible=True,
            hexpand=True,
            min=0.0,
            max=1.0,
            step=0.05,
        )
        percentage = Astal.Label(
            visible=True
        )

        speaker.bind_property("description", description, "label", SYNC)
        speaker.bind_property("volume-icon", icon, "icon", SYNC)
        speaker.bind_property("volume", slider, "value", SYNC)
        speaker.bind_property("volume", percentage, "label", SYNC, lambda _, value: f"{round(value * 100)}%")

        slider.connect("dragged", self.on_slider_dragged)

        box.add(icon)
        box.add(slider)
        box.add(percentage)
        self.add(description)
        self.add(box)

        Astal.widget_set_class_names(box, ["controls"])
        Astal.widget_set_class_names(description, ["description"])

    def on_slider_dragged(self, widget, *_):
        speaker = Wp.get_default().get_default_speaker()
        speaker.set_volume(widget.get_value())

class DefaultMic(Gtk.Box):
    def __init__(self) -> None:
        super().__init__(
            visible=True,
            orientation=Gtk.Orientation.VERTICAL,
            spacing=8
        )

        Astal.widget_set_class_names(self, ["default-mic"])

        mic = Wp.get_default().get_default_microphone()
        description = Astal.Label(
            visible=True
        )
        box = Gtk.Box(
            visible=True,
            spacing=8
        )
        icon = Astal.Icon(
            visible=True
        )
        slider = Astal.Slider(
            visible=True,
            hexpand=True,
            min=0.0,
            max=1.0,
            step=0.05,
        )
        percentage = Astal.Label(
            visible=True
        )

        mic.bind_property("description", description, "label", SYNC)
        mic.bind_property("volume-icon", icon, "icon", SYNC)
        mic.bind_property("volume", slider, "value", SYNC)
        mic.bind_property("volume", percentage, "label", SYNC, lambda _, value: f"{round(value * 100)}%")

        slider.connect("dragged", self.on_slider_dragged)

        box.add(icon)
        box.add(slider)
        box.add(percentage)
        self.add(description)
        self.add(box)

        Astal.widget_set_class_names(box, ["controls"])
        Astal.widget_set_class_names(description, ["description"])

    def on_slider_dragged(self, widget, *_):
        mic = Wp.get_default().get_default_microphone()
        mic.set_volume(widget.get_value())

class Speakers(Gtk.Box):
    def __init__(self) -> None:
        super().__init__(
            visible=True,
            orientation=Gtk.Orientation.VERTICAL,
            spacing=4
        )

        Astal.widget_set_class_names(self, ["speakers"])

        audio = Wp.get_default().get_audio()
        audio.connect("notify::speakers", self.sync)
        self.sync()

    def sync(self, *_):
        def set_to_default(speaker: Wp.Endpoint, *_):
            speaker.set_is_default(True)

        speakers = Wp.get_default().get_audio().get_speakers()
        for speaker in speakers:
            for child in self.get_children():
                if child.get_name() == str(speaker.get_id()):
                    continue

            if not speaker.get_is_default():
                speaker_box = Gtk.Box(
                orientation=Gtk.Orientation.VERTICAL,
                visible=True
                )
                speaker_box.set_name(str(speaker.get_id()))
                speaker_label = Astal.Label(
                    label=speaker.get_name(),
                    hexpand=True,
                    visible=True
                )
                speaker_button = Astal.Button(
                    label="Switch",
                    visible=True
                )
                speaker_button.connect("clicked", set_to_default)
                speaker_box.add(speaker_label)
                speaker_box.pack_end(speaker_button, False, False, 0)

                Astal.widget_set_class_names(speaker_box, ["speaker"])
                self.add(speaker_box)

        for child in self.get_children():
            found = False
            for speaker in speakers:
                if child.get_name() == str(speaker.get_id()):
                    found = True
                    continue
            if not found:
                child.destroy()

        if len(self.get_children()) < 1:
            self.set_visible(False)
        else:
            self.set_visible(True)

class Mics(Gtk.Box):
    def __init__(self) -> None:
        super().__init__(
            visible=True,
            orientation=Gtk.Orientation.VERTICAL,
            spacing=4
        )

        Astal.widget_set_class_names(self, ["mics"])

        audio = Wp.get_default().get_audio()
        audio.connect("notify::microphones", self.sync)
        self.sync()

    def sync(self, *_):
        def set_to_default(microphone: Wp.Endpoint, *_):
            microphone.set_is_default(True)

        microphones = Wp.get_default().get_audio().get_microphones()
        for microphone in microphones:
            for child in self.get_children():
                if child.get_name() == str(microphone.get_id()):
                    continue

            if not microphone.get_is_default():
                microphone_box = Gtk.Box(
                    orientation=Gtk.Orientation.VERTICAL,
                    visible=True
                )
                microphone_box.set_name(str(microphone.get_id()))
                microphone_label = Astal.Label(
                    label=microphone.get_description(),
                    hexpand=True,
                    visible=True
                )
                microphone_button = Astal.Button(
                    label="Switch",
                    visible=True
                )
                microphone_button.connect("clicked", set_to_default)
                microphone_box.add(microphone_label)
                microphone_box.pack_end(microphone_button, False, False, 0)

                Astal.widget_set_class_names(microphone_box, ["mic"])
                self.add(microphone_box)

        for child in self.get_children():
            found = False
            for microphone in microphones:
                if child.get_name() == str(microphone.get_id()):
                    found = True
                    continue
            if not found:
                child.destroy()

        if len(self.get_children()) < 1:
            self.set_visible(False)
        else:
            self.set_visible(True)

class MainWindow(Astal.Window):
    def __init__(self, monitor: Gdk.Monitor) -> None:
        super().__init__(
            anchor=Astal.WindowAnchor.BOTTOM
            | Astal.WindowAnchor.RIGHT,
            gdkmonitor=monitor,
            exclusivity=Astal.Exclusivity.NORMAL,
            layer=Astal.Layer.TOP,
            margin=4,
            name="audio"
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
        self.box.add(DefaultSpeaker())
        self.box.add(DefaultMic())
        self.box.add(Speakers())
        self.box.add(Mics())
        self.all_container.add(self.box)
        self.eventbox.add(self.all_container)

        Astal.widget_set_class_names(self.all_container, ["all-container"])
        Astal.widget_set_class_names(self.box, ["controls-container"])

        self.add(self.eventbox)
        self.set_size_request(375, -1)
        self.hide()

    def on_escape(self, widget, event, *args):
        if event.keyval == Gdk.KEY_Escape:
            AstalIO.Process.exec_async("astal -i audio -t audio")

    def on_focus_out(self, widget, event, *args):
        AstalIO.Process.exec_async("astal -i audio -t audio")
