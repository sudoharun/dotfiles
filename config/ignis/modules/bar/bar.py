from ignis.widgets import Widget
from .widgets import (
    Clock,
    Tray,
    Workspaces,
    NotificationButton,
    ControlsButton
)

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
                    ControlsButton(),
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
