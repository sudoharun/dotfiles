from ignis.widgets import Widget
from ignis.services.network import NetworkService
from ignis.services.audio import AudioService
from ignis.services.upower import UPowerService

network = NetworkService.get_default()
audio = AudioService.get_default()
upower = UPowerService.get_default()

class NetworkIcon(Widget.Icon):
    def __init__(self):
        super().__init__()

        network.ethernet.connect(
            'notify::is-connected',
            lambda *_: self.if_ethernet_is_available()
        )
        self.if_ethernet_is_available()

    def if_ethernet_is_available(self):
        if network.ethernet.is_connected or not (len(network.wifi.devices) > 0):
            self.image = network.ethernet.bind('icon-name')
            self.tooltip_text = network.ethernet.bind(
                'is-connected',
                transform=lambda x: 'Connected' if x else 'Disconnected' or 'Unavailable'
            )
        else:
            self.image = network.wifi.bind('icon-name')
            self.tooltip_text = network.wifi.bind(
                'is-connected',
                transform=lambda x: 'Connected' if x else 'Disconnected' or 'Unavailable'
            )

class SpeakerIcon(Widget.Icon):
    def __init__(self):
        super().__init__(
            image=audio.speaker.bind('icon-name'),
            tooltip_text=audio.speaker.bind(
                'volume',
                transform=lambda val: f'{str(val)}%' or 'Unavailable'
            )
        )

class BatteryIcon(Widget.Icon):
    def __init__(self):
        super().__init__(
            image=upower.display_device.bind('icon-name'),
            tooltip_text=upower.display_device.bind(
                'percent',
                transform=lambda val: f'{str(val)}%' or 'Unavailable'
            )
        )

class ControlsButton(Widget.Button):
    def __init__(self):
        super().__init__(
            css_classes=['controls-button'],
            child=Widget.Box(
                vertical=True,
                spacing=12,
                child=[
                    NetworkIcon(),
                    SpeakerIcon(),
                    BatteryIcon() if (len(upower.devices) > 0) else None
                ]
            )
        )
