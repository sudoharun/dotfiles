import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')
from gi.repository import Gtk, Gdk

from ignis.widgets import Widget
from ignis.services.applications import ApplicationsService
from rapidfuzz import fuzz

applications = ApplicationsService.get_default()

class AppEntry(Gtk.ListBoxRow):
    def __init__(self, app):
        super().__init__(
            css_classes=['apps-entry']
        )
        self.app = app
        self.set_child(
            Widget.Box(
                spacing=4,
                child=[
                    Widget.Icon(
                        image=app.icon
                        or 'application-default-icon',
                    ),
                    Widget.Label(
                        label=app.name
                    )
                ]
            )
        )
        self.connect(
            'activate',
            lambda *_: self.app.launch()
        )

class AppsLauncherContainer(Widget.Box):
    def __init__(self):
        super().__init__(
            vertical=True,
            css_classes=['apps-launcher-container']
        )

        self.search_bar = Widget.Entry(
            placeholder_text='Search applications...',
            primary_icon_name='system-search-symbolic',
            on_accept=lambda *_: self.activate_search(),
            on_change=lambda *_: self.initiate_search(),
            css_classes=['apps-launcher-search-bar']
        )
        self.apps_list = Widget.ListBox(
            activate_on_single_click=False,
            selection_mode='browse',
            css_classes=['apps-list']
        )

        self.search_bar.event_key_controller = Gtk.EventControllerKey.new()
        self.search_bar.add_controller(self.search_bar.event_key_controller)
        self.search_bar.event_key_controller.connect(
            'key-pressed',
            self.search_bar_key_event_handler
        )

        self.child = [
            self.search_bar,
            Widget.Scroll(
                vexpand=True,
                overlay_scrolling=False,
                child=self.apps_list
            )
        ]

        def filter_func(row):
            search_string = self.search_bar.get_text().lower()
            fuzzy_ratio = fuzz.partial_ratio(search_string, row.app.name.lower())
            if len(search_string) == 0:
                return True
            elif len(search_string) < 4:
                return fuzzy_ratio > (50+(len(search_string)*10))
            else:
                return fuzzy_ratio > 80

        def sort_func(row1, row2):
            search_string = self.search_bar.get_text().lower()
            row1_partial = fuzz.partial_ratio(search_string, row1.app.name.lower())
            row2_partial = fuzz.partial_ratio(search_string, row2.app.name.lower())
            if row1_partial == row2_partial:
                if len(row1.get_name().lower()) == len(row2.app.name.lower()):
                    return 0
                elif len(row1.get_name().lower()) < len(row2.app.name.lower()):
                    return -1
                else:
                    return 1
            elif row1_partial > row2_partial:
                return -1
            else:
                return 1

        self.apps_list.set_filter_func(filter_func)
        self.apps_list.set_sort_func(sort_func)

        self.populate_apps_list()
        if self.apps_list.get_row_at_index(0):
            self.apps_list.select_row(self.apps_list.get_row_at_index(0))

    def populate_apps_list(self):
        for app in applications.apps:
            app_entry = AppEntry(app)
            app_entry.event_key_controller = Gtk.EventControllerKey.new()
            app_entry.add_controller(app_entry.event_key_controller)
            app_entry.event_key_controller.connect(
                'key-pressed',
                self.app_entry_key_event_handler
            )
            self.apps_list.append(app_entry)

    def initiate_search(self):
        self.apps_list.invalidate_filter()
        self.apps_list.invalidate_sort()
        if self.apps_list.get_row_at_index(0):
            self.apps_list.select_row(self.apps_list.get_row_at_index(0))

    def activate_search(self):
        if self.apps_list.get_row_at_index(0):
            self.apps_list.get_row_at_index(0).activate()
        self.search_bar.set_text('')
        self.search_bar.grab_focus()
        self.get_parent().set_visible(False)

    def search_bar_key_event_handler(self, widget, keyval, keycode, state):
        if keyval == Gdk.KEY_Down:
            if self.apps_list.get_row_at_index(1):
                self.apps_list.get_row_at_index(1).grab_focus()
                self.apps_list.select_row(self.apps_list.get_row_at_index(1))

        elif keyval == Gdk.KEY_Return:
            self.apps_list.get_selected_row().activate()

    def app_entry_key_event_handler(self, widget, keyval, keycode, state):
        if keyval == Gdk.KEY_Up:
            if widget.get_widget().get_index() == 0:
                self.search_bar.grab_focus()

        elif keyval not in [Gdk.KEY_Down, Gdk.KEY_Return]:
            if self.apps_list.get_row_at_index(0):
                self.apps_list.get_row_at_index(0).grab_focus()
                self.apps_list.select_row(self.apps_list.get_row_at_index(0))
            self.search_bar.set_text(self.search_bar.get_text() + chr(Gdk.keyval_to_unicode(keyval)))
            self.search_bar.grab_focus()
            self.search_bar.set_position(-1)

class AppsLauncher(Widget.Window):
    def __init__(self, monitor):
        super().__init__(
            namespace=f'apps-launcher-{monitor}',
            monitor=monitor,
            anchor=['bottom', 'left'],
            kb_mode='exclusive',
            popup=True,
            visible=False,
            css_classes=['apps-launcher'],
            child=AppsLauncherContainer()
        )
        self.set_size_request(self.child.apps_list.get_preferred_size()[0].width+100, 400)
        self.child.search_bar.grab_focus()
