from ignis.widgets import Widget
from ignis.utils import Utils
from datetime import datetime

class Clock(Widget.Box):
    def __init__(self):
        super().__init__(
            vertical=True,
            halign='center'
        )

        self.hours = Widget.Label()
        self.minutes = Widget.Label()

        Utils.Poll(
            timeout=1_000,
            callback=lambda *_: self.set_time()
        )
        self.set_time()

        self.append(self.hours)
        self.append(self.minutes)

    def set_time(self):
        self.hours.label = datetime.now().strftime('%H')
        self.minutes.label = datetime.now().strftime('%M')
        self.tooltip_text = datetime.now().strftime('%A %d %B %Y')
