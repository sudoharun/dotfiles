from ignis.widgets import Widget
from ignis.services.niri import NiriService
from ignis.utils import Utils

niri = NiriService.get_default()

class ApplicationButton(Widget.Button):
    def __init__(self, window):
        super().__init__(
            child=Widget.Box(
                vertical=True,
                spacing=2,
                child=[
                    Widget.Icon(
                        vexpand=True,
                        image=Utils.get_app_icon_name(window.app_id)
                        or 'application-default-icon',
                        pixel_size=32
                    ),
                    Widget.Box(
                        hexpand=False,
                        halign='center',
                        css_classes=['window-indicator']
                    )
                ]
            ),
            tooltip_text=window.title,
            on_click=lambda _: self.__on_click(),
            css_classes=[
                'window-button',
                'focused-window-button'
                if window.is_focused else '']
            )

        self.id = window.id

    def __on_click(self):
        Utils.exec_sh(f'niri msg action focus-window --id {self.id}')

class DockContainer(Widget.EventBox):
    def __init__(self):
        super().__init__(
            hexpand=True,
            vexpand=True,
            spacing=2,
            css_classes=['dock'],
            on_hover_lost=lambda *_: self.on_focus_lost()
        )

        niri.connect(
            'notify::windows',
            lambda *_: self.on_any_change()
        )
        niri.connect(
            'notify::active-workspaces',
            lambda *_: self.on_any_change()
        )
        niri.connect(
            'notify::active-window',
            lambda *_: self.on_any_change()
        )

        self.connect(
            'notify::visible',
            lambda obj, _: self.set_timeout_if_not_focused()
        )

    def on_any_change(self):
        self.child = []

        windows = {}
        for window in niri.windows:
            if window.workspace_id == niri.active_window.workspace_id:
                windows[window.id] = window

        windows = dict(sorted(windows.items(), key=lambda item: item[0]))

        for id, window in windows.items():
            self.append(ApplicationButton(window))

        if len(self.child) < 1:
            self.append(Widget.Button(
                child=Widget.Icon(
                    image='desktop',
                    pixel_size=32
                )
            ))

    def on_focus_lost(self):
        self.get_parent().set_visible(False)

class Dock(Widget.Window):
    def __init__(self, monitor):
        super().__init__(
            namespace=f'dock-{monitor}',
            exclusivity="normal",
            anchor=["bottom"],
            monitor=monitor,
            visible=False,
            css_classes=['dock'],
            child=DockContainer()
        )
        self.set_size_request(-1, 40)

        self.timeout = None
        self.set_timeout_if_not_focused()
        self.connect(
            'notify::visible',
            lambda obj, _: self.set_timeout_if_not_focused()
        )
        self.child.on_hover = lambda *_: self.timeout.cancel()

    def set_timeout_if_not_focused(self):
        if self.timeout:
            self.timeout.cancel()

        self.timeout = Utils.Timeout(
            ms=1000,
            target=lambda: self.set_visible(False)
        )
