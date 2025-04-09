from pathlib import Path
from ignis.app import IgnisApp
from ignis.utils import Utils
from modules import (
    Bar,
    NotificationPopups,
    NotificationCenter,
    Dock,
    DockActivator,
    AppsLauncher,
    OSDWindow
)

scss = str(Path(__file__).parent.resolve() / "styles" / "default.scss")
app = IgnisApp.get_default()
app.apply_css(scss)

NotificationCenter()
NotificationPopups()

for monitor in range(Utils.get_n_monitors()):
    Bar(monitor)
    Dock(monitor)
    DockActivator(monitor)
    AppsLauncher(monitor)
    OSDWindow(monitor)
