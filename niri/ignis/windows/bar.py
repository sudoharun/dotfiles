from ignis import widgets
from ignis import utils
from ignis.window_manager import WindowManager
from ignis.services.niri import NiriService
from ignis.services.network import NetworkService
from ignis.services.audio import AudioService
from ignis.services.upower import UPowerService
from ignis.services.system_tray import SystemTrayService, SystemTrayItem
from datetime import datetime

window_manager = WindowManager.get_default()
niri = NiriService.get_default()
network = NetworkService.get_default()
audio = AudioService.get_default()
upower = UPowerService.get_default()
system_tray = SystemTrayService.get_default()

"""
Workspaces
"""

def workspace_button(ws_info):
    return widgets.Button(
        child=widgets.Label(label=str(ws_info.idx)),
        on_click=lambda *_: niri.switch_to_workspace_by_id(ws_info.id),
        css_classes=[
            "workspace-button",
            "active-workspace" if ws_info.is_active
            else "inactive-workspace"
        ]
    )

def per_output_workspaces(output_connector):
    return widgets.Box(
        spacing=4,
        css_classes=["workspaces"],
        child=niri.bind(
            "workspaces",
            transform=lambda workspaces: [
                workspace_button(ws)
                for ws in workspaces or []
                if ws.output == output_connector
            ]
        )
    )

def workspaces():
    return widgets.Box(
        spacing=8,
        child=[
            per_output_workspaces(monitor.get_connector())
            for monitor in utils.get_monitors()
        ]
    )

"""
Open windows
"""

def window_button(app):
    return widgets.Button(
        child=widgets.Icon(
            image=utils.get_app_icon_name(app.app_id)
            or 'application-default-icon'
        ),
        on_click=lambda *_: app.focus(),
        tooltip_text=app.title,
        css_classes=niri.active_window.bind(
            "id",
            transform=lambda value: [
                "window-button",
                "active-window-button" if value == app.id else "inactive-window-button"
            ]
        )
    )

def open_tiled_windows():
    def _setup(widget):
        def set_windows():
            widget.child = [
                window_button(window)
                for window in sorted(
                    niri.windows,
                    key=lambda win: 0 if win.is_floating else (
                        win.layout.pos_in_scrolling_layout[0]
                        if win.layout and hasattr(win.layout, 'pos_in_scrolling_layout')
                        and win.layout.pos_in_scrolling_layout
                        else -1
                    ))
                if niri.get_workspace_by_id(window.workspace_id) is not None
                and niri.get_workspace_by_id(window.workspace_id).is_focused
                and not window.is_floating
            ]

        widget.connect("notify::child", lambda *_: widget.set_visible(True)
            if len(widget.child) > 0 else widget.set_visible(False)
        )
        niri.connect("notify::workspaces", lambda *_: set_windows())

    return widgets.Box(
        setup=lambda self: _setup(self),
        spacing=4,
        css_classes=["window-buttons", "tiling-window-buttons"],
        child=niri.bind(
            "windows",
            transform=lambda windows: [
                window_button(window)
                for window in sorted(
                    windows,
                    key=lambda win: 0 if win.is_floating else (
                        win.layout.pos_in_scrolling_layout[0]
                        if win.layout and hasattr(win.layout, 'pos_in_scrolling_layout')
                        and win.layout.pos_in_scrolling_layout
                        else -1
                    ))
                if niri.get_workspace_by_id(window.workspace_id) is not None
                and niri.get_workspace_by_id(window.workspace_id).is_focused
                and not window.is_floating
            ]
        )
    )

