from os import major
from ignis.widgets import Widget
from ignis.services.notifications import NotificationService
from ignis.options import options
from .widgets import Notification

notifications = NotificationService.get_default()

class NotificationCenterTopSection(Widget.Box):
    def __init__(self):
        super().__init__(
            child=[
                Widget.Label(
                    hexpand=True,
                    halign='start',
                    valign='center',
                    label="Notifications"
                ),
                Widget.Button(
                    child=Widget.Icon(
                        image='delete',
                        pixel_size=24
                    ),
                    tooltip_text='Clear all notifications',
                    on_click=lambda *_: notifications.clear_all()
                )
            ]
        )

class NotificationCenterNotifications(Widget.Box):
    def __init__(self, *_):
        super().__init__(
            vertical=True,
            vexpand=True,
            spacing=8,
            child=[Notification(notification) for notification in reversed(notifications.notifications)]
        )

        notifications.connect(
            'notified',
            lambda _, notification: self.prepend(
                Notification(notification)
            )
        )

class NotificationCenterBottomSection(Widget.Box):
    def __init__(self):
        super().__init__(
            valign='end',
            child=[
                Widget.Label(
                    hexpand=True,
                    halign='start',
                    valign='center',
                    label="Do Not Disturb"
                ),
                Widget.Switch(
                    active=options.notifications.bind('dnd'),
                    on_change=lambda _, state: self.on_switched(state)
                )
            ]
        )

    def on_switched(self, state):
        options.notifications.dnd = state

class NotificationCenterContainer(Widget.Box):
    def __init__(self):
        super().__init__(
            vertical=True,
            spacing=8,
            css_classes=["notification-center"],
            child=[
                NotificationCenterTopSection(),
                Widget.Scroll(
                    vexpand=True,
                    overlay_scrolling=False,
                    child=NotificationCenterNotifications()
                ),
                NotificationCenterBottomSection()
            ]
        )

class NotificationCenter(Widget.Window):
    def __init__(self):
        super().__init__(
            namespace="notification-center",
            anchor=['top', 'left', 'bottom'],
            exclusivity="normal",
            layer="top",
            kb_mode="none",
            visible=False,
            css_classes=['notification-center'],
            child=NotificationCenterContainer()
        )
        self.set_size_request(500, -1)
