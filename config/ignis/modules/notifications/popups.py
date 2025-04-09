from ignis.widgets import Widget
from ignis.app import IgnisApp
from ignis.options import options
from ignis.services.notifications import NotificationService
from .widgets import Notification

app = IgnisApp.get_default()
notifications = NotificationService.get_default()

class NotificationPopupsContainer(Widget.Box):
    def __init__(self, *_):
        super().__init__(
            vertical=True,
            spacing=2,
            css_classes=["notification-popups"]
        )

        notifications.connect(
            'new-popup',
            lambda _, notification: self.append(
                Notification(notification, True)
            )
        )
        self.connect(
            'notify::child',
            lambda *_: self.hide_func()
        )
        app.get_window('notification-center').connect(
            'notify::visible',
            lambda *_: self.hide_func()
        )

    def hide_func(self):
        if (
            len(self.child) > 0
            and not app.get_window('notification-center').get_visible()
            and not options.notifications.dnd
        ):
            self.get_parent().set_visible(True)
        else:
            self.get_parent().set_visible(False)

class NotificationPopups(Widget.Window):
    def __init__(self):
        super().__init__(
            namespace="notification-popups",
            anchor=['top'],
            exclusivity="normal",
            layer="top",
            kb_mode="none",
            child=NotificationPopupsContainer()
        )
        self.set_size_request(400, 0)