def open_floating_windows():
    def _setup(widget):
        def set_windows():
            widget.child = [
                window_button(window)
                for window in niri.windows
                if niri.get_workspace_by_id(window.workspace_id) is not None
                and niri.get_workspace_by_id(window.workspace_id).is_focused
                and window.is_floating
            ]

        widget.connect("notify::child", lambda *_: widget.set_visible(True)
            if len(widget.child) > 0 else widget.set_visible(False)
        )
        niri.connect("notify::workspaces", lambda *_: set_windows())

    return widgets.Box(
        setup=lambda self: _setup(self),
        spacing=4,
        css_classes=["window-buttons", "floating-window-buttons"],
        child=niri.bind(
            "windows",
            transform=lambda windows: [
                window_button(window)
                for window in windows
                if niri.get_workspace_by_id(window.workspace_id) is not None
                and niri.get_workspace_by_id(window.workspace_id).is_focused
                and window.is_floating
            ]
        )
    )

"""
System Tray
"""

def tray_item(item: SystemTrayItem) -> widgets.Button:
    if item.menu:
        menu = item.menu.copy()
    else:
        menu = None

    return widgets.Button(
        child=widgets.Box(
            child=[
                widgets.Icon(image=item.bind("icon"), pixel_size=24),
                menu,
            ]
        ),
        setup=lambda self: item.connect("removed", lambda x: self.unparent()),
        tooltip_text=item.bind("tooltip"),
        on_click=lambda x: item.activate() if item else None,
        on_right_click=lambda x: menu.popup() if menu else None,
        css_classes=["tray-item"],
    )


def tray():
    def setup(widget):
        for item in system_tray.get_items():
            widget.prepend(widget.tray_item(item))

        system_tray.connect(
            'added',
            lambda _, item: widget.prepend(tray_item(item))
        )

    return widgets.Box(
        setup=lambda self: setup(self),
        spacing=2,
    )

"""
System Controls
"""

def notification_icon():
    return widgets.Icon()

def wifi_icon():
    return widgets.Icon(
        image=network.wifi.bind("icon-name"),
        visible=network.wifi.bind("enabled")
    )

def ethernet_icon():
    return widgets.Icon(
        image=network.ethernet.bind("icon-name"),
        visible=network.ethernet.bind("is-connected")
    )

def bluetooth_icon():
    pass

def audio_icon():
    return widgets.Icon(
        image=audio.speaker.bind("icon-name"),
        tooltip_text=audio.speaker.bind('volume', transform=lambda val: f"{val}%")
    )

def battery_icon():
    return widgets.Icon(
        image=upower.batteries[0].bind("icon-name"),
        tooltip_text=upower.batteries[0].bind("percent", transform=lambda val: f"{val}%")
    )

def system_controls(output_id):
    return widgets.Button(
        css_classes=["system-controls-applet"],
        child=widgets.Box(
            spacing=8,
            child=[
                ethernet_icon(),
                wifi_icon(),
                audio_icon(),
                battery_icon()
            ]
        ),
        on_click=lambda *_: window_manager.get_window(f"ignis-quick-settings-{output_id}").set_visible(
            not window_manager.get_window(f"ignis-quick-settings-{output_id}").get_visible()
        )
    )

def clock(output_id):
    date_time = widgets.Button(
        css_classes=["clock-applet"],
        child=widgets.Label(
            label=datetime.now().strftime("%H:%M%n%a %d %b %Y"),
            justify="right"
        ),
        on_click=lambda *_: window_manager.get_window(f"ignis-notifications-centre-{output_id}").set_visible(
            not window_manager.get_window(f"ignis-notifications-centre-{output_id}").get_visible()
        )
    )

    utils.Poll(
        timeout=1_000,
        callback=lambda _: date_time.child.set_label(
            datetime.now().strftime("%H:%M%n%a %d %b %Y")
        )
    )
    return date_time

"""
Bar
"""

def Bar(output_id):
    return widgets.Window(
        namespace=f"ignis-bar-{output_id}",
        monitor=output_id,
        anchor=["left", "bottom", "right"],
        # layer="bottom",
        exclusivity="exclusive",
        child=widgets.CenterBox(
            css_classes=["bar"],
            start_widget=workspaces(),
            center_widget=widgets.Box(
                spacing=8,
                child=[open_tiled_windows(), open_floating_windows()]
            ),
            end_widget=widgets.Box(
                spacing=8,
                child=[tray(), system_controls(output_id), clock(output_id)]
            )
        )
    )
