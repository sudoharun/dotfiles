from gi.repository import (
    Gtk,
    Gdk,
    GLib,
    GObject,
    Astal,
    AstalIO,
    AstalApps as Apps
)

class AppsBox(Gtk.Box):
    def __init__(self) -> None:
        super().__init__(orientation=Gtk.Orientation.VERTICAL, hexpand=True, vexpand=True, spacing=6, visible=True)
        self.set_size_request(375, 425)
        Astal.widget_set_class_names(self, ["apps-box"])
        self.focus_order = 0

        self.entry = Gtk.Entry(hexpand=True, vexpand=False, visible=True)
        self.entry.set_icon_from_icon_name(Gtk.EntryIconPosition.PRIMARY, "system-search-symbolic")
        self.entry.set_placeholder_text("Search...")
        self.entry.connect("changed", self.on_entry_changed)
        self.entry.connect("key-press-event", self.on_key_press)
        Astal.widget_set_class_names(self.entry, ["app-search"])
        self.add(self.entry)

        self.scrolled_window = Gtk.ScrolledWindow(hexpand=True, vexpand=True, visible=True)
        Astal.widget_set_class_names(self.scrolled_window, ["apps-scrolled"])
        self.apps_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, hexpand=True, vexpand=True, visible=True)

        self.scrolled_window.add(self.apps_box)
        self.add(self.scrolled_window)

        self.get_apps()
        if len(self.apps_box.get_children()) > 0:
            self.apps_box.get_children()[self.focus_order].set_state_flags(Gtk.StateFlags.PRELIGHT, True)
            self.scrolled_window.get_vadjustment().set_value(self.apps_box.get_children()[self.focus_order].get_allocation().y)
        self.entry.grab_focus()
        self.entry.set_position(self.entry.get_position())

    def scroll_to_button(self, *args):
        scrolled_vadj = self.scrolled_window.get_vadjustment()
        scrolled_alloc = self.scrolled_window.get_allocation()
        button_alloc = self.apps_box.get_children()[self.focus_order].get_allocation()
        if (scrolled_alloc.height + int(scrolled_vadj.get_value())) < (button_alloc.height + button_alloc.y):
            scrolled_vadj.set_value((button_alloc.height + button_alloc.y) - scrolled_alloc.height)
        elif (button_alloc.height + button_alloc.y) - scrolled_vadj.get_value() < button_alloc.height:
            scrolled_vadj.set_value(button_alloc.y)

    def on_entry_changed(self, *args):
        if len(self.apps_box.get_children()) > 0:
            self.apps_box.get_children()[self.focus_order].set_state_flags(Gtk.StateFlags.NORMAL, True)
        self.focus_order = 0
        self.get_apps(self.entry.get_text())
        if len(self.apps_box.get_children()) > 0:
            self.apps_box.get_children()[self.focus_order].set_state_flags(Gtk.StateFlags.PRELIGHT, True)
            self.scroll_to_button()
        return True

    def on_key_press(self, widget, event, *args):
        if event.keyval == 65293: # 65293 is Enter key in Gtk
            if len(self.apps_box.get_children()) > 0:
                self.apps_box.get_children()[self.focus_order].emit("clicked")
        elif event.keyval == 65364: # 65364 is down arrow
            if self.focus_order <= len(self.apps_box.get_children())-2 and len(self.apps_box.get_children()) > 0:
                self.apps_box.get_children()[self.focus_order].set_state_flags(Gtk.StateFlags.NORMAL, True)
                self.focus_order+=1
                self.apps_box.get_children()[self.focus_order].set_state_flags(Gtk.StateFlags.PRELIGHT, True)
                self.scroll_to_button()
            self.entry.grab_focus()
            self.entry.set_position(self.entry.get_position())
            return True
        elif event.keyval == 65362: # 65362 is up arrow
            if self.focus_order > 0:
                self.apps_box.get_children()[self.focus_order].set_state_flags(Gtk.StateFlags.NORMAL, True)
                self.focus_order-=1
                self.apps_box.get_children()[self.focus_order].set_state_flags(Gtk.StateFlags.PRELIGHT, True)
                self.scroll_to_button()
            self.entry.grab_focus()
            self.entry.set_position(self.entry.get_position())
            return True
        elif event.keyval == Gdk.KEY_Escape:
            self.apps_box.get_children()[self.focus_order].set_state_flags(Gtk.StateFlags.NORMAL, True)
            self.focus_order = 0
            self.apps_box.get_children()[self.focus_order].set_state_flags(Gtk.StateFlags.PRELIGHT, True)
            self.entry.set_text("")
            self.get_parent().hide()

    def get_apps(self, search_string=None):
        def launch_app(widget, app, *args):
            app.launch()
            self.entry.set_text("")
            self.get_parent().hide()

        for child in self.apps_box.get_children():
            child.destroy()

        if search_string is not None and len(search_string) > 0:
            apps = Apps.Apps(
                show_hidden=False,
                min_score=4
            ).fuzzy_query(search_string)
        else:
            apps = Apps.Apps().get_list()

        for app in apps:
            app_button = Astal.Button(hexpand=True, vexpand=False, visible=True)
            app_button.connect("clicked", launch_app, app)
            app_box = Gtk.Box(hexpand=True, vexpand=False, spacing=4, visible=True)

            app_icon = Astal.Icon(icon=app.get_icon_name(), hexpand=False, vexpand=True, valign=Gtk.Align.FILL, visible=True)
            app_label = Astal.Label(label=app.get_name(), hexpand=True, vexpand=True, halign=Gtk.Align.START, visible=True)

            app_box.add(app_icon)
            app_box.add(app_label)

            Astal.widget_set_class_names(app_button, ["app-button"])

            app_button.add(app_box)
            self.apps_box.add(app_button)

class AppsWindow(Astal.Window):
    def __init__(self, monitor: Gdk.Monitor) -> None:
        super().__init__(
            anchor=Astal.WindowAnchor.BOTTOM
            | Astal.WindowAnchor.LEFT,
            gdkmonitor=monitor,
            exclusivity=Astal.Exclusivity.NORMAL,
            keymode=Astal.Keymode.EXCLUSIVE,
            layer=Astal.Layer.TOP,
            margin=4,
            name="apps"
        )

        Astal.widget_set_class_names(self, ["AppsWindow"])

        self.add(AppsBox())
        self.hide()
