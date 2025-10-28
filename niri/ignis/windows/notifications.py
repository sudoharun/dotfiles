from ignis import widgets
from ignis import utils
from ignis.window_manager import WindowManager
from ignis.services.notifications import NotificationService
from datetime import datetime

window_manager = WindowManager.get_default()
notifications = NotificationService.get_default()

def notification(info, popup=False):
    def on_action_clicked(info, action):
        action.invoke()
        info.close()

    def _setup(widget):
        # idk why widget.unparent() doesn't work
        timeout = utils.Timeout(ms=info.timeout, target=lambda *_: widget.get_parent().remove(widget)) if popup else None
        info.connect('closed', lambda *_: timeout.cancel() if timeout else None)
        info.connect('closed', lambda *_: widget.get_parent().remove(widget) if widget.get_parent() else None)

    return widgets.Box(
        setup=lambda self: _setup(self),
        vertical=True,
        css_classes=["notification"],
        child=[
            widgets.Box(
                hexpand=True,
                spacing=8,
                child=[
                    widgets.Icon(
                        image=info.icon.replace("file://", "").replace("%20", " ")
                        if info.icon else 'application-default-icon',
                        halign="start",
                        hexpand=True if not info.app_name else False,
                        css_classes=["notification-app-icon"]
                    ),
                    widgets.Label(
                        label=info.app_name,
                        css_classes=["notification-app-name"],
                        hexpand=True,
                        halign="start",
                        ellipsize="end"
                    ) if info.app_name else None,
                    widgets.Label(
                        label=datetime.fromtimestamp(info.time).strftime('%H:%M')
                    ),
                    widgets.Button(
                        on_click=lambda *_: info.close(),
                        child=widgets.Icon(image="dialog-close"),
                        css_classes=["notification-close-button"],
                        halign="end"
                    )
                ]
            ),
            widgets.Box(
                vertical=True,
                spacing=4,
                child=[
                    widgets.Label(
                        label=info.summary,
                        css_classes=["notification-summary"],
                        xalign=0,
                        ellipsize="end"
                    ) if info.summary else None,
                    widgets.Label(
                        label=info.body.replace("\n", " ") if popup else info.body,
                        css_classes=["notification-body"],
                        wrap=True,
                        wrap_mode='word',
                        lines=4 if popup else -1,
                        xalign=0,
                        ellipsize="end" if popup else "none"
                    ) if info.body else None,
                    widgets.Box(
                        visible=True if len(info.actions) > 0 else False,
                        spacing=4,
                        child=[
                            widgets.Button(
                                hexpand=True,
                                label=action.label,
                                css_classes=["notification-action"],
                                on_click=lambda *_: on_action_clicked(info, action)
                            ) for action in info.actions
                        ]
                    )
                ]
            )
        ]
    )

def NotificationsPopups(output_id):
    def _setup(widget):
        def hide_func():
            if (
                len(widget.get_child()) > 0
                and not window_manager.get_window(f"ignis-notifications-centre-{output_id}").get_visible()
            ):
                widget.get_root().set_visible(True)
            else:
                widget.get_root().set_visible(False)

        # try add limit in future
        notifications.connect(
            "new-popup",
            lambda _, info: widget.prepend(notification(info, True))
        )

        # prevents "ghost" widgets
        widget.connect(
            "notify::child",
            lambda *_: hide_func()
        )

        window_manager.get_window(f"ignis-notifications-centre-{output_id}").connect(
            "notify::visible",
            lambda *_: hide_func()
        )

    box = widgets.Box(
        setup=lambda self: _setup(self),
        spacing=4,
        vertical=True,
        css_classes=["notifications-popups-box"]
    )

    window = widgets.Window(
        namespace=f"ignis-notifications-popups-{output_id}",
        monitor=output_id,
        anchor=["bottom", "right"],
        exclusivity="normal",
        layer="top",
        kb_mode="none",
        visible=True,
        child=box,
        css_classes=['notifications-popups-window']
    )
    window.set_size_request(350, 1)

    return window

def NotificationsCentrePlusCalendar(output_id):
    def _setup(widget):
        # Add all existing notifications
        for nf in notifications.notifications:
            widget.append(notification(nf))

        notifications.connect(
            "notified",
            lambda _, info: widget.append(notification(info))
        )

    notifications_centre = widgets.Scroll(
        overlay_scrolling=False,
        vexpand=True,
        css_classes=["notifications-centre-scroll"],
        child=widgets.Box(
            setup=lambda self: _setup(self),
            spacing=4,
            vertical=True,
            css_classes=['notifications-centre-box']
        )
    )

    return widgets.Window(
        namespace=f"ignis-notifications-centre-{output_id}",
        monitor=output_id,
        anchor=["bottom", "right", "top"],
        exclusivity="normal",
        visible=False,
        popup=True,
        child=widgets.Box(
            spacing=16,
            vertical=True,
            vexpand=True,
            child=[
                notifications_centre,
                widgets.Calendar()
            ]
        ),
        css_classes=['notifications-centre-window']
    )
