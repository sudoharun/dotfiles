from ignis.widgets import Widget
from ignis.services.backlight import BacklightService
from ignis.utils import Utils

backlight = BacklightService.get_default()

class BacklightOSD(Widget.Box):
    def __init__(self):
        super().__init__(
            vertical=True,
            visible=False,
            spacing=4,
            child=[
                Widget.Label(
                    halign='start',
                    label='Brightness'
                ),
                Widget.Box(
                    spacing=2,
                    child=[
                        Widget.Icon(
                            image='brightness-symbolic',
                            pixel_size=24
                        ),
                        Widget.Scale(
                            vexpand=True,
                            hexpand=True,
                            value=backlight.bind(
                                'brightness',
                                transform=lambda val: val / backlight.max_brightness * 100 or '0'
                            )
                        ),
                        Widget.Label(
                            label=backlight.bind(
                                'brightness',
                                transform=lambda val: f'{str(int(val / backlight.max_brightness * 100))}%' or '???'
                            )
                        )
                    ]
                )
            ],
            tooltip_text=backlight.bind(
                'brightness',
                transform=lambda val: str(val) or '???'
            )
        )
        self.timeout = None

        backlight.connect(
            'notify::brightness',
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
