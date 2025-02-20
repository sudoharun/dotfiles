from gi.repository import (
    Gtk,
    Astal,
    AstalIO
)
from .widgets.Backlight import BacklightGraphics

class TopLabel(Gtk.Box):
    def __init__(self) -> None:
        super().__init__()

        self.add_css_class('power-display-top-label')

        self.label = Gtk.Label(
            label="Power & Display",
            hexpand=True,
            xalign=0
        )

        self.lock_button = Gtk.Button()
        self.logout_button = Gtk.Button()
        self.reboot_button = Gtk.Button()
        self.shutdown_button = Gtk.Button()

        self.lock_button.set_tooltip_text("Lock")
        self.logout_button.set_tooltip_text("Log out")
        self.reboot_button.set_tooltip_text("Reboot")
        self.shutdown_button.set_tooltip_text("Shutdown")

        self.lock_button.set_child(
            Gtk.Image().new_from_icon_name('system-lock-screen-symbolic')
        )
        self.logout_button.set_child(
            Gtk.Image().new_from_icon_name("system-log-out-symbolic")
        )
        self.reboot_button.set_child(
            Gtk.Image().new_from_icon_name("system-reboot-symbolic")
        )
        self.shutdown_button.set_child(
            Gtk.Image().new_from_icon_name("system-shutdown-symbolic")
        )

        self.lock_button.connect("clicked", self.on_lock_button_click)
        self.logout_button.connect("clicked", self.on_logout_button_click)
        self.reboot_button.connect("clicked", self.on_reboot_button_click)
        self.shutdown_button.connect("clicked", self.on_shutdown_button_click)

        self.append(self.label)
        self.append(self.lock_button)
        self.append(self.logout_button)
        self.append(self.reboot_button)
        self.append(self.shutdown_button)

    def on_lock_button_click(self, *_):
        AstalIO.Process.subprocess("sh -c 'hyprlock &'")

    def on_logout_button_click(self, *_):
        AstalIO.Process.subprocess("sh -c 'pkill Hyprland'")

    def on_reboot_button_click(self, *_):
        AstalIO.Process.exec("systemctl reboot")

    def on_shutdown_button_click(self, *_):
        AstalIO.Process.exec("systemctl poweroff")

class PowerDisplayWidget(Gtk.Popover):
    def __init__(self) -> None:
        super().__init__()

        self.add_css_class('power-display')
        self.set_size_request(300, -1)

        self.box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=8
        )

        self.top_label = TopLabel()
        self.box.append(self.top_label)

        self.graphics = BacklightGraphics()
        self.box.append(self.graphics)

        self.set_child(self.box)
