from gi.repository import (
    Gtk,
    GObject,
    AstalIO,
    AstalWp as Wp
)
from .widgets.Audio import *

SYNC = GObject.BindingFlags.SYNC_CREATE

class SpeakerLabel(Gtk.Box):
    def __init__(self) -> None:
        super().__init__(
            hexpand=True
        )

        self.label = SpeakerDescription()
        self.append(self.label)

class MicrophoneLabel(Gtk.Box):
    def __init__(self) -> None:
        super().__init__(
            hexpand=True
        )

        self.label = MicrophoneDescription()
        self.append(self.label)

class OpenPavucontrol(Gtk.Button):
    def __init__(self) -> None:
        super().__init__(
            label="Open Volume Control"
        )

        self.connect('clicked', self.on_clicked)

    def on_clicked(self, *_):
        AstalIO.Process.subprocess('pavucontrol')

class AudioPopover(Gtk.Popover):
    def __init__(self) -> None:
        super().__init__()

        self.set_size_request(300, -1)
        self.add_css_class('audio-popover')

        self.box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            hexpand=True,
            vexpand=True,
            spacing=8
        )
        self.box.add_css_class('audio-popover-box')
        self.set_child(self.box)

        self.box.append(SpeakerLabel())
        self.box.append(SpeakerGraphics())
        self.box.append(MicrophoneLabel())
        self.box.append(MicrophoneGraphics())
        self.box.append(OpenPavucontrol())
