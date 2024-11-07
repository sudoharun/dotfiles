from gi.repository import (
    Gtk,
    Gdk,
    GLib,
    GObject,
    Astal,
    AstalIO,
    Pango,
    AstalNotifd as Notifd
)
from datetime import datetime
import os

HOME = os.getenv("HOME")

class Notification(Gtk.Box):
    def __init__(self, id, time, app_name, summary, body, image, actions, popup=False) -> None:
        super().__init__(visible=True, orientation=Gtk.Orientation.VERTICAL, hexpand=True)
        Astal.widget_set_class_names(self, ["Notification"])
        self.id = id
        self.app_name = app_name.strip().replace("\n", " ") or None
        self.summary = summary.strip().replace("\n", " ") or None
        self.body = body.strip().replace("\n", " ") or None
        self.image = image or None
        self.actions = actions
        self.popup = popup
        self.set_name(str(self.id))
        if popup:
            self.set_size_request(300, -1)

        time_object = datetime.fromtimestamp(time)
        self.time = datetime.strftime(time_object, "%I:%M%p")

        # Containers
        self.main_container = Gtk.Box(visible=True, orientation=Gtk.Orientation.HORIZONTAL)
        self.action_buttons_container = Gtk.Box(visible=True, hexpand=True)
        self.app_name_time_container = Gtk.Box(visible=True, hexpand=True)
        self.text_container = Gtk.Box(visible=True, hexpand=True, orientation=Gtk.Orientation.VERTICAL, spacing=2)

        self.app_name_label = Astal.Label(label=self.app_name or "Unknown", halign=Gtk.Align.START, hexpand=False, visible=True)
        self.app_name_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.app_name_label.set_max_width_chars(12)
        self.app_name_label.set_line_wrap(True)
        self.app_name_label.set_line_wrap_mode(Pango.WrapMode.WORD)

        self.time_label = Astal.Label(label=" @ " + str(self.time) or "", halign=Gtk.Align.START, hexpand=True, visible=True)

        self.app_name_time_container.add(self.app_name_label)
        self.app_name_time_container.add(self.time_label)
        Astal.widget_set_class_names(self.app_name_time_container, ["notification-app-name-time"])
        self.text_container.add(self.app_name_time_container)

        if self.summary is not None:
            self.summary_label = Astal.Label(label=self.summary, halign=Gtk.Align.START, visible=True)
            self.summary_label.set_ellipsize(Pango.EllipsizeMode.END)
            self.summary_label.set_line_wrap(True)
            self.summary_label.set_line_wrap_mode(Pango.WrapMode.WORD)
            Astal.widget_set_class_names(self.summary_label, ["notification-summary"])
            self.text_container.add(self.summary_label)

        if self.body is not None:
            self.body_label = Astal.Label(xalign=0, halign=Gtk.Align.START, hexpand=False, visible=True)
            if self.popup:
                self.body_label.set_label(self.body)
                self.body_label.set_ellipsize(Pango.EllipsizeMode.END)
            else:
                self.body_label.set_label(self.body[:147]+"...") if len(self.body) > 150 else self.body_label.set_label(self.body)
                self.body_label.set_line_wrap(True)
                self.body_label.set_line_wrap_mode(Pango.WrapMode.WORD)
            Astal.widget_set_class_names(self.body_label, ["notification-body"])
            self.text_container.add(self.body_label)

        if self.image is not None:
            self.icon = Astal.Icon(icon=self.image, visible=True)
            Astal.widget_set_class_names(self.icon, ["notification-icon"])
            self.main_container.add(self.icon)

        self.main_container.add(self.text_container)

        self.dismiss_button = Astal.Button(visible=True)
        self.dismiss_button.add(Astal.Icon(visible=True, icon="window-close-symbolic"))
        self.dismiss_button.connect("clicked", self.dismiss, True)
        self.main_container.add(self.dismiss_button)

        self.add(self.main_container)

        for action_index in range(len(self.actions)):
            action_button = Astal.Button(visible=True, hexpand=True, halign=Gtk.Align.FILL, label=self.actions[action_index].label)
            action_button.connect("clicked", self.invoke, self.actions[action_index].id)
            self.action_buttons_container.pack_start(action_button, True, True, 0)
        self.add(self.action_buttons_container)

        if self.popup:
            self.timeout_id = GLib.timeout_add(5000, self.dismiss)
            self.connect("destroy", self.on_destroy)

    # Functions
    def dismiss(self, btn=None, dismiss=False):
        if dismiss:
            Notifd.get_default().get_notification(self.id).dismiss()
        self.on_destroy()

    def invoke(self, btn=None, action_id=None):
        Notifd.get_default().get_notification(self.id).invoke(action_id)
        self.dismiss(None, True)

    def on_destroy(self, *args):
        if self.popup:
            if self.timeout_id is not None:
                GLib.source_remove(self.timeout_id)
        self.destroy()

class NotificationPopups(Gtk.Box):
    def __init__(self) -> None:
        super().__init__(visible=True, orientation=Gtk.Orientation.VERTICAL, spacing=4)
        self.set_name("Notification Popups")
        Astal.widget_set_class_names(self, ["NotificationPopups"])
        notifd = Notifd.get_default()
        notifd.connect("notified", self.add_notification)
        notifd.connect("resolved", self.remove_notification)

    def add_notification(self, _, id, *args):
        notification = Notifd.get_default().get_notification(id)
        self.add(Notification(
            notification.get_id(),
            notification.get_time(),
            notification.get_app_name(),
            notification.get_summary(),
            notification.get_body(),
            notification.get_image(),
            notification.get_actions(),
            True
        ))
        AstalIO.Process.exec_async(f"paplay {HOME}/.config/astal/notification.mp3")

    def remove_notification(self, _, id, *args):
        for child in self.get_children():
            if child.get_name() == str(id):
                child.destroy()
                return

