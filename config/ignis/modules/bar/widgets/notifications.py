from ignis.widgets import Widget
from ignis.app import IgnisApp

app = IgnisApp.get_default()

class NotificationButton(Widget.Button):
    def __init__(self):
        super().__init__(
            child=Widget.Icon(
                image='notification-inactive-symbolic'
            ),
            on_click=lambda *_: self.on_self_click()
        )

    def on_self_click(self):
        app.toggle_window('notification-center')
