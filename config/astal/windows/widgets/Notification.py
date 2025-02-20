from gi.repository import (
    Gtk,
    GLib,
    Pango,
    AstalNotifd as Notifd,
)
from datetime import datetime
import os

HOME = os.getenv("HOME")

class TopLabel(Gtk.Box):
    def __init__(self, id=None, label=None, icon=None, time=None, popup=False) -> None:
        super().__init__(
            visible=True,
            spacing=8,
            orientation=Gtk.Orientation.HORIZONTAL
        )

        self.add_css_class('notification-top-label')

        self.popup = popup
        self.id = id
        self.icon = Gtk.Image(
            visible=True
        )

        self.label = Gtk.Label(
            hexpand=True,
            xalign=0
        )
        self.label.set_size_request(40, -1) if popup else self.label.set_size_request(50, -1)
        self.label.set_wrap(False)
        self.label.set_ellipsize(Pango.EllipsizeMode.END)

        self.time = Gtk.Label(
            hexpand=False,
            halign=Gtk.Align.END
        )
        self.close_button = Gtk.Button(
            halign=Gtk.Align.END
        ).new_from_icon_name('window-close-symbolic')
        self.close_button.add_css_class('notification-close-button')

        if icon:
            self.icon.set_from_file(icon)
        else:
            self.icon.set_visible(False)

        if label:
            self.label.set_label(label)
        else:
            self.label.set_visible(False)

        if time:
            time_obj = datetime.fromtimestamp(time)
        else:
            time_obj = None
        if time_obj:
            time = datetime.strftime(time_obj, "%I:%M%p")
        if time:
            self.time.set_label(time)
        else:
            self.time.set_visible(False)

        self.close_button.connect('clicked', self.on_clicked)

        self.append(self.icon)
        self.append(self.label)
        self.append(Gtk.Box(
            visible=True,
            hexpand=True
        ))
        self.append(self.time)
        self.append(self.close_button)

    def on_clicked(self, *_):
        if self.popup:
            GLib.source_remove(self.get_parent().timeout_id)
            GLib.source_remove(self.get_parent().get_parent().get_parent().timeout_id)
            self.get_parent().get_parent().get_parent().hide()

        try:
            Notifd.get_default().get_notification(self.id).dismiss()
        except Exception:
            self.get_parent().unparent()

class Information(Gtk.Box):
    def __init__(self, summary=None, body=None, popup=False) -> None:
        super().__init__(
            visible=True,
            orientation=Gtk.Orientation.VERTICAL,
            halign=Gtk.Align.START,
            spacing=4
        )

        self.add_css_class('notification-information')

        self.summary = Gtk.Label(
            hexpand=True,
            xalign=0
        )
        self.summary.add_css_class('notification-summary')
        self.summary.set_size_request(100, -1) if popup else self.summary.set_size_request(150, -1)
        self.summary.set_wrap(False)
        self.summary.set_ellipsize(Pango.EllipsizeMode.END)

        self.body = Gtk.Label(
            xalign=0
        )
        self.body.set_size_request(100, -1) if popup else self.body.set_size_request(150, -1)
        self.body.set_wrap(True)
        self.body.set_wrap_mode(Pango.WrapMode.WORD_CHAR)
        self.body.set_ellipsize(Pango.EllipsizeMode.END)
        self.body.set_lines(5)

        if summary:
            self.summary.set_label(summary)
        else:
            self.summary.set_visible(False)

        if body:
            self.body.set_label(body)
        else:
            self.body.set_visible(False)

        self.append(self.summary)
        self.append(self.body)

class ActionButtons(Gtk.Box):
    def __init__(self, parent, notification: Notifd.Notification) -> None:
        super().__init__(
            visible=True,
            hexpand=True,
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=4
        )

        self.add_css_class('notification-actions')

        self.parent = parent
        self.notification = notification
        self.notification_id = notification.get_id()
        self.actions = notification.get_actions()

        for action in self.actions:
            action_button = Gtk.Button(
                visible=True,
                hexpand=True,
                halign=Gtk.Align.FILL
            )
            action_button.set_label(action.label)
            action_button.connect('clicked', self.on_clicked, action.id)
            self.append(action_button)

    def on_clicked(self, _, action_id):
        self.notification.invoke(action_id)
        self.notification.dismiss()
        self.parent.unparent()

class Notification(Gtk.Box):
    def __init__(self, notification: Notifd.Notification, popup=False) -> None:
        super().__init__(
            visible=True,
            orientation=Gtk.Orientation.VERTICAL,
            spacing=4
        )

        self.add_css_class('notification')

        self.timeout_id = None
        self.top_label = TopLabel(
            id=notification.get_id(),
            label=notification.get_app_name(),
            icon=notification.get_image(),
            time=notification.get_time(),
            popup=popup
        )

        self.information = Information(
            summary=notification.get_summary(),
            body=notification.get_body(),
            popup=popup
        )

        self.action_buttons = ActionButtons(
            parent=self,
            notification=notification
        )

        self.append(self.top_label)
        self.append(self.information)
        if notification.get_actions():
            self.append(self.action_buttons)

        notification.connect('resolved', self.on_resolved)

    def on_resolved(self, *_):
        self.unparent()
