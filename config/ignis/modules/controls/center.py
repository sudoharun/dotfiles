from ignis.widgets import Widget
from .widgets import (
    EthernetButton,
    WifiSettings
)

class ControlCenterContainer(Widget.Box):
    def __init__(self):
        super().__init__(
            vertical=True,
            spacing=4,
            child=[
                EthernetButton(),
                WifiSettings()
            ]
        )

class ControlCenter(Widget.Window):
    def __init__(self):
        super().__init__(
            namespace="control-center",
            anchor=['top', 'right', 'bottom'],
            exclusivity="normal",
            layer="top",
            kb_mode="none",
            visible=True,
            css_classes=['control-center'],
            child=ControlCenterContainer()
        )
        #self.set_size_request(500, -1)
        self.set_size_request(100, -1)
