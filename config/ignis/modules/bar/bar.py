from ignis.widgets import Widget
from ignis.services.network import NetworkService
from .widgets import (
    SpeakerButton,
    BatteryButton,
    Clock,
    WifiButton,
    EthernetButton,
    Tray,
    Workspaces,
    NotificationButton
)

network = NetworkService.get_default()

class Container(Widget.CenterBox):
    def __init__(self):
        super().__init__(
            vertical=True,
            css_classes=['bar'],
            start_widget=Widget.Box(
                vertical=True,
                spacing=16,
                child=[
                    Clock(),
                    Widget.Separator(),
                    Workspaces(),
                ]
            ),
            center_widget=Widget.Box(
                vertical=True,
                child=[]
            ),
            end_widget=Widget.Box(
                vertical=True,
                spacing=4,
                child=[
                    Tray(),
                    WifiButton(),
                    EthernetButton(),
                    SpeakerButton(),
                    BatteryButton(),
                    NotificationButton()
                ]
            )
        )

class Bar(Widget.Window):
    def __init__(self, monitor):
        super().__init__(
            namespace=f"ignis-bar-{monitor}",
            exclusivity="exclusive",
            anchor=["top", "left", "bottom"],
            child=Container(),
            monitor=monitor,
            css_classes=['bar']
        )
