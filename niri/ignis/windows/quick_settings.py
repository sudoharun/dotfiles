from ignis import widgets
from ignis import utils
from ignis.services.audio import AudioService
from ignis.services.backlight import BacklightService
from ignis.services.network import NetworkService
import asyncio

audio = AudioService.get_default()
backlight = BacklightService.get_default()
network = NetworkService.get_default()

def powermenu():
    return widgets.Box(
        vertical=True,
        child=[
            widgets.Button(
                child=widgets.Box(child=[
                    widgets.Icon(image="lock-symbolic"),
                    widgets.Label(label="Lock", hexpand=True, justify="right")
                ]),
                on_click=lambda _: asyncio.create_task(utils.exec_sh_async("pidof swaylock || swaylock"))
            ),
            widgets.Button(
                child=widgets.Box(child=[
                    widgets.Icon(image="system-suspend-symbolic"),
                    widgets.Label(label="Suspend", hexpand=True, justify="right")
                ]),
                on_click=lambda _: asyncio.create_task(utils.exec_sh_async("systemctl suspend"))
            ),
            widgets.Button(
                child=widgets.Box(child=[
                    widgets.Icon(image="system-log-out-symbolic"),
                    widgets.Label(label="Log Out", hexpand=True, justify="right")
                ]),
                on_click=lambda _: asyncio.create_task(utils.exec_sh_async("niri msg action quit"))
            ),
            widgets.Button(
                child=widgets.Box(child=[
                    widgets.Icon(image="system-reboot-symbolic"),
                    widgets.Label(label="Reboot", hexpand=True, justify="right")
                ]),
                on_click=lambda _: asyncio.create_task(utils.exec_sh_async("systemctl reboot"))
            ),
            widgets.Button(
                child=widgets.Box(child=[
                    widgets.Icon(image="system-shutdown-symbolic"),
                    widgets.Label(label="Shutdown", hexpand=True, justify="right")
                ]),
                on_click=lambda _: asyncio.create_task(utils.exec_sh_async("systemctl poweroff"))
            ),
        ]
    )

def slider_template(image, scale_value, button_func, scale_func):
    return widgets.Box(
        css_classes=[],
        child=[
            widgets.Button(
                child=widgets.Icon(image=image, pixel_size=24),
                on_click=lambda *_: button_func()
            ),
            widgets.Scale(
                vertical=False,
                hexpand=True,
                min=0,
                max=100,
                step=1,
                value=scale_value,
                on_change=lambda val: scale_func(val.value)
            )
        ]
    )

def sliders():
    return widgets.Box(
        vertical=True,
        child=[
            slider_template(
                audio.speaker.bind("icon-name"),
                audio.speaker.bind("volume"),
                lambda: audio.speaker.set_is_muted(not audio.speaker.get_is_muted()),
                lambda value: audio.speaker.set_volume(value)
            ),
            slider_template(
                "brightness-symbolic",
                backlight.bind(
                    "brightness",
                    transform=lambda val: float(val) / backlight.max_brightness * 100
                ),
                None,
                lambda value: asyncio.create_task(backlight.set_brightness_async(value * backlight.max_brightness / 100))
            )
        ]
    )

def controls_button_template(icon, label, button_func, visibility, target_stack=None):
    return widgets.Button(
        visible=visibility,
        child=widgets.Box(child=[
            widgets.Icon(image=icon, pixel_size=24),
            widgets.Label(label=label, ellipsize="end", hexpand=True, halign="center"),
            widgets.Icon(image="arrow-right", pixel_size=24) if target_stack else None
        ]),
        on_click=lambda widget: button_func(widget)
    )

def controls_grid():
    return widgets.Grid(
        column_num=2,
        column_homogeneous=True,
        row_spacing=8,
        column_spacing=8,
        hexpand=True,
        child=[
            controls_button_template(
                network.wifi.bind("icon-name"),
                network.wifi.devices[-1].ap.bind("ssid"),
                lambda *_: print(),
                network.wifi.bind("is-connected"),
                # Add stack to switch to
            ),
            controls_button_template(
                network.ethernet.bind("icon-name"),
                "Connected",
                lambda *_: print(),
                network.ethernet.bind("is-connected")
            ),
        ]
    )

def QuickSettings(output_id):
    window = widgets.Window(
        namespace=f"ignis-quick-settings-{output_id}",
        monitor=output_id,
        anchor=["bottom", "right"],
        exclusivity="normal",
        visible=False,
        popup=True,
        child=widgets.Box(
            spacing=4,
            vertical=True,
            child=[
                controls_grid(),
                sliders(),
                powermenu()
            ]
        ),
        css_classes=['notifications-quick-settings-window'],
        margin_bottom=8,
        margin_right=8
    )
    window.set_size_request(350, -1)

    return window
