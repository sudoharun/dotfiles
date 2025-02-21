from gi.repository import (
    Gtk,
    GObject,
    Astal,
    AstalIO,
    AstalPowerProfiles as PowerProfiles
)
from .widgets.Backlight import BacklightGraphics

SYNC = GObject.BindingFlags.SYNC_CREATE

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

class PowerProfilesDropdown(Gtk.Box):
    def __init__(self) -> None:
        super().__init__(
            spacing=8
        )

        self.add_css_class('power-profiles-dropdown')

        self.icon = Gtk.Image()

        self.label = Gtk.Label(
            label='Power Profile:',
            hexpand=True,
            xalign=0
        )

        self.profiles = {
            'Power-saver': 0,
            'Balanced': 1,
            'Performance': 2
        }

        self.i_profile = 0

        power_profiles = PowerProfiles.get_default()
        power_profiles.connect('notify::active-profile', self.on_active_profile_changed)
        power_profiles.bind_property('icon-name', self.icon, 'icon-name', SYNC)

        self.dropdown = Gtk.DropDown.new_from_strings(list(self.profiles.keys()))
        self.dropdown.set_selected(self.profiles[power_profiles.get_active_profile().capitalize()])
        self.dropdown.connect('notify::selected', lambda *_: power_profiles.set_active_profile(list(self.profiles.keys())[self.dropdown.get_selected()].lower()))

        self.append(self.icon)
        self.append(self.label)
        self.append(self.dropdown)

    def on_active_profile_changed(self, *_):
        power_profiles = PowerProfiles.get_default()
        if self.i_profile == 0:
            self.i_profile = 1
            return
        if list(self.profiles.keys())[self.dropdown.get_selected()].lower() != power_profiles.get_active_profile():
            self.dropdown.set_selected(self.profiles[power_profiles.get_active_profile().capitalize()])
        self.i_profile = 0

class PowerDisplayWidget(Gtk.Popover):
    def __init__(self) -> None:
        super().__init__()

        self.add_css_class('power-display')
        self.set_size_request(350, -1)

        self.box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=8
        )

        self.top_label = TopLabel()
        self.box.append(self.top_label)

        self.graphics = BacklightGraphics()
        self.box.append(self.graphics)

        self.power_profiles = PowerProfilesDropdown()
        self.box.append(self.power_profiles)

        self.set_child(self.box)
