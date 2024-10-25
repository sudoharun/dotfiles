from gi.repository import (
    Gtk,
    Gdk,
    GLib,
    GObject,
    Astal,
    Pango,
    AstalNotifd as Notifd
)

class NotificationCenter(Gtk.Box):
    def __init__(self) -> None:
        super().__init__(visible=True, orientation=Gtk.Orientation.VERTICAL, spacing=4)
        self.notifs = {}
        Astal.widget_set_class_names(self, ["NotificationCenter"])
        notifd = Notifd.get_default()
        notifd.connect("notified", self.sync)

    def sync(self, _: Notifd.Notification, id: str, *args):
        notification = Notifd.get_default().get_notification(id)

        notif_h_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        notif_v_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        notif_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        notif_text = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        notif_app = Astal.Label(label=notification.get_app_name())
        notif_summary = Astal.Label(label=notification.get_summary())
        notif_body = Astal.Label(label=notification.get_body())

        notif_app.set_halign(Gtk.Align.START)
        notif_summary.set_halign(Gtk.Align.START)
        notif_body.set_halign(Gtk.Align.START)

        notif_app.set_ellipsize(Pango.EllipsizeMode.END)
        notif_app.set_line_wrap(True)
        notif_app.set_line_wrap_mode(Pango.WrapMode.WORD)

        notif_summary.set_ellipsize(Pango.EllipsizeMode.END)
        notif_summary.set_line_wrap(True)
        notif_summary.set_line_wrap_mode(Pango.WrapMode.WORD)

        notif_body.set_ellipsize(Pango.EllipsizeMode.END)
        notif_body.set_line_wrap(True)
        notif_body.set_line_wrap_mode(Pango.WrapMode.WORD)

        if notification.get_image() is not None:
            notif_icon = Astal.Icon()
            notif_icon.set_icon(notification.get_image())
            Astal.widget_set_class_names(notif_icon, ["notif-icon"])
        else:
            notif_icon = None

        if len(notif_app.get_label()) > 0:
            notif_text.add(notif_app)

        if len(notif_summary.get_label()) > 0:
            notif_text.add(notif_summary)

        if len(notif_body.get_label()) > 0:
            notif_text.add(notif_body)

        if notif_icon is not None:
            notif_h_container.add(notif_icon)

        notif_h_container.pack_start(notif_text, True, True, 0)

        dismiss_btn = Astal.Button()
        dismiss_btn.add(Astal.Icon(icon='window-close-symbolic'))
        notif_h_container.pack_end(dismiss_btn, False, False, 0)

        def dismiss(dismiss_btn=None, dismiss_bool=False):
            for child in self.get_children():
                if child.get_name() == str(id):
                    child.destroy()
            if dismiss_bool:
                notification.dismiss()

        dismiss_btn.connect("clicked", dismiss, True)

        notif_container.add(notif_h_container)

        def invoke_action(btn, action_id):
            notification.invoke(action_id)
            dismiss(None, True)

        btns_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, hexpand=True)

        for action_index in range(len(notification.get_actions())):
            btn = Astal.Button(label=notification.get_actions()[action_index].label)
            btn.set_halign(Gtk.Align.FILL)
            btn.connect("clicked", invoke_action, notification.get_actions()[action_index].id)
            Astal.widget_set_class_names(btn, ["action"])
            btns_container.pack_start(btn, True, True, 0)

        notif_container.add(btns_container)

        notif_container.set_name(str(id))
        notif_container.set_size_request(300, -1)
        self.add(notif_container)

class NotifWindow(Astal.Window):
    def __init__(self, monitor: Gdk.Monitor) -> None:
        super().__init__(
            anchor=Astal.WindowAnchor.BOTTOM
            | Astal.WindowAnchor.RIGHT,
            gdkmonitor=monitor,
            exclusivity=Astal.Exclusivity.NORMAL,
            layer=Astal.Layer.TOP
        )

        Astal.widget_set_class_names(self, ["Notifications"])

        self.add(Notification())

        self.show_all()
