import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
from gi.repository import Gtk, Gdk

from ignis import widgets
from ignis import utils
from ignis.services.applications import ApplicationsService

apps = ApplicationsService.get_default()

def activate_app(widget, app=None):
    if type(widget) == widgets.Button:
        app.launch() if app else None
        entry = widget.get_parent().get_parent().child[0]
        entry.text = ""
        widget.get_root().visible = False
    elif type(widget) == widgets.Entry:
        sibling = widget.get_parent().child[-1]
        if len(sibling.child) > 0:
            sibling.child[0].emit("clicked")

def app_entry(app):
    return widgets.Button(
        child=widgets.Box(
            child=[
                widgets.Icon(image=app.icon or 'application-default-icon'),
                widgets.Label(label=app.name)
            ]
        ),
        on_click=lambda widget: activate_app(widget, app),
        css_classes=['apps-entry']
    )

def launcher():
    apps_list = widgets.Box(
        vertical=True,
        child=[app_entry(app) for app in apps.apps[:3]],
        css_classes=['apps-launcher-container']
    )

    @utils.debounce(50)
    def update_list(text):
        apps_list.visible = False
        apps_list.child = [app_entry(app) for app in apps.search(apps.apps, text)[:3]]
        if len(text) == 0:
            apps_list.child = [app_entry(app) for app in apps.apps[:3]]
        elif len(apps_list.child) == 0:
            apps_list.child = [widgets.Box(vertical=True, child=[widgets.Label(label="No Results!")])]
        apps_list.visible = True

    search_bar_inst = widgets.Entry(
        placeholder_text="Search applications...",
        on_change=lambda widget: update_list(widget.text),
        on_accept=lambda widget: activate_app(widget)
    )

    def on_key_pressed(controller, keyval, keycode, state):
        if keyval == Gdk.KEY_Down:
            if len(apps_list.child) > 1 and isinstance(apps_list.child[1], widgets.Button):
                apps_list.child[1].grab_focus()
            elif len(apps_list.child) > 0 and isinstance(apps_list.child[0], widgets.Button):
                apps_list.child[0].grab_focus()
            return True
        return False

    key_controller = Gtk.EventControllerKey.new()
    key_controller.connect("key-pressed", on_key_pressed)
    search_bar_inst.add_controller(key_controller)

    return widgets.Box(
        vertical=True,
        spacing=4,
        child=[search_bar_inst, apps_list]
    )

def Launcher(output_id):
    window = widgets.Window(
        namespace=f"ignis-apps-launcher-{output_id}",
        monitor=output_id,
        anchor=[],
        exclusivity="normal",
        popup=True,
        kb_mode="exclusive",
        visible=False,
        child=launcher(),
        css_classes=['apps-launcher']
    )

    def focus_search_entry():
        search_entry = window.child.child[0]
        search_entry.set_text("")
        search_entry.set_position(-1)
        search_entry.grab_focus()
        return False

    window.set_size_request(500, -1)
    window.connect("notify::visible", lambda *_: focus_search_entry())

    # from gi.repository import GLib
    # GLib.idle_add(focus_search_entry)

    return window
