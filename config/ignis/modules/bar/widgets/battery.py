from ignis.widgets import Widget
from ignis.services.upower import UPowerService

upower = UPowerService.get_default()

class BatteryButton(Widget.Button):
    def __init__(self):
        super().__init__(
            child=Widget.Icon(
                image=upower.display_device.bind('icon-name')
            ),
            tooltip_text=upower.display_device.bind(
                'percent',
                transform=lambda val: f'{str(val)}%' or 'Unavailable'
            )
        )
