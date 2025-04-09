from ignis.widgets import Widget
from ignis.utils import Utils
from ignis.services.niri import NiriService

niri = NiriService.get_default()

class WorkspaceButton(Widget.Button):
    def __init__(self, id, is_focused):
        super().__init__(
            setup=self._setup,
            css_classes=['workspace', 'focused-workspace' if is_focused else ''],
            child=Widget.Label(
                label=str(id)
            ),
            tooltip_text=f'Switch to Workspace {id}',
            on_click=lambda *_: niri.switch_to_workspace(id)
        )

    def _setup(self, *_):
        pass

class PerOutputWorkspaces(Widget.Box):
    def __init__(self, output):
        super().__init__(
        vertical=True,
        css_classes=['workspaces'],
        spacing=4,
        child=niri.bind(
            "workspaces",
            transform=lambda value: [
                WorkspaceButton(
                    workspace.get_idx(),
                    workspace.get_is_focused()
                ) if workspace.get_output() == output else None for workspace in value or []
            ]
        )
    )

class Workspaces(Widget.Box):
    def __init__(self):
        super().__init__(
            vertical=True,
            child=[PerOutputWorkspaces(Utils.get_monitor(id).get_connector()) for id in range(Utils.get_n_monitors())]
        )
