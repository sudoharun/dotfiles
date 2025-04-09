from ignis.widgets import Widget
from ignis.utils import Utils
from datetime import datetime

class NotificationIcon(Widget.Icon):
    def __init__(self, image):
        super().__init__(
            image=image.replace("file://", "").replace("%20", " "),
            pixel_size=32
        )

class NotificationTopBar(Widget.Box):
    def __init__(self, notification, timeout):
        super().__init__(
            spacing=8,
            child=[
                Widget.Icon(
                    image=notification.icon.replace("file://", "").replace("%20", " "),
                    pixel_size=18
                ) if notification.icon else None,
                Widget.Label(
                    hexpand=True,
                    halign="start",
                    label=notification.app_name.strip(),
                    ellipsize="end"
                ) if notification.app_name else None,
                Widget.Label(
                    label=datetime.fromtimestamp(notification.time).strftime('%H:%M')
                ),
                Widget.Button(
                    css_classes=['notification-close'],
                    child=Widget.Icon(
                        image='window-close-symbolic'
                    ),
                    on_click=lambda *_: self._on_click()
                )
            ]
        )

        self.notification = notification
        self.timeout = timeout

    def _on_click(self):
        self.notification.close()
        self.timeout.cancel() if self.timeout else None

class NotificationInformation(Widget.Box):
    def __init__(self, notification):
        super().__init__(
            vertical=True,
            spacing=4,
            child=[
                Widget.Label(
                    label=notification.summary.strip(),
                    hexpand=True,
                    halign="start",
                    ellipsize="end"
                ) if notification.summary else None,
                Widget.Label(
                    label=notification.body.strip(),
                    halign="start",
                    valign="start",
                    xalign=0,
                    ellipsize="end",
                    wrap=True,
                    lines=5
                ) if notification.body else None
            ]
        )

class NotificationActions(Widget.Box):
    def __init__(self, notification, timeout):
        super().__init__(
            spacing=2,
            child=[
                Widget.Button(
                    css_classes=['notification-action'],
                    hexpand=True,
                    label=action.label,
                    on_click=lambda _: self.on_action_clicked(action)
                ) for action in notification.actions
            ]
        )

        self.notification = notification
        self.timeout = timeout

    def on_action_clicked(self, action):
        action.invoke()
        self.notification.close()
        self.timeout.cancel() if self.timeout else None

class Notification(Widget.Box):
    def __init__(self, notification, is_popup=False):
        if is_popup:
            self.timeout = Utils.Timeout(
                ms=3_000,
                target=lambda: self.unparent()
            )
        else:
            self.timeout = None

        super().__init__(
            vertical=True,
            spacing=4,
            css_classes=['notification'],
            child=[
                NotificationTopBar(notification, self.timeout),
                NotificationInformation(notification),
                NotificationActions(notification, self.timeout)
            ]
        )
        notification.connect(
            'closed',
            lambda *_: self._on_resolved()
        )

    def _on_resolved(self):
        self.unparent()
