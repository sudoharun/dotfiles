from gi.repository import (
    Gtk,
    GObject,
    Pango,
    Astal,
    AstalWp as Wp
)

SYNC = GObject.BindingFlags.SYNC_CREATE

class SpeakerDescription(Gtk.Label):
    def __init__(self) -> None:
        super().__init__(
            hexpand=True,
            xalign=0
        )

        self.set_max_width_chars(1)
        self.set_wrap(False)
        self.set_ellipsize(Pango.EllipsizeMode.END)

        speaker = Wp.get_default().get_default_speaker()
        speaker.bind_property('description', self, 'label', SYNC)
        speaker.bind_property('description', self, 'tooltip-text', SYNC)

class SpeakerIcon(Gtk.Image):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        speaker = Wp.get_default().get_default_speaker()
        speaker.bind_property('volume-icon', self, 'icon-name', SYNC)

class SpeakerSlider(Astal.Slider):
    def __init__(self) -> None:
        super().__init__(
            hexpand=True,
            min=0.0,
            max=1.0,
            step=1
        )

        speaker = Wp.get_default().get_default_speaker()
        speaker.bind_property('volume', self, 'value', SYNC)

        self.connect('value-changed', self.on_dragged)

    def on_dragged(self, *_):
        speaker = Wp.get_default().get_default_speaker()
        speaker.set_volume(self.get_value())

class SpeakerPercentage(Gtk.Label):
    def __init__(self) -> None:
        super().__init__()

        speaker = Wp.get_default().get_default_speaker()
        speaker.bind_property(
            'volume',
            self,
            'label',
            SYNC,
            lambda _, value: f'{round(value*100)}%'
        )

class SpeakerGraphics(Gtk.Box):
    def __init__(self) -> None:
        super().__init__(
            spacing=2
        )

        self.add_css_class('audio-popover-controls')

        self.icon = SpeakerIcon()
        self.slider = SpeakerSlider()
        self.percentage = SpeakerPercentage()

        self.button = Gtk.Button()
        self.button.set_child(self.icon)
        self.button.connect("clicked", self.on_clicked)

        self.icon.set_size_request(20, -1)
        self.percentage.set_size_request(40, -1)

        self.append(self.button)
        self.append(self.slider)
        self.append(self.percentage)

    def on_clicked(self, *_):
        speaker = Wp.get_default().get_default_speaker()
        speaker.set_mute(not speaker.get_mute())

class MicrophoneDescription(Gtk.Label):
    def __init__(self) -> None:
        super().__init__(
            hexpand=True,
            xalign=0
        )

        self.set_max_width_chars(1)
        self.set_wrap(False)
        self.set_ellipsize(Pango.EllipsizeMode.END)

        microphone = Wp.get_default().get_default_microphone()
        microphone.bind_property('description', self, 'label', SYNC)
        microphone.bind_property('description', self, 'tooltip-text', SYNC)

class MicrophoneIcon(Gtk.Image):
    def __init__(self) -> None:
        super().__init__()

        microphone = Wp.get_default().get_default_microphone()
        microphone.bind_property('volume-icon', self, 'icon-name', SYNC)

class MicrophoneSlider(Astal.Slider):
    def __init__(self) -> None:
        super().__init__(
            hexpand=True,
            min=0.0,
            max=1.0,
            step=1
        )

        microphone = Wp.get_default().get_default_microphone()
        microphone.bind_property('volume', self, 'value', SYNC)

        self.connect('value-changed', self.on_dragged)

    def on_dragged(self, *_):
        microphone = Wp.get_default().get_default_microphone()
        microphone.set_volume(self.get_value())

class MicrophonePercentage(Gtk.Label):
    def __init__(self) -> None:
        super().__init__()

        microphone = Wp.get_default().get_default_microphone()
        microphone.bind_property(
            'volume',
            self,
            'label',
            SYNC,
            lambda _, value: f'{round(value*100)}%'
        )

class MicrophoneGraphics(Gtk.Box):
    def __init__(self) -> None:
        super().__init__(
            spacing=2
        )

        self.add_css_class('audio-popover-controls')

        self.icon = MicrophoneIcon()
        self.slider = MicrophoneSlider()
        self.percentage = MicrophonePercentage()

        self.button = Gtk.Button()
        self.button.set_child(self.icon)
        self.button.connect("clicked", self.on_clicked)

        self.icon.set_size_request(20, -1)
        self.percentage.set_size_request(40, -1)

        self.append(self.button)
        self.append(self.slider)
        self.append(self.percentage)

    def on_clicked(self, *_):
        microphone = Wp.get_default().get_default_microphone()
        microphone.set_mute(not microphone.get_mute())
