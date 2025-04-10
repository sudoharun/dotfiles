from ignis.widgets import Widget

from .widgets import AudioOSD, BacklightOSD

class OSDContainer(Widget.Box):
    def __init__(self):
        super().__init__(
            vertical=True,
            spacing=8,
            css_classes=['osd-container'],
            child=[
                AudioOSD(),
                BacklightOSD(),
            ]
        )

        for child in self.child:
            child.connect(
                'notify::visible',
                lambda *_: self.set_visibility_based_on_children()
            )
            child.css_classes = ['osd']

    def set_visibility_based_on_children(self):
        visible_children = [child for child in self.child if child.get_visible()]
        if len(visible_children) == 0 and self.get_visible():
            self.set_visible(False)
        elif not self.get_visible():
            self.set_visible(True)

class OSDWindow(Widget.Window):
    def __init__(self, monitor):
        super().__init__(
            namespace=f'osd-window-{monitor}',
            monitor=monitor,
            layer='overlay',
            anchor=['bottom'],
            kb_mode='none',
            margin_bottom=64,
            css_classes=['osd-window'],
            child=OSDContainer()
        )
        self.set_size_request(225, -1)
        self.child.connect(
            'notify::visible',
            lambda *_: self.set_visibility_based_on_child()
        )

    def set_visibility_based_on_child(self):
        self.set_visible(self.child.get_visible())