class NotificationCenter(Gtk.Box):
    def __init__(self) -> None:
        super().__init__(visible=True, orientation=Gtk.Orientation.VERTICAL, spacing=4)
        self.set_name("Notification Center")
        Astal.widget_set_class_names(self, ["NC"])

        self.ids = []

        notifd = Notifd.get_default()
        notifd.connect("notified", self.add_notification)
        notifd.connect("resolved", self.remove_notification)

        self.add_notification()

    def sort_by_time(self, *args):
        self.ids.clear()

        notifd = Notifd.get_default()
        for notification in notifd.get_notifications():
            self.ids.append(notification.get_id())

        count = 1
        while count != 0:
            count = 0
            for i in range(len(self.ids)):
                if i+1 < len(self.ids):
                    if notifd.get_notification(self.ids[i]).get_time() > notifd.get_notification(self.ids[i+1]).get_time():
                        count+=1
                        temp_var = self.ids[i+1]
                        self.ids.insert(i, temp_var)
                        self.ids.pop(i+2)

    def add_notification(self, _=None, *args):
        for child in self.get_children():
            child.destroy()

        self.sort_by_time()

        notifd = Notifd.get_default()
        for id in self.ids:
            self.add(Notification(
                notifd.get_notification(id).get_id(),
                notifd.get_notification(id).get_time(),
                notifd.get_notification(id).get_app_name(),
                notifd.get_notification(id).get_summary(),
                notifd.get_notification(id).get_body(),
                notifd.get_notification(id).get_image(),
                notifd.get_notification(id).get_actions()
            ))

        if len(self.get_children()) < 1:
            self.label = Astal.Label(label="All Caught Up!", visible=True)
            Astal.widget_set_class_names(self.label, ["nc-no-notifications-label"])
            self.add(self.label)

    def remove_notification(self, _, id, *args):
        for child in self.get_children():
            if child.get_name() == str(id):
                child.destroy()

        if len(self.get_children()) < 1:
            self.label = Astal.Label(label="All Caught Up!", visible=True)
            Astal.widget_set_class_names(self.label, ["nc-no-notifications-label"])
            self.add(self.label)

class NCLabel(Gtk.Box):
    def __init__(self) -> None:
        super().__init__(visible=True)
        Astal.widget_set_class_names(self, ["nc-top-label"])

        self.label = Astal.Label(visible=True, label="Notifications", halign=Gtk.Align.START, valign=Gtk.Align.CENTER, hexpand=True)

        self.button = Astal.Button(visible=True)
        self.button.add(Astal.Icon(visible=True, icon="list-remove-all-symbolic"))
        self.button.connect("clicked", self.clear_all)

        self.add(self.label)
        self.add(self.button)

    def clear_all(self, button, *args):
        notifications = Notifd.get_default().get_notifications()

        for notification in notifications:
            notification.dismiss()

class NPWindow(Astal.Window):
    def __init__(self, monitor: Gdk.Monitor) -> None:
        super().__init__(
            anchor=Astal.WindowAnchor.BOTTOM
            | Astal.WindowAnchor.RIGHT,
            gdkmonitor=monitor,
            exclusivity=Astal.Exclusivity.NORMAL,
            layer=Astal.Layer.TOP,
            visible=True,
            name="notification-popups"
        )

        Astal.widget_set_class_names(self, ["NPWindow"])
        self.add(NotificationPopups())
        self.show_all()

class NCWindow(Astal.Window):
    def __init__(self, monitor: Gdk.Monitor) -> None:
        super().__init__(
            anchor=Astal.WindowAnchor.BOTTOM
            | Astal.WindowAnchor.RIGHT,
            gdkmonitor=monitor,
            exclusivity=Astal.Exclusivity.NORMAL,
            keymode=Astal.Keymode.EXCLUSIVE,
            layer=Astal.Layer.TOP,
            margin=4,
            name="notification-center"
        )

        self.scrolled_window = Gtk.ScrolledWindow(visible=True, hexpand=True, vexpand=True)
        Astal.widget_set_class_names(self.scrolled_window, ["nc-scrollable"])
        self.scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.scrolled_window.add(NotificationCenter())

        self.box = Gtk.Box(visible=True, spacing=4, hexpand=True, vexpand=True, orientation=Gtk.Orientation.VERTICAL)
        Astal.widget_set_class_names(self.box, ["nc-container"])
        self.box.set_size_request(375, round(Gdk.Screen.get_default().get_height()*0.4))
        self.box.add(NCLabel())
        self.box.add(self.scrolled_window)

        self.eventbox = Astal.EventBox(visible=True, hexpand=True, vexpand=True)
        Astal.widget_set_class_names(self.eventbox, ["nc-eventbox"])
        self.eventbox.add(self.box)
        self.eventbox.connect("key-press-event", self.on_escape)
        self.eventbox.connect("hover-lost", self.on_focus_out)
        self.add(self.eventbox)

        Astal.widget_set_class_names(self, ["NCWindow"])
        self.hide()

    def on_escape(self, widget, event, *args):
        if event.keyval == Gdk.KEY_Escape:
            AstalIO.Process.exec_async("astal -i notifications -t notification-center")
            AstalIO.Process.exec_async("astal -i notifications -t notification-popups")

    def on_focus_out(self, widget, event, *args):
        AstalIO.Process.exec_async("astal -i notifications -t notification-center")
        AstalIO.Process.exec_async("astal -i notifications -t notification-popups")
