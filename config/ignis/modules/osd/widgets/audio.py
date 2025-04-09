from ignis.widgets import Widget
from ignis.services.audio import AudioService
from ignis.utils import Utils

audio = AudioService.get_default()

class AudioOSD(Widget.Box):
    def __init__(self):
        super().__init__(
            vertical=True,
            visible=False,
            spacing=4,
            child=[
                Widget.Label(
                    halign='start',
                    label=audio.speaker.bind('description'),
                    ellipsize='end'
                ),
                Widget.Box(
                    spacing=2,
                    child=[
                        Widget.Icon(
                            image=audio.speaker.bind('icon-name'),
                            pixel_size=24
                        ),
                        Widget.Scale(
                            vexpand=True,
                            hexpand=True,
                            visible=audio.speaker.bind(
                                'is-muted',
                                lambda val: not val or False
                            ),
                            value=audio.speaker.bind('volume')
                        ),
                        Widget.Label(
                            visible=audio.speaker.bind(
                                'is-muted',
                                lambda val: not val or False
                            ),
                            label=audio.speaker.bind(
                                'volume',
                                transform=lambda val: f'{str(val)}%' or '???'
                            )
                        ),
                        Widget.Label(
                            visible=audio.speaker.bind('is-muted'),
                            label='Muted'
                        )
                    ]
                )
            ],
            tooltip_text=audio.speaker.bind('description')
        )
        self.timeout = None

        audio.speaker.connect(
            'notify::volume',
            lambda *_: self.timeout_func()
        )
        audio.speaker.connect(
            'notify::is-muted',
            lambda *_: self.timeout_func()
        )
        audio.connect(
            'notify::speakers',
            lambda *_: self.timeout_func()
        )

    def timeout_func(self):
        if self.timeout:
            self.timeout.cancel()

        self.set_visible(True)
        self.timeout = Utils.Timeout(
            ms=2000,
            target=lambda: self.set_visible(False)
        )
