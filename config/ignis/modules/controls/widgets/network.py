from ignis.widgets import Widget
from ignis.services.network import NetworkService
import asyncio

network = NetworkService.get_default()

class AccessPoint(Widget.Box):
    def __init__(self, ap):
        super().__init__(
            spacing=4,
            vertical=True
        )
        self.ap = ap

        self.icon = Widget.Icon(
            image=self.ap.bind(
                'icon_name',
                transform=lambda x: x or 'network-wireless-disconnected-symbolic'
            )
        )
        self.label = Widget.Label(
            label=self.ap.bind(
                'strength',
                lambda x: f'{self.ap.ssid or "Unknown"} ({x}%)' or (self.ap.ssid or "Unknown")
            ),
            tooltip_text=self.ap.bind(
                'frequency',
                transform=lambda x: f'{x}mHz' or '???mHz'
            )
        )
        self.button = Widget.Button(
            child=Widget.Box(
                spacing=4,
                child=[
                    self.icon,
                    self.label
                ]
            )
        )

        self.actions_revealer = Widget.Revealer(
            transition_type='slide_down',
            transition_duration=200,
            reveal_child=False
        )

        if self.ap.is_connected:
            pass
        else:
            self.actions_revealer.child = Widget.Button(
                child=Widget.Label(
                    label='Connect',
                    tooltip_text='Connect to this network'
                ),
                on_click=lambda *_: asyncio.create_task(self.ap.connect_to_graphical())
            )

        self.ap.connect(
            'removed',
            lambda *_: self.unparent() if self.get_parent() is not None else None
        )

        self.button.connect(
            'clicked',
            lambda *_: self.on_button_clicked()
        )

        self.child = [
            self.button,
            self.actions_revealer
        ]

    def on_button_clicked(self):
        if not self.ap.is_connected:
            self.actions_revealer.reveal_child = not self.actions_revealer.reveal_child

class EthernetButton(Widget.Box):
    def __init__(self):
        super().__init__(
            spacing=4,
            visible=network.ethernet.bind('is-connected'),
            child=[
                Widget.Icon(
                    image=network.ethernet.bind('icon-name')
                ),
                Widget.Label(
                    label=network.ethernet.bind(
                        'is-connected', transform=lambda x: 'Connected' if x else 'Disconnected'
                    ),
                    ellipsize='end'
                )
            ],
            tooltip_text=network.ethernet.bind(
                'is-connected', transform=lambda x: 'Connected' if x else 'Disconnected'
            )
        )

class WifiDeviceButton(Widget.Box):
    def __init__(self, device):
        super().__init__(
            spacing=4,
            vertical=True
        )
        self.device = device

        self.icon = Widget.Icon(
            image=self.device.ap.bind(
                'icon_name',
                transform=lambda x: x or 'network-wireless-disconnected-symbolic'
            )
        )
        self.label = Widget.Label(
            label=self.device.ap.bind(
                'ssid',
            ),
            tooltip_text=self.device.ap.bind(
                'strength',
                transform=lambda x: f'{x}%' or '???%'
            )
        )
        self.button = Widget.Button(
            child=Widget.Box(
                spacing=4,
                child=[
                    self.icon,
                    self.label
                ]
            )
        )

        self.reconnect_button = Widget.Button(
            child=Widget.Label(
                label='Reconnect',
                tooltip_text='Disconnect then reconnect to this network'
            ),
            on_click=lambda *_: asyncio.create_task(self.reconnect(self.device.ap))
        )

        self.disconnect_button = Widget.Button(
            child=Widget.Label(
                label='Disconnect',
                tooltip_text='Disconnect to this network'
            ),
            on_click=lambda *_: asyncio.create_task(self.disconnect(self.device.ap))
        )

        self.forget_button = Widget.Button(
            child=Widget.Label(
                label='Forget',
                tooltip_text='Disconnect and forget this network'
            ),
            on_click=lambda *_: asyncio.create_task(self.forget(self.device.ap))
        )

        self.actions_revealer = Widget.Revealer(
            child=Widget.Box(
                vertical=True,
                spacing=2,
                child=[
                    self.reconnect_button,
                    self.disconnect_button,
                    self.forget_button
                ]
            ),
            transition_type='slide_down',
            transition_duration=200,
            reveal_child=False
        )

        self.device.connect(
            'removed',
            lambda *_: self.unparent() if self.get_parent() is not None else None
        )

        self.button.connect(
            'clicked',
            lambda *_: self.on_button_clicked()
        )

        self.child = [
            self.button,
            self.actions_revealer
        ]

    def on_button_clicked(self):
        self.actions_revealer.reveal_child = not self.actions_revealer.reveal_child

    async def disconnect(self, ap):
        await ap.disconnect_from()

    async def reconnect(self, ap):
        await ap.disconnect_from()
        await ap.connect_to(ap.psk)

    async def forget(self, ap):
        await ap.disconnect_from()
        self.device._device.get_active_connection().get_connection().delete()

class WifiSettings(Widget.Box):
    def __init__(self):
        super().__init__(
            vertical=True,
            vexpand=True,
            spacing=4
        )
        self.active_wifi_device = network.wifi.bind(
            'devices',
            transform=lambda x: x[-1] or None
        )

        self.top_label = Widget.Box(
            spacing=4,
            child=[
                Widget.Label(
                    label='WiFi',
                    ellipsize='end',
                    xalign=0,
                    hexpand=True
                ),
                Widget.Button(
                    label='Scan',
                    on_click=lambda *_: self.scan_for_aps()
                )
            ]
        )

        self.child = [
            Widget.Box(
                vertical=True,
                spacing=2,
                child=network.wifi.bind(
                    'devices',
                    lambda x: [WifiDeviceButton(device) for device in x] or None
                )
            ),
            self.top_label,
            Widget.Scroll(
                vexpand=True,
                hscrollbar_policy='never',
                child=Widget.Box(
                    vertical=True,
                    child=[
                        Widget.Box(
                            vertical=True,
                            spacing=2,
                            child=self.populate_aps(device)
                        ) for device in network.wifi.devices
                    ]
                )
            )
        ]

    def populate_aps(self, device):
        list_to_return = []
        for ap in device.access_points:
            if not ap.is_connected and ap.ssid is not None:
                list_to_return.append(AccessPoint(ap))
        return list_to_return

    def scan_for_aps(self):
        for device in network.wifi.devices:
            asyncio.create_task(device.scan())
