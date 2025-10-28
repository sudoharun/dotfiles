from ignis import widgets
from ignis import utils
from ignis.services.backlight import BacklightService
from ignis.services.audio import AudioService

backlight = BacklightService.get_default()
audio = AudioService.get_default()

def osd_template(image, scale_value, connector_func):
    box = widgets.Box(
        css_classes=["osd"],
        visible=False,
        child=[
            widgets.Icon(image=image, pixel_size=24),
            widgets.Scale(
                vertical=False,
                hexpand=True,
                min=0,
                max=100,
                value=scale_value
            )
        ]
    )
    box.timeout = None
    connector_func(box)

    return box

def RootOSDWindow(output_id):
    def timeout_func(widget):
        if widget.timeout:
            widget.timeout.cancel()

        widget.set_visible(True)
        widget.timeout = utils.Timeout(
            ms=3000,
            target=lambda: widget.set_visible(False)
        )

    def set_visibility_based_on_children(widget):
        visible_children = [child for child in widget.child if child.get_visible()]
        if len(visible_children) == 0 and window.get_visible():
            window.set_visible(False)
        elif len(visible_children) > 0 and not window.get_visible():
            window.set_visible(True)

    box = widgets.Box(
        vertical=True,
        spacing=8,
        child=[
            osd_template(
                audio.speaker.bind("icon-name"),
                audio.speaker.bind("volume"),
                lambda widget: audio.speaker.connect("notify::volume", lambda *_: timeout_func(widget))
            ),
            osd_template(
                "brightness-symbolic",
                backlight.bind(
                    "brightness",
                    transform=lambda val: float(val) / backlight.max_brightness * 100
                ),
                lambda widget: backlight.connect("notify::brightness", lambda *_: timeout_func(widget))
            )
        ]
    )

    window = widgets.Window(
        namespace=f"ignis-osd-{output_id}",
        monitor=output_id,
        layer="overlay",
        anchor=["bottom"],
        exclusivity="normal",
        margin_bottom=8,
        visible=False,
        child=box,
        css_classes=['osd-window']
    )
    window.set_size_request(300, -1)

    for child in box.child:  # Use box.child (Ignis list) instead of get_child()
        child.connect(
            'notify::visible',
            lambda *_: set_visibility_based_on_children(box)
        )

    return window
