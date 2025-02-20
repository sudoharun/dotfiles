from gi.repository import (
    Gtk,
    AstalApps as Apps
)

class Information(Gtk.Box):
    def __init__(self, icon=None, title=None) -> None:
        super().__init__(
            spacing=8
        )

        if icon:
            self.icon = Gtk.Image().new_from_icon_name(icon)
            self.append(self.icon)

        if title:
            self.title = Gtk.Label(
                label=title
            )
            self.append(self.title)

class AppEntry(Gtk.ListBoxRow):
    def __init__(self, application: Apps.Application) -> None:
        super().__init__()

        self.application = application

        self.information = Information(
            icon=self.application.get_icon_name(),
            title=self.application.get_name()
        )
        self.set_child(self.information)

        self.set_name(self.application.get_name())
        self.connect('activate', self.on_self_activated)

    def on_self_activated(self, *_):
        self.application.launch()

    def get_application(self):
        return self.application
