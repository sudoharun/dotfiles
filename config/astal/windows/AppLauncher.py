from gi.repository import (
    Gtk,
    Gdk,
    Astal,
    AstalApps as Apps
)
from .widgets.App import AppEntry
from rapidfuzz import fuzz

class SearchBar(Gtk.Entry):
    def __init__(self) -> None:
        super().__init__()

        self.set_icon_from_icon_name(Gtk.EntryIconPosition.PRIMARY, 'system-search-symbolic')
        self.set_placeholder_text('Search Applications...')

class AppsList(Gtk.ListBox):
    def __init__(self, requested_apps: list=[]) -> None:
        super().__init__()

        apps = Apps.Apps(
            show_hidden=False
        )

        self.apps = apps.get_list()
        apps.connect('notify::list', self.populate_entries)

        self.populate_entries()

    def populate_entries(self, *_):
        child = self.get_first_child()
        while child is not None:
            child.unparent()
            child = child.get_next_sibling()

        for app in self.apps:
            app_entry = AppEntry(app)
            app_entry.add_css_class('app-entry')
            self.append(app_entry)

class AppLauncher(Astal.Window):
    def __init__(self, app: Astal.Application) -> None:
        super().__init__(
            anchor=Astal.WindowAnchor.BOTTOM
            | Astal.WindowAnchor.LEFT,
            exclusivity=Astal.Exclusivity.NORMAL,
            layer=Astal.Layer.TOP,
            keymode=Astal.Keymode.EXCLUSIVE,
            application=app,
            name='app-launcher'
        )

        self.set_size_request(375, 425)
        self.add_css_class('app-launcher')

        self.box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL
        )
        self.box.add_css_class('app-launcher')
        self.set_child(self.box)

        self.search_bar = SearchBar()
        self.search_bar.add_css_class('app-search')

        self.apps = AppsList()
        self.apps.add_css_class('apps-list')
        self.apps.set_activate_on_single_click(True)

        self.scrolled_apps = Gtk.ScrolledWindow(
            vexpand=True
        )
        self.scrolled_apps.set_child(self.apps)
        self.scrolled_apps.add_css_class('apps-scrolled-window')

        self.box.append(self.search_bar)
        self.box.append(self.scrolled_apps)

        def filter_func(row):
            search_string = self.search_bar.get_text().lower()
            fuzzy_ratio = fuzz.partial_ratio(search_string, row.get_name().lower())
            if len(search_string) == 0:
                return True
            elif len(search_string) < 4:
                return fuzzy_ratio > 25
            else:
                return fuzzy_ratio > 70

        def sort_func(row1, row2):
            search_string = self.search_bar.get_text().lower()
            row1_ratio = fuzz.ratio(search_string, row1.get_name().lower())
            row2_ratio = fuzz.ratio(search_string, row2.get_name().lower())
            if row1_ratio == row2_ratio:
                return 0
            elif row1_ratio > row2_ratio:
                return -1
            else:
                return 1

        self.apps.set_filter_func(filter_func)
        self.apps.set_sort_func(sort_func)

        self.apps_controller = Gtk.EventControllerKey.new()
        self.apps.add_controller(self.apps_controller)
        self.apps_controller.connect('key-pressed', self.on_apps_key_press)
        self.apps.connect('row-activated', lambda *_: self.set_visible(False))

        self.search_bar_controller = Gtk.EventControllerKey.new()
        self.search_bar.add_controller(self.search_bar_controller)
        self.search_bar_controller.connect('key-pressed', self.on_search_key_press)
        self.search_bar.connect('activate', self.on_search_activate)
        self.search_bar.connect('changed', self.on_search_entry_changed)

        self.connect('notify::visible', self.on_visibility_changed)
        self.set_visible(False)

    def on_apps_key_press(self, widget, keyval, keycode, *_):
        if keyval == Gdk.KEY_Up:
            if not self.apps.get_selected_row() or not self.apps.get_row_at_index(self.apps.get_selected_row().get_index()-1):
                self.search_bar.grab_focus()

        if keyval == Gdk.KEY_Escape:
            self.set_visible(False)

    def on_visibility_changed(self, *_):
        if self.get_visible():
            if self.apps.get_row_at_index(0):
                self.apps.select_row(self.apps.get_row_at_index(0))
            self.search_bar.set_text('')
            self.search_bar.grab_focus()

    def on_search_key_press(self, widget, keyval, keycode, *_):
        if keyval == Gdk.KEY_Down:
            if self.apps.get_row_at_index(1):
                self.apps.get_row_at_index(1).grab_focus()
                self.apps.select_row(self.apps.get_row_at_index(1))
            elif self.apps.get_row_at_index(0):
                self.apps.get_row_at_index(0).grab_focus()
                self.apps.select_row(self.apps.get_row_at_index(0))

        if keyval == Gdk.KEY_Escape:
            self.set_visible(False)

    def on_search_entry_changed(self, *_):
        self.apps.invalidate_filter()
        self.apps.invalidate_sort()
        self.apps.select_row(self.apps.get_row_at_index(0))

    def on_search_activate(self, *_):
        if self.apps.get_row_at_index(0):
            self.apps.get_row_at_index(0).emit('activate')
