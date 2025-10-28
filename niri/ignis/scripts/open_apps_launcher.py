from ignis.app import IgnisApp
from ignis import utils
from ignis.services.niri import NiriService

app = IgnisApp.get_initialized()
niri = NiriService.get_default()

for id in range(utils.get_n_monitors()):
    if utils.get_monitors()[id].get_connector() == niri.active_output:
        app.toggle_window(f'ignis-apps-launcher-{id}')
