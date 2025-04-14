from ignis.widgets import Widget
from ignis.services.niri import NiriService
from ignis.app import IgnisApp

app = IgnisApp.get_default()
niri = NiriService.get_default()

class ActivatorContainer(Widget.EventBox):
    def __init__(self, parent_namespace):
        super().__init__(
            on_hover=lambda _: self.on_focused()
        )

        self.parent_namespace = parent_namespace

        niri.connect(
            'notify::windows',
            lambda *_: self.adapt_width()
        )
        app.get_window(f"dock-{self.parent_namespace[-1]}").connect(
            'notify::visible',
            lambda obj, _: self.get_parent().set_visible(not obj.get_property('visible'))
        )

    def on_focused(self):
        app.toggle_window(self.parent_namespace)
        app.get_window(f"dock-{self.parent_namespace[-1]}").set_visible(True)

    def adapt_width(self):
        self.set_size_request(
            app.get_window(
                f"dock-{self.parent_namespace[-1]}"
            ).get_preferred_size()[0].width,
            4
        )

class DockActivator(Widget.Window):
    def __init__(self, monitor):
        super().__init__(
            namespace=f'dock-activator-{monitor}',
            monitor=monitor,
            exclusivity="normal",
            anchor=["bottom"],
            css_classes=['dock-activator']
        )

        self.child = ActivatorContainer(self.get_namespace())
