from gi.repository import Astal, AstalIO, Gtk

class Desktop(Astal.Window):
    def __init__(self, app: Astal.Application) -> None:
        super().__init__(
            anchor=Astal.WindowAnchor.TOP
            | Astal.WindowAnchor.BOTTOM
            | Astal.WindowAnchor.LEFT
            | Astal.WindowAnchor.RIGHT,
            exclusivity=Astal.Exclusivity.NORMAL,
            layer=Astal.Layer.BOTTOM,
            application=app,
            name="desktop"
        )

        self.desktop = Gtk.Box(
            visible=True,
            hexpand=True,
            vexpand=True
        )

        self.add_css_class('desktop-borders')
        self.desktop.add_css_class('desktop')

        self.set_child(self.desktop)
        self.present()

class LeftEdge(Astal.Window):
    def __init__(self, app: Astal.Application) -> None:
        super().__init__(
            anchor=Astal.WindowAnchor.TOP
            | Astal.WindowAnchor.LEFT
            | Astal.WindowAnchor.BOTTOM,
            exclusivity=Astal.Exclusivity.EXCLUSIVE,
            layer=Astal.Layer.BOTTOM,
            application=app,
            name="left-edge"
        )

        self.set_size_request(8, -1)
        self.present()

class RightEdge(Astal.Window):
    def __init__(self, app: Astal.Application) -> None:
        super().__init__(
            anchor=Astal.WindowAnchor.TOP
            | Astal.WindowAnchor.RIGHT
            | Astal.WindowAnchor.BOTTOM,
            exclusivity=Astal.Exclusivity.EXCLUSIVE,
            layer=Astal.Layer.BOTTOM,
            application=app,
            name="right-edge"
        )

        self.set_size_request(8, -1)
        self.present()

class TopEdge(Astal.Window):
    def __init__(self, app: Astal.Application) -> None:
        super().__init__(
            anchor=Astal.WindowAnchor.LEFT
            | Astal.WindowAnchor.TOP
            | Astal.WindowAnchor.RIGHT,
            exclusivity=Astal.Exclusivity.EXCLUSIVE,
            layer=Astal.Layer.BOTTOM,
            application=app,
            name="top-edge"
        )

        self.set_size_request(-1, 8)
        self.present()
