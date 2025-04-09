from ignis.widgets import Widget
from ignis.services.network import NetworkService

network = NetworkService.get_default()

class WifiButton(Widget.Button):
    def __init__(self):
        super().__init__(
            visible=network.wifi.bind('is-connected'),
            child=Widget.Icon(
                image=network.wifi.bind('icon-name')
            ),
            tooltip_text=network.wifi.bind(
                'is-connected',
                transform=lambda x: 'Connected' if x else 'Disconnected' or 'Unavailable'
            )
        )

class EthernetButton(Widget.Button):
    def __init__(self):
        super().__init__(
            visible=network.ethernet.bind('is-connected'),
            child=Widget.Icon(
                image=network.ethernet.bind('icon-name')
            ),
            tooltip_text=network.ethernet.bind(
                'is_connected',
                transform=lambda x: 'Connected' if x else 'Disconnected' or 'Unavailable'
            )
        )
