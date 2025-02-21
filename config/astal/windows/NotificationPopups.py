from gi.repository import (
    Gtk,
    GLib,
    Astal,
    AstalIO,
    AstalNotifd as Notifd,
)
from .widgets.Notification import Notification

class EmptyExpandedBox(Gtk.Box):
    def __init__(self) -> None:
        super().__init__(
            hexpand=True,
            vexpand=True
        )

class NotificationPopups(Astal.Window):
    def __init__(self, app: Astal.Application, notification_center_reference) -> None:
        super().__init__(
            anchor=Astal.WindowAnchor.BOTTOM
            | Astal.WindowAnchor.RIGHT,
            exclusivity=Astal.Exclusivity.NORMAL,
            layer=Astal.Layer.TOP,
            keymode=Astal.Keymode.NONE,
            application=app,
            name="notification-popups"
        )

        self.timeout_id = None
        self.notification_center_reference = notification_center_reference
        self.add_css_class('notification-popups')
        self.set_size_request(300, 0)
        self.set_default_size(1, 1)

        self.box = Astal.Box(
            visible=True,
            orientation=Gtk.Orientation.VERTICAL,
            spacing=0
        )
        self.set_child(self.box)

        notifd = Notifd.get_default()
        notifd.connect('notified', self.add_notification)
        notifd.connect('notify::dont-disturb', lambda obj, _: self.set_visible(False) if obj.get_dont_disturb() else self.set_visible(True))

    def add_notification(self, obj: Notifd.Notifd=None, id: int=-1, *_):
        notification = Notification(
            notification=Notifd.get_default().get_notification(id),
            popup=True
        )
        self.box.append(notification)
        if not Notifd.get_default().get_dont_disturb():
            AstalIO.Process.subprocess('mpv assets/notification_sound.mp3')
        self.set_timeout(notification)

    def set_timeout(self, notification):
        if self.timeout_id is None:
            self.timeout_id = GLib.timeout_add(3001, lambda *_: self.set_visible(False))
        else:
            GLib.source_remove(self.timeout_id)
            self.timeout_id = None
            self.timeout_id = GLib.timeout_add(3001, self.hide)

        if notification.timeout_id is None:
            notification.timeout_id = GLib.timeout_add(3000, notification.unparent)
        else:
            notification.unparent()
            GLib.source_remove(notification.timeout_id)
            notification.timeout_id = None
            notification.timeout_id = GLib.timeout_add(3000, notification.unparent)

        if not Notifd.get_default().get_dont_disturb() and not self.notification_center_reference.get_visible():
            self.set_visible(True)
