from gi.repository import (
    Gtk,
    Astal,
    AstalNotifd as Notifd,
)
from .widgets.Notification import Notification

class TopLabel(Gtk.Box):
    def __init__(self) -> None:
        super().__init__(
            hexpand=True
        )

        self.add_css_class('notification-center-top-label')

        self.label = Gtk.Label(
            label='Notifications',
            hexpand=True,
            xalign=0
        )

        self.clear_button = Gtk.Button()
        self.icon = Gtk.Image().new_from_icon_name('user-trash-symbolic')
        self.clear_button.set_child(self.icon)

        self.clear_button.connect('clicked', self.clear_notifications)

        self.append(self.label)
        self.append(self.clear_button)

    def clear_notifications(self, *_):
        notifd = Notifd.get_default()
        for notification in notifd.get_notifications():
            notification.dismiss()

class DoNotDisturb(Gtk.Box):
    def __init__(self) -> None:
        super().__init__()

        notifd = Notifd.get_default()

        self.label = Gtk.Label(
            label='Do Not Disturb',
            hexpand=True,
            xalign=0
        )
        self.append(self.label)

        self.switch = Gtk.Switch()
        self.append(self.switch)

        self.switch.set_active(notifd.get_dont_disturb())
        self.switch.connect('state-set', self.set_dnd)

    def set_dnd(self, *_):
        notifd = Notifd.get_default()
        notifd.set_dont_disturb(self.switch.get_active())

class NotificationCenter(Astal.Window):
    def __init__(self, app: Astal.Application) -> None:
        super().__init__(
            anchor=Astal.WindowAnchor.BOTTOM
            | Astal.WindowAnchor.RIGHT,
            exclusivity=Astal.Exclusivity.NORMAL,
            layer=Astal.Layer.TOP,
            keymode=Astal.Keymode.ON_DEMAND,
            application=app,
            name='notification-center'
        )

        self.add_css_class('notification-center')
        self.set_size_request(400, 450)

        self.box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=0
        )
        self.box.add_css_class('notification-center')
        self.set_child(self.box)

        self.top_label = TopLabel()
        self.top_label.clear_button.connect('clicked', self.clear_notifications)
        self.box.append(self.top_label)

        self.scrolled = Gtk.ScrolledWindow(
            visible=True,
            vexpand=True
        )
        self.notifications_container = Astal.Box(
            visible=True,
            orientation=Gtk.Orientation.VERTICAL,
            spacing=0
        )
        self.scrolled.set_child(self.notifications_container)
        self.scrolled.add_css_class('notifications-scrolled')
        self.box.append(self.scrolled)

        self.dnd = DoNotDisturb()
        self.dnd.add_css_class('notification-center-dnd')
        self.box.append(self.dnd)

        notifd = Notifd.get_default()
        notifd.connect('notified', self.add_notification)

        for notification in notifd.get_notifications():
            notification = Notification(notification=notification)
            self.notifications_container.append(notification)

        self.focus_controller = Gtk.EventControllerFocus.new()
        self.add_controller(self.focus_controller)
        self.focus_controller.connect('leave', self.on_focus_lost)

        self.connect('notify::visible', lambda _, value: self.grab_focus() if value else self.set_visible(value))

    def add_notification(self, obj: Notifd.Notifd=None, id: int=-1, *_):
        notification = Notification(notification=Notifd.get_default().get_notification(id))
        self.notifications_container.prepend(notification)

    def clear_notifications(self, *_):
        for child in self.notifications_container.get_children():
            child.unparent()

    def on_focus_lost(self, *_):
        if not self.has_focus():
            self.set_visible(False)
