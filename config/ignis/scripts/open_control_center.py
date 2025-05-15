from ignis.app import IgnisApp
from ignis.utils import Utils
from ignis.services.niri import NiriService

app = IgnisApp.get_default()
niri = NiriService.get_default()

for id in range(Utils.get_n_monitors()):
    if Utils.get_monitors()[id].get_connector() == niri.active_output:
        app.toggle_window(f'control-center-{id}')
