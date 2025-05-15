import gi

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

from ignis.widgets import Widget
from ignis.services.system_tray import SystemTrayService

tray = SystemTrayService.get_default()

class Tray(Widget.Box):
    def __init__(self):
        super().__init__(
            setup=lambda self: self.tray_setup(),
            vertical=True,
            child=[]
        )

    def tray_item(self, item):
        if item.menu:
            menu = item.menu.copy()
            menu.set_has_arrow(False)
            menu.set_position(Gtk.PositionType.RIGHT)
        else:
            menu = None

        return Widget.Button(
            halign='center',
            child=Widget.Box(
                halign='center',
                child=[
                    Widget.Icon(
                        halign='center',
                        image=item.bind("icon"),
                        pixel_size=18
                    ),
                    menu,
                ]
            ),
            setup=lambda self: item.connect("removed", lambda x: self.unparent()),
            tooltip_text=item.bind("tooltip"),
            on_click=lambda x: menu.popup() if menu else None,
            on_right_click=lambda x: menu.popup() if menu else None,
            css_classes=["tray-item"],
        )

    def tray_setup(self, *_):
        for item in tray.get_items():
            self.prepend(self.tray_item(item))

        tray.connect(
            'added',
            lambda _, item: self.prepend(self.tray_item(item))
        )
